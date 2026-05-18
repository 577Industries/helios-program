# arXiv Preprint Draft Dispatch Spec

**Type**: forward-looking dispatch spec.
**Status**: ready to dispatch (parallel-safe — does not require any operator prerequisite to BEGIN; the results §4 fills in after Sprint D runs).
**Estimated agent runtime**: 4-6 hours (drafting + figure assembly + bib).

---

## TL;DR

Drafts the full skeleton of the HELIOS fusion-engine arXiv preprint with everything except the §4 results filled in. The results section is a clearly-labelled placeholder that one commit fills in once `helios-program/results/<date>-killgate.json` lands from Sprint D.

**Why parallel-safe**: by writing §§1-3 + §§5-6 + bib + figures NOW, the operator's decision window between "kill-gate result lands" and "preprint goes to arXiv" shrinks from ~3 weeks (typical drafting time) to ~1 day (results fill + final review). That's the difference between submitting a preprint *while the result is newsworthy* and submitting *after the conversation has moved on*.

## Target venue

- **Primary**: arXiv `astro-ph.SR` (Solar and Stellar Astrophysics — heliophysics community)
- **Cross-list**: `cs.LG` (Machine Learning — calibration + conformal methodology audience)
- Length target: 12 pages including figures + references; 8 main-text pages
- License: arXiv perpetual non-exclusive (default) + Apache 2.0 on associated LaTeX source

## arXiv endorsement

Thomas Waweru is the corresponding author. Per arXiv submission policy for first-time submitters to a category, an endorser may be required. **Operator action at submission time** (not now): identify an endorser from the named SME consultant + 577 Industries network. Document the endorser email in the submission cover letter draft.

## Skeleton sections

### Title
"Calibrated, Provenance-Tracked Fusion of Solar Energetic Particle Forecasts for NASA Mission Operations"

(Working title; can be refined at submission.)

### Authors
1. Thomas Waweru — 577 Industries Inc. (corresponding)
2. [Named Senior ML Engineer] — 577 Industries Inc.
3. [Named Space-Weather / Ionospheric SME] — subcontract

Placeholder pattern: the agent inserts `\todo{...}` markers for the unconfirmed names.

### Abstract (~250 words)
- Translation-gap framing (proposal §1.1)
- Calibrated fusion innovation (proposal §4.2 innovation #1)
- Pre-registered hold-out methodology (master plan §C kill-gate)
- Headline result (placeholder until Sprint D lands)
- One sentence on the Phase II vision (proposal §3.3)

### §1 Introduction
- Calibration-vs-accuracy distinction in operational SEP forecasting (cite Whitman 2023, 2024 — proposal refs [11], [13])
- The provenance affordance for CCMC proving-ground evaluation (cite the RFC-0001 doc URL — `helios-provenance-spec` v0.1.0)
- ISEP partnership + SEP Scoreboards A/B/C context (cite proposal §1.2)
- Contribution statement

### §2 Methods
- §2.1 BMA orchestrator (cite Hoeting et al. 1999 for the canonical BMA reference)
- §2.2 Isotonic-regression reliability calibration (cite Niculescu-Mizil & Caruana 2005); justify rejection of Platt scaling at extremes
- §2.3 Conformal prediction wrappers (split + Mondrian per Kp severity; cite Vovk 2022 — proposal ref [31])
- §2.4 CCMC-compatible metrics (HSS Donaldson 1975; reliability slope; Brier; CRPS)
- §2.5 Pre-registration discipline (cite the OSF URL; the locked commit SHA)

### §3 Data
- §3.1 ISWA SEP Scoreboards data tree + Jan 2017 cutover finding (cite the Sprint C-Training-v2 coverage matrix URL on the helios-program Pages site)
- §3.2 NOAA SESC archive ground-truth labels (cite `umbra.nascom.nasa.gov/SEP/seps.html`)
- §3.3 Table 3-1 split (7 train + 3 hold-out; locked dates)
- §3.4 Per-(component, event) source labeling (cite Sprint C-Training-v2's `iswa_real`/`synthetic_proxy`/`swpc_archive_truth` policy)

### §4 Results (PLACEHOLDER until Sprint D)
- **§4.1 Hold-out HSS**: fused vs. best-component; per-Kp-stratum + aggregate; bootstrapped 95% CIs.
  *Agent inserts*: a `\todo{INSERT FROM results/<date>-killgate.json HSS_section}` block + a stub table with 3 rows × 6 columns (event × {fused-HSS, best-component-HSS, Δ%, 95% CI}).
- **§4.2 Reliability**: per-stratum slope; quiet/moderate/extreme.
  *Agent inserts*: `\todo{INSERT reliability-diagram figure}` referring to `results/<date>-killgate-reliability-diagrams.png`.
- **§4.3 Brier / CRPS**: secondary metrics.
- **§4.4 Decision routing** (per master plan §C): PASS-both / PASS-one / FAIL-both — text varies by branch; agent provides 3 stock paragraphs the operator picks from at fill-in time.

### §5 Discussion
- Limitations: ISWA pre-2017 cutover; synthetic-proxy training substrate for pre-2017 events
- Generalizability: hold-out events span Cycle 25 ramp; covers solar quiet (2022) through G5 extreme (Gannon 2024)
- Phase II vision (cite proposal §3.3)
- Equipment-aware GNSS pathway (forward reference to the §2 Obj. 4 TFT pathway per `specs/2026-05-18-TFT-TEC-forecasting-spec.md`)

### §6 Reproducibility and data availability
- Code: 5 public GitHub repos + Pages docs URLs
- Data: connectors handle real-time + archive; pre-warmed cache available on request
- Trained weights: `helios-fusion-internal` (private; access on request for verification)
- Provenance: every figure cites the OSF pre-reg URL + the locked commit SHA + the relevant `helios-program/results/<date>-killgate.json` artifact

### References (bib)
- Proposal refs [1]-[32] (already enumerated in `companion/companion.md` §8)
- New refs as needed: Hoeting 1999 (BMA), Niculescu-Mizil & Caruana 2005 (calibration comparison), Donaldson 1975 (HSS), Lim 2021 (already proposal ref [32])

## Files to be created

Layout under `helios-fusion-engine/paper/`:

```
helios-fusion-engine/paper/
├── main.tex                        # or main.md + Pandoc; agent chooses
├── refs.bib                        # BibTeX
├── figures/
│   ├── architecture.png            # Mermaid graph from helios-program (rendered to PNG)
│   ├── reliability-diagrams.png    # PLACEHOLDER until Sprint D writes results/<date>-killgate-reliability-diagrams.png
│   ├── bootstrap-distributions.png # PLACEHOLDER similar
│   └── gannon-bz-timeline.png      # DSCOVR Bz=-59.16 nT visual (already exists in gannon-storm-rtk-analysis or can be regenerated)
├── tables/
│   └── table-3-1.tex               # 7 train + 3 hold-out events
└── .github/workflows/paper.yml     # auto-build to PDF on every push to feat/v0.2-paper
```

## Agent brief sketch

1. **Setup**: worktree at `~/577i-Projects/.worktrees/helios-fusion-engine-paper/` on branch `feat/v0.2-paper`.
2. **Choose format**: LaTeX (recommended for arXiv) vs. Markdown + Pandoc. Decision criteria: if the agent is comfortable with `pylatex` for figure-table assembly use LaTeX; otherwise Pandoc.
3. **Draft sections §1-§3, §5-§6** in full. The §4 placeholders go in with explicit `\todo{...}` or `<!-- TODO: fill from results/<date>-killgate.json -->` markers.
4. **Assemble figures** that don't need Sprint D results:
   - Architecture diagram (Mermaid → PNG via `mmdc` CLI, or hand-built TikZ)
   - Table 3-1 (the 10-event train/hold-out split table)
   - Gannon Bz=-59.16 nT timeline (regenerate via the existing `DscovrAdapter.fetch_mag` call for the Gannon week; matplotlib figure)
5. **Bib assembly**: write `refs.bib` with all proposal refs + the 3-4 new ones noted above.
6. **Auto-build CI**: `.github/workflows/paper.yml` builds the PDF on every push; uploads as a release artifact.
7. **Cover-letter draft** at `paper/COVER_LETTER.md` for arXiv submission.
8. **Submission checklist** at `paper/SUBMISSION_CHECKLIST.md` for the operator.

## How Sprint D fills in §4

After Sprint D lands `helios-program/results/<date>-killgate.json`:

1. Operator (or a small fill-in agent) reads the JSON.
2. Branches:
   - **PASS H1 ∧ PASS H2**: §4.1 table fills in; §4.2 reliability figure embeds; §4.3 Brier/CRPS table fills; §4.4 routes to "full paper" stock paragraph.
   - **PASS one ∧ FAIL one**: §4.1 + §4.2 fill in; §4.3 may pass or fail (separate row); §4.4 routes to "honest ablation" stock paragraph; abstract reframes around honest-negative-result.
   - **FAIL H1 ∧ FAIL H2**: §4.4 routes to "negative result"; abstract reframes; **decision to actually submit goes to the operator** — the spec says "no paper" but a thoughtful honest-negative paper might still be valuable.
3. Commit on the `feat/v0.2-paper` branch; rebuild PDF; ready for operator review + arXiv submission.

## Verification gates

1. `paper/main.pdf` renders without errors via CI (LaTeX build green).
2. All `\todo{...}` markers in the non-results sections are zero (results section markers are expected until Sprint D fills them).
3. Every figure has a generation script committed (no orphan PNGs).
4. `refs.bib` has DOIs where available; passes `bibtex --strict`.
5. Cover-letter draft cites the OSF pre-reg URL + the kill-gate JSON URL.

## Operator outreach at submission (not part of this sprint)

- SPASE community list announcement
- sunpy-dev list announcement
- CCMC feedback channel
- 577 Industries LinkedIn announcement
- Companion footnote `fusion_engine.preprint` populated within 7 days (per master plan §C)

## What this sprint does NOT do

- Does NOT submit the preprint to arXiv (operator action after kill-gate result + final review).
- Does NOT include the TFT-TEC content (that's a separate paper or §1.4 future-work note).
- Does NOT change any pre-registered methodology.

## Cross-references

- Master plan §C kill-gate decision tree
- `specs/2026-05-18-Sprint-D-kill-gate-spec.md` (the upstream sprint that fills §4)
- `companion/companion.md` (the same content, but for general audiences vs the paper's heliophysics + ML audience)
- `orchestration/osf_preregistration.template.md` (the pre-reg that §2.5 + §3.4 cite)
