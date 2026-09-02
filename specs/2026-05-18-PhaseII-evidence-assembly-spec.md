# Phase II Evidence Assembly Dispatch Spec

**Type**: forward-looking dispatch spec (incremental — runs once initially; refreshed each session as artifacts ship).
**Status**: ready to dispatch.
**Estimated agent runtime**: 2-3 hours initial assembly; 30-60 min per refresh.

---

## TL;DR

Assembles a Phase II proposal evidence package from the current portfolio: companion document as the lead narrative, 5 public artifact URLs with current status, 4 (eventually 5) citable Gannon ground-truth observations, RFC community engagement record, customer-discovery letter-of-intent tracker, NASA-center engagement log, refined commercialization plan. Output is operator-facing summary material ready for Phase II proposal embed.

## Why this matters now

Phase I is shipped. The HELIOS portfolio is **Phase-II-ready**. The window to convert that into a strong Phase II proposal is open. Every Phase II reviewer asks the same question: "what did you actually deliver in Phase I?" Having a single curated evidence package — with URLs the reviewer can immediately click — is the highest-leverage proposal-prep work outside the actual technical objectives.

## Prerequisites

None on the agent side. The operator-action items below are independent and can land in any order, refreshed iteratively:

| Operator-action input | Where it goes |
|---|---|
| LoI signatures from named-candidate ML Engineer + SME consultant | `phase-ii/letters/{ml-engineer.pdf, sme-consultant.pdf}` |
| Customer-discovery interview notes (≥4 ag-industry; ≥2 NASA-center) | `phase-ii/customer-discovery/<interview-date>-<organization>.md` |
| NASA-center engagement record (CCMC, M2M SWAO, SRAG, SPoRT) | `phase-ii/nasa-engagement/<center>-<date>.md` |
| Commercialization plan refined per Phase I learnings | `phase-ii/commercialization-plan-refined.md` |

The agent can assemble what already exists today and document placeholders for the operator-driven items.

## Evidence inventory

7 categories of evidence the agent compiles from existing artifacts:

### 1. Lead narrative

- **`helios-program/companion/companion.md`** — the public-facing mirror of the submitted proposal with live citations. Already at v0.2.0; updated weekly via `companion_sync.py`.
- Hosted live at <https://577industries.github.io/helios-program/companion/>.
- This IS the proposal evidence backbone. The evidence-package PDF references it throughout.

### 2. Public artifact URLs with current status

Pull from `companion/footnotes.yaml` (auto-synced):

| Artifact | Current release | Pages | PyPI (if applicable) |
|---|---|---|---|
| `helios-program` | v0.2.0 | <https://577industries.github.io/helios-program/> | n/a |
| `helios-provenance-spec` | v0.1.0 | <https://577industries.github.io/helios-provenance-spec/> | TBD (pending trusted-publishing config) |
| `helios-spaceweather-connectors` | v0.2.1 | <https://577industries.github.io/helios-spaceweather-connectors/> | TBD |
| `helios-fusion-engine` | v0.1.2 | <https://577industries.github.io/helios-fusion-engine/> | TBD |
| `gannon-storm-rtk-analysis` | v0.1.0 | <https://577industries.github.io/gannon-storm-rtk-analysis/> | n/a (analysis repo) |

The 5-public-Pages portfolio is itself the most compelling evidence: every claim in the proposal has a click-through reviewer can audit independently.

### 3. Citable Gannon ground-truth observations

4 (will be 5 after Sprint D) verifiable measurements, each traceable to a specific record with full provenance lineage:

1. **Kp peak = 9.0** on 2024-05-11 (SwpcAdapter via GFZ Potsdam; CC-BY-4.0)
2. **Bz peak = -59.16 nT** on 2024-05-10 (DscovrAdapter via DSCOVR L2 SPDF; GSE frame; 86,400 1-second samples)
3. **TEC peak = 55.1 TECU at Columbus OH** at 2024-05-10T20:00 UTC (CddisGimAdapter synthetic; real-data confirmation pending Earthdata creds)
4. **1,302 station-hours over 2.5 cm** across 25 NGS CORS stations IA/IL/IN/OH (`gannon-storm-rtk-analysis` v0.1.0; v2 upgrade via TFT-TEC pending)
5. **(After Sprint D)** Kill-gate hold-out HSS / Brier / CRPS for Gannon event — the proof point that calibrated fusion beats best-component on the proposal's marquee event

### 4. RFC community engagement

- **RFC-0001 issue**: <https://github.com/577Industries/helios-provenance-spec/issues/4>
- Comments accumulated to date (snapshot at evidence-assembly time)
- Cross-posts to SPASE community list / sunpy-dev / CCMC feedback channel (operator action; document URLs when sent)

### 5. Sprint C-Training v1 + v2 review packs (methodology evolution)

Demonstrates the program's rigor + adaptability:
- **v1 review pack**: `specs/2026-05-17-Sprint-C-Training-review-pack.md` — initial training, honest synthetic-proxy disclosure
- **v2 review pack**: `specs/2026-05-17-Sprint-C-Training-v2-review-pack.md` — exhaustive ISWA probe, hybrid Path A+B decision, real NOAA SESC truth labels
- ISWA coverage matrix: `results/2026-05-17-iswa-coverage-matrix.md` (the empirical Jan 2017 cutover finding)

This is the **discipline signal** for reviewers: when an assumption broke (v1's synthetic-proxy fallback was unnecessarily blanket), the program empirically probed, documented, and refit — without claiming a result it didn't have.

### 6. Kill-gate result (post-Sprint D)

- `helios-program/results/<date>-killgate.json`
- Reliability diagrams per Kp stratum
- Bootstrap CI distributions
- Decision-tree branch routing (full paper / honest ablation / no paper)

After Sprint D this becomes the headline.

### 7. arXiv preprint URL (post-Sprint D, post-submission)

- arXiv ID + DOI
- Cover letter
- Pre-registration linkage

## New `helios-program/phase-ii/` directory layout

```
helios-program/phase-ii/
├── README.md                        # 1-page overview pointing at the evidence package
├── evidence-package.md              # Single-file curated summary (becomes PDF)
├── evidence-package.pdf             # Auto-built via pandoc on every push (GH Pages workflow)
├── letters/
│   ├── README.md                    # Inventory: who, role, status (operator-maintained)
│   ├── ml-engineer-loi.pdf          # Operator action
│   ├── sme-consultant-loi.pdf       # Operator action
│   ├── nasa-center-loi-1.pdf        # CCMC / M2M SWAO / SRAG / SPoRT (≥2 per proposal §2 Obj. 5)
│   ├── nasa-center-loi-2.pdf
│   ├── ag-industry-loi-1.pdf        # OSU Extension / OARDC / Deere / AGCO / CNH (≥2 per proposal §2 Obj. 5)
│   └── ag-industry-loi-2.pdf
├── customer-discovery/
│   ├── README.md                    # Inventory of interviews
│   └── YYYY-MM-DD-<organization>.md # One file per interview (operator-driven)
├── nasa-engagement/
│   ├── README.md                    # Inventory of NASA-center contacts
│   ├── ccmc-YYYY-MM-DD.md
│   ├── m2m-swao-YYYY-MM-DD.md
│   ├── srag-YYYY-MM-DD.md
│   └── sport-YYYY-MM-DD.md
├── commercialization-plan-refined.md # Phase I learnings → Phase II plan refinement
└── phase-ii-proposal-draft.md       # The actual Phase II proposal (when ready)
```

## Agent brief sketch

The agent doesn't need a worktree (touches only `helios-program/`); commit directly on a feature branch `feat/phase-ii-evidence-assembly`.

1. **Read** all existing artifacts in inventory categories 1-5 (categories 6, 7 await Sprint D).
2. **Assemble `phase-ii/evidence-package.md`** — single curated document covering the 7 categories. Each section pulls from the live source artifacts (cross-link URLs, don't duplicate content).
3. **Auto-render to PDF** via `pandoc evidence-package.md -o evidence-package.pdf --pdf-engine=xelatex` (or similar). Add a CI workflow that rebuilds on every push.
4. **Scaffold the operator-action subdirectories** (`letters/`, `customer-discovery/`, `nasa-engagement/`) with README inventories + empty placeholders. Don't create fake LoI PDFs.
5. **Refine commercialization plan** at `phase-ii/commercialization-plan-refined.md`:
   - Phase I learnings → Phase II adjustments (e.g., ISWA pre-2017 cutover discovered + worked around → demonstrates resilience; v0.2.1 registry expansion → demonstrates rigor)
   - Refine the §6.2 revenue model per Phase I customer-discovery if interview notes are committed
   - Update the §6.3 go-to-market based on actual partnership conversations (operator-driven)
6. **Phase II proposal draft scaffold** at `phase-ii/phase-ii-proposal-draft.md`:
   - Use the submitted Phase I proposal as the template (`/home/twawe/577i-Projects/GitHub/577Industries/sbir-nasa-helios-proposal/drafts/_archive/HELIOS_NASA_SBIR_PhaseI_Proposal_2026-05-17_CANONICAL_v0.docx`)
   - Update §1.3 Gannon to reference the v2 real-SPP analysis (when TFT lands)
   - Update §2 success criteria to reflect Phase II thresholds (CCMC proving-ground evaluation, OEM partnership commitments, etc.)
   - Update §3.3 Phase II vision → Phase II execution plan
   - Add a §4.3 "Phase I results" section heavily citing the evidence package URLs

## Files to be created

| Path | Action |
|---|---|
| `helios-program/phase-ii/README.md` | NEW |
| `helios-program/phase-ii/evidence-package.md` | NEW (the curated summary) |
| `helios-program/phase-ii/letters/README.md` | NEW (inventory) |
| `helios-program/phase-ii/customer-discovery/README.md` | NEW (inventory) |
| `helios-program/phase-ii/nasa-engagement/README.md` | NEW (inventory) |
| `helios-program/phase-ii/commercialization-plan-refined.md` | NEW |
| `helios-program/phase-ii/phase-ii-proposal-draft.md` | NEW (scaffold; operator fills) |
| `helios-program/.github/workflows/phase-ii-pdf.yml` | NEW (auto-renders evidence-package.pdf) |
| `helios-program/mkdocs.yml` | Edit (add `phase-ii/` to nav or to "Plans" section) |

## Verification gates

1. `evidence-package.md` renders to PDF without errors via the new CI workflow.
2. Every URL in evidence-package.md returns HTTP 200 (lychee link-check in the existing companion-check workflow).
3. The 4 (or 5) citable Gannon ground-truth observations are each traceable to a specific commit SHA + record ID + provenance JSON.
4. `commercialization-plan-refined.md` references at least 3 specific Phase I learnings with cross-links to the source artifacts.
5. The Phase II proposal scaffold has all section headings from the Phase I proposal preserved.

## Incremental refresh policy

After this first assembly, the evidence package should be refreshed:

- **After Sprint D**: add the kill-gate result + reliability diagrams
- **After arXiv submission**: add the preprint URL
- **After TFT-TEC ships**: update the §1.3 Gannon ground-truth observation #4 to real-SPP-v2
- **As operator-action items land**: LoI PDFs, customer-discovery notes, NASA-center engagement records all incrementally added to their subdirectories

Each refresh is a small focused commit; the README at `phase-ii/README.md` tracks the last-refresh date.

## What this sprint does NOT do

- Does NOT solicit LoIs (operator action).
- Does NOT conduct customer-discovery interviews (operator action).
- Does NOT submit the Phase II proposal (operator action; the actual submission deadline depends on the NASA Phase II solicitation cycle).
- Does NOT change any technical content in the artifact repos.

## Cross-references

- Submitted Phase I proposal: `/home/twawe/577i-Projects/GitHub/577Industries/sbir-nasa-helios-proposal/drafts/_archive/HELIOS_NASA_SBIR_PhaseI_Proposal_2026-05-17_CANONICAL_v0.docx`
- Companion document: `helios-program/companion/companion.md`
- All 5 review packs in `helios-program/specs/`
- `OPERATOR_TODO.md` items 5-7 (operator-driven inputs)
- Master plan §6 (Phase II commercialization context)
