# HELIOS Phase II — evidence package

**Last refreshed**: 2026-05-18 (initial assembly)
**Status**: incremental — refreshed each session as new artifacts ship.

This directory holds the **Phase II proposal evidence package** — operator-facing summary material curated from the existing HELIOS portfolio, ready to embed in the Phase II proposal narrative or hand to NASA-center reviewers as a one-shot orientation packet.

## Read these in order

1. **[`evidence-package.md`](./evidence-package.md)** — the single curated summary covering the 7 evidence categories (lead narrative, public artifacts, Gannon ground-truth observations, RFC engagement, Sprint C-Training methodology evolution, kill-gate placeholder, arXiv placeholder). **This is the document the operator hands to reviewers.** An auto-built PDF is uploaded as a workflow artifact on every push to `main` via [`.github/workflows/phase-ii-pdf.yml`](https://github.com/577Industries/helios-program/blob/main/.github/workflows/phase-ii-pdf.yml).
2. **[`commercialization-plan-refined.md`](./commercialization-plan-refined.md)** — Phase I learnings → Phase II strategy refinement. Cites 5 specific Phase I learnings with cross-links to source artifacts. Refines proposal §6.2 revenue model and §6.3 go-to-market based on what Phase I actually surfaced.
3. **[`phase-ii-proposal-draft.md`](./phase-ii-proposal-draft.md)** — section-by-section scaffold mirroring the submitted Phase I proposal's §1-8 structure, with placeholders flagging the Phase II adjustments (§1.3 Gannon retrospective → v2 real-SPP; §2 → Phase II success criteria; §3.3 vision → execution plan; new §4.3 "Phase I results" with cross-links to the evidence package).

## Operator-action subdirectories

Each holds a README inventory plus `.gitkeep` placeholder. **No fake LoI PDFs.** The operator fills these as outreach lands.

| Subdirectory | What it tracks | Operator action |
|---|---|---|
| [`letters/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/README.md) | 8 LoI slots (ML engineer · SME consultant · ≥2 NASA-center · ≥2 ag-industry · 2 spare) | OPERATOR_TODO.md item 6-7 |
| [`customer-discovery/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/customer-discovery/README.md) | ≥10 prospective customers (Ohio/Midwest cooperatives, large family operations, OEM platform teams) | OPERATOR_TODO.md item 5 |
| [`nasa-engagement/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/README.md) | CCMC · M2M SWAO · SRAG · SPoRT contact records | OPERATOR_TODO.md item 7 |

## Refresh policy

Each refresh = a small focused commit with the trigger noted in the commit message and the **Last refreshed** line above advanced.

| Trigger | Refresh action |
|---|---|
| Sprint D ships | Replace the §6 kill-gate placeholder in `evidence-package.md` with real HSS / Brier / CRPS numbers + reliability-diagram PNG + `results/<date>-killgate.json` cross-link |
| arXiv submitted | Replace the §7 arXiv placeholder with `arXiv:YYYY.NNNNN` + DOI + cover letter URL |
| TFT-TEC ships | Update Gannon ground-truth observation #3 (TEC 55.1 TECU) from CDDIS-synthetic to CDDIS-real and `gannon-storm-rtk-analysis` to v0.2.0 (v2 real-SPP) |
| LoI lands | Drop the signed PDF into `letters/`; update `letters/README.md` inventory row |
| Customer-discovery interview | New file at `customer-discovery/YYYY-MM-DD-<organization>.md`; update inventory |
| NASA-center engagement record | New file at `nasa-engagement/<center>-YYYY-MM-DD.md`; update inventory |

The auto-render workflow ([`phase-ii-pdf.yml`](https://github.com/577Industries/helios-program/blob/main/.github/workflows/phase-ii-pdf.yml)) rebuilds `evidence-package.pdf` on every push to `main` that touches `phase-ii/evidence-package.md`. The PDF is downloadable from the workflow run. Stale signals: if **Last refreshed** is more than 60 days behind the most recent companion footnotes-sync commit, the operator runs a top-to-bottom refresh.

## Cross-references

- Submitted Phase I proposal (locked): `/home/twawe/577i-Projects/SBIR Working Folder/NASA/HELIOS_NASA_SBIR_PhaseI_Proposal.docx`
- Public companion (the lead narrative): [`../companion/companion.md`](https://github.com/577Industries/helios-program/blob/main/companion/companion.md)
- Master plan: [`../plan/master-plan.md`](https://github.com/577Industries/helios-program/blob/main/plan/master-plan.md)
- Dispatch spec for this assembly: [`../specs/2026-05-18-PhaseII-evidence-assembly-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-PhaseII-evidence-assembly-spec.md)
- Operator TODO: [`../OPERATOR_TODO.md`](https://github.com/577Industries/helios-program/blob/main/OPERATOR_TODO.md)
