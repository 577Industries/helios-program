# Wave 2a · Agent DSCOVR — `helios-spaceweather-connectors` review pack

**Agent**: Wave 2a · DSCOVR wrapper (background, dispatched 2026-05-17)
**Branch**: `feat/v0.2-dscovr-adapter` at commit `d7f0ae6` (local; not pushed)
**Worktree**: `~/577i-Projects/.worktrees/helios-spaceweather-connectors-dscovr/`

---

## TL;DR

**38 unit + 1 live tests, 92% line+branch coverage** on `dscovr.py` (target ≥80%). `ruff`, `mypy --strict` clean. Real Gannon-storm smoke test (May 10 2024): downloaded the actual DSCOVR L2 mag CDF from SPDF (6.9 MB), parsed 86,400 1-second mag samples in **GSE** frame, lineage cites the NCEI portal. **Peak Bz = -59.16 nT** — among the most extreme southward IMF excursions on record; this is the input that drove the May 10 magnetopause reconnection cascade.

**Recommend merging** as the last of the three Wave 2a branches (after GOES and DSCOVR), then proceeding with the atomic provenance-swap PR before tagging connectors v0.2.0a1.

## What landed

- `src/helios_connectors/adapters/dscovr.py` (284 stmts) — `DscovrAdapter(BaseAdapter)` with `fetch_mag`, `fetch_plasma`, unified `fetch(start, end, products=None)`
- `tests/test_dscovr.py` — 38 unit tests + 1 live (`@pytest.mark.live`)
- 4 fixtures under `tests/fixtures/dscovr/`: SWPC plasma + mag JSON, plus tplot-shape Gannon-week mag + plasma snippets
- `docs/adapters/dscovr.md` — product table, routing rule, **GSE vs GSM coordinate-frame discussion**, overlap with `SwpcAdapter`, rate-limit notes
- Shared-file edits: `schema.py` adds `DSCOVR_MAG` + `DSCOVR_PLASMA`, `pyproject.toml` adds `helios-provenance-spec>=0.1.0` + `[pyspedas]` extra, `.gitignore` adds `dscovr_data/`, `CHANGELOG.md` entry

## ⚠️ Coordinate-frame ambiguity (real sharp edge)

The DSCOVR data ecosystem has **two coordinate-frame conventions** that the adapter exposes correctly but downstream consumers must respect:

| Source | Frame published | Notes |
|---|---|---|
| DSCOVR L2 archive (PySPEDAS path) | **GSE** and **RTN** | No GSM in the L2 product. Adapter emits `frame = "GSE"` on this path. |
| NOAA SWPC near-real-time JSON | **GSM** | Pre-transformed. Column names `bx_gsm`, `by_gsm`, `bz_gsm`. Adapter emits `frame = "GSM"` on this path. |

- Bz sign convention is identical in both frames (negative = southward).
- Bx and By transformation between GSE and GSM has a non-trivial dipole-tilt rotation.
- Plasma velocity is a **GSE vector** on the PySPEDAS path (`vx_gse`, `vy_gse`, `vz_gse` propagated to `record.value`); SWPC publishes only scalar `speed`, no vector.
- Records carry the frame explicitly in `record.value["frame"]`.

**Downstream rule**: feature-engineering code in `helios-fusion-engine` MUST branch on `record.value["frame"]` or call PySPEDAS's `cotrans_tools.cotrans` for GSE↔GSM normalization before stacking the two streams into a single feature column. Mixing them silently corrupts feature vectors.

## PySPEDAS quirks (echoes GOES + adds DSCOVR-specific)

1. **Namespace churn**: top-level `pyspedas.dscovr` does NOT exist in 2.x. The correct path is `pyspedas.projects.dscovr`. **Same finding as GOES agent**. This is consistent across PySPEDAS missions; fold into the connectors `docs/design.md`.
2. **`mag` and `fc` are partial-style wrappers** around a single `load()` function with `instrument="mag"` / `instrument="fc"` pre-bound. They accept all the same kwargs as `load()`.
3. **`pyspedas.tplot_tools.get_data`** returns a custom namedtuple-like object with `.times` (epoch seconds) and `.y` (numpy array). Adapter's `_tplot_to_mag_rows` / `_tplot_to_plasma_rows` duck-type on those attributes so tests substitute a plain namedtuple without importing pyspedas.
4. **Default download dir is `dscovr_data/` in cwd** — agent added to `.gitignore`.
5. **Default `trange` is `['2018-10-16', '2018-10-17']`** if you forget to pass one. Always pass.

## Coordination signal — worth folding into Wave 2b dispatch

Agent reports a real cross-agent interference event: **the GOES sibling agent was running in the main repo (`~/577i-Projects/helios-spaceweather-connectors/`)**, the SWPC sibling was in its own worktree, and **switching branches on the main repo wiped this agent's untracked work mid-session**. Agent recovered cleanly by rebuilding in an isolated worktree at `~/577i-Projects/.worktrees/helios-spaceweather-connectors-dscovr/`.

**For Wave 2b dispatch** (next step): explicitly assign each of the 2 agents (SEP Scoreboards, CDDIS GIMs) its own worktree path in the dispatch prompt:
```
worktree: ~/577i-Projects/.worktrees/helios-spaceweather-connectors-scoreboards/
worktree: ~/577i-Projects/.worktrees/helios-spaceweather-connectors-cddis/
```

That eliminates the friction.

## Merge-conflict expectation

Same union-resolution as the other two Wave 2a branches. Expect conflicts on:
- `src/helios_connectors/schema.py` — each branch adds different `SourceID` members; take union (DSCOVR adds `DSCOVR_MAG` + `DSCOVR_PLASMA`, GOES adds `GOES` + `SWPC`, SWPC adds `SWPC_KP`).
  - **Recommended cleanup at merge**: drop `SWPC_KP`; consolidate to `SourceID.SWPC` with `record_type="kp"` / `"dst"` discriminator on the record. This matches the GOES agent's cleaner pattern.
- `src/helios_connectors/__init__.py` and `adapters/__init__.py` — each adds its adapter export; take union.
- `pyproject.toml` — all three add `helios-provenance-spec>=0.1.0` (deduplicate) and add `[pyspedas]` extra (deduplicate).
- `CHANGELOG.md` — three entries under `[Unreleased]`; concatenate.
- `.gitignore` — DSCOVR adds `dscovr_data/`; GOES likely added `goes_data/`; union.

All additive, no semantic conflicts.

## Merge readiness

- ✅ 38 unit tests pass; 92% coverage on `dscovr.py`
- ✅ lint/type/format clean
- ✅ Fixtures committed (4 files)
- ✅ Adapter docs written with GSE/GSM discussion
- ✅ Real-data smoke test passed against live SPDF + PySPEDAS
- ⏳ Merge-time conflict union on 5 shared files (deterministic; ~5 min operator time)
- ⏳ Atomic provenance-swap PR still pending after Wave 2a merge

## Headline science observation

The real-data smoke test produced a citable observation worth memorializing in the master plan execution log:

> **Peak Bz over May 10, 2024 Gannon storm: -59.16 nT** (DSCOVR L2 mag, GSE frame, 1-second cadence, 86,400 samples).

Combined with the SWPC adapter's GFZ-Kp=9.0 peak the same day and the gannon-storm-rtk-analysis 1,302-station-hours-over-threshold result, HELIOS now has **three live ground-truth observations of Gannon** — all traceable to specific records with full provenance lineage. That's the §4.2 innovation #2 (provenance-aware architecture) made concrete and citable for Phase II reviewers.

---

**Bottom line**: ready to merge. Resolve the 5 union conflicts mechanically per the recipe above; then run the atomic provenance-swap PR; then tag connectors `v0.2.0a1` (4 adapters live: DONKI + SWPC + GOES + DSCOVR).
