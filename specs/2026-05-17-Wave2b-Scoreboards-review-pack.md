# Wave 2b · Agent SEP Scoreboards — `helios-spaceweather-connectors` review pack

**Agent**: Wave 2b · SEP Scoreboards adapter (background, dispatched 2026-05-17)
**Branch**: `feat/v0.2-sep-scoreboards-adapter` at commit `93727b4` (local; not pushed)
**Worktree**: `~/577i-Projects/.worktrees/helios-spaceweather-connectors-scoreboards/` (explicitly isolated)

---

## TL;DR

**50/50 tests pass at 90% line+branch coverage** on `sep_scoreboards.py` (target ≥80%). `ruff check .`, `ruff format --check .`, `mypy --strict` all clean across the whole repo (from this branch's vantage). Full repo suite 246/247 — the single failure is `tests/test_goes.py::test_default_pyspedas_loader_dispatches_xray`, an unrelated venv issue (pyspedas not installed) from Wave 2a.

**Recommend merging** alongside the CDDIS branch.

## Critical finding: actual ISWA data-tree URLs (the brief's guesses were wrong)

The brief speculatively pointed at `https://ccmc.gsfc.nasa.gov/scoreboards/sep/scoreboards/A/` — that returns **404**. The live SPAs at `https://sep.ccmc.gsfc.nasa.gov/{probability,intensity,allclear}` are JavaScript apps that fetch via private AJAX endpoints unsuitable for adapter use.

The **machine-accessible mirror** that the agent discovered is the ISWA data tree:

```
https://iswa.ccmc.gsfc.nasa.gov/iswa_data_tree/model/heliosphere/sep_scoreboard/
    <MODEL>/[<variant>/]<energy>/<YYYY>/<MM>/<filename>.json
```

Per-model variant chains differ (`UMASEP/v3_X/...`, `SEPSTER/Parker/...`, `MagPy/3.X/VEC/...`). Default registry covers 8 models. **HESPERIA REleASE family explicitly excluded** (`RELEASE`, `RELEASE_PLUS`, `STEREO_RELEASE`, `STEREO_RELEASE_PLUS`).

**This URL discovery is the most important contribution of this adapter beyond the code itself.** The connectors `docs/design.md` playbook should be updated with the discovery process (probe SPA → trace AJAX → fall back to ISWA tree).

## Schema finding: A/B/C are projections, not separate API surfaces

Each model emits a single `sep_forecast_submission` file with a `forecasts[]` array. The adapter projects each forecast row into A-, B-, and C-shaped records depending on which fields are populated:

| Scoreboard | Source field in forecast | Records emitted |
|---|---|---|
| A — onset probability | `probabilities`, `all_clear` | Onset / all-clear records |
| B — peak flux | `peak_intensity` | Peak-flux records |
| C — event time profiles | `event_lengths`, `threshold_crossings`, `sep_profile` | Time-series records |

A single forecast can legitimately contribute to all three boards. The adapter handles this correctly (the per-board `source_id` is set on each yielded record; the same upstream forecast can yield records for multiple boards).

### Schema consistency wins (unlike SWPC's chaos)

- **Time format**: consistent ISO-8601 with `Z` suffix throughout. No mixed formats.
- **NaN encoding**: simply absent keys (no sentinel values).
- **Units**: per-forecast `energy_channel.units` field (typically `MeV`); peak intensity has per-record `units` (`pfu` for integral, `MeV^-1*s^-1*cm^-2*sr^-1` for differential channels).

This is the **cleanest upstream schema** so far across all 6 adapters. Worth noting in the kill-gate's metric-extraction code.

## REleASE-free guarantee

Example lineage tuple for a UMASEP-10 Scoreboard A record:

```python
(
  'spase://CCMC/SimulationModel/UMASEP/v3',
  'model/UMASEP-10',
  'https://iswa.ccmc.gsfc.nasa.gov/iswa_data_tree/.../UMASEP10_prediction_*.json',
  'trigger/cme/2024-05-08T16:00:00-CME-001',
  'trigger/flare/2024-05-10T15:35Z'
)
```

**REleASE never appears in lineage** — the adapter only fetches model-level JSON from non-REleASE directories. The regression test `test_no_url_contains_release_or_hesperia` enforces this by **sweeping every URL the adapter would issue** for any reasonable parameter range. This is the right shape of compliance test for licensing constraints; should be promoted to the connectors `docs/design.md` playbook as the canonical pattern.

## Per-board source_id discrimination

Every yielded record carries `source ∈ {SEP_SCOREBOARD_A, SEP_SCOREBOARD_B, SEP_SCOREBOARD_C}` regardless of the per-class `source_id` attribute. The class-level `source_id` defaults to `SEP_SCOREBOARD_A` for `BaseAdapter` contract compatibility but is dynamically overridden per-record. Downstream fusion can filter by `source` to get per-board projections.

## Files landed

- `src/helios_connectors/adapters/sep_scoreboards.py` (~990 lines)
- `src/helios_connectors/__init__.py` (updated)
- `src/helios_connectors/adapters/__init__.py` (updated)
- `tests/test_sep_scoreboards.py` (50 tests)
- `tests/fixtures/sep_scoreboards/scoreboard-{a,b,c}-recent.json` (recent ISWA snippets)
- `tests/fixtures/sep_scoreboards/scoreboard-{a,b}-sep2017.json` (the 2017 Sep storm — Table 3-1 training event)
- `tests/fixtures/sep_scoreboards/listing-umasep-10-2024-05.html` (Apache index format mirror)
- `docs/adapters/sep_scoreboards.md` — endpoint table, REleASE exclusion policy, worked example for 2017 storm
- `docs/index.md` (status table updated)
- `mkdocs.yml` (nav updated)
- `CHANGELOG.md` (entry under `[Unreleased]`)

## Open questions / surface decisions

1. **Model registry is incomplete by design**: only 8 of 16 visible top-level model directories are wired in. Easy to extend via `models=` kwarg without code changes. Some models (SEPMOD, SPRINTS-SEP, iPATH) had directory layouts the agent didn't fully probe; defaulting to `variants=()` may miss subdirectory levels these models actually require. **If those models matter for the kill-gate eval, probe and adjust before tagging v0.2.0a1.**

2. **Live ISWA listings are large** — 5.5 MB for one month of UMASEP-10. Committed fixture trims to ~40 entries (12.9 KB) while preserving the real Apache-index format. Production fetches will pull these full listings; consider pagination if memory becomes a concern.

3. **2017 fixtures use SEPSTER's `v20190101` directory** (historical mode) since UMASEP-10's `v3_X` doesn't extend back to 2017. Adapter transparently handles either case; regression test confirms cross-window coverage.

4. **Provenance swap pattern**: followed GOES (`to_helios_model_output()` static converter; `helios-provenance-spec` already pinned by GOES in Wave 2a). No new `pyproject.toml` deps needed.

## Merge-conflict expectation (with sibling CDDIS branch)

The agent expected union conflicts on:
- `src/helios_connectors/__init__.py` — adds `SepScoreboardsAdapter`; CDDIS adds `CddisGimAdapter`
- `src/helios_connectors/adapters/__init__.py` — same
- `docs/index.md` — both updated the status table
- `mkdocs.yml` — CDDIS added `cddis.md` to nav; Scoreboards added `sep_scoreboards.md`
- `CHANGELOG.md` — two entries under `[Unreleased]`; concatenate

All deterministic union resolutions.

## Merge readiness

- ✅ 50/50 tests; 90% coverage on `sep_scoreboards.py`
- ✅ ruff/mypy --strict clean
- ✅ REleASE exclusion enforced + tested
- ✅ Forward-compatible `to_helios_model_output()` converter
- ✅ Live test marked `@pytest.mark.live`; 2017-storm + recent fixtures committed
- ⏳ Merge-time union conflict on 5 shared files (deterministic)
- ⏳ Model-registry expansion (SEPMOD, SPRINTS-SEP, iPATH) — Sprint C-Training pre-work or follow-up issue
- ⏳ Atomic provenance-swap PR (after merge) consolidates `SourceID.SEP_SCOREBOARD_*` if desired, applies real `HeliosModelOutputRecord` shape across all 6 adapters

## Downstream impact

- **Sprint C-Training** now has direct access to per-model SEP-forecast envelopes for the 7 Table 3-1 training events. The fact that the 2017 storm fixture is already committed is a head start.
- **Kill-gate evaluation** consumes Scoreboard A projections for HSS computation; this adapter is the canonical source.
- **The REleASE compliance pattern** (URL-sweep regression test) should be promoted to `docs/design.md` as the standard for licensing-constrained adapters.

---

**Bottom line**: ready to merge. The actual-URL discovery (ISWA data tree, not the scoreboards/sep/ SPA paths) is documentation gold. After this lands, all 6 connectors are operational; the atomic provenance-swap PR is the natural next step before tagging v0.2.0 stable.
