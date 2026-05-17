# HELIOS — Public Companion Document

**Heliophysics-Enhanced Location Integrity and Operations System**
*Calibrated Space-Weather Decision Intelligence for NASA Mission Operations and U.S. Precision Agriculture*

**Submitted by**: 577 Industries Inc. — Columbus, Ohio — <https://www.577industries.com>
**Principal Investigator**: Thomas Waweru
**NASA Subtopic**: SPWX.1.S26A — Advanced Data-Driven Applications for Space Weather R2O2R
**Lead Center**: MSFC — **Participating Centers**: GSFC, JSC, ARC, LaRC

---

> **About this document.** This public companion mirrors 577 Industries' submitted NASA SBIR Phase I proposal "HELIOS". Where the submitted document made paper claims, this companion attaches **live citations** to the public artifacts that back those claims — repositories, preprints, blog posts, and reproducible notebooks. Use the status field next to each artifact to gauge maturity:
>
> **scaffolding** → repo exists, implementation in progress · **rfc** → draft circulated for comment · **in-development** → functional but not v1 · **stable** → v1.0+ tagged release
>
> Audiences: Phase II re-pitch reviewers · NASA-center engagement (CCMC, M2M SWAO, SRAG, SPoRT) · customer-discovery pre-reads · public web presence.

---

## Artifact registry

| # | Artifact | Repository | Status (2026-05-17) | Cited in |
|---|---|---|---|---|
| 1 | helios-provenance-spec | [github.com/577Industries/helios-provenance-spec](https://github.com/577Industries/helios-provenance-spec) | scaffolding | §1.4 CONOPS · §4.2 innovation #2 |
| 2 | helios-spaceweather-connectors | [github.com/577Industries/helios-spaceweather-connectors](https://github.com/577Industries/helios-spaceweather-connectors) | scaffolding | §2 Obj. 1 · §3 T1 |
| 3 | helios-fusion-engine *(public framework)* | [github.com/577Industries/helios-fusion-engine](https://github.com/577Industries/helios-fusion-engine) | scaffolding | §2 Obj. 2 · §3.1 · §4.2 innovation #1 |
| 4 | gannon-storm-rtk-analysis | [github.com/577Industries/gannon-storm-rtk-analysis](https://github.com/577Industries/gannon-storm-rtk-analysis) | scaffolding | §1.3 Gannon · §2 Obj. 4 · §4.2 innovation #4 |

A canonical machine-readable artifact registry lives at [`footnotes.yaml`](./footnotes.yaml). It is rebuilt automatically from each artifact's README on every merge to `main` via `orchestration/companion_sync.py`.

---

## Technical Abstract

577 Industries Inc. proposes **HELIOS** — a calibrated, provenance-tracked decision-intelligence layer that fuses mature NASA and NOAA space-weather model outputs and translates them into the specific operational decisions two user communities act on. Phase I develops and validates two tightly scoped vertical slices, both demonstrated against named historical events.

**Slice 1 — NASA mission operations.** Translation of fused SEP forecasts from the CCMC SEP Scoreboards (A onset, B peak flux, C time profiles), DONKI event linkages, and GOES/SWPC inputs into all-clear-status revocation probabilities and time-to-threshold estimates aligned with SRAG's ALARA decision framework. Outputs are designed to be compatible with the Acute Radiation Risk Tool (ARRT), not to replace it.

**Slice 2 — U.S. precision agriculture GNSS.** Translation of ionospheric disturbance forecasts into equipment-specific RTK positioning-accuracy products for the John Deere StarFire, Trimble RTK, and AgLeader receivers that dominate the U.S. row-crop install base. Outputs are field-level go/no-go maps against operator-configurable accuracy thresholds (typically 2.5 cm planting, 5 cm spraying), not raw geophysical indices.

HELIOS is **not a new space-weather model**. The innovation is a **model-agnostic fusion layer** applying Bayesian Model Averaging with isotonic-regression reliability calibration and conformal prediction across heterogeneous model outputs, paired with industry-native translation modules. Every output traces to its underlying models, data feeds, and assumptions — supporting CCMC proving-ground evaluation, ARRT-compatible integration, and operator trust in safety-critical applications.

Phase I delivers (i) a multi-source ingestion pipeline (DONKI, CCMC SEP Scoreboards, NOAA SWPC, NASA CDDIS GIMs, GOES, DSCOVR) with feature-level provenance[^1]; (ii) a calibrated fusion engine[^3] validated against a pre-registered set of ten historical SEP events with explicit 7/3 training/hold-out split (Table 3-1); (iii) the two translation modules above, with the GNSS slice validated against the May 2024 Gannon superstorm plus three hold-out G2+ events[^4]; (iv) a working RESTful API and demonstration dashboard; and (v) letters of intent from at least two NASA-relevant and two precision-agriculture organizations. Expected TRL at completion: 3-4, consistent with the SPWX.1.S26A range.

The **May 2024 Gannon superstorm** (G5, Kp=9) made the translation gap concrete. RTK-GNSS positioning failed across the U.S. Midwest during peak planting; equipment shutdowns were widely documented; no commercial product converted federal space-weather data into terms a row-crop operator could act on. HELIOS closes that gap with a beachhead in U.S. precision agriculture and a NASA mission-operations slice that targets the SRAG console workflow directly. The subtopic's two named critical gaps — **nowcasting/forecasting tools for energetic particles aiding spacecraft anomaly resolution**, and **techniques to predict ionospheric variability disrupting GNSS** — map one-to-one onto the two slices.

---

## Table of Contents

1. [Identification and Significance of the Problem](#1-identification-and-significance-of-the-problem)
2. [Technical Objectives](#2-technical-objectives)
3. [Work Plan, Validation Framework, Risk, and Phase II Vision](#3-work-plan-validation-framework-risk-and-phase-ii-vision)
4. [Related R&D and HELIOS Innovation](#4-related-rd-and-helios-innovation)
5. [Key Personnel and Facilities](#5-key-personnel-and-facilities)
6. [Potential Post Applications and Commercialization Plan](#6-potential-post-applications-and-commercialization-plan)
7. [Budget Summary](#7-budget-summary)
8. [References](#8-references)

---

## 1. Identification and Significance of the Problem

### 1.1 The Translation Gap

The federal space-weather enterprise has world-class models. CCMC hosts over 100 of them. NOAA SWPC issues operational forecasts. NASA's SEP Scoreboards — built through the ISEP partnership of CCMC, M2M SWAO, and SRAG — consolidate research SEP models into a unified operational view across Scoreboard A (onset probability), Scoreboard B (peak flux prediction), and Scoreboard C (event time profiles). DONKI provides intelligent event linkages via JSON API. **The problem HELIOS addresses is not a shortage of models or data. It is the absence of a calibrated, provenance-tracked translation layer that converts heterogeneous and sometimes contradictory model outputs into the specific decisions operators must make.**

This is the same gap the PROSWIFT Act [1] charged the Space Weather Advisory Group (SWAG) with characterizing. The resulting 2023 report [2] produced 46 findings and 113 recommendations; Finding 1 identified insufficient coordination across the federal, commercial, and academic sectors, and Recommendation 2.2.3 explicitly encouraged regional and local alerts developed through private-sector partnerships. Subtopic SPWX.1.S26A operationalizes those findings; HELIOS targets two of the subtopic's named critical gaps directly:

- *"Nowcasting and forecasting tools for energetic particles and plasma conditions that directly aid in spacecraft anomaly resolution."* — addressed by the NASA mission-operations slice (§1.2, §2 Obj. 3).
- *"Techniques to characterize and predict ionospheric variability, which can disrupt global navigation and communication systems."* — addressed by the precision-agriculture slice (§1.3, §2 Obj. 4).

### 1.2 NASA Mission-Operations Slice: SRAG's All-Clear Translation Problem

An SRAG console operator assessing whether all-clear status should be revoked under the operational SEP thresholds (>10 MeV at 10 pfu; >100 MeV at 1 pfu) currently cross-references raw outputs from UMASEP, HESPERIA REleASE, SEPMOD, and MagPy across three Scoreboards. No existing system provides a calibrated, probabilistic fusion of these models with quantified confidence bounds, source provenance, and time-to-threshold estimates suitable for high-tempo monitoring. The cognitive load and risk of unstructured model disagreement scale with the demands of Artemis cislunar operations and, eventually, Earth-independent decision support for Mars transit, where light-time latency precludes ground intervention.

HELIOS **does not replace** SRAG's Acute Radiation Risk Tool (ARRT). It produces decision-calibrated fused inputs designed to be compatible with ARRT's downstream dose-rate computation, supporting the consolidated risk presentation flight controllers need under ALARA. The mission-operations slice maps directly to subtopic shortfalls "Provide Earth-independent safety and crew health and performance countermeasures during long duration missions" and "Perform advanced remote sensing and science measurements with improved sensing capabilities and autonomy."

### 1.3 Precision-Agriculture Slice: The Gannon Case Study

The **May 10-12, 2024 Gannon superstorm (G5, Kp=9)** was the most powerful geomagnetic storm in over two decades. RTK-GNSS positioning failed across the U.S. Midwest during peak corn and soybean planting season; the American Farm Bureau Federation [27] and OSU Extension [28] documented equipment shutdowns lasting 12-48 hours. In Brazil, Equatorial Plasma Bubbles routinely disrupt GNSS during harvest [16]. In the UK, autonomous agricultural vehicles were severely disrupted by the same storm [29]. **No commercial product converted federal space-weather data into terms a row-crop operator could act on** — not a Kp index, not a TEC map, but a field-level *"your StarFire 6000 will not hold sub-3 cm RTK for the next four hours; recommend manual operations until 19:00 local."*

[^4]: A retrospective reanalysis of the May 10-12, 2024 Gannon storm using NGS CORS data across IA / IL / IN / OH is published at [`gannon-storm-rtk-analysis`](https://github.com/577Industries/gannon-storm-rtk-analysis) (status: scaffolding; v0.1 in progress). Notebook + blog post + 2D error envelope plots forthcoming.

Precision agriculture is the beachhead for three reasons. **First, install base concentration:** more than 80% of U.S. row-crop acres operate under GPS guidance [27]; the John Deere StarFire 6000/7000, Trimble RTK, and AgLeader Surefire/Versa families dominate. Deere's Operations Center alone connects 500,000+ machines. **Second, observable, dollar-quantified disruption:** the May 2024 storm produced widely reported equipment shutdowns during peak planting, with daily opportunity costs documented at the national level. **Third, geographic concentration:** the IA/IL/IN/OH corridor — within one day's drive of 577 Industries' Columbus, OH base — concentrates the customer base where OEM, cooperative, and operator conversations are tractable on a Phase I budget.

Market sizing for the beachhead: global precision-agriculture market reached $12.9 B in 2024 (CAGR ~15% through 2030); the U.S. SAM dominated by row-crop guidance, RTK services, and equipment telematics is several billion dollars and growing. Autonomous transportation, geospatial surveying, satellite-drag forecasting for LEO operators, and parametric space-weather insurance are Phase II expansion verticals enabled by the same fusion engine; they are explicitly not Phase I deliverables (§6.4).

### 1.4 Concept of Operations

HELIOS operates as a continuously running cloud service. The ingestion tier[^2] pulls upstream data on its native cadence (DONKI: minutes; SEP Scoreboards: minutes-to-hours; CDDIS GIMs: 2-hour; GOES/DSCOVR: 1-minute) and normalizes each source into a common feature schema with full provenance[^1]. The fusion tier[^3] applies BMA weights, isotonic calibration, and conformal-prediction wrappers on a configurable schedule (operational: every 5 minutes; analytical: on-demand). The translation tier splits into the two slices: the SRAG-oriented radiation-risk module emits all-clear revocation probability, time-to-threshold conformal intervals, and ARRT-compatible dose-rate inputs; the precision-ag module emits receiver-family-specific 2D accuracy distributions over 0-24 hour horizons with location-aware adjustments. Operators consume HELIOS via the RESTful API (JSON) or via the dashboard (web view).

**Every output exposes a drill-down to its full provenance chain** — which upstream models contributed at which weights, with which calibration history. This provenance affordance is essential for SRAG console adoption and for the CCMC proving-ground evaluation pathway, and is formalized as a public, community-comment RFC[^1].

[^1]: The provenance affordance is formalized as a public, machine-readable JSON Schema (draft 2020-12) plus a pydantic v2 reference implementation: [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec). Currently scaffolding; v0.1 RFC issued for community comment shortly.

[^2]: The ingestion pipeline is implemented as a Python package: [`helios-spaceweather-connectors`](https://github.com/577Industries/helios-spaceweather-connectors). Currently scaffolding; first adapter (DONKI) v0.1 in progress.

[^3]: The fusion engine framework is open source: [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine). Trained weights and BMA priors live in the private companion `helios-fusion-internal`. Currently scaffolding.

---

## 2. Technical Objectives

Phase I establishes the technical feasibility of HELIOS through five integrated objectives. Each has measurable success criteria; the validation framework is pre-registered in §3.1 to forestall any concern about post-hoc metric tuning or cherry-picked event selection.

### Objective 1 — Multi-Source Ingestion Pipeline

Deploy a resilient ETL architecture continuously ingesting: (a) NASA DONKI API — CME, flare, SEP notifications in JSON with intelligent event linkages [8]; (b) CCMC SEP Scoreboards A, B, and C — onset probability, peak flux, time profiles; (c) NOAA SWPC real-time solar wind, Kp, Dst, and probabilistic SEP forecasts; (d) NASA CDDIS Global Ionosphere Maps — vertical TEC at 2-hour/2.5° resolution; (e) GOES X-ray and proton flux; (f) DSCOVR upstream solar-wind parameters. All sources align to a common temporal grid; every downstream output traces to its source models, ingestion timestamps, and feature lineage[^2].

**Success criterion**: automated ingestion of ≥6 sources with median end-to-end latency <15 min and 100% feature-level provenance, verified against an ingestion-audit log.

### Objective 2 — Probabilistic Calibration and Fusion Engine

Raw outputs from upstream models differ in cadence, bias structure, uncertainty representation, and event definition. Naive averaging is unsafe at operational thresholds. HELIOS implements:

- **Bayesian Model Averaging (BMA)** with dynamic weights conditioned on rolling 90-day verification skill per model.
- **Isotonic regression reliability calibration** so predicted probabilities match observed event frequencies (Platt scaling considered and rejected for known miscalibration at extremes).
- **Conformal prediction** for distribution-free confidence intervals on continuous outputs (TEC, proton flux, 2D positioning error). Required because parametric uncertainty assumptions break at tail events.
- **Severity-stratified validation** across quiet, moderate, and extreme conditions (Kp-stratified bins) to prevent calibration collapse on the events that matter most.

**Success criterion**: reliability-diagram slope within 0.15 of perfect calibration across all severity strata on the pre-registered validation set; Brier score and CRPS improvements over the best individual component model on hold-out events. The public framework is at [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine); validation runs on the pre-registered Table 3-1 events with full reproducibility[^3].

### Objective 3 — NASA Mission Radiation-Risk Translation Module

Translate fused SEP predictions from Scoreboards B and C into SRAG-aligned operational products: (a) all-clear-revocation probability and timing at the >10 MeV/10 pfu and >100 MeV/1 pfu thresholds; (b) time-to-threshold estimates with conformal confidence intervals suitable for EVA and mission planning; (c) outputs structured for compatibility with the ARRT framework for downstream dose-rate computation; (d) console-oriented consolidated summaries that reduce cognitive load on high-tempo SRAG operators without removing access to underlying provenance.

**Success criterion**: on the pre-registered 10-event historical SEP set (Table 3-1), the fused all-clear-revocation prediction improves Heidke Skill Score by ≥15% over the best individual component model on the 3-event hold-out, with calibrated time-to-threshold conformal intervals.

### Objective 4 — Precision-Ag GNSS Degradation Translation

Build a three-component ensemble that maps ionospheric disturbance forecasts to equipment-specific RTK positioning-accuracy products. Each component is chosen to backstop a specific failure mode of the others:

- **Temporal Fusion Transformer (TFT)** for multi-horizon TEC forecasting from 20+ years of CDDIS GIM data, with solar wind and Dst as exogenous variables. Captures long-range solar-terrestrial temporal coupling.
- **Gradient-boosted regressors (XGBoost/LightGBM)** mapping disturbance indices (S4 scintillation, σφ phase variance, ROTI) to observed 2D RTK positioning errors from NGS CORS stations in IA/IL/IN/OH. SMOTE oversampling addresses severe class imbalance (G2+ events <2% of all time steps).
- **Physics-informed neural network (PINN) regularization** imposing Chapman ionization profiles and equatorial-anomaly geometry as soft constraints, enforcing physical consistency on extreme events outside the training distribution.

The equipment translation layer applies receiver-family-specific transfer functions for the John Deere StarFire 6000/7000, Trimble RTK, and AgLeader Surefire/Versa families, calibrated against documented receiver behavior and CORS-derived ground truth. Location-aware adjustments account for geomagnetic latitude, multipath environment, and RTK baseline length. Outputs are field-level accuracy maps with go/no-go recommendations against operator-configurable thresholds (typically 2.5 cm planting; 5 cm spraying).

**Success criterion**: on the May 2024 Gannon storm[^4] and three hold-out G2+ events, predicted 2D RTK error within 30% of observed CORS-derived error for the three receiver families; Heidke Skill Score improvement ≥20% over climatological persistence at the 6-hour forecast horizon.

### Objective 5 — End-User Validation and Phase II Commercialization Framework

**NASA slice**: structured engagement with CCMC (validation-framework compliance), M2M SWAO (operational relevance), SRAG (operational threshold and ARRT-compatibility alignment), and SPoRT/MSFC (R2O2R transition pathway). **Ag slice**: structured interviews with at least 10 prospective customers across Ohio/Midwest cooperatives, large family operations, and OEM platform teams (Deere Operations Center, AGCO Fuse, CNH AFS Connect). TABA funds support customer discovery, FTO/IP review of the fusion architecture, and pricing-model validation.

**Success criterion**: letters of intent from ≥2 NASA-relevant organizations and ≥2 commercial precision-ag organizations; completed Phase II commercialization plan with named pilot partners; stakeholder-approved Concept of Operations.

---

## 3. Work Plan, Validation Framework, Risk, and Phase II Vision

Phase I executes over six months across five concurrent tasks (T1-T5) aligned with the technical objectives. Total proposed price: $150,000 plus $6,500 TABA.

### T1 — Ingestion and Pipeline Architecture (Months 1-3)

Month 1 finalizes the stakeholder-approved CONOPS through structured elicitation with CCMC, M2M SWAO, and three precision-ag stakeholders. Months 1-3 deploy the ETL pipeline on AWS (S3 staging, Lambda transforms, RDS metadata) with authenticated DONKI ingestion, SEP Scoreboard scrapers respecting CCMC rate limits, SWPC real-time feeds, CDDIS GIMs, GOES X-ray/proton flux, and DSCOVR. The model-adapter layer normalizes each upstream source into a common feature schema with provenance preserved at every transformation[^2]. The architecture separates HELIOS-proprietary fusion logic from licensed upstream models — HESPERIA REleASE in particular requires a separate licensing agreement for commercial use [30]; HELIOS connectors use public outputs only, with the IP value concentrated in the fusion and translation layers. **Deliverables**: CONOPS; functioning ETL pipeline; provenance-tracked data store; IT Security Plan compliant with the NASA contract.

### T2 — Fusion and Calibration Engine (Months 2-4)

Build the model-adapter library (one adapter per upstream source). Implement BMA with rolling 90-day weight updates. Deploy isotonic regression reliability calibration on probability outputs. Build conformal-prediction wrappers for continuous-quantity outputs. Implement the severity-stratified validation framework on the events in Table 3-1, with calibration-curve diagnostics per Kp severity bin. **Deliverables**: model-adapter library; fusion engine[^3]; calibration validation report with severity-stratified reliability diagrams.

### T3 — Translation Modules (Months 3-5)

Months 3-4: NASA mission radiation-risk module — all-clear revocation prediction, ARRT-compatible output schema, time-to-threshold conformal intervals, console-summary view with full provenance drill-down. Months 3-5: precision-ag GNSS module — three-component ensemble per §2 Obj. 4, equipment-specific transfer functions, location-aware geomagnetic/multipath/baseline adjustments, operator-configurable accuracy thresholds. **Deliverables**: radiation-risk module; GNSS degradation ensemble; equipment transfer functions; receiver-performance database.

### T4 — API, Dashboard, and Pre-Registered Validation (Months 4-6)

Months 4-5: RESTful API (Python/FastAPI) serving HELIOS products as JSON, queryable by location, time window, equipment type, and accuracy threshold. Web dashboard with two views: a SRAG-oriented mission radiation summary and an operator-facing precision-ag accuracy map with go/no-go overlay. Months 5-6: execute the pre-registered retrospective validation on hold-out events from Table 3-1 and the GNSS hold-out set, computing CCMC-compatible metrics (HSS, TSS, POD, FAR, Brier, CRPS) with severity stratification. **Deliverables**: API with documentation; dashboard prototype; retrospective validation report.

### T5 — End-User Engagement and Commercialization (Months 1-6)

Months 1-3: structured customer-discovery interviews via OSU Extension, the Ohio Agricultural Research and Development Center (OARDC), and OEM platform teams; engagement with operators through the George Washington Carver Science Park ecosystem at OSU. Months 3-5: NASA-center engagement with CCMC (validation), M2M SWAO (operational), SRAG (threshold alignment), SPoRT/MSFC (transition pathway). Months 5-6: Phase II commercialization plan including SaaS pricing, OEM integration roadmap, IP/FTO strategy. **Deliverables**: customer-discovery report; letters of intent; Phase II commercialization plan.

### 3.1 Pre-Registered Validation Framework

A common reviewer concern is that retrospective validation against a curated event list looks strong on paper and fails in production. HELIOS pre-registers training and hold-out events and metric thresholds in this proposal, before Task 4 model selection. **Any deviation in the final report is documented as a deviation; metrics are not re-baselined post hoc.** The pre-registration is filed publicly on the Open Science Framework before any hold-out evaluation runs; see `orchestration/osf_preregistration.template.md` in the helios-program meta-repo for the binding text.

#### Table 3-1. Pre-registered SEP validation events for the NASA mission-operations slice

| Event | Date | Use | Notes |
|---|---|---|---|
| Bastille Day | 2000 Jul 14 | Train | Major X5.7 flare; well-characterized SEP profile |
| Halloween storms | 2003 Oct 28 - Nov 4 | Train | Cycle 23 peak; multiple X-class events |
| Mid-cycle 23 | 2005 Jan 20 | Train | X7.1; fast onset; ground-level enhancement |
| Late cycle 23 | 2006 Dec 13 | Train | X3.4; tests low-solar-activity calibration |
| Cycle 24 onset | 2012 Mar 7 | Train | X5.4; tests cross-cycle generalization |
| Cycle 24 mid | 2012 May 17 | Train | M5.1; tests sub-X event sensitivity |
| Sep 2017 storm | 2017 Sep 6 / Sep 10 | Train | X9.3 + back-side X8.2; dual-event sequence |
| Cycle 25 onset | 2022 Jan 20 | **Hold-out** | M5.5; tests cycle-25 distribution shift |
| Mid-cycle 25 | 2023 Feb 17 | **Hold-out** | X2.2; mid-cycle hold-out anchor |
| Gannon (G5) | 2024 May 11 | **Hold-out** | Largest storm in >20 yr; dual-use anchor event |

The GNSS slice uses the May 2024 Gannon storm (G5) plus three hold-out G2+ events: March 2024 (G4), October 2024 (G3), and February 2024 (G2).

### 3.2 Risk Assessment and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Upstream model licensing constraints | Medium | Some CCMC models restrict commercial use | Connector-based architecture using public outputs only; HELIOS IP concentrated in fusion/calibration/translation; FTO review |
| Insufficient extreme-event training data | High | G3+ events <2% of time steps; tail-event learning is hard | SMOTE oversampling on event classes; PINN physics regularization for OOD extrapolation; severity-stratified validation |
| Calibration instability across severity regimes | Medium | Reliability may hold for quiet conditions but fail at extremes | Severity-stratified isotonic regression; conformal prediction for distribution-free bounds; conservative uncertainty composition |
| Validation event cherry-picking | Low (mitigated) | Reviewer concern about selective retrospective performance reporting | Pre-registered 7/3 train/hold-out split in Table 3-1; metric thresholds set in this proposal; deviations documented in final report |
| Non-traditional end-user adoption barriers | Medium | Agricultural operators unfamiliar with space-weather concepts | Equipment-native outputs (go/no-go, accuracy windows) not geophysical indices; OSU Extension and OARDC as trusted intermediaries |
| Key-personnel recruiting risk | Low | ML Engineer role requires specialized skills | Named candidates identified at OSU ECE and Byrd Center; backup candidates in 577 network; PI absorbs critical-path work |

### 3.3 Phase II Vision

A Phase II effort (24 months; scope consistent with NASA SBIR Phase II funding limits) would advance HELIOS from proof-of-concept to functioning operational prototype (TRL 5-6) through: (a) real-time operational deployment with live model retraining; (b) field validation across 5-10 precision-ag operations during the 2028 planting season; (c) CCMC proving-ground evaluation; (d) prototype deployment to M2M SWAO and SPoRT for mission-operations evaluation; (e) production-grade API at 99.9% uptime; (f) pilot integration with at least one precision-ag OEM telematics platform; (g) expansion into the four Phase II verticals described in §6.4 — autonomous-vehicle GNSS integrity, geospatial surveying, satellite drag prediction for LEO operators, and parametric space-weather insurance. Post-Phase II commercialization is funded through SaaS recurring revenue and OEM revenue share.

---

## 4. Related R&D and HELIOS Innovation

### 4.1 Current State of the Art

HELIOS extends, not replaces, existing operational capability. CCMC's MagPy estimates flare/CME/SEP probabilities from solar magnetic-energy proxies. OSPREI models CME evolution for improved ICME propagation prediction. UMASEP and HESPERIA REleASE address SEP forecasting with complementary methodologies. Ovation Prime maps auroral particle precipitation. NAIRAS provides global radiation nowcasts for aircraft and spacecraft [15]. SEPMOD models SEP propagation. Each model serves its designed purpose but produces heterogeneous outputs requiring expert interpretation.

The ISEP project (CCMC-M2M SWAO-SRAG, since 2018) consolidates research SEP models into the operational SEP Scoreboards A/B/C [7, 11, 13]. DONKI chronicles daily analyst interpretations with intelligent event linkages via JSON API [8]. Transformer architectures have demonstrated state-of-the-art performance on solar flare prediction (SolarFlareNet using SDO/HMI magnetograms; Sun et al. [14]), and probabilistic ensemble methods are emerging in the SEP literature [25, 26]. **To the best of our literature review, no published ML system connects solar-event prediction through ionospheric response to receiver-level GNSS positioning error in an end-to-end decision pipeline.**

Commercial GNSS correction services (Trimble RTX, John Deere StarFire, Hexagon SmartNet) provide real-time corrections but do not incorporate space-weather forecasts; their integrity monitoring is reactive — detecting degradation after occurrence rather than predicting it. **No commercial service today provides 2-24 hour predictive warning of ionospheric degradation in terms an agricultural operator can act on.**

### 4.2 What Is Innovative About HELIOS

The novelty claim is framed conservatively. HELIOS is innovative in five specific ways, each defensible against the literature:

1. **Model-agnostic decision-calibrated fusion.** Bayesian Model Averaging with isotonic-regression reliability calibration applied across heterogeneous CCMC and SWPC SEP outputs. Operational ensemble work to date has emphasized model averaging without explicit reliability calibration; HELIOS combines both with conformal-prediction uncertainty bounds. *Implementation*: [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine)[^3].

2. **Provenance-aware architecture.** Every output traces to its underlying models, data feeds, and assumptions — a property required for CCMC proving-ground evaluation, ARRT-compatible mission integration, and the operator trust that safety-critical adoption demands. *Specification*: [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec)[^1] — open RFC composing SPASE 2.7.1, W3C PROV-JSON, and RO-Crate 1.2 JSON-LD with a novel feature-level transformation chain. To our knowledge, the first feature-level lineage standard for heliophysics fusion systems.

3. **Dual-use translation from a common fusion core.** NASA mission operations and precision agriculture share fusion infrastructure but use separate translation modules. The R2O2R feedback loop is bidirectional: operator feedback informs model weighting, and the commercial workload funds operational maturation that NASA would otherwise need to fund alone. The commercial slice produces three independent benefits to NASA: it generates real-world calibration data on rare extreme events (every G2+ event is an inadvertent validation campaign for the fusion engine), it amortizes the operational cost of keeping the system live, and it documents trust patterns from non-traditional users that inform future NASA acquisitions.

4. **Equipment-aware GNSS prediction.** To our knowledge, HELIOS is the first system to translate ionospheric disturbance forecasts into receiver-family-specific RTK accuracy distributions for named precision-ag receivers, rather than generic K-index or TEC warnings. *Foreshadowing analysis*: the May 2024 Gannon storm retrospective[^4] demonstrates the data pipeline and equipment-transfer-function concept on real CORS data.

5. **Industry-native output.** HELIOS delivers decisions in the operator's language — accuracy windows, go/no-go field maps, all-clear-status probability with time-to-threshold — not raw Kp or pfu values that require expert interpretation.

### 4.3 577 Industries Relevant Experience

577 Industries Inc. (Columbus, OH) brings directly applicable capabilities:
(a) three successfully executed DoD SBIR Phase I contracts applying AI/ML to defense data analytics, demonstrating on-budget, on-schedule SBIR execution;
(b) the **FORGE OS** platform — production-grade ML pipeline infrastructure including data ingestion, feature engineering, training, and deployment, with proven containerized portability between AWS and on-premises;
(c) the **IRIS** sparse-data learning approach, internally benchmarked to yield substantial accuracy gains on severely imbalanced classification tasks directly applicable to the <2% G2+ event rate;
(d) experience building explainable decision-support tools that translate complex sensor data into operator-actionable intelligence for DoD customers — exactly the translation discipline HELIOS applies to civilian space weather.

---

## 5. Key Personnel and Facilities

### 5.1 Key Personnel

**Thomas Waweru**, Principal Investigator (50% effort, 6 months). Founder and PI, 577 Industries Inc. Led FORGE OS platform development and executed three DoD SBIR Phase I contracts in AI/ML for defense applications. Expertise: ML system architecture, sparse-data learning, predictive modeling, edge AI, NLP, computer vision, cybersecurity analytics. Will provide overall technical leadership, fusion-engine architecture, NASA-center engagement, and end-user discovery. Primary employment is with the small business, satisfying NFS 1852.219-83.

**Senior ML Engineer** (35% effort, 6 months; named candidates identified). Required profile: transformer architectures for scientific time-series; ionospheric physics or GNSS signal-processing familiarity; Python ML stack (PyTorch, scikit-learn, XGBoost, LightGBM); operational ML deployment. Candidates identified through Ohio State University's Department of Electrical and Computer Engineering, the OSU Byrd Polar and Climate Research Center, and 577 Industries' existing technical network. Conditional offers will be extended on award.

**Space-Weather / Ionospheric Physics SME Consultant** (15% effort; subcontract). Will support fusion-engine validation, CCMC framework compliance, and SRAG operational-threshold alignment. Candidate identified through the OSU geophysical-imaging and Byrd Center research community; formal engagement contingent on award. Required: peer-reviewed publication in SEP forecasting or ionospheric disturbance characterization, plus prior experience with CCMC or NOAA SWPC products.

### 5.2 Facilities and Equipment

577 Industries operates from Columbus, OH. No major capital equipment is required for this software-centric Phase I, concentrating funds on labor, validation, and stakeholder engagement. Facilities include AWS cloud compute (GPU instances for ML training; $8,000 budgeted), the FORGE OS containerized ML pipeline, secured developer workstations, and access to public archives (CDDIS, DONKI, SWPC, GOES, DSCOVR, IGS, NGS CORS) requiring no special agreements.

### 5.3 NASA Center Engagement

- **CCMC at GSFC** — HELIOS APIs designed for compatibility with CCMC containerization standards. Target validation-framework benchmarking and — on sufficient maturity — submission to the CCMC model catalog.
- **M2M SWAO at GSFC** — Primary evaluation partner for the mission-operations translation module. Ingest DONKI linkages generated by M2M analysts; coordinate on cislunar and Mars-environment products.
- **SRAG at JSC** — Validate the radiation-risk translation module against SRAG operational thresholds and ARRT compatibility. HELIOS positions as compatible upstream input, not a replacement.
- **SPoRT Center at MSFC** — Engage SPoRT's established decision-support transition framework as a candidate operational-end-user pathway for HELIOS products.

---

## 6. Potential Post Applications and Commercialization Plan

### 6.1 Beachhead Market: U.S. Precision Agriculture

The precision-agriculture beachhead is selected for the three reasons stated in §1.3 (install-base concentration, dollar-quantified disruption, geographic concentration). Bottom line: more than 80% of U.S. row-crop acres operate under GPS guidance; the John Deere StarFire family, Trimble RTK, and AgLeader Surefire/Versa receivers dominate; Deere's Operations Center connects 500,000+ machines; the IA/IL/IN/OH corridor concentrates the addressable customer base within a one-day drive of Columbus, OH. The global precision-agriculture market reached $12.9 B in 2024 with a CAGR near 15% through 2030; the U.S. SAM dominated by row-crop guidance and RTK services is several billion dollars and growing.

### 6.2 Revenue Model

Bottom-up near-term SAM (Years 1-3) is estimated at $15-30M across precision-ag enterprise customers, NASA and government operational users, and selected commercial satellite operators. SaaS recurring revenue is supplemented by OEM revenue share (target 70/30 HELIOS/OEM) at Phase II maturity.

| Tier | Monthly | Target customer |
|---|---|---|
| Basic | $200 | Individual operators; single-operation row-crop farms |
| Professional | $1,000 | Mid-size operations; ag-tech retailers; cooperative branch operations |
| Enterprise | $5,000-$10,000 | Large cooperatives; OEM telematics integrations; fleet operators; satellite operators; NASA/government tier |

**Indicative three-year post-Phase-II revenue projection** (conservative against the addressable base; NASA/government and satellite-operator tiers excluded for conservatism):

| Year | Basic ($200/mo) | Professional ($1,000/mo) | Enterprise ($5-10K/mo) |
|---|---|---|---|
| Y1 — pilot & OEM launch | 80 subs (~$0.19M ARR) | 20 subs (~$0.24M ARR) | 3 subs (~$0.30M ARR) |
| Y2 — OEM scale-up | 400 subs (~$0.96M ARR) | 120 subs (~$1.44M ARR) | 10 subs (~$1.00M ARR) |
| Y3 — multi-vertical entry | 1,200 subs (~$2.88M ARR) | 400 subs (~$4.80M ARR) | 30 subs (~$3.00M ARR) |

Year-3 indicative top line: ~$10.7M ARR across the three tiers shown. Achieving these numbers requires at least one OEM telematics integration (Phase II goal), the parametric-insurance pilot (Phase II goal), and continued OSU Extension / OARDC distribution. Failing those, the direct-SaaS-only path yields a slower but still meaningful trajectory (~$1.5-3M ARR by Y3).

### 6.3 Go-to-Market Strategy

- **NASA mission transition** (concurrent with commercial entry). CCMC proving-ground deployment, M2M SWAO operational evaluation, SRAG threshold compatibility, NOAA SWPC collaboration. The White House R2O2R implementation plan [4] explicitly calls for improved public-private transition mechanisms, into which HELIOS fits directly.
- **Precision-ag OEM integration.** Partnership conversations with John Deere Operations Center, AGCO Fuse, and CNH AFS Connect for telematics integration with revenue share. OEM integration converts customer acquisition from the SaaS direct model to platform distribution — a step-change in CAC and time-to-revenue.
- **Direct SaaS sales.** Large cooperatives (CHS Inc., Land O'Lakes), commercial ag retailers (Nutrien Ag Solutions), and large family operations approached through the OSU Extension network and OARDC.

### 6.4 Phase II Expansion Verticals

Once the fusion engine and provenance architecture are proven, Phase II opens four expansion verticals using the same core, each requiring only a new translation module:

- **Autonomous-vehicle and trucking GNSS integrity** — Smart Columbus / DriveOhio ecosystem; May Mobility and large fleet operators with lane-level safety thresholds.
- **Geospatial surveying and construction guidance** — Trimble, Hexagon, and large national survey firms; cm-level accuracy windows for time-bounded projects.
- **Satellite drag prediction for LEO operators** — Atmospheric-density forecasting for constellation operators where conjunction risk and orbit-keeping fuel scale with thermospheric variability.
- **Parametric space-weather insurance** — Agricultural reinsurers (Munich Re, Swiss Re, Lloyd's syndicates) where verified threshold crossings trigger parametric payouts; HELIOS provides the audit-grade data backbone.

### 6.5 NASA Mission Applications Beyond SRAG

Beyond commercial markets and beyond the Phase I SRAG translation, HELIOS supports: Artemis crew radiation protection and EVA planning; lunar-surface GNSS architecture using THEMIS-ARTEMIS cislunar data; LEO operations GNSS integrity for ISS and commercial-crew vehicles; satellite drag prediction; and integration with NAIRAS for aviation GNSS integrity supporting ADS-B mandates.

### 6.6 Competitive Positioning and IP Strategy

HELIOS's defensibility rests on: (1) calibrated probabilistic fusion across multiple models, not single-model wrappers; (2) provenance-aware architecture enabling proving-ground evaluation and operator trust; (3) equipment-specific GNSS predictions unavailable from either pure-play space-weather companies or GNSS correction services; (4) dual-use design from common infrastructure; (5) first-mover position in space-weather-to-receiver-accuracy prediction. The IP strategy protects 577 Industries' proprietary value in **orchestration, calibration logic, the receiver-performance ontology, event-translation rules, and operator UI/UX**, while respecting upstream model licensing — HESPERIA REleASE in particular [30]. SBIR data rights are asserted on the fusion and translation layers.

The hybrid open/private architecture supports this: the fusion-engine framework is open source (Apache 2.0) to maximize community trust, CCMC compatibility, and academic citation; the trained weights, BMA priors fitted on Table 3-1 events, and equipment transfer functions live in a private companion repo and constitute the commercial IP.

---

## 7. Budget Summary

| Budget Category | Amount |
|---|---|
| Direct Labor — PI Thomas Waweru (50% effort, 6 months) | $52,000 |
| Direct Labor — Senior ML Engineer (35% effort, 6 months) | $35,000 |
| Fringe Benefits (30% of direct labor) | $26,100 |
| Subcontract — Space-Weather/Ionospheric SME (15% effort) | $18,000 |
| Cloud Computing (AWS GPU instances, S3, API hosting) | $8,000 |
| Travel (NASA centers; agricultural end-user engagement) | $4,500 |
| Materials and Software Licenses | $2,000 |
| Subtotal Direct Costs | $145,600 |
| Fee / Profit | $4,400 |
| **TOTAL PROPOSED PRICE** | **$150,000** |
| TABA Request (commercialization vendor support) | $6,500 |

**Subcontracting compliance**: subcontract cost ($18,000) + G&A allocation (≈$1,260) = $19,260 total subcontracting against direct technical cost of $145,600. Subcontracting percentage = $19,260 / ($150,000 − $4,400) = **13.2%**, well below the 33% maximum for SBIR Phase I (NFS 1852.219-80). PI primary employment is with the small business (NFS 1852.219-83). All work performed in the United States.

**Budget rationale.** Direct labor maximizes technical execution within the Phase I ceiling. Cloud compute supports transformer model training on 20+ years of CDDIS GIM and CORS positioning data. Travel funds NASA center engagement (GSFC, MSFC, JSC) and Ohio-Midwest end-user discovery. TABA funds (maximum $6,500 allowed) support customer discovery, FTO/IP review of the fusion architecture, and pricing validation through an approved TABA vendor.

---

## 8. References

[1] *Promoting Research and Observations of Space Weather to Improve the Forecasting of Tomorrow Act*, Pub. L. No. 116-181, 134 Stat. 886 (2020).
[2] *Findings and Recommendations to Successfully Implement PROSWIFT and Transform the National Space Weather Enterprise*, Space Weather Advisory Group (2023).
[3] *National Space Weather Strategy and Action Plan*, National Science and Technology Council (2019).
[4] *Space Weather Research-to-Operations and Operations-to-Research Framework*, SWORM Subcommittee (2022).
[5] *Decadal Survey for Solar and Space Physics (Heliophysics) 2024-2033*, National Academies (2025).
[6] Hapgood, M.A. et al., *The Space Weather Science and Observation Gap Analysis*, Advances in Space Research, 72(12), 5389-5417 (2023).
[7] SEP Scoreboard, Space Radiation Analysis Group, NASA JSC: <https://srag.jsc.nasa.gov/SpaceWeather/SEPScoreboard.cfm>
[8] DONKI: Space Weather Database of Notifications, Knowledge, Information, NASA CCMC: <https://kauai.ccmc.gsfc.nasa.gov/DONKI/>
[9] Community Coordinated Modeling Center, NASA GSFC: <https://ccmc.gsfc.nasa.gov>
[10] Moon to Mars Space Weather Analysis Office, NASA GSFC: <https://science.gsfc.nasa.gov/674/m2m-website.html>
[11] Whitman, K. et al., *Tools Used in Space Radiation Operations*, NASA Technical Reports (2023).
[12] Collado-Vega, Y. et al., *CCMC Space Weather Research Analysis for NASA Robotic Missions*, NASA Technical Reports (2023).
[13] Whitman, K. et al., *NASA's Ongoing SEP Model Validation Effort Driving an Effective R2O2R Process*, COSPAR (2024).
[14] Sun, Z. et al., *Operational prediction of solar flares using a transformer-based framework*, Scientific Reports, 13, 12603 (2023).
[15] Mertens, C.J. et al., *NAIRAS Version 3 Atmospheric Ionizing Radiation Validation*, Space Weather, 23 (2025).
[16] *Assessment of Space Weather Impact on Precision Agriculture Using GNSS in Brazilian Farms*, NASA NTRS (2025).
[17] *Effect of Space Weather on Autonomous Vehicle Navigation*, SAE Technical Paper 2020-01-0140.
[18] *Space Environment Engineering and Science Applications Workshop — Ionospheric Impacts: Precision Agriculture (SEESAW-II)*, USDA ARS (2022).
[19] *Solar Storm Risk to the North American Electric Grid*, Lloyd's of London and AER, Inc. (2013).
[20] London Economics, *The Economic Impact on the UK of a Disruption to GNSS* (2017).
[21] *Space Weather Phase 1 Benchmarks*, SWORM Subcommittee (2018).
[22] Executive Order No. 13744, *Coordinating Efforts to Prepare the Nation for Space Weather Events* (2016).
[23] Executive Order No. 13865, *Coordinating National Resilience to Electromagnetic Pulses* (2019).
[24] Space Foundation, *The Space Report 2025 Q2: Global Space Economy at $613 Billion*.
[25] Bobra, M.G. and Couvidat, S., *Solar Flare Prediction Using SDO/HMI Vector Magnetic Field Data*, ApJ, 798, 135 (2015).
[26] Poduval, B. et al., *AI-ready data in space science and solar physics*, Frontiers in Astronomy and Space Sciences, 10 (2023).
[27] American Farm Bureau Federation, *Precision Agriculture Technology Survey Results* (2024).
[28] OSU Extension, *Space Weather Disturbances and Farm GPS Interruptions* (2024).
[29] Starion Group, *Space Weather: A Risk to Autonomous Transport?* (2024).
[30] CCMC HESPERIA REleASE Model Page, commercial-use licensing note: <https://ccmc.gsfc.nasa.gov/models/HESPERIA_REleASE~v20190101/>
[31] Vovk, V., Gammerman, A., Shafer, G., *Algorithmic Learning in a Random World (Conformal Prediction)*, 2nd ed., Springer (2022).
[32] Lim, B., Arik, S.O., Loeff, N., Pfister, T., *Temporal Fusion Transformers for interpretable multi-horizon time series forecasting*, International Journal of Forecasting, 37(4), 1748-1764 (2021).

---

*This companion document is maintained at [github.com/577Industries/helios-program](https://github.com/577Industries/helios-program) (public; pull requests welcome from interested reviewers and stakeholders).
Rendered HTML and PDF versions auto-publish to the project's GitHub Pages site on every artifact merge.
Last updated: 2026-05-17. Contact: <engineering@577industries.com>.*
