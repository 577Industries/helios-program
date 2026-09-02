# HELIOS Phase II Proposal — DRAFT SCAFFOLD

**Status**: SCAFFOLD ONLY — section headers + key-phrasing carry-over + cross-link placeholders. The operator writes actual Phase II copy.
**Submission deadline**: TBD — depends on the NASA Phase II solicitation cycle (subtopic SPWX.1.S26A continuation, when announced).
**Last refreshed**: 2026-05-18 (initial scaffold).
**Template source**: submitted Phase I proposal at `/home/twawe/577i-Projects/GitHub/577Industries/sbir-nasa-helios-proposal/drafts/_archive/HELIOS_NASA_SBIR_PhaseI_Proposal_2026-05-17_CANONICAL_v0.docx` (locked); for plaintext, run `python-docx` against that `.docx` (the old harness extraction file no longer exists).

---

> **About this scaffold.** The Phase I §1-8 structure is preserved verbatim. Each section flags either *"carry forward from Phase I, refresh dates and TRL claims"* or *"PHASE II ADJUSTMENT — operator action"* with a specific cross-reference to where the new content originates. The four required Phase II adjustments per the dispatch spec are flagged in §1.3, §2, §3.3, and §4.3.

---

## NASA SBIR Phase II proposal — cover

- **Subtopic**: SPWX.1.S26A — Advanced Data-Driven Applications for Space Weather R2O2R (Phase II continuation)
- **Title**: HELIOS — Heliophysics-Enhanced Location Integrity and Operations System
- **Subtitle**: Calibrated Space-Weather Decision Intelligence for NASA Mission Operations and U.S. Precision Agriculture — Phase II Operational Prototype
- **Submitted by**: 577 Industries Inc. — Columbus, Ohio
- **Principal Investigator**: Thomas Waweru
- **Lead Center**: MSFC
- **Participating Centers**: GSFC · JSC · ARC · LaRC
- **Phase I award reference**: TBD (insert award number if Phase I lands)
- **Phase II proposed period of performance**: 24 months
- **Phase II proposed price**: TBD (consistent with NASA SBIR Phase II ceiling)

---

## Technical Abstract

> **Carry forward from Phase I abstract.** Refresh: (a) replace "Phase I develops and validates two tightly scoped vertical slices" with "Phase II advances HELIOS to TRL 5-6 operational prototype"; (b) cite Phase I deliverables by URL (see [`evidence-package.md`](./evidence-package.md) §2); (c) update the Gannon paragraph to cite v2 real-SPP retrospective when [TFT-TEC](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-TFT-TEC-forecasting-spec.md) lands.

---

## Table of Contents

1. Identification and Significance of the Problem
2. Technical Objectives
3. Work Plan, Validation Framework, Risk, and Phase III Vision
4. Related R&D, HELIOS Innovation, and Phase I Results
5. Key Personnel and Facilities
6. Potential Post Applications and Commercialization Plan
7. Budget Summary
8. References

---

## 1. Identification and Significance of the Problem

### 1.1 The Translation Gap

> **Carry forward from Phase I §1.1.** No substantive changes. The PROSWIFT framing, the 46 findings / 113 recommendations, the two-named-critical-gaps mapping all hold for Phase II.

### 1.2 NASA Mission-Operations Slice: SRAG's All-Clear Translation Problem

> **Carry forward from Phase I §1.2.** Update: cite the Phase I kill-gate result (when Sprint D ships per [`specs/2026-05-18-Sprint-D-kill-gate-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-Sprint-D-kill-gate-spec.md)) as the proof point. Reference [`evidence-package.md`](./evidence-package.md) §3.5 + §6.

### 1.3 Precision-Agriculture Slice: The Gannon Case Study — **PHASE II ADJUSTMENT**

> **PHASE II ADJUSTMENT — operator action.** The Gannon retrospective is upgraded from v1 climatological to **v2 real-SPP via the CDDIS adapter** once the TFT-TEC forecasting work lands ([`specs/2026-05-18-TFT-TEC-forecasting-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-TFT-TEC-forecasting-spec.md)). When v2 ships:
> - Replace the 1,302-station-hour headline with the v2 figure (likely different — methodology changes the computation)
> - Cite `gannon-storm-rtk-analysis` v0.2.0 instead of v0.1.0
> - Update the TEC peak observation (currently 55.1 TECU synthetic) with the real-CDDIS value
> - Preserve the climatological-v1 disclosure in a "Phase I retrospective" footnote (do not strip)
> - Cross-reference [`evidence-package.md`](./evidence-package.md) §3.4

The substantive narrative — install-base concentration, dollar-quantified disruption, IA/IL/IN/OH corridor, market sizing at $12.9 B 2024 with 15% CAGR — carries forward unchanged from Phase I §1.3.

### 1.4 Concept of Operations

> **Carry forward from Phase I §1.4.** Update: the CONOPS is **stakeholder-approved** in Phase II (Phase I §2 Obj. 5 success criterion) — cite the LoIs in [`letters/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/) when filled.

---

## 2. Technical Objectives — **PHASE II ADJUSTMENT**

> **PHASE II ADJUSTMENT — operator action.** Phase II objectives advance from TRL 3-4 feasibility to TRL 5-6 operational prototype. The five Phase I objectives become five Phase II objectives with **new success criteria** reflecting operational thresholds (CCMC proving-ground evaluation, OEM partnership commitments, 99.9% API uptime, field validation across 5-10 precision-ag operations during the 2028 planting season).

### Objective 1 — Operational Multi-Source Ingestion (TRL 5)

> Phase II refines Phase I Obj. 1 from "automated ingestion of ≥6 sources" to **production-grade operational ingestion at 99.9% uptime** with full feature-level provenance on `helios-spaceweather-connectors` v1.0.

**Success criterion**: 99.9% uptime over the 24-month Phase II period; <5 min median end-to-end latency (down from Phase I's <15 min); deployed on AWS with automated failover; CCMC-compatible API contract validated.

### Objective 2 — Real-Time Calibrated Fusion at Operational Scale (TRL 5-6)

> Phase II refines Phase I Obj. 2 from "calibration validation on the pre-registered set" to **real-time operational fusion with live model retraining**. The kill-gate result from Phase I (see [`evidence-package.md`](./evidence-package.md) §6 when populated) is the predicate.

**Success criterion**: TBD — operator-driven based on kill-gate outcome. If Phase I kill-gate PASSES H1+H2 → Phase II commits to maintaining reliability-diagram slope within 0.10 of 1.0 across all severity strata in operational stream. If ablation-paper outcome → Phase II commits to the documented honest reduction.

### Objective 3 — NASA Mission Operational Integration

> Phase II refines Phase I Obj. 3 from "all-clear-revocation prediction on the 10-event hold-out" to **prototype integration with M2M SWAO and SPoRT for operational evaluation**. Cite [`nasa-engagement/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/) records when filled.

**Success criterion**: prototype deployed to ≥1 NASA-center operational-evaluation environment; SRAG threshold compatibility validated against ARRT downstream; M2M SWAO operational analysts complete a structured evaluation cycle.

### Objective 4 — Precision-Ag OEM Telematics Integration

> Phase II refines Phase I Obj. 4 from "GNSS degradation ensemble validated on Gannon + 3 hold-outs" to **pilot OEM integration during the 2028 planting season** with ≥1 of Deere Operations Center / AGCO Fuse / CNH AFS Connect. Cite [`letters/ag-industry-loi-*.pdf`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/) when filled.

**Success criterion**: TFT-TEC operational across the 0-24 hour horizon; v2 Gannon retrospective shipped (see §1.3); ≥1 OEM telematics integration deployed in pilot mode; field validation across 5-10 precision-ag operations.

### Objective 5 — Phase III Commercialization and Stakeholder-Approved Operations

> Phase II refines Phase I Obj. 5 from "≥2 NASA-relevant + ≥2 commercial LoIs + Phase II commercialization plan" to **Phase III commercialization plan + Phase II SaaS production deployment**. Cite [`commercialization-plan-refined.md`](./commercialization-plan-refined.md).

**Success criterion**: ≥3 paying customers in pilot tier; ≥1 OEM revenue-share agreement signed; production-grade SaaS at 99.9% uptime; Phase III commercialization plan with named investors or strategic partners.

---

## 3. Work Plan, Validation Framework, Risk, and Phase III Vision — **PHASE II ADJUSTMENT**

> Phase II executes over 24 months across five concurrent tasks (T1-T5) aligned with the new objectives. The task structure mirrors Phase I's T1-T5 framing but extends each task to a 24-month timeline with operational milestones.

### T1 — Operational Ingestion at Scale (Months 1-12, sustained ops Months 13-24)
### T2 — Real-Time Calibrated Fusion Engine (Months 1-12, sustained ops Months 13-24)
### T3 — Operational Translation Modules (Months 4-18)
### T4 — Production API, Dashboard, and Operational Validation (Months 6-24)
### T5 — Field Validation, OEM Pilots, and Phase III Commercialization (Months 1-24)

### 3.1 Pre-Registered Validation Framework (updated)

> **Carry forward from Phase I §3.1** + add Phase I kill-gate result citation when Sprint D ships. The pre-registration discipline carries forward verbatim. Cite the v1 → v2 methodology evolution (Sprint C-Training v2 review pack at [`../specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-v2-review-pack.md)) as evidence of demonstrated rigor.

### 3.2 Risk Assessment and Mitigation (updated)

> **Carry forward from Phase I §3.2 risk table.** The "Validation event cherry-picking" row is now **Likelihood: Low (mitigated and demonstrated)** — change from Phase I's "Low (mitigated)" — because the v1 → v2 evolution proves the pre-registration discipline survived a real methodology surprise.

### 3.3 Phase II Execution Plan — **PHASE II ADJUSTMENT**

> **PHASE II ADJUSTMENT — operator action.** Phase I §3.3 ("Phase II Vision") becomes Phase II §3.3 ("Phase II Execution Plan") — replace the "vision" framing with concrete deliverables. The seven sub-bullets (a-g) from Phase I §3.3 each get a Phase II-specific milestone date, owner, and acceptance test. Reference:
> - The [`evidence-package.md`](./evidence-package.md) for what Phase I delivered
> - The [`commercialization-plan-refined.md`](./commercialization-plan-refined.md) §A for the five Phase I learnings that shape Phase II execution
> - This document's §6 for the Phase III vision (formerly Phase II vision)

---

## 4. Related R&D, HELIOS Innovation, and Phase I Results

### 4.1 Current State of the Art

> **Carry forward from Phase I §4.1.** Refresh: cite any peer-reviewed publications appearing between Phase I submission and Phase II submission that change the SOTA framing.

### 4.2 What Is Innovative About HELIOS

> **Carry forward from Phase I §4.2.** The five innovations (model-agnostic decision-calibrated fusion · provenance-aware architecture · dual-use translation · equipment-aware GNSS prediction · industry-native output) all carry forward. Update each to cite the relevant Phase I shipped artifact URL — see [`evidence-package.md`](./evidence-package.md) §2.

### 4.3 Phase I Results — **PHASE II ADJUSTMENT (NEW SECTION)**

> **PHASE II ADJUSTMENT — operator action.** This is a **new** section that did not exist in the Phase I proposal. It heavily cites the [`evidence-package.md`](./evidence-package.md) URLs. The new section is the single highest-leverage Phase II proposal addition — reviewers ask "what did you actually deliver in Phase I?" and §4.3 answers in one page.

Structure:
- **§4.3.1 Public-portfolio deliverables** — cite [`evidence-package.md`](./evidence-package.md) §2 with each of the 5 public Pages sites + the 4 public repos + the 1 private companion
- **§4.3.2 Citable ground-truth observations** — cite [`evidence-package.md`](./evidence-package.md) §3 with each of the 5 Gannon ground-truth observations (Kp peak · Bz peak · TEC peak · 1,302 station-hours · kill-gate result)
- **§4.3.3 Community engagement and standards work** — cite [`evidence-package.md`](./evidence-package.md) §4 (RFC-0001)
- **§4.3.4 Methodology evolution** — cite [`evidence-package.md`](./evidence-package.md) §5 (Sprint C-Training v1 → v2)
- **§4.3.5 Peer-reviewable artifact** — cite [`evidence-package.md`](./evidence-package.md) §7 (arXiv preprint when submitted)

### 4.4 577 Industries Relevant Experience

> **Carry forward from Phase I §4.3** (now renumbered to §4.4). Add: HELIOS Phase I as the **most recent** SBIR Phase I execution, delivered in 6 months with the public portfolio at [`evidence-package.md`](./evidence-package.md) §2.

---

## 5. Key Personnel and Facilities

### 5.1 Key Personnel

> **Carry forward from Phase I §5.1.** Refresh: replace "named candidates identified" with **named-with-LoIs** when [`letters/ml-engineer-loi.pdf`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/) and [`letters/sme-consultant-loi.pdf`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/) are signed.

### 5.2 Facilities and Equipment

> **Carry forward from Phase I §5.2.** Update: AWS production-grade deployment costs for 24-month operations (vs. Phase I's prototype scale).

### 5.3 NASA Center Engagement

> **Carry forward from Phase I §5.3.** Refresh: replace "Target validation-framework benchmarking" framings with **demonstrated engagement** when [`nasa-engagement/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/README.md) records are filled. If LoIs from NASA centers land, cite them in [`letters/nasa-center-loi-*.pdf`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/).

---

## 6. Potential Post Applications and Commercialization Plan

> **Reference**: [`commercialization-plan-refined.md`](./commercialization-plan-refined.md) — Phase I learnings → Phase II strategy refinement. This section in the Phase II proposal pulls heavily from that document.

### 6.1 Beachhead Market: U.S. Precision Agriculture
### 6.2 Revenue Model
### 6.3 Go-to-Market Strategy
### 6.4 Phase III Expansion Verticals

> Phase II §6.4 covers what Phase I §6.4 called "Phase II Expansion Verticals" — autonomous-vehicle GNSS integrity · geospatial surveying · satellite drag prediction · parametric space-weather insurance. Phase II makes these **fundable** Phase III work, anchored on the Phase II operational prototype.

### 6.5 NASA Mission Applications Beyond SRAG
### 6.6 Competitive Positioning and IP Strategy

---

## 7. Budget Summary

> **Carry forward Phase I §7 structure**, scaled to the Phase II ceiling and 24-month period of performance. Categories:
>
> - Direct Labor (PI, ML Engineer, additional Phase II hires)
> - Fringe Benefits
> - Subcontract (SME consultant continuing; possibly additional)
> - Cloud Computing (production-grade AWS for 24 months)
> - Travel (NASA centers, OEM partner sites, ag-industry conferences)
> - Materials and Software Licenses
> - Fee / Profit
> - TABA Request (if eligible at Phase II)
>
> Subcontracting must remain below the SBIR Phase II 50% cap (NFS 1852.219-80). PI primary employment with the small business preserved per NFS 1852.219-83. All work in the United States.

---

## 8. References

> **Carry forward Phase I §8 references** [1]-[32]. Add Phase II-specific additions:
>
> - [33] HELIOS Phase I evidence package: <https://577industries.github.io/helios-program/phase-ii/evidence-package/>
> - [34] HELIOS public companion document: <https://577industries.github.io/helios-program/companion/>
> - [35] HELIOS arXiv preprint: arXiv:YYYY.NNNNN (when submitted)
> - [36] HELIOS OSF pre-registration: <https://osf.io/...> (when filed)
> - [37] HELIOS GitHub portfolio: <https://github.com/577Industries/helios-program>

---

## Phase II adjustment checklist (for operator review)

The dispatch spec calls for these four specific Phase II adjustments — confirming each is flagged in this scaffold:

- [x] **§1.3** Gannon retrospective → cite v2 real-SPP analysis when TFT-TEC lands
- [x] **§2** Phase II success criteria reflect TRL 5-6 operational thresholds (CCMC proving-ground evaluation, OEM partnership commitments, 99.9% uptime)
- [x] **§3.3** Phase II "vision" → Phase II "execution plan" (replace vision framing with concrete milestones)
- [x] **§4.3 NEW** "Phase I results" section citing the evidence-package URLs heavily

---

## Cross-references

- Submitted Phase I proposal (locked; do not modify): `/home/twawe/577i-Projects/GitHub/577Industries/sbir-nasa-helios-proposal/drafts/_archive/HELIOS_NASA_SBIR_PhaseI_Proposal_2026-05-17_CANONICAL_v0.docx`
- Plaintext: run `python-docx` against the canonical `.docx` (no cached extraction exists)
- Public companion (Phase I mirror): [`../companion/companion.md`](https://github.com/577Industries/helios-program/blob/main/companion/companion.md)
- Evidence package (this Phase II evidence index): [`evidence-package.md`](./evidence-package.md)
- Refined commercialization plan: [`commercialization-plan-refined.md`](./commercialization-plan-refined.md)
- Phase II evidence-assembly dispatch spec: [`../specs/2026-05-18-PhaseII-evidence-assembly-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-PhaseII-evidence-assembly-spec.md)
- Sprint D dispatch spec: [`../specs/2026-05-18-Sprint-D-kill-gate-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-Sprint-D-kill-gate-spec.md)
- TFT-TEC dispatch spec: [`../specs/2026-05-18-TFT-TEC-forecasting-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-TFT-TEC-forecasting-spec.md)
- arXiv preprint dispatch spec: [`../specs/2026-05-18-arXiv-preprint-draft-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-arXiv-preprint-draft-spec.md)
