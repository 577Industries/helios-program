# Sprint C-Training — Design Spec

**Status**: spec ready; **dispatch blocked on** `helios-spaceweather-connectors` v0.2.0 stable (which depends on the atomic provenance-swap PR being merged + the connectors package being pip-installable from PyPI or git).

**When unblocked**: dispatch a single `general-purpose` agent in an isolated worktree against `helios-fusion-engine`, scope as specified below.

---

## Goal

Fit BMA priors + isotonic calibrators on the **seven Table 3-1 training events**, using real Scoreboard A data flowing through `helios-spaceweather-connectors`. Persist trained artifacts to `helios-fusion-internal/weights/` (the private companion repo). **Do NOT run hold-out evaluation** — that's gated on OSF pre-registration filing per the master plan's kill-gate discipline.

## What "trained" means here

Per `~/577i-Projects/GitHub/577Industries/helios-program/orchestration/osf_preregistration.template.md`:

- **H1 metric**: fused all-clear-revocation HSS beats best-component HSS by ≥15% on the 3-event hold-out (2022-01-20, 2023-02-17, 2024-05-11 Gannon).
- **H2 metric**: reliability slope within 0.15 of 1.0 across all Kp severity strata.

To compute these on the hold-out, we need:
1. BMA weights per component model — fit on training-event windows.
2. Isotonic calibrators per Kp severity stratum — fit on training-event windows.
3. Conformal residual sets for split + Mondrian — held in calibration set (last training-event window or rolling 90-day window).

**Sprint C-Training produces all three artifacts and commits them to `helios-fusion-internal/weights/`.** Hold-out evaluation is a *separate* sprint after OSF pre-reg filing.

## Seven training events (locked per Table 3-1)

| Event | Date | Notes |
|---|---|---|
| Bastille Day | 2000-07-14 | Major X5.7 flare; well-characterized SEP profile |
| Halloween storms | 2003-10-28 to 2003-11-04 | Cycle 23 peak; multiple X-class events |
| Mid-cycle 23 | 2005-01-20 | X7.1; fast onset; ground-level enhancement |
| Late cycle 23 | 2006-12-13 | X3.4; tests low-solar-activity calibration |
| Cycle 24 onset | 2012-03-07 | X5.4; cross-cycle generalization |
| Cycle 24 mid | 2012-05-17 | M5.1; sub-X event sensitivity |
| September 2017 storm | 2017-09-06 + 2017-09-10 | X9.3 + back-side X8.2; dual event |

Each event window is ±5 days of the primary onset.

## Component models (BMA averages across these)

Per OSF pre-reg template:

- UMASEP
- HESPERIA REleASE (excluded from data pull — licensing per proposal §3 T1; but referenced in the consensus that `helios_connectors.adapters.SepScoreboardsAdapter` returns)
- SEPMOD
- MagPy
- SEP Scoreboard A (consensus onset probability)
- SEP Scoreboard B (consensus peak flux)
- SEP Scoreboard C (consensus event time profile)

The `SepScoreboardsAdapter` already discovered which models contribute via the ISWA data tree. Sprint C-Training uses the **per-model** projections (already discriminated in `record.value["model"]`), not just the consensus.

**Important**: if SEPMOD or SPRINTS-SEP have directories in the ISWA tree that weren't probed in the Scoreboards adapter (see Wave 2b Scoreboards review pack open question #1), probe and wire them BEFORE the training run. They contribute meaningfully to the BMA average.

## Deliverables

### Code (in `helios-fusion-engine`)

- `src/helios_fusion/training/__init__.py`
- `src/helios_fusion/training/load_table_3_1.py` — function that pulls Scoreboard A/B/C records for the 7 training-event windows via the connectors package; returns a `pandas.DataFrame` per event with rows for each model + timestamp.
- `src/helios_fusion/training/fit_bma.py` — fits per-event BMA weights using the rolling-90-day skill metric (the canonical pattern in `helios_fusion.bma.weights.compute_skill_weights` already implemented).
- `src/helios_fusion/training/fit_isotonic.py` — fits severity-stratified isotonic calibrators (`SeverityStratifiedCalibrator` already implemented; just need to pipe in the right training data).
- `src/helios_fusion/training/fit_conformal.py` — fits the split + Mondrian conformal regressors' calibration sets.
- `notebooks/02-train-on-table-3-1.ipynb` — reproducible end-to-end training run. Cell outputs committed for the operator to inspect.

### Trained artifacts (in `helios-fusion-internal`)

Persist to `helios-fusion-internal/weights/`:

- `bma_priors_table_3_1.npz` — BMA weight vectors per event (named by event ID)
- `isotonic_calibrators_stratified.npz` — fitted calibrator state-dicts per Kp severity stratum
- `conformal_residuals_split.npz` + `conformal_residuals_mondrian.npz` — calibration residual sets
- `weights/manifest.json` — index of which file came from which training run; commit SHA of the fusion-engine code; date; OSF pre-reg URL (initially `null`; filled when operator files)
- Each file paired with a sibling `<name>.provenance.json` record per `helios-provenance-spec` (this confirms the swap PR has landed since BaseAdapter now emits `HeliosModelOutputRecord` natively)

### Documentation

- `helios-fusion-engine/docs/training.md` — full reproducibility walkthrough: prereqs, env vars, expected runtime, expected outputs, where weights go.
- Update `helios-fusion-engine/README.md` "Status" section to note "trained weights available at `helios-fusion-internal` for HELIOS team; framework is reproducible from public sources".
- Update `helios-program/companion/footnotes.yaml` to add the training-run date + commit SHA so the companion document accurately reflects program state.

### Tests

- Test that `load_table_3_1()` correctly windows each event ±5 days.
- Test that `fit_bma()` produces weights summing to 1 (existing invariant; just confirm on real data).
- Test that calibrator state-dicts round-trip after persistence.
- **Synthetic-data sanity test for the full pipeline**: load synthetic equivalents of the 7 events (already in `helios-fusion-engine/tests/conftest.py`), run end-to-end, verify the BMA weights converge to expected ratios per the synthetic-stream biases. This is the kill-gate's *pre-flight* check — if this fails, the real-data run will also fail.

## What this sprint explicitly does NOT do

- Does **not** run hold-out evaluation on the 3-event hold-out (2022-01-20, 2023-02-17, 2024-05-11 Gannon).
- Does **not** write the arXiv paper draft.
- Does **not** modify the kill-gate runner (`helios-program/orchestration/kill_gate.py` stays a stub).
- Does **not** make any decisions that retune the BMA weight-update formula or the isotonic-calibration approach. Both are pre-registered.

These are intentionally fenced off from Sprint C-Training so the OSF pre-registration discipline holds — the operator files pre-reg BEFORE any hold-out work.

## Verification gate

- All 7 training-event windows successfully pull data from the connectors.
- `bma_priors_table_3_1.npz` contains 7 named entries (one per training event).
- `isotonic_calibrators_stratified.npz` contains 3 calibrators (quiet, moderate, extreme).
- Each persisted file has a sibling `.provenance.json` validating against `helios-provenance-spec` v0.1.
- The synthetic-data sanity test passes end-to-end.
- `~/577i-Projects/helios-fusion-internal/weights/manifest.json` records the training-run metadata.

## Dispatch readiness checklist (verify before dispatching)

- [ ] `helios-spaceweather-connectors` v0.2.0 stable tagged + released
- [ ] `helios-spaceweather-connectors` installable via `pip install helios-spaceweather-connectors` (PyPI) OR via `pip install git+https://...@v0.2.0` (git fallback)
- [ ] `helios_provenance` importable (came in with the v0.2.0 swap)
- [ ] All 6 connector adapters import cleanly
- [ ] SEPMOD/SPRINTS-SEP/iPATH probed in SepScoreboardsAdapter if needed (see Wave 2b Scoreboards review pack open question #1)
- [ ] `helios-fusion-internal/weights/` directory exists (it does; created in session 1)
- [ ] `helios-fusion-internal/.gitignore` allows tracked `weights/*.npz` files (already configured in session 1)

When all 7 checkboxes are ticked: dispatch the Sprint C-Training agent against this spec.

## Estimated effort

- ~2 hours of agent runtime (loading 7 event windows from CDDIS + Scoreboards + SWPC; fitting BMA + isotonic + conformal; persisting + writing tests)
- The bottleneck is likely CDDIS GIM download throughput; pre-warming the cache before dispatch would cut runtime in half.
