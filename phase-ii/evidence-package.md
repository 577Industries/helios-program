---
title: "HELIOS Phase II — Evidence Package"
subtitle: "Curated Phase I deliverables for Phase II proposal embed"
author: "577 Industries Inc. — Columbus, Ohio"
date: "2026-05-18"
---

# HELIOS Phase II — Evidence Package

**Heliophysics-Enhanced Location Integrity and Operations System**
*Calibrated Space-Weather Decision Intelligence for NASA Mission Operations and U.S. Precision Agriculture*

**Submitted by**: 577 Industries Inc. — Columbus, Ohio — <https://www.577industries.com>
**Principal Investigator**: Thomas Waweru
**NASA Phase I subtopic**: SPWX.1.S26A — Advanced Data-Driven Applications for Space Weather R2O2R
**Last refreshed**: 2026-05-18 (initial assembly)

---

> **About this document.** This evidence package is a one-shot orientation packet for Phase II proposal reviewers and NASA-center contacts. It curates the Phase I portfolio across 7 evidence categories — every claim has a clickable URL the reviewer can audit independently. It does **not** duplicate the public companion document ([`companion/companion.md`](https://github.com/577Industries/helios-program/blob/main/companion/companion.md)); the companion is the *narrative*, this is the *evidence index*.

## Quick map for reviewers

| Question a reviewer asks | Section |
|---|---|
| "What did 577 Industries actually deliver in Phase I?" | §1 (narrative), §2 (artifact URLs) |
| "Show me one verifiable, citable claim" | §3 (5 Gannon ground-truth observations) |
| "Are they engaging the community?" | §4 (RFC-0001) |
| "Did the methodology survive contact with real data?" | §5 (Sprint C-Training v1 → v2 evolution) |
| "Does the calibrated fusion beat best-component?" | §6 (kill-gate result — post-Sprint D) |
| "Is there a peer-reviewable artifact?" | §7 (arXiv preprint — post-submission) |

---

## 1. Lead narrative

The Phase I deliverable narrative is in the public companion document:

- **Companion (live)**: <https://577industries.github.io/helios-program/companion/>
- **Companion (source)**: [`companion/companion.md`](https://github.com/577Industries/helios-program/blob/main/companion/companion.md) in this repo (v0.2.0; updated weekly via `companion_sync.py`)

The companion mirrors the submitted Phase I proposal section-by-section and attaches **live citations** to every public artifact as it ships. Use the companion as the reading-order entry point; the evidence package below is the index that lets a reviewer jump directly to any specific claim's underlying artifact.

---

## 2. Public artifact URLs with current status

Five public Pages sites and four public repositories (plus one private companion for the trained-weights IP). All claims in the Phase I proposal map to one of these.

| # | Artifact | Repo | Pages (HTTP 200) | Release | Cited in proposal | Notes |
|---|---|---|---|---|---|---|
| 1 | `helios-program` (meta) | [GitHub](https://github.com/577Industries/helios-program) | [docs](https://577industries.github.io/helios-program/) | v0.2.0 | (meta) | Master plan, companion, specs, operations |
| 2 | `helios-provenance-spec` | [GitHub](https://github.com/577Industries/helios-provenance-spec) | [docs](https://577industries.github.io/helios-provenance-spec/) | v0.1.0 (RFC) | §1.4 · §4.2 innovation #2 | JSON Schema draft 2020-12 + pydantic v2 ref impl |
| 3 | `helios-spaceweather-connectors` | [GitHub](https://github.com/577Industries/helios-spaceweather-connectors) | [docs](https://577industries.github.io/helios-spaceweather-connectors/) | v0.2.1 | §2 Obj. 1 · §3 T1 | 6 adapters live (DONKI · SWPC · GOES · DSCOVR · CDDIS · Scoreboards) |
| 4 | `helios-fusion-engine` | [GitHub](https://github.com/577Industries/helios-fusion-engine) | [docs](https://577industries.github.io/helios-fusion-engine/) | v0.1.2 | §2 Obj. 2 · §3.1 · §4.2 innovation #1 | BMA + isotonic + Mondrian conformal; 176 tests; ≥80% coverage |
| 5 | `gannon-storm-rtk-analysis` | [GitHub](https://github.com/577Industries/gannon-storm-rtk-analysis) | [docs](https://577industries.github.io/gannon-storm-rtk-analysis/) | v0.1.0 | §1.3 Gannon · §2 Obj. 4 · §4.2 innovation #4 | 1,302 station-hours over 2.5 cm (v1 climatological) |
| 6 | `helios-fusion-internal` | (private — IP-gated) | n/a (private) | refit at `00a80eb` | (proprietary) | Trained BMA priors, isotonic calibrators, equipment transfer functions |

**Machine-readable artifact registry**: [`companion/footnotes.yaml`](https://github.com/577Industries/helios-program/blob/main/companion/footnotes.yaml) — auto-synced via `python -m orchestration.companion_sync`.

The **5-public-Pages portfolio is itself the strongest evidence**: every claim in the proposal has a click-through path a reviewer can audit without 577 Industries' cooperation.

---

## 3. Citable Gannon ground-truth observations

Five verifiable measurements anchored to the May 10-12, 2024 Gannon G5 superstorm. Each has full provenance lineage (record ID + commit SHA + `.provenance.json` path). The 5th lands after Sprint D ships.

### 3.1 Kp peak = 9.0 on 2024-05-11

- **Source**: NOAA SWPC archive via `SwpcAdapter` (helios-spaceweather-connectors v0.2.1)
- **Upstream license**: CC-BY-4.0 (NOAA SWPC data) / GFZ Potsdam Kp index
- **Record ID**: `swpc.kp_index.2024-05-11.peak`
- **Adapter commit SHA**: see [`helios-spaceweather-connectors` v0.2.1 release](https://github.com/577Industries/helios-spaceweather-connectors/releases/tag/v0.2.1)
- **Cross-references in companion**: §1.3 Gannon paragraph, §3.1 Table 3-1 hold-out row, §4.2 innovation #4
- **Adapter docs**: <https://577industries.github.io/helios-spaceweather-connectors/adapters/swpc/>

### 3.2 Bz peak = -59.16 nT on 2024-05-10 (GSE frame)

- **Source**: NASA SPDF DSCOVR L2 via `DscovrAdapter` (helios-spaceweather-connectors v0.2.1)
- **Coordinate frame**: GSE
- **Sample density**: 86,400 1-second samples over the 24-hour window
- **Record ID**: `dscovr.l2.2024-05-10.bz_min`
- **Adapter docs**: <https://577industries.github.io/helios-spaceweather-connectors/adapters/dscovr/>
- **Review pack**: [`specs/2026-05-17-Wave2a-DSCOVR-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Wave2a-DSCOVR-review-pack.md)

### 3.3 TEC peak = 55.1 TECU at Columbus OH at 2024-05-10T20:00 UTC

- **Source**: NASA CDDIS Global Ionosphere Maps (IONEX) via `CddisGimAdapter` (helios-spaceweather-connectors v0.2.1)
- **Resolution**: 2-hour temporal, 2.5° latitude × 5° longitude
- **Current evidence-state**: synthetic (verified against the v1 climatological model); **real-data confirmation pending Earthdata credentials** (operator action — `OPERATOR_TODO.md` item 2). When credentials land, this row is refreshed to "real" and the Gannon analysis is retagged v0.2.0.
- **Record ID**: `cddis.gim.2024-05-10T20Z.columbus`
- **Adapter docs**: <https://577industries.github.io/helios-spaceweather-connectors/adapters/cddis/>
- **Review pack**: [`specs/2026-05-17-Wave2b-CDDIS-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Wave2b-CDDIS-review-pack.md)

### 3.4 1,302 station-hours over 2.5 cm across 25 NGS CORS stations

- **Coverage**: IA / IL / IN / OH; 25 stations; May 10-12, 2024
- **Threshold**: 2D horizontal positioning error > 2.5 cm (the planting threshold for John Deere StarFire 6000 / Trimble RTK / AgLeader)
- **Model version**: v1 climatological (single-frequency ionosphere proxy) — **headline carries an inline climatological-v1 disclosure** per `gannon-storm-rtk-analysis/docs/methodology.md`. *Do not strip the disclosure.*
- **v2 upgrade pending**: full pseudo-range SPP via the CDDIS adapter once the TFT-TEC forecasting work (spec [`2026-05-18-TFT-TEC-forecasting-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-TFT-TEC-forecasting-spec.md)) lands. v2 will swap the climatological ionosphere proxy for forecast TEC and re-compute the station-hours headline.
- **Repo**: <https://github.com/577Industries/gannon-storm-rtk-analysis> v0.1.0
- **Docs**: <https://577industries.github.io/gannon-storm-rtk-analysis/>
- **Methodology note**: <https://577industries.github.io/gannon-storm-rtk-analysis/methodology/>
- **Blog post** (lay-audience explainer): <https://577industries.github.io/helios-program/blog/when-the-sky-stopped-the-tractors/>
- **Review pack**: [`specs/2026-05-17-D-gannon-analysis-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-D-gannon-analysis-review-pack.md)

### 3.5 Kill-gate hold-out HSS / Brier / CRPS — PENDING SPRINT D

> **Placeholder.** This observation lands when Sprint D ships per spec [`2026-05-18-Sprint-D-kill-gate-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-Sprint-D-kill-gate-spec.md). Blocked on **OSF pre-registration filing** (OPERATOR_TODO.md item 3).

Expected fields when filled:
- Kill-gate hold-out HSS vs. best-component-model HSS (PASS threshold: ≥15% relative improvement on the 3-event hold-out)
- Reliability-diagram slope per Kp stratum (PASS threshold: within 0.15 of 1.0)
- Brier score + CRPS with bootstrap 95% CIs
- Decision-tree branch routing (full paper / honest ablation / no paper)
- Result JSON at `results/<date>-killgate.json`
- OSF pre-registration URL on file at `orchestration/osf_preregistration.url`
- `helios-fusion-engine` `prereg-v1.0` tag at the locked commit (currently `ac53eb6`)

---

## 4. RFC community engagement

The provenance schema is filed as an open RFC, demonstrating community-engaged standards development before commercial lock-in.

- **RFC-0001 source**: <https://github.com/577Industries/helios-provenance-spec/blob/main/rfc/RFC-0001-feature-lineage.md>
- **RFC issue (open for comment)**: <https://github.com/577Industries/helios-provenance-spec/issues/4>
- **8 §6 design questions** open for community input (SPASE 2.7.1 composition, W3C PROV-JSON binding, RO-Crate 1.2 JSON-LD nesting, transformation-chain depth limits, etc.)
- **Cross-posts** (operator action — `OPERATOR_TODO.md` item 4): SPASE info list · sunpy-dev · CCMC feedback channel · 577 Industries LinkedIn

The novelty claim — **first feature-level lineage standard for heliophysics fusion systems** — is testable: the RFC composition (SPASE + W3C PROV-JSON + RO-Crate) is novel relative to any single-standard predecessor, but the RFC is open so the community can challenge the framing before v0.2.

---

## 5. Sprint C-Training v1 → v2 — methodology evolution

Demonstrates the program's rigor + adaptability. When v1's blanket synthetic-proxy assumption broke under empirical probing, the program documented the deviation, re-fit, and shipped — without claiming a result it didn't have.

### v1 review pack
[`specs/2026-05-17-Sprint-C-Training-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-review-pack.md) — initial Table 3-1 training run; honest synthetic-proxy disclosure for pre-2018 events.

### v2 review pack
[`specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-v2-review-pack.md) — exhaustive ISWA probe, hybrid Path A+B decision, real NOAA SESC archive truth labels, per-(component, event) source labeling.

Key empirical finding: the **ISWA Jan 2017 cutover** — documented in [`results/2026-05-17-iswa-coverage-matrix.md`](https://github.com/577Industries/helios-program/blob/main/results/2026-05-17-iswa-coverage-matrix.md) — established that 6 of 7 Table 3-1 training events have zero real ISWA Scoreboard coverage. v1 had assumed blanket synthetic-proxy fallback; v2 confirmed empirically and labeled per-(component, event) as `iswa_real` (12 tuples for Sept 2017) or `synthetic_proxy` (the remainder).

The OSF "Deviations" methodology note for the pre-registration is drafted at the bottom of the v2 review pack — operator drops it verbatim into the OSF filing.

### v2 release artifacts
- `helios-fusion-engine` v0.1.2: <https://github.com/577Industries/helios-fusion-engine/releases/tag/v0.1.2>
- 176 tests pass; ≥80% aggregate coverage; per-file 82-100%
- `ruff check`, `ruff format --check`, `mypy --strict src/` all clean
- Refit weights in `helios-fusion-internal` `weights/manifest.json` — `training_runs[0]` (v1) preserved, `training_runs[1]` (v2) appended

**The discipline signal for reviewers**: an assumption broke, the program empirically probed, documented the deviation in a public review pack, and re-fit against a different fitness function. The top-weighted component for Sept 2017 shifted from v1's `iPATH` (synthetic-only) to v2's `SAWS_ASPECS/1.X_Nowcasts_Probability` (real ISWA stream) — a different model entirely, reflecting the honest change in evaluation methodology.

---

## 6. Kill-gate result — PENDING SPRINT D

> **Placeholder.** Refreshed when Sprint D ships per [`specs/2026-05-18-Sprint-D-kill-gate-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-Sprint-D-kill-gate-spec.md).

The pre-registered kill-gate is the headline Phase II result. Hypotheses (binding, OSF-filed before any hold-out run):
- **H1**: fused all-clear-revocation HSS on the 3-event hold-out exceeds the best-component-model HSS by ≥15% (relative)
- **H2**: reliability-diagram slope within 0.15 of 1.0 across all three Kp severity strata
- **Hold-out events**: 2022-01-20 (M5.5), 2023-02-17 (X2.2), 2024-05-11 (Gannon G5)
- **Decision rules**: PASS both → full arXiv paper · PASS one → honest ablation paper · FAIL both → no paper

Expected artifacts when filled:
- `results/<YYYY-MM-DD>-killgate.json` — full metrics manifest
- Reliability diagrams per Kp stratum (PNG)
- Bootstrap CI distributions
- Decision branch (paper / ablation / no paper) — documented either way

---

## 7. arXiv preprint URL — POST-SUBMISSION

> **Placeholder.** Refreshed when the arXiv preprint is submitted per [`specs/2026-05-18-arXiv-preprint-draft-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-arXiv-preprint-draft-spec.md). The arXiv draft agent works in a parallel worktree on `helios-fusion-engine/paper/` — no overlap with this evidence package's workspace.

Expected fields when filled:
- arXiv ID (e.g., `arXiv:2026.NNNNN`)
- DOI
- Cover letter (PDF)
- Pre-registration linkage (OSF URL referenced in the paper's pre-registration section)
- Companion repo tag at the submitted commit

---

## Appendix A — verification checklist for this evidence package

The Phase II evidence package itself is a deliverable; this checklist confirms it stays honest as the portfolio evolves.

- [x] Every URL in §2 returns HTTP 200 (Pages-checker pattern; same as `companion-check.yml` lychee step)
- [x] The 4 (currently; 5 after Sprint D) Gannon ground-truth observations each have provenance lineage documented (record ID + adapter + commit-SHA pointer + .provenance.json path)
- [x] `commercialization-plan-refined.md` cites ≥3 specific Phase I learnings with cross-links to source artifacts (5 cited)
- [x] `phase-ii-proposal-draft.md` preserves the Phase I proposal's §1-8 section structure
- [x] `mkdocs build --strict` passes locally with `phase-ii/` content in nav
- [x] `evidence-package.md` renders to PDF without errors via [`.github/workflows/phase-ii-pdf.yml`](https://github.com/577Industries/helios-program/blob/main/.github/workflows/phase-ii-pdf.yml)
- [ ] §6 kill-gate placeholder replaced with real numbers (post-Sprint D)
- [ ] §7 arXiv placeholder replaced with preprint URL (post-submission)
- [ ] §3.3 TEC observation upgraded synthetic → real (post-Earthdata creds + TFT-TEC ship)

---

*This evidence package is maintained at [github.com/577Industries/helios-program](https://github.com/577Industries/helios-program). Auto-built PDF artifact attached to every workflow run on `main` via `.github/workflows/phase-ii-pdf.yml`. Contact: <engineering@577industries.com>.*
