# Wave 2a · Agent GOES — `helios-spaceweather-connectors` review pack

**Agent**: Wave 2a · GOES wrapper (background, dispatched 2026-05-17)
**Branch**: `feat/v0.2-goes-adapter` at commit `7bc9344` (local; not pushed)
**Commits**: conventional commits on top of `main`

---

## TL;DR

**51 tests passing, 94% line+branch coverage** on `goes.py` (well above the 80% target). `ruff`, `mypy --strict` clean. Real Gannon-week smoke test against live PySPEDAS archive confirmed correct routing: 6 daily NetCDF files pulled from NCEI; first records at `2024-05-08T00:00:00Z` show flux=1.19e-5 / 5.25e-7 / 2.96e-7 pfu at the 10 / 50 / 100 MeV proxy channels — monotonically decreasing as expected outside an SEP event.

**Recommend merging** alongside the other Wave 2a branches. One operational concern (differential-channel proxies for SEP thresholds) is documented but needs Sprint C-Training attention before kill-gate evaluation.

## What landed

- `src/helios_connectors/adapters/goes.py` (897 lines) — `GoesAdapter(BaseAdapter)` with `fetch_xray`, `fetch_protons`, unified `fetch`
- `tests/test_goes.py` (51 tests)
- 4 fixtures under `tests/fixtures/goes/`: SWPC NRT JSON (xray + protons), PySPEDAS Gannon-week snippets (xray + protons)
- `docs/adapters/goes.md` — product table, routing rule, overlap-with-SWPC notes, differential-channel-proxy caveat
- `src/helios_connectors/schema.py` — added `SourceID.SWPC` and `SourceID.GOES`
- `pyproject.toml` — added `helios-provenance-spec>=0.1.0` runtime dep + optional `[pyspedas]` extra (the GOES agent chose to add this; the SWPC agent chose to defer — see "Atomic provenance swap" below)
- `CHANGELOG.md` entry under `[Unreleased]`

## ⚠️ Important caveat: GOES SGPS L2 differential-channel proxies

The proposal §2 Obj. 3 invokes the operational SEP thresholds **>10 MeV at 10 pfu** and **>100 MeV at 1 pfu** — both are *pre-integrated* flux values.

The 1-minute SGPS L2 file (`sgps-l2-avg1m`) does **NOT** publish pre-integrated >=10/>=50/>=100 MeV channels. It publishes:
- `AvgDiffProtonFlux` — shape `(N, 2, 13)` (time × east/west × 13 differential channels)
- `AvgIntProtonFlux` — single >=500 MeV channel only

The agent's `_extract_proton_samples` implementation selects the **differential channels closest to 10 / 50 / 100 MeV** (channels 5 / 7 / 8 with effective energies ≈ 16 / 54 / 91 MeV), averages east/west sensors, and emits these as proxies. This is **clearly documented** in:
- `_extract_proton_samples` docstring
- `docs/adapters/goes.md`
- The CHANGELOG entry

**Sprint C-Training implication**: before the kill-gate hold-out evaluation runs, either:
1. Re-integrate the 13 differential channels to compute true >10 / >100 MeV integrals (proper but ~50 lines of physics-aware code), OR
2. Use the SWPC NRT JSON path for these thresholds, which gives pre-integrated values from SWPC's own derivation, OR
3. Pull the 5-minute SGPS L2 product (which may publish integrals — check NOAA NCEI for `sgps-l2-int1m` or similar before assuming it doesn't).

This caveat is real but **not blocking for Wave 2a merge** — the framework is correct; the threshold-mapping refinement is a focused Sprint C-Training task.

## PySPEDAS quirks (gold for any agent touching PySPEDAS later)

1. **Namespace churn**: `pyspedas.goes` is outdated; current (v2.x) namespace is `pyspedas.projects.goes`. Prompts/docs that quote the old paths are stale.
2. **Blocking + chatty**: PySPEDAS calls are blocking and noisy on stdout. Adapter wraps them in `asyncio.to_thread` + a stdout-suppression context manager. Copy this pattern to the DSCOVR adapter.
3. **First-call side-effect**: PySPEDAS downloads to `goes_data/` in `cwd`. Subsequent calls cache there. CI should set `cwd` to a tmpdir or PySPEDAS's `local_data_dir` config.
4. **Numpy ABI warning** on one test (`RuntimeWarning: numpy.ndarray size changed`) — cosmetic, doesn't affect correctness. Ignore in test filterwarnings or pin numpy more tightly.

## Provenance handling — incrementally smarter than SWPC

The GOES agent diverged from the SWPC agent on the provenance question:

| | SWPC adapter | GOES adapter |
|---|---|---|
| `pyproject.toml` adds `helios-provenance-spec` | ❌ deferred | ✅ added |
| `SourceID` enum additions | `SWPC_KP` (would also need SWPC_DST) | added `SWPC` and `GOES` (cleaner shape) |
| Real `HeliosModelOutputRecord` emission | not done; placeholder only | placeholder + static `to_helios_model_output()` converter |

The GOES agent's approach is better aligned with the eventual atomic-swap PR: when that PR lands, `BaseAdapter._emit_provenance` just calls the converter pattern (or replaces with direct real-model emission), no per-adapter rework needed.

**Resolution at merge**: take GOES's `pyproject.toml` addition + GOES's `SourceID.SWPC` enum value. Drop SWPC's `SWPC_KP` member; update SWPC adapter to use the cleaner `SourceID.SWPC` with `record_type="kp"` / `"dst"` discriminator (an arguably better design anyway).

## Coordination friction noted

The 3 Wave 2a agents (SWPC, GOES, DSCOVR) **shared the same physical checkout**, contrary to the assumption in my brief that each worked in an isolated worktree. The GOES agent reports:
- Linter hook auto-rewrote `adapters/__init__.py` mid-build to import the sibling `DscovrAdapter`
- Agent worked around it by writing files via shell + verifying staged diffs before commit
- Confirmed staged `__init__.py` only contains GoesAdapter changes

**Implication for the merge**: each branch will have edited shared files (`adapters/__init__.py`, `schema.py`, `pyproject.toml`, `CHANGELOG.md`). Expect 4 trivial conflicts that resolve by **union** (combine all 3 enum additions, all 3 exports, all 3 dep additions, all 3 CHANGELOG entries). No semantic conflicts.

## Merge readiness

- ✅ 51 tests passing, 94% coverage on `goes.py`
- ✅ lint/type/format clean
- ✅ Fixtures committed
- ✅ Adapter docs written
- ✅ CHANGELOG entry
- ✅ `pyproject.toml` has the right helios-provenance-spec dep
- ⚠️ Differential-channel-proxy caveat needs Sprint C-Training resolution before kill-gate
- ⏳ Atomic provenance-swap PR still recommended (the GOES agent went halfway; the SWPC agent didn't go at all — finish the swap in one focused PR)

## Sequence at merge (recommended, in branch order)

```bash
cd ~/577i-Projects/helios-spaceweather-connectors

# Merge order: GOES first (medium diff), DSCOVR second, SWPC last (biggest diff + needs the smoothest conflict-resolution surface)
git checkout main
git merge --no-ff feat/v0.2-goes-adapter -m "feat(adapters): GOES wrapper — PySPEDAS for historical + SWPC NRT for last ~30 days"

# Each subsequent merge will conflict on adapters/__init__.py, schema.py, pyproject.toml, CHANGELOG.md
# Resolution: take union of additions; don't drop anything
git merge --no-ff feat/v0.2-dscovr-adapter -m "feat(adapters): DSCOVR wrapper — PySPEDAS for historical + SWPC NRT for last ~24-48 hours"
# (resolve unions on the 4 shared files)

git merge --no-ff feat/v0.2-swpc-adapter -m "feat(adapters): NOAA SWPC with GFZ Potsdam + Kyoto WDC historical fallback"
# (resolve unions; drop SWPC_KP and re-emit SWPC adapter records with SourceID.SWPC + record_type discriminator)

git push origin main

# Then: atomic provenance swap PR (see SWPC review pack open question #1)
# Then: tag connectors v0.2.0a1
```

## Downstream impact

- The differential-channel-proxy caveat must be threaded into Sprint C-Training's eval harness. Specifically: the EvalReport at the OSF pre-reg defines pre-integrated >10/>100 MeV thresholds — when consuming GOES data via this adapter, either use the SWPC NRT path (pre-integrated) or layer a re-integration pass between the adapter and the metric.
- The `to_helios_model_output()` static helper is a forward-compatible bridge to the real `helios_provenance` schema. Encourage Wave 2b adapters to provide the same helper shape until the atomic swap lands.

---

**Bottom line**: ready to merge. One real Sprint C-Training task spawned (re-integrate or switch to NRT for SEP thresholds), one operational refinement needed at merge time (union the schema.py and adapters/__init__.py changes across all 3 Wave 2a branches).
