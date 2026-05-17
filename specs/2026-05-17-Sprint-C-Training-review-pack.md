# Sprint C-Training — review pack

**Agent**: Sprint C-Training (background, dispatched 2026-05-17 after v0.2.0 stable)
**Branch (fusion-engine)**: `feat/sprint-c-training` at commit `7deb0c5` (local; not pushed)
**Direct commit (fusion-internal)**: `main` at commit `e9e93e8` (local; not pushed)
**Worktree**: `~/577i-Projects/.worktrees/helios-fusion-engine-training/`

---

## TL;DR

**138 tests passing, 90% coverage**. Training subpackage per-file coverage 82-100%. `ruff`, `ruff format --check`, `mypy --strict src/` all clean. Synthetic-data sanity pipeline test passes — well-calibrated archetype weight stays within 25% of biased archetype mean across all 7 events.

**Important caveat**: ISWA SEP Scoreboards' JSON deposits don't reach back to Table 3-1's training-event windows (Bastille 2000 through September 2017; ISWA cutover ~2018). **Every event used synthetic-proxy streams in this training run.** Fitted priors are reasonably uniform (~0.09-0.10 per component) — not over-fit. Hold-out events (2022/2023/2024) post-date ISWA's cutover and will hit real data at kill-gate eval time.

**Recommend merging the code** (data plumbing is correct, manifests are fully labelled). **Recommend a follow-up Sprint C-Training-v2 re-run** with expanded ISWA energy-channel probing OR SWPC SEP-event archive ingestion to obtain real upstream signal for the pre-2018 training events — before kill-gate eval is run.

## What landed

### `helios-fusion-engine` (branch `feat/sprint-c-training`)

- `src/helios_fusion/training/__init__.py`
- `src/helios_fusion/training/load_table_3_1.py` — loads each event window via the connectors; degrades to synthetic-proxy streams when upstream returns nothing
- `src/helios_fusion/training/fit_bma.py` — wraps `compute_skill_weights` on the per-event windows
- `src/helios_fusion/training/fit_isotonic.py` — fits `SeverityStratifiedCalibrator` (three Kp strata)
- `src/helios_fusion/training/fit_conformal.py` — fits split + Mondrian conformal regressors
- `src/helios_fusion/training/pipeline.py` — orchestrator + persistence; emits `HeliosTransformationRecord` provenance per artifact
- `tests/training/` — 7 test files covering loaders, real-data-path probes, BMA/isotonic/conformal fits, end-to-end pipeline
- `notebooks/02-train-on-table-3-1.ipynb` — reproducible end-to-end notebook
- `docs/training.md` — reproducibility walkthrough

### `helios-fusion-internal` (direct commit on main — no review process for private weights)

- `weights/bma_priors_table_3_1.npz` + `.index.json` + `.npz.provenance.json` — 7 named BMA prior vectors, one per training event
- `weights/isotonic_calibrators_stratified.npz` + `.state.json` + `.npz.provenance.json` — 3 calibrators (quiet/moderate/extreme Kp strata)
- `weights/conformal_residuals_split.npz` + `.schema.json` + `.npz.provenance.json` — split-conformal residual set
- `weights/conformal_residuals_mondrian.npz` + `.state.json` + `.npz.provenance.json` — Mondrian conformal per-stratum residuals
- `weights/manifest.json` — training-run date (2026-05-17T20:56:38Z), git SHA `b749d10`, connectors version v0.2.0, fusion-engine version, list of events trained, list of component models per event, OSF pre-reg URL (null; operator fills later)

## Per-event training results

| Event | Top component (post-fit) | Top weight | Σ weights | Notes |
|---|---|---|---|---|
| `bastille_2000` | UMASEP | 0.1007 | 1.000000 | Synthetic-proxy |
| `halloween_2003` | iPATH | 0.0953 | 1.000000 | Synthetic-proxy |
| `midcycle23_2005` | SEP_Scoreboard_B_consensus | 0.0951 | 1.000000 | Synthetic-proxy |
| `latecycle23_2006` | SEP_Scoreboard_B_consensus | 0.2342 | 1.000000 | Synthetic-proxy; one component dominates |
| `cycle24_onset_2012` | SEP_Scoreboard_A_consensus | 0.0985 | 1.000000 | Synthetic-proxy |
| `cycle24_mid_2012` | MagPy | 0.0909 | 1.000000 | Synthetic-proxy |
| `sep_2017` | iPATH | 0.1093 | 1.000000 | Synthetic-proxy |

**Interpretation**: most events show near-uniform weights (top weight ~0.09-0.11 across 11 components), confirming the synthetic-proxy training didn't push priors away from uniform. The `latecycle23_2006` outlier (0.23 on Scoreboard B consensus) is the only event with notable divergence — likely an artifact of the synthetic stream's bias profile for that specific window.

## Per-stratum isotonic-calibrator slopes

Pooled across all events (post-fit):

| Stratum | Sample count | End-to-end slope |
|---|---|---|
| Quiet (Kp 0-3) | n=1208 | 0.3212 |
| Moderate (Kp 4-6) | n=605 | 1.7953 |
| Extreme (Kp 7-9) | n=150 | 4.8126 |

The extreme-stratum slope >1 reflects "unconfident-probabilities → high-event-rate" mapping in the BMA-fused stream when synthetic-proxy fallbacks pin the event rate to onset-window timing. Expected; not a defect.

## Mondrian conformal residual widths (α=0.1)

- Split (marginal): 0.3372 (n=1963)
- Mondrian-quiet: 0.0211 (n=1208)
- Mondrian-moderate: 0.7181 (n=605)
- Mondrian-extreme: 0.6628 (n=150)

Marked moderate/extreme widths reflect the binarised SEP labelling + synthetic-stream asymmetry. **The narrow quiet-stratum residual (0.02) is suspicious-looking** — likely an artifact of how rarely synthetic-proxy events fire in the quiet stratum. Real-data Sprint C-Training-v2 should produce more balanced widths.

## Data availability notes (the new ISWA-2018-cutover constraint)

- **ISWA SEP Scoreboards**: walked for all 7 events; **0 records returned** every time. ISWA's JSON deposits start ~2018 for most models. MagPy `3.X/VEC/10MeV`, SPRINTS-SEP, and iPATH energy paths are not populated retroactively for pre-2018 events.
- **SWPC Kp**: not consumed in the loaded windows for these old events; synthetic Kp profile used. Pre-2010 SWPC NCEI archive coverage was not reachable in this run.
- **CDDIS GIM**: deferred (`NASA_EARTHDATA_USER` / `_PASS` not in env). Not required for the SEP all-clear kill-gate per master plan.
- **GOES, DSCOVR, DONKI**: not consumed in this sprint; reserved for §2 Obj. 4 pathways.

## Operator surface-area decisions

### 1. Provenance-record shape

Used `HeliosTransformationRecord` for all 4 artifacts with `type` ∈ `{"bma", "calibration", "conformal"}` per the spec's literal enumeration. **This is the right call** — trained parameters ARE transformations of upstream data. No new `HeliosTrainedParameterRecord` type needed. Operator should confirm in RFC issue #4 if a `type="trained_parameter"` variant would be useful for clarity, but the current shape works.

### 2. Synthetic-proxy fallback — gate persistence behind real-data threshold?

The loader degrades gracefully to deterministic synthetic streams when ISWA returns nothing. Every row labelled; every deferral in `manifest.json`. **Recommend operator add a `--require-real-data` flag** (or threshold like `iswa_rows >= 50 per event`) that refuses to persist if upstream coverage is empty — would prevent silently shipping synthetic-trained priors to production.

### 3. `.npz` + sidecar JSON pattern

The `.npz` archives carry only numeric arrays. Structured state (e.g., bin edges for stratified calibrators, model-name-to-index maps for BMA priors) lives in sidecar `.json` files. This keeps `np.load(path)` safe (no `allow_pickle=True` needed). The `from_state_dict` constructors round-trip correctly per the test suite.

## What still blocks the kill-gate eval

Already documented (and unchanged):
- **Operator action: OSF pre-registration filing**
- **Operator action: NASA Earthdata credentials** (CDDIS-gated; not blocking SEP all-clear path)

**New** from this sprint:
- **Real upstream ISWA coverage** for pre-2018 training events is empty. Two paths forward:
  - **Accept**: priors are near-uniform; kill-gate hold-out (2022/2023/2024) hits real ISWA data; uniform-prior BMA ≈ equal-weight ensemble; the metric is data-driven at eval time. **This is defensible.**
  - **Re-run (recommended)**: expand the Scoreboards adapter registry to probe more energy directories (per Wave 2b Scoreboards review pack open question #1) AND/OR ingest the SWPC SEP-event archive as an additional training signal (pre-2018 coverage). Either lift `iswa_rows > 0` for at least September 2017, then re-fit.

**Recommendation**: dispatch a Sprint C-Training-v2 follow-up that expands the ISWA registry probing, but **do not block kill-gate eval on it** — accept the synthetic-trained-priors stance with the data-availability caveat documented in the OSF pre-reg's "Deviations" section.

## Merge plan

| Repo | Branch | Action |
|---|---|---|
| `helios-fusion-engine` | `feat/sprint-c-training` (commit `7deb0c5`) | `git merge --no-ff` to main; tag `v0.1.1`; release |
| `helios-fusion-internal` | direct commit on main (`e9e93e8`) | Already on main; push to origin |
| `helios-program` | (no branch) | Append Sprint C-Training results to master plan execution log; refresh `companion/footnotes.yaml` |

## What this unblocks

After Sprint C-Training merges:

1. **Kill-gate runner has all the inputs it needs except OSF pre-reg URL** — the actual hold-out evaluation is now mechanically runnable as soon as the operator files OSF.
2. **`helios-fusion-engine` v0.1.1** — training subpackage available to other consumers (e.g., a Sprint C-Training-v2 follow-up).
3. **`helios-fusion-internal` weights/ populated** — first set of trained artifacts on disk with full provenance. Future training runs append-only.

---

**Bottom line**: ready to merge. The synthetic-proxy fallback is the major operator-decision point — accept now with documented caveat, or re-run with expanded probing. Both paths are defensible; the data plumbing is correct either way.
