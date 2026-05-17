# OPERATOR_TODO

> Actions only the operator (Thomas) can take. Each item is gated on credentials,
> external accounts, or one-time configurations that an automated agent can't
> complete. Crossed-off when done.

---

## Immediate (unblock v0.2.0 stable + Sprint C-Training)

### 1. Configure PyPI trusted publishing for 3 packages

**Why**: After the atomic provenance-swap PR lands and connectors v0.2.0 is tagged, the existing `.github/workflows/publish.yml` workflows (already committed to `helios-provenance-spec` and `helios-fusion-engine`; will be added to `helios-spaceweather-connectors` at v0.2.0) will fire on release publication and attempt PyPI publish via OIDC. Without trusted publishing configured on pypi.org, they will fail at the publish step.

**Steps** (repeat for each of the 3 packages):

1. Go to <https://pypi.org/manage/account/publishing/>
2. Under "Add a new publisher (GitHub)", fill:
   - **Publisher**: GitHub
   - **PyPI Project Name**: `helios-provenance-spec` (or `helios-fusion-engine` or `helios-spaceweather-connectors`)
   - **Owner**: `577Industries`
   - **Repository name**: `helios-provenance-spec` (matching the project name)
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`
3. Click "Add"
4. Verify by re-running the latest release's `publish.yml` workflow via `gh workflow run publish.yml --repo 577Industries/<package-name>` (or by tagging a v0.1.1 patch and watching the publish step succeed)

**Status**: ⏳ pending. **Blocks**: PyPI publication of A, C, and (after v0.2.0) connectors.

### 2. Set Earthdata Login credentials

**Why**: `CddisGimAdapter` requires NASA Earthdata Login to fetch IONEX TEC maps. Without credentials, the live test is gated and Sprint C-Training can't pull real CDDIS data for the 7 Table 3-1 training events.

**Steps**:

1. Register at <https://urs.earthdata.nasa.gov/> (if not already)
2. Log in and go to "Applications" → "Authorized Apps"
3. Approve "NASA GESDISC DATA ARCHIVE" (this is the CDDIS authorization)
4. Set local env vars:
   ```bash
   echo 'export NASA_EARTHDATA_USER="<your_user>"' >> ~/.bashrc
   echo 'export NASA_EARTHDATA_PASS="<your_pass>"' >> ~/.bashrc
   ```
5. For CI: add as repository secrets at <https://github.com/577Industries/helios-spaceweather-connectors/settings/secrets/actions>:
   - `NASA_EARTHDATA_USER`
   - `NASA_EARTHDATA_PASS`
6. Verify locally: `cd ~/577i-Projects/helios-spaceweather-connectors && pytest -m live tests/test_cddis_gim.py::test_live_cddis_columbus_gannon`

**Status**: ⏳ pending. **Blocks**: CDDIS live tests; Sprint C-Training (needs real GIM data for Table 3-1 events).

### 3. File OSF pre-registration (before Sprint C-Training's hold-out phase)

**Why**: The pre-registered kill-gate is non-negotiable program discipline. The OSF URL must be on file BEFORE any hold-out evaluation runs. The kill-gate runner (`helios-program/orchestration/kill_gate.py`) will refuse to execute without it.

**Steps**:

1. Open `~/577i-Projects/helios-program/orchestration/osf_preregistration.template.md`
2. Fill in the `TO_BE_FILLED` fields:
   - **Investigators** (already has PI Thomas; add SME consultant name + ML Engineer name when those hires are confirmed)
   - **Date filed (UTC ISO 8601)**: filled at filing time
   - **OSF DOI**: filled after OSF assigns it
   - **Model freeze date**: today's date when Sprint C-Training tags the locked commit
   - **Hold-out evaluation date**: planned date (must be after OSF filing)
   - **Git commit SHA**: tag at the locked commit; OSF references that SHA
3. Submit on OSF: <https://osf.io/dashboard/> → "Create new project" → "Registrations" → use the AsPredicted template
4. Save the OSF URL to `~/577i-Projects/helios-program/orchestration/osf_preregistration.url`:
   ```bash
   echo "https://osf.io/<your-registration-id>/" > orchestration/osf_preregistration.url
   ```
5. Tag the helios-fusion-engine commit:
   ```bash
   cd ~/577i-Projects/helios-fusion-engine
   git tag -a prereg-v1.0 -m "OSF pre-registration v1.0 — filed at <OSF URL>"
   git push origin prereg-v1.0
   ```

**For the OSF "Deviations" section**: the Sprint C-Training-v2 review pack at [`specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](specs/2026-05-17-Sprint-C-Training-v2-review-pack.md) contains a **ready-to-paste methodology-note draft** documenting v2's hybrid truth approach (real NOAA SESC archive labels + per-(component, event) source labeling from the empirical ISWA coverage matrix). Drop it verbatim into the OSF "Deviations" section before filing; adjust the dates and OSF URL placeholder when known.

**Tag target after merge**: as of session 4, the locked commit is `helios-fusion-engine` at `ac53eb6` (post-v0.1.2 merge). If any docs PRs land before pre-reg filing, retag at the new HEAD.

**Status**: ⏳ pending. **Blocks**: kill-gate execution (the hold-out evaluation).

---

## RFC and outreach (community engagement)

### 4. Cross-post RFC-0001 link

**Why**: The RFC issue is open at <https://github.com/577Industries/helios-provenance-spec/issues/4> but only people who visit the repo will see it. The community engagement framing in §4.2 innovation #2 needs the link to land where the heliophysics community looks.

**Steps**:

1. Email the SPASE info list (<spase-info@googlegroups.com>) with subject "RFC: feature-level provenance for heliophysics fusion systems". Body: a 3-paragraph intro + the issue URL.
2. Email sunpy-dev (<https://groups.google.com/g/sunpy>) with similar framing — emphasize the SPASE + W3C PROV-JSON composition.
3. Email CCMC feedback at <ccmc-feedback@helio.gsfc.nasa.gov> (if that's the right address; the operator should pick the right CCMC contact based on their existing relationships).
4. Cross-post to LinkedIn from the 577 Industries page (or Thomas's personal account) — the post draft is at `~/577i-Projects/helios-program/docs/blog/social/2026-05-17-linkedin.md` (which is the Gannon blog post draft; either repurpose its closing CTA to point at the RFC, or write a separate LinkedIn post).

**Status**: ⏳ pending. **Impact**: drives RFC §6 community comments → informs v0.2 of the schema.

### 5. Publish the Gannon retrospective blog post

**Why**: The post staged at <https://577industries.github.io/helios-program/blog/when-the-sky-stopped-the-tractors/> is the program's strongest customer-discovery hook. Currently lives on the project docs site; mirroring to 577industries.com gives it the canonical home for outbound marketing.

**Steps**:

1. Copy `~/577i-Projects/helios-program/docs/blog/posts/2026-05-17-when-the-sky-stopped-the-tractors.md` into the 577industries.com WordPress (or whatever CMS).
2. Schedule the LinkedIn post (draft at `docs/blog/social/2026-05-17-linkedin.md`) — **preserve the inline climatological-v1 caveat**.
3. Schedule the 9-tweet Twitter/X thread (draft at `docs/blog/social/2026-05-17-twitter-thread.md`).
4. Send courtesy heads-ups to:
   - OSU Extension (your existing contacts)
   - Ohio Agricultural Research and Development Center (OARDC)
   - American Farm Bureau Federation (which documented Gannon impacts in their 2024 survey [ref 27 in the proposal])
   - John Deere Operations Center / AGCO Fuse / CNH AFS Connect platform teams (this is the §6.3 OEM-integration cold open)

**Status**: ⏳ pending. **Impact**: customer-discovery interviews per §2 Obj. 5 (target: ≥10 prospective customers + ≥4 LOIs).

---

## Recruiting

### 6. Identified key personnel — confirm intent before NASA award

Per proposal §5.1:

- **Senior ML Engineer** (35% effort): named candidates at OSU ECE + Byrd Polar and Climate Research Center. **Send conditional-offer letters** ("on NASA award, we'd extend...") so the proposal-submission claim is backed by real people.
- **Space-Weather / Ionospheric Physics SME Consultant** (15%; subcontract): identified through OSU geophysical-imaging community. **Same** — confirm intent.

**Status**: ⏳ pending. **Why now**: even though Phase I award is uncertain, having LOIs from the named hires strengthens the Phase II re-pitch substantially.

---

## NASA-center engagement

### 7. Reach out to CCMC / M2M SWAO / SRAG / SPoRT before Phase II

Per proposal §5.3, the NASA-center engagement plan during Phase I is:

- **CCMC at GSFC** — validation-framework alignment + (on sufficient maturity) submission to the CCMC model catalog
- **M2M SWAO at GSFC** — DONKI integration + operational mission relevance
- **SRAG at JSC** — ARRT-compatibility alignment for the radiation-risk translation module
- **SPoRT Center at MSFC** — operational-end-user transition pathway

**Action**: send each center a courtesy email with the helios-program companion URL <https://577industries.github.io/helios-program/companion/> and the master plan URL. Frame: "We're building public infrastructure that fits your framework; here's how it slots in; we'd value your read on the RFC and any specific gaps."

**Status**: ⏳ pending. **Impact**: ≥2 NASA-relevant Letters of Intent for §2 Obj. 5 success criterion + Phase II commercialization plan stakeholder section.

---

## Long arc

### 8. SBIR Phase I award outcome (informational; nothing to do)

Whether or not the Phase I award lands, HELIOS continues. If awarded: the Phase I work plan kicks in for 6 months (T1-T5 per master plan §3). If rejected: the Phase II re-pitch uses everything in this companion document.

### 9. Phase II proposal (eventual)

Per master plan §3.3 — 24-month effort to advance HELIOS to TRL 5-6. The Sprint C-Training results + kill-gate paper + companion document become the Phase II evidence base.

---

## How this file is maintained

This file is the operator-facing checklist. **Update statuses** as items move ⏳ → ✅. Add new items at the top when they emerge. Cross-references:

- Per-artifact details: `helios-program/specs/`
- Master plan execution log: `helios-program/plan/master-plan.md`
- Per-Claude-session context: `helios-program/CLAUDE.md`
- Public-facing companion: `helios-program/companion/companion.md`

Last edited: 2026-05-17 (this is the canonical "what the operator still needs to do" doc at the end of Session 2; will be refreshed each session).
