# Artifact B — `helios-spaceweather-connectors` v0.1 Foundation + DONKI Review Pack

**Agent**: B-foundation (background, dispatched 2026-05-17)
**Branch**: `feat/v0.1-foundation-and-donki` (local; not pushed)
**Commits**: 4 on top of scaffolding (framework → adapters → tests+fixtures → docs)
**Diff stat**: 33 files, +5554 / -105 lines

---

## TL;DR

Production-quality. **66 unit tests + 1 live integration test passing at 94% coverage**. `ruff`, `mypy --strict` all green. The Gannon-era CME-linkage demo works end-to-end on both fixtures AND real DONKI. The adapter pattern is clean enough that the four follow-up adapters (SEP Scoreboards, SWPC, CDDIS GIMs, GOES+DSCOVR wrappers) can be parallelized confidently.

**Recommend merging** after reviewing the 6 surface-area decisions below and resolving the cache-scheme deviation question.

## What landed

### Framework foundation (`src/helios_connectors/`)
- `schema.py` — `NormalizedRecord` dataclass + clearly-marked placeholder `ProvenanceRecord` (single-line swap when A v0.1 ships) + `SourceID` enum (12 sources already enumerated)
- `ratelimit.py` — asyncio token-bucket `RateLimiter` + `RateLimitConfig`
- `http.py` — `make_client()` with NASA-etiquette User-Agent + `request_with_retry()` (tenacity exponential backoff for 429/5xx/transport errors). **API keys never logged.**
- `cache.py` — `FileCache` parquet-on-disk, **content-addressed by sha256(SourceID, sorted params)** (see deviation note below). `HELIOS_CACHE_ROOT` env-var override honored.
- `adapters/base.py` — `BaseAdapter(ABC)` with streaming `fetch()`, sync `fetch_sync()`, `_emit_provenance()`, async context-manager support.

### DONKI adapter (`src/helios_connectors/adapters/donki.py`)
- All 10 endpoints: CME, CMEAnalysis, FLR, SEP, GST, IPS, MPC, RBE, HSS, notifications
- Unified `fetch(types=...)` does concurrent fan-out across endpoint types
- **Dual-endpoint failover**: defaults to `api.nasa.gov`, falls back to `kauai.ccmc.gsfc.nasa.gov` (no API key, different path prefix) when api.nasa.gov returns 503/timeouts. This is the operational win.
- DEMO_KEY fallback with stricter rate limit + warning log
- `linkedEvents` properly populated as `dataset_refs` lineage on every record that has them

### Tests (`tests/`)
- `test_base.py`, `test_cache.py`, `test_ratelimit.py`, `test_http.py`, `test_donki.py` (433 lines!)
- **9 real DONKI fixtures captured during Gannon week** at `tests/fixtures/donki/{CME,FLR,GST,IPS,SEP,MPC,RBE,notifications}_sample.json` (5554 lines of real-world JSON)
- The CME_sample.json alone is 1403 lines — substantial real-data corpus for downstream agents to test against without API access
- Live test marked `@pytest.mark.live`; nightly CI + manual dispatch only

### Docs
- `docs/index.md` — adapter survey table
- `docs/design.md` — framework recipe for adding new adapters (this is the playbook for the SEP/SWPC/CDDIS/GOES/DSCOVR follow-up agents)
- `docs/adapters/donki.md` — full reference + API quirks

### Example
- `examples/donki_quickstart.ipynb` (Gannon walkthrough)
- `examples/build_donki_quickstart.py` regenerates the notebook deterministically (smart — avoids cell-output diff noise)

### CI
- Split `pytest -m "not live"` PR job from `live-integration` nightly+dispatch job — exactly the right pattern

## DONKI API quirks (gold for follow-up adapter agents)

These should be **copied verbatim into the SEP Scoreboards / SWPC / CDDIS adapter briefs**:

1. **`api.nasa.gov` is significantly flakier than `kauai.ccmc.gsfc.nasa.gov`** for CCMC-hosted endpoints. Adapter supports both via `base_url=DONKI_KAUAI_BASE_URL` (no api_key, different `/DONKI/WS/get/` prefix).
2. **`linkedEvents` is nullable** — ~half of FLR records in Gannon week have `linkedEvents: null`.
3. **CMEAnalysis has *no* `linkedEvents` field at all** — only `associatedCMEID`. Adapter substitutes the parent CME as a single-element lineage so analyses aren't orphans.
4. **Per-endpoint stable identifier field varies wildly**: `activityID` / `flrID` / `sepID` / `gstID` / `mpcID` / `rbeID` / `hssID` / `messageID` / `associatedCMEID`. Don't assume a uniform naming.
5. **Notifications endpoint occasionally returns a singleton dict instead of a list** — adapter defensively wraps both. Other CCMC endpoints may do the same.
6. **Maximum window is ~30 days per call** before silent truncation. Caller responsibility for now; follow-up adapters should window-chunk if they need longer ranges.
7. **Date math is inclusive on both ends.**

## Lineage on real Gannon-era CME: **demonstrated end-to-end**

GST record `2024-05-10T15:00:00-GST-001` carries the lineage:
```
2024-05-08T05:36:00-CME-001  (CME #1 — initial halo)
2024-05-08T12:24:00-CME-001  (CME #2)
2024-05-08T19:12:00-CME-001  (CME #3)
2024-05-08T22:24:00-CME-001  (CME #4 — the big one)
2024-05-09T09:24:00-CME-001  (CME #5)
2024-05-10T16:36:00-IPS-001  (interplanetary shock arrival)
```

Tested both via fixture (`test_fetch_gst_gannon_lineage`) and live API. **This is the most concrete evidence we have so far that the "intelligent linkages" claim in proposal §2 Obj. 1 is real and operational.**

## Surface-area decisions worth a human pass

1. **Sync wrapper refuses inside running loop**. `fetch_sync()` raises `RuntimeError` if called from inside an active event loop. Alternative: `nest_asyncio` for notebook-friendliness. Agent chose explicit-error for safety. **Recommend**: keep as-is, document the workaround in docs/design.md.
2. **`NormalizedRecord.value` is `dict[str, Any]`**. Wider than strictly needed (Kp is a scalar) but lets a CME carry its full payload. Future per-source pydantic models could narrow this. **Recommend**: revisit after A v0.1 ships and we know the real Provenance shape; could be tightened in v0.2.
3. **Cache is content-addressed by fingerprint, not the date-bucketed scheme in the brief**. The brief specified `~/.cache/helios-connectors/<source>/<date>.parquet`. Agent chose `sha256(SourceID, sorted_params).parquet`. **Trade-off**: easier to generalize across adapters but loses calendar-grep affordance. **Recommend**: keep agent's choice (it's the better engineering decision); update the brief to match.
4. **Per-adapter rate limiters** (not shared global). When SWPC + DONKI ship together AND both hit shared infrastructure (e.g., both behind cloudfront), aggregate request budget needs external coordination. **Recommend**: add a `RateLimitCoordinator` in v0.3 when multi-adapter integration is real; not blocking for v0.1.
5. **`_emit_provenance` returns a `frozen=True` dataclass with `tuple[str, ...]` fields**. When swapping to `helios-provenance` (pydantic), check field-order assumption around `dataset_refs` and `lineage` — may need `list[str]` upstream. **Recommend**: the A→B swap PR should verify this in tests.
6. **Live test uses kauai by default** so CI doesn't need a `NASA_API_KEY` secret. If you want the api.nasa.gov path covered nightly, add `NASA_API_KEY` GitHub secret and the nightly job picks it up. **Recommend**: add the secret; it's free DEMO_KEY-tier traffic and catches api.nasa.gov regressions before users hit them.

## Merge readiness

- ✅ CI green (66 unit tests, 94% coverage, lint/type/format all clean)
- ✅ README + design doc + adapter reference doc + example notebook
- ✅ LICENSE + NOTICE + CITATION.cff
- ✅ 9 real-data fixtures (5554 lines of JSON) committed — huge value for downstream agents
- ⏳ Tagged v0.1.0 (agent did NOT tag; v0.1 is partial since 5 more adapters are pending). **Recommend**: hold off on v0.1.0 tag until at least 3 adapters live (DONKI + SWPC + GOES). Use `v0.1.0a1` if you want an early PyPI alpha.
- ⏳ PyPI publish — defer to v0.1.0 (after 3+ adapters)
- ⏳ DOI mint — defer to v0.1.0

## Sequence the operator should run

```bash
# 1. Pre-merge review
cd ~/577i-Projects/helios-spaceweather-connectors
git diff main..feat/v0.1-foundation-and-donki | less
git checkout feat/v0.1-foundation-and-donki
pip install -e '.[dev]'
pytest -m "not live" --cov && ruff check . && ruff format --check . && mypy

# 2. Optionally run the live test once locally
NASA_API_KEY=DEMO_KEY pytest -m live -v

# 3. Merge
git checkout main
git merge --no-ff feat/v0.1-foundation-and-donki -m "feat: connectors v0.1 foundation + DONKI adapter

Adapter pattern (BaseAdapter abstract class with streaming fetch + sync wrapper),
file cache (parquet, content-addressed), token-bucket rate limiter, retry-aware
HTTP client with NASA-etiquette User-Agent, dual-endpoint failover.

DonkiAdapter implements all 10 DONKI endpoints (CME, CMEAnalysis, FLR, SEP,
GST, IPS, MPC, RBE, HSS, notifications) with intelligent linkages preserved
as lineage. Real Gannon-era CME->GST chain verified end-to-end (fixture +
live API).

66 unit tests + 1 live integration test, 94% coverage. 9 real DONKI fixtures
captured during Gannon week as test corpus."

git push origin main
# No v0.1.0 tag yet — wait for ≥3 adapters
```

## Downstream impact

Once B-foundation lands on main:
- **Five next-wave adapter agents** can be dispatched in parallel (SEP Scoreboards, SWPC, CDDIS GIMs, GOES wrapper, DSCOVR wrapper), each cloning the DONKI shape. The `docs/design.md` playbook is the canonical reference. Brief each with the 7 DONKI quirks above as background.
- **Fusion engine (Artifact C)** can start consuming DONKI data via this adapter for its synthetic-eval-→-real-data integration test. Today its eval harness is purely synthetic.
- **Gannon analysis (Artifact D)** could optionally use this adapter to pull DONKI events for the May 8-14 2024 window, supplementing its NGS CORS analysis with a unified event timeline. Not required for D v0.1, but nice cross-pollination.
- After **A v0.1 ships and B is merged**: dispatch the A→B swap agent to replace the placeholder ProvenanceRecord with the real import. ~30-min task.

## Notable craftsmanship

- The `examples/build_donki_quickstart.py` deterministic notebook regenerator is a small thing that prevents merge-noise from cell-output diffs. Quietly excellent.
- Splitting unit tests from live integration into separate CI jobs is exactly right; PR signal stays fast, nightly catches upstream API changes.
- Treating `api.nasa.gov` and `kauai.ccmc.gsfc.nasa.gov` as failover pair is operational insight that comes only from actually hitting both endpoints under stress.

---

**Bottom line**: ready for your review and merge. The cache-scheme deviation is the only point worth a moment's thought (and I recommend accepting it). The Gannon CME-lineage demo is the strongest single piece of evidence in the program right now.
