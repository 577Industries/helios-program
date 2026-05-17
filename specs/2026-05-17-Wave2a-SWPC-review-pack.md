# Wave 2a · Agent SWPC — `helios-spaceweather-connectors` review pack

**Agent**: Wave 2a · SWPC adapter (background, dispatched 2026-05-17)
**Branch**: `feat/v0.2-swpc-adapter` (local; not pushed)
**Worktree**: `~/577i-Projects/.worktrees/helios-spaceweather-connectors-swpc/`
**Commits**: 4 conventional commits on top of `main`

---

## TL;DR

**42 unit + 1 live tests, 89% line+branch coverage** on the new `swpc.py` (exceeds 85% target). Full repo suite **108 passing**, zero regressions on existing DONKI / base / cache / http / ratelimit tests. `ruff check`, `ruff format --check`, `mypy --strict` all clean.

**Real Gannon-week smoke test** (real GFZ archive, not mocked):
```
fetch_kp(start=2024-05-08, end=2024-05-14)  →  49 records
2024-05-08T00:00:00Z  Kp=1.0    lineage=('swpc/kp', 'GFZ Potsdam/Kp_ap_Ap_SN_F107_since_1932.txt')
...
2024-05-11T00:00:00Z  Kp=9.0  ← Gannon peak
```

The mocked regression test `test_fetch_kp_gannon_routes_to_archive` asserts zero requests hit `services.swpc.noaa.gov` for that window — the 30-day-archive-limit gotcha is correctly enforced.

**Recommend merging** after Wave 2a sibling branches (GOES, DSCOVR) return. The operator should plan a follow-up PR for the provenance-import swap before tagging v0.2.0a1 (see open question #1 below).

## What landed

### Code (`src/helios_connectors/adapters/swpc.py`, ~1054 lines)
- `SwpcAdapter(BaseAdapter)` with: `fetch_kp`, `fetch_dst`, `fetch_plasma`, `fetch_mag`, `fetch_sep_forecast`, unified `fetch(start, end, products=None)`
- Transparent historical fallback: any query with `start < (now - 30 days)` routes Kp to **GFZ Potsdam** (`Kp_ap_Ap_SN_F107_since_1932.txt`) and Dst to **Kyoto WDC**. Quality tier (`provisional`, `final`) preserved on every record.
- Six defensive parsers (the schema chaos detailed below)

### Tests (`tests/test_swpc.py`, 42 unit + 1 live)
- Recorded fixtures: `kp-realtime.json`, `plasma-7-day.json`, `mag-7-day.json`, `goes-protons-7-day.json`, `sep-forecast.txt`, `gfz-kp-2024-05.txt`, `kyoto-dst-2405.html`
- Critical regression: `test_fetch_kp_gannon_routes_to_archive` (asserts no SWPC requests for >30-day-old queries)
- Live test: `test_swpc_live_realtime` marked `@pytest.mark.live`

### Docs
- `docs/adapters/swpc.md` — product table, routing rule, rate-limit notes, GFZ + Kyoto WDC attribution and citation
- `docs/index.md` updated to include SWPC in the adapter survey
- `CHANGELOG.md` appended under `[Unreleased]`

## 6 SWPC schema inconsistencies (gold for Wave 2b)

These come from real API probing. Wave 2b adapter agents should inherit this list as background:

1. **Wrong URL paths in original docs/briefs**: `/json/solar-wind/plasma-7-day.json` 404s; the real path is `/products/solar-wind/...`. Update any external references that quote the old paths.
2. **3-day forecast is a text product**, not JSON: `/text/3-day-forecast.txt` with Kp/S/R probability tables — required a custom regex parser. There is no JSON equivalent.
3. **Two JSON shapes coexist on SWPC**:
   - *Header-as-first-row CSV-style*: `plasma-7-day.json`, `mag-7-day.json` use `[[col,col,...], [val,val,...], ...]` with string-encoded floats.
   - *List-of-dict*: `noaa-planetary-k-index.json`, `integral-protons-7-day.json` use the more typical shape with native-typed floats.
4. **Three different time-string formats across products**: plasma/mag use `"2026-05-10 16:34:00.000"` (space, no TZ); Kp uses `"2026-05-10T00:00:00"` (T, no TZ); protons use `"2026-05-10T16:35:00Z"` (T, Z). All need defensive parsing.
5. **GFZ archive format is daily-row, not 3-hourly-row** — different from Agent D's parser in `gannon-storm-rtk-analysis/src/gannon_analysis/swpc.py`. Each line has `Kp1..Kp8` + `ap1..ap8` inline; the new SWPC parser correctly handles this.
6. **`kp.gfz-potsdam.de` 301-redirects to `kp.gfz.de`** — use the canonical short URL going forward.

## Open questions / surface-area decisions

1. **Provenance import swap deferred — recommended path**: do a separate atomic PR `chore(provenance): swap placeholder ProvenanceRecord → helios_provenance.HeliosModelOutputRecord` *after* Wave 2a merges. That PR:
   - Touches `BaseAdapter._emit_provenance`, `NormalizedRecord.provenance` type, all 4 existing adapters (DONKI + Wave 2a's three), and the DONKI tests (~32) that assert against the placeholder shape.
   - Adds `helios-provenance-spec>=0.1.0` to `pyproject.toml` (the published PyPI name is `helios-provenance-spec`; the import path is `helios_provenance`).
   - The real spec has different shape: `agent` field, `confidence_interval` field, `extra` dict, no `lineage` field as in the placeholder — the migration is one-shot translation per field.

   Doing this swap atomically (not per-adapter) avoids merge-conflict thrash on shared types.

2. **No `SourceID.SWPC_DST` member**. Dst records currently emit `SourceID.SWPC_KP` with `record_type="dst"`. If downstream fusion needs SourceID-level discrimination, add `SWPC_DST` to the enum.

3. **Kyoto final-vs-provisional tier mixing**: the 6-12 month lag for `dst_final` means historical-window queries can return mixed `quality_tier` values across months. Acceptable for HELIOS internal consumers; flag if downstream serialization needs uniformity.

4. **`coverage.xml`** is dirty in working tree — pre-existing untracked file, not from this branch.

## Merge readiness

- ✅ CI green: 42 SWPC tests + 66 carried-forward tests = 108 passing
- ✅ 89% line+branch coverage on `swpc.py` (target ≥85%)
- ✅ `ruff check`, `ruff format --check`, `mypy --strict` clean
- ✅ Recorded fixtures committed (no live data dependency for CI)
- ✅ CHANGELOG.md entry added
- ✅ Docs adapter reference written
- ⏳ Provenance import swap → separate atomic follow-up PR (see open question #1)
- ⏳ Connectors v0.2.0a1 tag held until all 3 Wave 2a adapters merge (DONKI + SWPC + GOES + DSCOVR = 4 adapters live, then tag)

## Sequence the operator should run (after sibling Wave 2a agents return)

```bash
# 1. Inspect SWPC branch
cd ~/577i-Projects/helios-spaceweather-connectors
git checkout feat/v0.2-swpc-adapter
pip install -e '.[dev]'
pytest -m "not live" --cov=src/helios_connectors
ruff check . && ruff format --check . && mypy

# 2. Optionally run the live test
pytest -m live tests/test_swpc.py::test_swpc_live_realtime -v

# 3. Inspect the diff
git diff main..feat/v0.2-swpc-adapter --stat

# 4. Merge (in branch order; SWPC last because it touches the most files; GOES/DSCOVR first)
git checkout main
git merge --no-ff feat/v0.2-goes-adapter -m "feat(adapters): GOES wrapper over PySPEDAS + SWPC near-real-time"
git merge --no-ff feat/v0.2-dscovr-adapter -m "feat(adapters): DSCOVR wrapper over PySPEDAS + SWPC near-real-time"
git merge --no-ff feat/v0.2-swpc-adapter -m "feat(adapters): NOAA SWPC with GFZ Potsdam + Kyoto WDC historical fallback"
git push origin main

# 5. Open the provenance-swap PR atomically (see open question #1)
# 6. After that lands, tag connectors v0.2.0a1 (4 adapters live: DONKI + SWPC + GOES + DSCOVR)
```

## Downstream impact

- **Sprint C-Training** can now use real Kp + Dst time series for Table 3-1 training events via GFZ + Kyoto fallback (the SWPC archive limit was the blocker).
- **`gannon-storm-rtk-analysis` v2** can swap its current standalone GFZ/Kyoto parsers for `SwpcAdapter.fetch_kp(...)` / `SwpcAdapter.fetch_dst(...)` once the package is on PyPI. That collapses ~150 lines of duplicate parsing.

---

**Bottom line**: ready for merge after sibling Wave 2a agents return. The deferred provenance-import swap is the right call — schedule that atomic PR before tagging v0.2.0a1.
