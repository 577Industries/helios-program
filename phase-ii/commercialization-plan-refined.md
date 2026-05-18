# HELIOS Phase II — refined commercialization plan

**Status**: Phase I learnings → Phase II strategy refinement (initial draft).
**Last refreshed**: 2026-05-18.
**Supersedes (for Phase II proposal use only)**: §6 of the submitted Phase I proposal (companion mirror at <https://577industries.github.io/helios-program/companion/#6-potential-post-applications-and-commercialization-plan>). The Phase I §6 remains canonical for the submitted proposal; this document is the **Phase II re-pitch refinement** built on top of it.

---

## How this document is structured

§A surfaces the five concrete Phase I learnings that should shape Phase II strategy. §B threads each learning into the relevant Phase I §6 sub-section and proposes a specific Phase II refinement. §C documents what is **not** yet refined (operator-action inputs still pending — customer-discovery interviews, OEM conversations, NASA-center engagement records).

---

## §A. Phase I learnings that shape Phase II strategy

These five learnings are each grounded in a specific shipped artifact. They are the most credible foundation for a Phase II re-pitch.

### Learning 1 — ISWA Jan 2017 cutover demonstrates empirical-rigor discipline

**What we learned**: ISWA's earliest SEP Scoreboard deposits are calendar-year 2017, not "around 2018" as v1 had assumed. 6 of 7 Table 3-1 training events (Bastille 2000 through Cycle 24 mid 2012) have **zero** real ISWA coverage. Confirmed by an exhaustive May 17 probe of every model directory × every event window.

**Source artifact**: [`results/2026-05-17-iswa-coverage-matrix.md`](https://github.com/577Industries/helios-program/blob/main/results/2026-05-17-iswa-coverage-matrix.md)

**What it demonstrates to a Phase II reviewer**:
1. The program runs empirical probes before claiming results.
2. When an assumption breaks, the deviation is documented in a public review pack — not papered over.
3. The fix preserves the v1 fitness function in the manifest (`training_runs[0]`) and appends v2 (`training_runs[1]`), so future auditors can reproduce the methodology evolution.

**Phase II refinement**: Phase II §3.1 ("Pre-Registered Validation Framework") gets a new sub-bullet documenting the ISWA-cutover empirical finding as the model for how we handle methodology surprises in Phase II. The Phase II proposal can credibly commit to "we will document any methodology deviation in a public review pack with the same discipline we applied in Phase I (Sprint C-Training v2)."

### Learning 2 — Connector v0.2.1 registry expansion demonstrates real engineering execution

**What we learned**: The Phase I §3 T1 plan committed to **≥6 data sources** with **<15 min median latency** and **100% feature-level provenance**. We shipped all six adapters as live `helios-spaceweather-connectors` v0.2.1 — DONKI · NOAA SWPC · NASA CDDIS GIMs · GOES · DSCOVR · CCMC SEP Scoreboards — with 304+ tests at 87-94% per-adapter coverage. The registry expanded beyond the Phase I commitment as the team encountered real upstream-source quirks.

**Source artifact**: <https://github.com/577Industries/helios-spaceweather-connectors/releases/tag/v0.2.1>

**What it demonstrates to a Phase II reviewer**:
1. Phase I §2 Obj. 1 success criterion (≥6 sources, <15 min latency, 100% provenance) is **shipped, not promised**.
2. The 7 documented API quirks in the DONKI design (per `helios-spaceweather-connectors/docs/design.md`) demonstrate the real-engineering muscle Phase II needs for 99.9%-uptime API operations.
3. Per-adapter review packs ([`specs/2026-05-17-Wave2a-*-review-pack.md`](../specs/) — SWPC, GOES, DSCOVR) document the empirical engineering decisions.

**Phase II refinement**: Phase II §6.3 OEM-integration go-to-market is **credibly defensible**. The connector library proves we can absorb upstream API drift and rate-limiting quirks; this is exactly the engineering posture an OEM (Deere Operations Center, AGCO Fuse, CNH AFS Connect) needs from a telematics-integration partner. The Phase II §6.3 OEM-conversation framing can lean on the v0.2.1 connector portfolio as the technical-credibility anchor.

### Learning 3 — Sprint C-Training v1 → v2 evolution demonstrates pre-registration discipline

**What we learned**: When v1's blanket synthetic-proxy assumption broke under empirical probing (Learning 1), we re-fit BMA priors using per-(component, event) source labels and replaced v1's closed-loop synthetic Kp-derived truth with the **NOAA Space Environment Services Center "Solar Proton Events Affecting the Earth Environment 1976-present" archive**. The OSF "Deviations" methodology note documenting the change is **operator-ready** — drafted at the bottom of the v2 review pack, ready to drop verbatim into OSF before kill-gate eval runs.

**Source artifacts**:
- [`specs/2026-05-17-Sprint-C-Training-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-review-pack.md) (v1)
- [`specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-v2-review-pack.md) (v2 with OSF Deviations draft)

**What it demonstrates to a Phase II reviewer**:
1. The kill-gate pre-registration is **not a marketing gesture**. It survived a real methodology surprise.
2. The deviations note is written *before* the hold-out evaluation runs — pre-registration discipline preserved.
3. The fitness function changed (synthetic Kp truth → real NOAA SESC archive truth), and the top-weighted component for Sept 2017 shifted accordingly (v1 `iPATH` → v2 `SAWS_ASPECS/1.X_Nowcasts_Probability`) — showing the change *had real consequence*, not a cosmetic re-fit.

**Phase II refinement**: Phase II §3.1 ("Pre-Registered Validation Framework") and §3.2 ("Risk Assessment") can claim **pre-registration discipline as a demonstrated capability**, not an aspirational one. The Phase II proposal's "Validation event cherry-picking" risk row (Likelihood: Low — mitigated) gets concrete evidence rather than just procedural commitment.

### Learning 4 — Synthetic-proxy + real-truth hybrid demonstrates honest negative-result handling

**What we learned**: For the 6 pre-2017 Table 3-1 events, no real ISWA coverage exists; v2 keeps the per-(component, event) `synthetic_proxy` label on those components and fits BMA priors against the **real NOAA SESC truth labels** anyway. The result: BMA weights remain near-uniform because all synthetic proxies anchor on the same Kp profile and correlate similarly with SWPC archive events. The honest framing — "the spread will grow at kill-gate eval when the 2022-2024 hold-out events receive native real-data Scoreboard streams" — is in the v2 review pack itself.

**Source artifact**: [`specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-v2-review-pack.md) §"Why weights are still compressed"

**What it demonstrates to a Phase II reviewer**:
1. The program reports compressed BMA weights *as compressed weights*, with the empirical reason, rather than declaring a result it doesn't have.
2. The 2022-2024 hold-out events (which post-date the ISWA cutover) will receive native real-data streams at kill-gate — so the final go/no-go check is **not** subject to the synthetic-proxy substitution.
3. This is the kind of honest negative-result handling that Phase II reviewers reward.

**Phase II refinement**: Phase II §4.2 innovations #1 (decision-calibrated fusion) and #5 (industry-native output) can cite the v2 review pack as evidence of the program's reporting discipline. The "we don't overclaim" posture is itself a Phase II differentiator vs. competing fusion proposals that may hide negative results.

### Learning 5 — 1,302-station-hour Gannon headline survived peer-pressure to oversimplify

**What we learned**: The Gannon retrospective headline — **1,302 station-hours over 2.5 cm across 25 NGS CORS stations IA/IL/IN/OH during May 10-12, 2024** — carries an inline **climatological-v1 disclosure** baked into the methodology doc and the blog post. Removing it for "marketing simplicity" was an explicit temptation; preserving it is documented as a non-negotiable in CLAUDE.md §10. The v2 upgrade (full pseudo-range SPP via the CDDIS adapter) is **identified, scoped, and gated on the TFT-TEC forecasting spec** — not hand-waved.

**Source artifacts**:
- <https://github.com/577Industries/gannon-storm-rtk-analysis> v0.1.0
- <https://577industries.github.io/gannon-storm-rtk-analysis/methodology/> (the disclosure)
- <https://577industries.github.io/helios-program/blog/when-the-sky-stopped-the-tractors/> (lay explainer with disclosure preserved)
- [`specs/2026-05-18-TFT-TEC-forecasting-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-TFT-TEC-forecasting-spec.md) (v2 upgrade plan)

**What it demonstrates to a Phase II reviewer**:
1. The program protects credibility over marketing punch.
2. The v2 upgrade path is concrete — not a "we'll improve this in Phase II" promise but a specifically scoped dispatch spec.
3. The 1,302-station-hour observation is itself the strongest customer-discovery hook for §6 ag-industry outreach.

**Phase II refinement**: Phase II §1.3 ("Precision-Agriculture Slice") and §6.1 ("Beachhead Market") cite the Gannon retrospective with the v2 upgrade plan explicit in §3.3 ("Phase II execution plan"). The Phase II proposal can credibly commit "Phase II will deliver the v2 real-SPP analysis as a peer-reviewable arXiv preprint" because the framework (TFT-TEC spec) is already drafted.

---

## §B. Phase I §6 → Phase II refinement (sub-section-by-sub-section)

### §6.1 Beachhead market

**Phase I framing** (unchanged): U.S. precision agriculture, IA/IL/IN/OH corridor, install-base concentration on Deere StarFire / Trimble RTK / AgLeader.

**Phase II refinement**: Add the **1,302-station-hour Gannon retrospective** (Learning 5) as the empirical credibility anchor for the beachhead claim. Reviewers can audit the methodology in the public Gannon repo before evaluating the Phase II ask.

### §6.2 Revenue model

**Phase I framing** (unchanged for now): 3-tier SaaS (Basic $200 / Professional $1,000 / Enterprise $5-10K monthly); indicative Y3 ARR ~$10.7M with OEM integration + parametric insurance.

**Phase II refinement**: The numbers themselves stay until customer-discovery interviews (operator action — `OPERATOR_TODO.md` item 5) provide empirical signal on pricing sensitivity. When ≥5 interviews land in [`customer-discovery/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/customer-discovery/), this section gets revised with **price-tier validation evidence** (which tier did each interviewee say they'd actually pay; what time-horizon mattered for their go/no-go gate). The aggregation file at `customer-discovery/INSIGHTS.md` feeds this refinement.

### §6.3 Go-to-market strategy

**Phase I framing** (unchanged): NASA mission transition (CCMC proving-ground, M2M SWAO, SRAG, NOAA SWPC) + precision-ag OEM integration (Deere / AGCO / CNH) + direct SaaS sales (cooperatives + retailers via OSU Extension / OARDC).

**Phase II refinement**: The **technical-credibility anchor** for OEM integration is now Learning 2 (v0.2.1 connector portfolio with 6 live adapters + 304+ tests + per-adapter review packs). The Phase II §6.3 OEM-integration paragraph can credibly commit "Phase II delivers production-grade telematics-overlay integration to ≥1 OEM platform during the 2028 planting season" because the connector engineering is shipped, not aspirational.

When OEM conversations actually land (operator action), the named-pilot-partner section gets filled with specifics.

### §6.4 Phase II expansion verticals

**Phase I framing** (unchanged): autonomous-vehicle GNSS integrity · geospatial surveying · satellite drag prediction · parametric space-weather insurance.

**Phase II refinement**: The expansion verticals were always Phase II material; the Phase I deliverable inventory (5 public artifacts) **doesn't change them substantively**, but the v0.1.2 fusion engine (Learning 3) shipping with full BMA + isotonic + Mondrian conformal **proves the fusion core is reusable** across verticals — exactly the "common fusion core" framing Phase I §4.2 innovation #3 promised.

### §6.5 NASA mission applications beyond SRAG

**Phase I framing** (unchanged): Artemis crew radiation protection, lunar-surface GNSS, LEO operations GNSS integrity, satellite drag, NAIRAS integration.

**Phase II refinement**: When NASA-center engagement records land in [`nasa-engagement/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/), this section gets concrete signal on which beyond-SRAG applications NASA itself prioritizes. Currently this is a *forward* list; Phase II can convert it to a *demand-signaled* list.

### §6.6 Competitive positioning and IP strategy

**Phase I framing** (unchanged): Apache 2.0 fusion-engine framework + private `helios-fusion-internal` weights = hybrid open/private architecture.

**Phase II refinement**: The hybrid architecture is now **demonstrated** — `helios-fusion-engine` v0.1.2 public, `helios-fusion-internal` `00a80eb` private with `manifest.json` carrying both v1 and v2 training-run lineage. SBIR data rights are asserted exactly where the master plan said they would be. Learning 4 (honest negative-result reporting) is itself a competitive moat: prospective enterprise customers in safety-critical contexts (NASA SRAG, Deere telematics) reward the program that reports honestly more than the program that markets aggressively.

---

## §C. What is NOT yet refined (operator-action gates)

The following sub-sections of Phase I §6 wait on operator-action inputs before substantive refinement:

| Refinement | Gate | Where the input lands |
|---|---|---|
| §6.2 price-tier validation (real customer signal vs. indicative ARR) | ≥5 customer-discovery interviews | [`customer-discovery/INSIGHTS.md`](https://github.com/577Industries/helios-program/blob/main/phase-ii/customer-discovery/README.md) |
| §6.3 named OEM-pilot partner | Deere / AGCO / CNH conversation lands | [`letters/ag-industry-loi-1.pdf`](https://github.com/577Industries/helios-program/blob/main/phase-ii/letters/README.md) |
| §6.3 named NASA-center pilot | Engagement record from CCMC / M2M SWAO / SRAG / SPoRT | [`nasa-engagement/<center>-YYYY-MM-DD.md`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/README.md) |
| §6.5 demand-signaled NASA applications list | NASA-center engagement records | [`nasa-engagement/`](https://github.com/577Industries/helios-program/blob/main/phase-ii/nasa-engagement/README.md) |
| Kill-gate result citation in §6.6 IP strategy | Sprint D ships per [`specs/2026-05-18-Sprint-D-kill-gate-spec.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-18-Sprint-D-kill-gate-spec.md) | `../results/<date>-killgate.json` |

When any of those gates clears, the relevant §B sub-section gets updated and the **Last refreshed** line at the top of this document is advanced.

---

## Cross-references

- Phase I proposal §6 (canonical for the submitted proposal): <https://577industries.github.io/helios-program/companion/#6-potential-post-applications-and-commercialization-plan>
- Evidence package: [`evidence-package.md`](./evidence-package.md)
- Phase II proposal scaffold: [`phase-ii-proposal-draft.md`](./phase-ii-proposal-draft.md)
- Sprint C-Training v2 review pack: [`../specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](https://github.com/577Industries/helios-program/blob/main/specs/2026-05-17-Sprint-C-Training-v2-review-pack.md)
- ISWA coverage matrix: [`../results/2026-05-17-iswa-coverage-matrix.md`](https://github.com/577Industries/helios-program/blob/main/results/2026-05-17-iswa-coverage-matrix.md)
- Gannon retrospective: <https://github.com/577Industries/gannon-storm-rtk-analysis>
- OPERATOR_TODO.md: [`../OPERATOR_TODO.md`](https://github.com/577Industries/helios-program/blob/main/OPERATOR_TODO.md)
