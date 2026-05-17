# Atomic Provenance-Swap PR — review pack (post-merge)

**Branch**: `chore/v0.2-provenance-swap` (merged to main; tagged `v0.2.0`)
**Worktree**: `~/577i-Projects/.worktrees/helios-spaceweather-connectors-provswap/`
**Commits**: 3 focused commits on top of v0.2.0a1

---

## TL;DR

The placeholder `ProvenanceRecord` is gone. All 6 adapters now emit real `helios_provenance.HeliosModelOutputRecord` natively via `BaseAdapter._emit_provenance`. `SourceID` consolidated from 16 redundant per-product members to 8 stable identifiers + `record_type` discriminator on `NormalizedRecord.value`. **305 tests pass at 90% repo-wide coverage**; per-adapter coverage 87-94%. All linters clean.

Two follow-up fixes folded in:
- **Test pollution issue #4** — `test_safe_log_params_filters` now filters caplog to only `helios_connectors.http` records. Issue closeable on merge.
- **GOES `mypy --strict` error** resolved as a side-effect of the migration (the dict-typed-value implicit-Any disappeared when the placeholder path was removed).

v0.2.0 stable released at <https://github.com/577Industries/helios-spaceweather-connectors/releases/tag/v0.2.0>.

## The 3 commits

| Commit | Scope |
|---|---|
| `d662cc3` | `refactor(schema)`: consolidate SourceID + emit HeliosModelOutputRecord |
| `398f7c8` | `refactor(adapters)`: migrate every adapter to HeliosModelOutputRecord |
| `73aa69e` | `test`: update suite for HeliosModelOutputRecord + consolidated SourceID |

Clean staged-by-purpose history; reviewers can step through one logical change at a time.

## Schema changes

### `SourceID` enum, before and after

**Before** (16 members; redundant per-product proliferation):
```python
DONKI, SWPC, SWPC_KP, SWPC_PLASMA, SWPC_MAG, SWPC_SEP_FORECAST,
GOES, GOES_XRAY, GOES_PROTON,
DSCOVR, DSCOVR_MAG, DSCOVR_PLASMA,
CDDIS_GIM,
SEP_SCOREBOARD_A, SEP_SCOREBOARD_B, SEP_SCOREBOARD_C
```

**After** (8 stable identifiers):
```python
class SourceID(StrEnum):
    DONKI = "donki"
    SWPC = "swpc"
    GOES = "goes"
    DSCOVR = "dscovr"
    CDDIS_GIM = "cddis_gim"
    SEP_SCOREBOARD_A = "sep_scoreboard_a"
    SEP_SCOREBOARD_B = "sep_scoreboard_b"
    SEP_SCOREBOARD_C = "sep_scoreboard_c"
```

Product/variant discrimination moved to `NormalizedRecord.value["record_type"]` (`"kp"`, `"dst"`, `"plasma"`, `"mag"`, `"xray"`, `"proton"`, `"tec_map"`, `"sep_forecast"`, etc.).

### `BaseAdapter._emit_provenance`

Now returns a real `helios_provenance.HeliosModelOutputRecord`. Adds:

- `_helios_agent()` helper — creates the `Agent` record per the spec
- `_ensure_utc` — strict timestamp normalization
- `model_version` ClassVar on `BaseAdapter` so subclasses declare per-source version strings

## Per-adapter design judgment calls (from the agent's report)

Each requires operator awareness; none are blocking for v0.2.0.

| Adapter | Decision |
|---|---|
| **CDDIS `tec_map`** | Scalar = spatial mean of all numeric grid cells. Full `tec_grid` + `tec_grid_shape` in `extra`. Matches the Wave 2b CDDIS review pack design call. |
| **DONKI** | Per-event-class scalar pick: `FLR.classType` like `"X1.2"`; `CMEAnalysis.speed` km/s; `GST.kpIndex`. Intelligent linkages → `extra["lineage"]`; full payload → `extra["payload"]`. |
| **DSCOVR** | Mag scalar = `Bz` (drives geomagnetic activity); plasma scalar = bulk `speed`. Frame (GSE/GSM) preserved in `extra`. |
| **GOES** | `model_id` clean (`"goes/xray"`, `"goes/protons"`); archive-vs-realtime via `model_version` (`"ncei_archive"` vs `"swpc_nrt"`) — the cleaner discrimination axis. |
| **SWPC** | `model_version` discriminates `realtime` / `gfz_archive` / `kyoto_wdc_final` / `kyoto_wdc_provisional`. Dst lives under `SourceID.SWPC` (no `SWPC_DST` proliferation) with `record_type="dst"`. |
| **Scoreboard C** | Scalar = 0/1 threshold-crossing flag. Onset/crossing times in `extra["payload"]`. **Worth operator review**: a future PR could flip this to the threshold value or onset time depending on downstream fusion need. |

## Test changes

Total: 19 test files touched, +123 / -87 lines. Lighter than the spec-estimate of ~270 test updates because most existing assertions are on `record.value` not on the provenance shape.

| Test file | Δ |
|---|---|
| `test_base.py` | smoke tests for new BaseAdapter helpers |
| `test_cache.py` | minor (4 lines) — uses real HeliosModelOutputRecord in fixtures |
| `test_cddis_gim.py` | scalar/grid assertions updated |
| `test_donki.py` | lineage-in-extra checks; scalar value per event class |
| `test_dscovr.py` | Bz/speed scalar checks; frame in extra |
| `test_goes.py` | drops to_helios_model_output bridge tests; model_id/model_version split |
| `test_http.py` | test_safe_log_params_filters now filters caplog to helios_connectors.http (issue #4 fix) |
| `test_sep_scoreboards.py` | A/B/C scalar pick verified per projection |
| `test_swpc.py` | Dst under SWPC + record_type; model_version routing |

**305 tests pass**, 7 deselected (5 `live`-marked; 2 pyspedas-loader env-gated when pyspedas not installed).

## Open questions for v0.2.x patches

The agent flagged four surface-area decisions worth a future-PR look:

1. **Scoreboard C scalar** — 0/1 crossing flag vs threshold value vs onset time. Local edit in `_forecast_scalar`.
2. **DONKI `value_units`** — currently `"GOES_class"` for `FLR.classType`. Non-SPASE-standard; revisit if downstream serializers prefer `"none"` or a SPASE-aligned token.
3. **SWPC SEP forecast scalar** — Day-1 S-storm probability. Tweakable in `_forecast_scalar` if Day-1 G-scale or R-blackout is preferred.
4. **Synthetic `dataset_refs` fallback** — `helios-connectors://{source_id}` when no canonical URL. Register URL stubs for completeness.

None block v0.2.0; all are 1-line tweaks if revisited.

## Why this matters for Phase II

Three concrete reviewer-facing wins this PR delivered:

1. **The placeholder is gone**. The whole stack now emits the same provenance shape that `helios-provenance-spec` v0.1 documents as the open RFC. Reviewers reading the RFC + the connector code see consistent shape end-to-end.

2. **Tamper-evident hashing** is now applied to every fused output downstream of these adapters (because `HeliosModelOutputRecord` participates in `HeliosFusedOutputRecord.lineage`'s SHA-256 chain). Per proposal §1.4 / §4.2 innovation #2.

3. **Sprint C-Training is unblocked**. The training pipeline can now consume real `HeliosModelOutputRecord` from `helios-spaceweather-connectors` v0.2.0 and emit `HeliosTransformationRecord`/`HeliosFusedOutputRecord` for the fitted artifacts. End-to-end provenance from raw upstream model → trained BMA prior → fused output.

## Downstream now unblocked

- `helios-fusion-engine` Sprint C-Training (dispatched immediately after this merged)
- `gannon-storm-rtk-analysis` v2 swap to real SPP via the CDDIS adapter (when operator wires Earthdata creds)
- PyPI publication for all 3 publishable packages (once operator configures trusted publishing)
- Kill-gate execution (still blocked on OSF pre-registration filing, but the data plumbing is now real)

---

**Bottom line**: clean, well-staged PR. Operator confirmed merge + tagged v0.2.0. Sprint C-Training is the natural next step.
