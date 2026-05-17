# Artifact A — `helios-provenance-spec` v0.1 Review Pack

**Agent**: A (background, dispatched 2026-05-17)
**Branch**: `feat/v0.1-rfc` (local; not pushed)
**Local tag**: `v0.1.0` (annotated; not pushed)
**Commits**: 3 on top of scaffolding (schema → tests → docs/RFC)

---

## TL;DR

Substantial and clean. 98 tests passing at **98% coverage** on `src/helios_provenance/`. `ruff check`, `ruff format --check`, and `mypy --strict` all green. The centerpiece worked example (a `HeliosFusedOutputRecord` with full 3-step lineage tracing back through conformal wrapping → BMA averaging → isotonic calibration to three Scoreboard A inputs) is implemented at `schema/examples/11-fused-sep-all-clear.json` and round-trips through tamper-detecting hashing.

**Recommend merging** after reviewing the 4 open questions below.

## What landed (file-by-file highlights)

### Schema (`schema/`)
- `helios-provenance-v0.1.json` — JSON Schema 2020-12 with 4 record types under `oneOf` discriminator. Uses `unevaluatedProperties: false` per-branch (cleaner than `additionalProperties` for `allOf` composition).
- `examples/01..11-*.json` — 11 valid records: DONKI flare, Scoreboard A (UMASEP-10), SWPC Kp, CDDIS GIM TEC, GOES protons, DSCOVR solar wind, isotonic/BMA/conformal transformations, and the fused output.
- `crosswalks/{spase,prov,ro-crate}.md` — field-by-field mappings.

### Python reference impl (`src/helios_provenance/`)
- `__init__.py` — version `0.1.0`; full public API exported.
- `models.py` — pydantic v2 with `extra="forbid"`; `parse_record()`, `to_jsonld()`, `HeliosFusedOutputRecord.build_with_hash()`, `verify_hash()`.
- `hashing.py` — RFC 8785 JCS canonical-JSON hashing with documented fallback, null-stripping normalization, rejection of non-finite floats. **Hash payload covers** `lineage + prediction_target + timestamp + value + value_units + schema_version`. **Does NOT cover** `conformal_interval`, `location`, `agent` — see open question #1.
- `validator.py` — `HeliosProvenanceValidator` class + `helios-provenance-validate` CLI (supports stdin via `-`).
- `crosswalk.py` — `dataset_to_spase_xml()` + `records_to_prov_json()`.
- `_schema/helios-provenance-v0.1.json` — schema shipped inside the wheel.

### Tests (`tests/`)
- `conftest.py`, `test_smoke.py`, `test_models.py`, `test_hashing.py`, `test_validator.py`, `test_crosswalk.py` — 98 tests total, 0.91s runtime.

### RFC + docs
- `rfc/RFC-0001-feature-lineage.md` — ~2000 words. **Section 6 has 8 explicit open questions** flagged for community comment (see below).
- `docs/{index,schema,examples,api}.md` + mirrored crosswalks/RFC.
- `mkdocs.yml` updated.

### Release-prep additions
- `CHANGELOG.md` (new) — v0.1.0 entry.
- `README.md` refreshed.
- `CITATION.cff` bumped to 0.1.0.
- `pyproject.toml` — added `jsonschema`, `rfc8785`, `rfc3339-validator`, `rfc3987` runtime deps; added `helios-provenance-validate` script entry point.

## Open questions — your call

1. **Push the `v0.1.0` tag now?**
   - Plan says no (operator gates releases). Agent followed plan. The tag is annotated and on `feat/v0.1-rfc` locally.
   - Recommend: review the diff, run `pytest --cov` yourself, then `git checkout main && git merge --no-ff feat/v0.1-rfc && git push origin main && git push origin v0.1.0`.

2. **Open Issue #1 ("RFC-0001: feature-level provenance for heliophysics fusion systems") on GitHub.**
   - Agent deferred this until the branch is on main. Reasonable — the issue body cites `rfc/RFC-0001-feature-lineage.md` and the link needs to resolve.
   - After merge, run `gh issue create --repo 577-Industries/helios-provenance-spec --title "RFC-0001: feature-level provenance for heliophysics fusion systems" --body-file rfc/RFC-0001-feature-lineage.md` (or a hand-edited intro pointing to the file).

3. **The 8 open RFC §6 questions** — community-comment items. Worth scanning to confirm none should be pre-resolved before publishing the RFC. The two most consequential per my read:
   - **Q1 (code_ref shape)**: free-form string vs. structured `{git_url, sha, path}`. Structured is more rigorous; free-form is easier for early adopters. The agent left it as string. Reasonable for v0.1 RFC.
   - **Q8 (hash payload composition)**: should `conformal_interval`, `location`, `agent` be inside the hash? Trade-off: including them makes records tamper-evident across MORE dimensions but breaks hash stability when, e.g., a conformal recalibration recomputes intervals without changing the underlying fused value. The agent excluded them; the rationale is reasonable and worth confirming.

4. **`@context` URI is a placeholder** (`577-industries.github.io/.../v0.1.jsonld`) in `to_jsonld()` output. Real URL becomes the MkDocs site address once docs deploy. Fix as a v0.1.1 patch alongside docs deployment.

## Merge readiness checklist (per master plan §"Per-Artifact 'citable'-readiness")

- ✅ CI green on main (will run on push; local pytest/ruff/mypy all green)
- ✅ README with badges + working quick-start
- ✅ LICENSE (Apache 2.0) + NOTICE + CITATION.cff
- ⏳ Tagged v0.1.0 (local; not pushed)
- ⏳ Published to PyPI (post-merge via GH release)
- ⏳ DOI minted via Zenodo (post-tag-push)
- ⏳ RFC issue open and circulated (post-merge; see open question #2)
- *N/A in this RFC pass*: pre-registration on OSF (that's for Artifact C)

## Sequence the operator should run

```bash
# 1. Pre-merge review
cd ~/577i-Projects/helios-provenance-spec
git diff main..feat/v0.1-rfc | less
git checkout feat/v0.1-rfc
pip install -e '.[dev]'
pytest --cov && ruff check . && ruff format --check . && mypy

# 2. Merge
git checkout main
git merge --no-ff feat/v0.1-rfc -m "feat: helios-provenance-spec v0.1.0 RFC

JSON Schema 2020-12 for 4 record types (Dataset / ModelOutput /
Transformation / FusedOutput). pydantic v2 reference implementation with
tamper-evident lineage hashing. 11 worked examples including end-to-end
fused SEP all-clear lineage. SPASE / PROV-JSON / RO-Crate crosswalks.
RFC-0001 issued for community comment.

98 tests, 98% coverage."

# 3. Push branch + tag
git push origin main
git push origin v0.1.0

# 4. Open GitHub release (auto-trigger PyPI publish if trusted publishing is configured)
gh release create v0.1.0 --generate-notes --repo 577-Industries/helios-provenance-spec

# 5. Open RFC discussion issue
gh issue create --repo 577-Industries/helios-provenance-spec \
  --title "RFC-0001: feature-level provenance for heliophysics fusion systems" \
  --body "See \`rfc/RFC-0001-feature-lineage.md\`. Comments welcome on the 8 open questions in §6."

# 6. Notify the helios-program companion that A has shipped
cd ~/577i-Projects/helios-program
python -m orchestration.companion_sync
git add companion/footnotes.yaml
git commit -m "chore: companion sync after helios-provenance-spec v0.1.0"
git push
```

## Downstream impact

Once A v0.1.0 lands and is pushed:
- **Connectors (Artifact B)** has a placeholder `ProvenanceRecord` it can now swap for `from helios_provenance.models import HeliosModelOutputRecord` etc. Dispatch a follow-up agent against `helios-spaceweather-connectors` on `feat/v0.2-real-provenance` to do this swap, update tests, and tag v0.2.0.
- **Fusion engine (Artifact C)** also has placeholder types in `src/helios_fusion/types.py`. Same swap. Dispatch in parallel.
- **Companion document** updates automatically via `companion_sync` — once v0.1.0 is tagged on GH, `companion/footnotes.yaml` will reflect `version: 0.1.0` and `status: in-development`.

## Confidence notes

- The schema design is conservative (composes existing standards rather than inventing) but adds a genuinely novel feature-level lineage record. That's the right shape for an RFC — easier to gather community comments than to defend something fully novel.
- The `rfc8785` library handles JCS canonical JSON. If the maintainers ever break compatibility, the documented fallback (in `hashing.py`) ensures backward decodability. Reasonable defensive choice.
- The agent added 4 runtime deps (`jsonschema`, `rfc8785`, `rfc3339-validator`, `rfc3987`). All small, well-maintained. Acceptable for a spec library.

---

**Bottom line**: ready for your review and merge. No blocking issues found; 4 questions are gated on your decision, none of which change the implementation.
