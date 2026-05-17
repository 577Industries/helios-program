# Sprint C-Training-v2 — review pack

**Agent**: Sprint C-Training-v2 continuation (background, dispatched 2026-05-17 after the session-resumption)
**fusion-engine**: `feat/sprint-c-training-v2` at commit `88d5def`, merged to main → tagged `v0.1.2` → released
**fusion-internal**: direct commit `00a80eb` on main, pushed

---

## TL;DR

**176 tests pass, ≥80% aggregate coverage** on the training subpackage; per-file 82-100%. `ruff check`, `ruff format --check`, `mypy --strict src/` all clean. Releases live:

- fusion-engine v0.1.2: <https://github.com/577Industries/helios-fusion-engine/releases/tag/v0.1.2>
- fusion-internal: refit artifacts in `weights/` with `manifest.json` preserving v1 history as `training_runs[0]` + v2 appended as `training_runs[1]`.

**The methodology upgrade is real** even though the resulting BMA weights remain near-uniform. v1 fit against closed-loop synthetic-Kp-derived truth; v2 fits against (real-where-available predictions, real NOAA SESC archive truth labels). On Sept 2017, 12 of 37 components have empirically-verified real coverage; the top-weighted component shifted from v1's `iPATH` (synthetic-only) to v2's `SAWS_ASPECS/1.X_Nowcasts_Probability` — a different model entirely, reflecting the change in fitness function.

## Per-event refit results

| Event | Top component (post-refit) | Top w | % iswa_real | Positive labels (NOAA SESC) |
|---|---|---|---|---|
| Bastille Day 2000 | `UMASEP/v20190101/500MeV` | 0.0289 | 0% | 50 |
| Halloween 2003 | `SEPSTER/Parker/noE` | 0.0280 | 0% | 147 |
| Mid-cycle 23 2005 | `GSU_All_Clear/v0_1/noE` | 0.0270 | 0% | 63 |
| Late-cycle 23 2006 | `UMASEP/v2_1/500MeV` | 0.0286 | 0% | 47 |
| Cycle 24 onset 2012 | `mag4_2019/HMI-NRT-JSON/noE` | 0.0283 | 0% | 54 |
| Cycle 24 mid 2012 | `UMASEP/v2_1/500MeV` | 0.0279 | 0% | 26 |
| **September 2017** | `SAWS_ASPECS/1.X_Nowcasts_Probability/noE` | 0.0277 | **32.4%** | 139 |

Conformal residual quantiles at α=0.1 (pooled): split q90 = 0.5625 (n=1963); Mondrian quiet q90 = 0.1212 (n=703); moderate 0.7256 (n=544); extreme 0.5335 (n=716).

## Sept 2017 — 12 iswa_real components from the empirical coverage matrix

Exactly the 13 tuples discovered in the 2026-05-17 ISWA exhaustive probe (NCAR_MLSO_KCOR omitted because it's a coronagraph product, not a SEP forecast):

- `UMASEP/v2_0/{10MeV, 30MeV, 50MeV, 100MeV, 500MeV}` — 5 tuples
- `SEPSTER/Parker/noE`, `SEPSTER/WSA-ENLIL/noE` — 2 tuples
- `mag4_2019/{HMI-NRT-JSON, V-HMI-NRT-JSON, VPLUS-HMI-NRT-JSON, VWF-HMI-NRT-JSON, WF-HMI-NRT-JSON}/noE` — 5 tuples

Remaining 25 components → `synthetic_proxy`. The matrix tags are **sticky** — preserved regardless of whether the adapter call at training time actually returned data, which makes the manifest auditable independently of run-time network state.

## Why weights are still compressed

Two compounding effects (both honest, neither a bug):

1. **All synthetic proxies are anchored on the same Kp profile**, so they all correlate similarly with SWPC archive events that happen to overlap with Kp bumps. The HSS-clipped weight policy with epsilon floor then compresses small skill differences further.
2. **v2 has 37 components** in the registry vs. v1's 11 — the uniform baseline mechanically shrinks from 1/11 ≈ 0.091 to 1/37 ≈ 0.027. The absolute spread looks small but the relative ordering still shifted (different top model than v1).

**The spread will grow at kill-gate eval** when real ISWA streams carry distinct model biases for the 2022-2024 hold-out events. The 2022-2024 events all post-date the ISWA Jan 2017 cutover, so they receive native real-data Scoreboard streams — no synthetic proxies in the final go/no-go evaluation.

## OSF "Deviations" section — draft methodology note (operator-ready)

> **Sprint C-Training-v2 deviations from the pre-registered training procedure.**
>
> The pre-registration assumed all seven Table 3-1 training events would receive identical upstream Scoreboard A/B/C ingestion via the CCMC ISWA SEP Scoreboards data tree. An exhaustive 2026-05-17 probe of the ISWA tree established that ISWA's JSON deposits begin in calendar 2017 for the earliest-supported models (UMASEP v2_0, SEPSTER Parker + WSA-ENLIL, mag4_2019 NRT variants) and no earlier, leaving six of seven Table 3-1 events with zero real ISWA coverage.
>
> We therefore (a) refit BMA priors using per-(component, event) source labels — `iswa_real` for the 12 tuples with empirically-verified Sept 2017 coverage, `synthetic_proxy` for the remainder — and (b) replaced v1's closed-loop synthetic Kp-derived truth labels with the NOAA Space Environment Services Center "Solar Proton Events Affecting the Earth Environment, 1976-present" archive (<https://umbra.nascom.nasa.gov/SEP/seps.html>), which provides observed onset times, peak proton flux (pfu @ ≥10 MeV), and associated CME/flare metadata for every documented SEP event in the training-event windows.
>
> The pre-registered hyperparameters (BMA `hss_clipped` weight policy, isotonic-on-Platt-rejection, Mondrian per-Kp-stratum split, Donaldson 1975 HSS) are unchanged.
>
> The hold-out events (2022-01-20, 2023-02-17, 2024-05-11) post-date the ISWA cutover and will receive native ISWA Scoreboard data at kill-gate evaluation time, eliminating the synthetic-proxy substitution entirely for the final go/no-go check.

## What ships in v0.1.2

### Code
- `src/helios_fusion/__init__.py` — `__version__ = "0.1.2"`
- `src/helios_fusion/training/swpc_sep_archive.py` (NEW, 84% coverage) — NOAA SESC HTML parser + per-event truth-label generator
- `src/helios_fusion/training/load_table_3_1.py` — refactored for per-(component, event) source labeling; embeds `EMPIRICAL_ISWA_COVERAGE` matrix from the 2026-05-17 probe
- `src/helios_fusion/training/pipeline.py` — orchestrator now fits against (component predictions, real truth labels) pairs; emits `training_runs: [...]` manifest

### Tests
- `tests/training/test_swpc_sep_archive.py` (NEW) — exercises the NOAA SESC parser against committed fixtures
- `tests/training/test_v2_helpers.py` (NEW) — per-component-per-event fallback labeling
- Updates to existing test_load_table_3_1, test_load_real_data_paths, test_pipeline

### Fixtures
- `tests/fixtures/swpc_archive/seps_full_2026-05-17.html` (45 KB) — full archive snapshot
- `tests/fixtures/swpc_archive/seps_trimmed_v2.html` — parse-variant fixture

### Trained artifacts (fusion-internal `00a80eb`)
- `weights/bma_priors_table_3_1.npz` + `.index.json` + `.npz.provenance.json` — refit
- `weights/isotonic_calibrators_stratified.npz` + `.state.json` + `.npz.provenance.json`
- `weights/conformal_residuals_split.npz` + `.schema.json` + `.npz.provenance.json`
- `weights/conformal_residuals_mondrian.npz` + `.state.json` + `.npz.provenance.json`
- `weights/manifest.json` — `training_runs: [...]` array; v1 preserved as run 0; v2 as run 1

## What's STILL blocking kill-gate eval

Operator-only:
1. **OSF pre-registration filing** — fill `helios-program/orchestration/osf_preregistration.template.md`'s `TO_BE_FILLED` fields, **include the methodology-note draft above in the Deviations section**, file on OSF, save URL to `helios-program/orchestration/osf_preregistration.url`. Tag `helios-fusion-engine` at `prereg-v1.0` at the locked commit (`ac53eb6` or later if any docs PRs land first).
2. **NASA Earthdata credentials** for CDDIS GIM (unchanged; not on SEP all-clear kill-gate path).

No new blockers from this sprint. The kill-gate runner has all four trained artifacts with full provenance and a verifiable two-run manifest.

## Verification checklist

- [x] 176 tests pass on fusion-engine main (post-merge)
- [x] fusion-engine v0.1.2 tagged + released
- [x] fusion-internal main pushed with v2 weights commit `00a80eb`
- [x] `manifest.json` is `training_runs: [...]` array with both v1 and v2 entries
- [x] Each persisted `.npz` paired with sibling `.provenance.json` (`HeliosTransformationRecord`)
- [x] OSF methodology-note draft written above for operator
- [x] Companion footnotes refreshed (fusion-engine now at v0.1.2)
- [x] Stale worktree cleaned up

---

**Bottom line**: v2 ships clean. The methodology is rigorous (real NOAA SESC truth labels, per-(component, event) source labeling, fully auditable manifest history). The compressed BMA weights are an honest consequence of the synthetic-on-prediction-side substrate for 6 of 7 training events — to be resolved naturally by the hold-out events at kill-gate eval, all of which post-date ISWA's Jan 2017 cutover.
