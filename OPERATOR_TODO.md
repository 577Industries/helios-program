# OPERATOR_TODO

> Step-by-step ordered checklist for actions only the operator (Thomas) can take. Each step is gated on credentials, external accounts, or one-time configurations an automated agent can't complete. Items are numbered in **execution order** with explicit gating notes.
>
> **Last refreshed**: 2026-05-18 (Session 6 — production deploy + GitHub consolidation).

---

## Status as of last refresh

✅ **Tracks 3 + 4 shipped**: arXiv preprint draft merged to `helios-fusion-engine` v0.2.0; Phase II evidence assembly merged to `helios-program` v0.3.0. Both Pages sites rebuilt and serving.

✅ **GitHub consolidated**: HELIOS submoduled under `helios-program/submodules/`; 5 FORGE OS libs renamed to `forge-*` and consolidated under `577Industries` org; 2 dormant experiments archived on personal account; org profile README live at <https://github.com/577Industries>.

✅ **Workspace clean**: ~76 MB of regenerable caches swept; paper worktree pruned; all 6 HELIOS repos clean trees.

⏳ **Two of the four Session 5 tracks remain gated on operator prereqs** (Steps 2 + 3 below).

---

## The ordered checklist

### Step 1 — Review + merge any pending dependabot PRs (optional, ~5 min)

3 dependabot PRs are open on `helios-fusion-engine` (routine GH Actions bumps: `actions/checkout 4→6`, `actions/setup-python 5→6`, `codecov/codecov-action 4→6`). Safe to merge or close.

```bash
gh pr list --repo 577Industries/helios-fusion-engine --author dependabot
gh pr merge <number> --squash --delete-branch --repo 577Industries/helios-fusion-engine
```

**When done**: `gh pr list --repo 577Industries/helios-fusion-engine --author dependabot` returns empty.

**Gates**: nothing — purely housekeeping.

---

### Step 2 — Set NASA Earthdata Login credentials (~10 min)

**Why**: `CddisGimAdapter` requires Earthdata Login for IONEX TEC maps. Gates the Track 2 (§2 Obj. 2 TFT for TEC forecasting) dispatch + the CDDIS live tests.

1. Register at <https://urs.earthdata.nasa.gov/> if not already.
2. Log in → "Applications" → "Authorized Apps" → approve **"NASA GESDISC DATA ARCHIVE"** (CDDIS authorization).
3. Set local env vars in `~/.bashrc`:
   ```bash
   echo 'export NASA_EARTHDATA_USER="<user>"' >> ~/.bashrc
   echo 'export NASA_EARTHDATA_PASS="<pass>"' >> ~/.bashrc
   source ~/.bashrc
   ```
4. Add CI secrets at <https://github.com/577Industries/helios-spaceweather-connectors/settings/secrets/actions>:
   - `NASA_EARTHDATA_USER`
   - `NASA_EARTHDATA_PASS`
5. Verify locally:
   ```bash
   cd ~/577i-Projects/helios-spaceweather-connectors
   pytest -m live tests/test_cddis_gim.py::test_live_cddis_columbus_gannon
   ```

**When done**: `pytest -m live` against CDDIS passes; both secrets visible at the Actions secrets page.

**Gates / unblocks**: Track 2 dispatch (TFT-TEC). Also unblocks `gannon-storm-rtk-analysis` v2 (real-SPP via TFT-predicted TEC).

---

### Step 3 — File OSF pre-registration (~30 min)

**Why**: The pre-registered kill-gate is non-negotiable program discipline. The OSF URL must be on file **BEFORE** any hold-out evaluation runs. `orchestration/kill_gate.py` refuses to execute without it. Gates the Track 1 (Sprint D) dispatch.

1. Open `~/577i-Projects/helios-program/orchestration/osf_preregistration.template.md`.
2. Fill in the `TO_BE_FILLED` fields:
   - **Investigators** (already lists PI Thomas; add SME consultant + ML Engineer names when those hires confirm — see Step 6)
   - **Date filed (UTC ISO 8601)** — at filing time
   - **OSF DOI** — after OSF assigns
   - **Model freeze date** — today's date when Sprint D tags the locked commit
   - **Hold-out evaluation date** — planned date (must post-date OSF filing)
   - **Git commit SHA** — see "tag target" below
3. **Methodology-note for the "Deviations" section**: paste verbatim from [`specs/2026-05-17-Sprint-C-Training-v2-review-pack.md`](specs/2026-05-17-Sprint-C-Training-v2-review-pack.md) (documents v2's hybrid truth approach + per-(component, event) source labeling from the empirical ISWA coverage matrix). Adjust dates + OSF URL placeholder when known.
4. Submit on OSF: <https://osf.io/dashboard/> → "Create new project" → "Registrations" → use the AsPredicted template.
5. Save the OSF URL:
   ```bash
   echo "https://osf.io/<your-registration-id>/" > ~/577i-Projects/helios-program/orchestration/osf_preregistration.url
   ```
6. Tag the locked commit on `helios-fusion-engine`:
   ```bash
   cd ~/577i-Projects/helios-fusion-engine
   git pull
   git tag -a prereg-v1.0 -m "OSF pre-registration v1.0 — filed at <OSF URL>"
   git push origin prereg-v1.0
   ```
7. Commit + push the URL file:
   ```bash
   cd ~/577i-Projects/helios-program
   git add orchestration/osf_preregistration.url
   git commit -m "chore(orchestration): pin OSF pre-registration URL for kill-gate"
   git push
   ```

**Tag target as of Session 6**: `helios-fusion-engine` at `v0.2.0` (current main HEAD). If any docs PRs land before pre-reg filing, retag at the new HEAD.

**When done**: `cat ~/577i-Projects/helios-program/orchestration/osf_preregistration.url` returns a real OSF URL; `git ls-remote --tags origin | grep prereg-v1.0` returns one row.

**Gates / unblocks**: Track 1 dispatch (Sprint D kill-gate execution).

---

### Step 4 — Signal "prereqs done" to dispatch Sprint D + TFT (~1 min)

After Steps 2 + 3 land: open the next Claude Code session in `~/577i-Projects/helios-program/` and write:

> prereqs done — dispatch Sprint D and TFT

The session will fire both Track 1 + Track 2 agents in parallel per their dispatch specs in [`specs/`](specs/).

**Gates / unblocks**: end-to-end kill-gate execution + arXiv §4 results fill-in (Track 3 finishes when Sprint D's results JSON lands) + TFT-TEC v2 path for `gannon-storm-rtk-analysis`.

---

### Step 5 — Configure PyPI trusted publishing for 3 packages (~15 min)

**Why**: After v0.x releases ship, the existing `.github/workflows/publish.yml` workflows fire on release publication and attempt PyPI publish via OIDC. Without trusted publishing configured on pypi.org, the publish step fails silently.

Repeat for each of the 3 publishable packages:

1. Go to <https://pypi.org/manage/account/publishing/>
2. Under "Add a new publisher (GitHub)", fill:
   - **Publisher**: GitHub
   - **PyPI Project Name**: `helios-provenance-spec` / `helios-fusion-engine` / `helios-spaceweather-connectors`
   - **Owner**: `577Industries`
   - **Repository name**: matches PyPI Project Name
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`
3. Click "Add".
4. Verify by tagging a v0.x.(N+1) patch on the relevant repo and watching the `publish.yml` workflow succeed, OR by re-running the latest release's workflow:
   ```bash
   gh workflow run publish.yml --repo 577Industries/<package>
   ```

**When done**: `pip install helios-provenance-spec helios-fusion-engine helios-spaceweather-connectors` succeeds; each visible at `https://pypi.org/project/<name>/`.

**Gates**: nothing operationally — packages work via `git+https://...` until then.

---

### Step 6 — Send conditional-offer letters to named hires (~2 hours total)

Per proposal §5.1, three named key personnel need conditional-intent commitments **before** the Phase II re-pitch:

- **Senior ML Engineer** (50% effort): named candidates at OSU ECE + Byrd Polar and Climate Research Center.
- **Data Engineer** (40% effort): identified through 577 Industries network; owns connectors v0.3 + PPP/RTK pipeline.
- **Space-Weather / Ionospheric Physics SME Consultant** — Byrd Polar and Climate Research Center subcontract (~250 hrs / $25K over 6 months): institutional partner named at the $225K plan; specific faculty contact named at LoC signing.

**Steps**:

1. Draft conditional-offer letter (template: "on NASA award, we'd extend at $X salary / Y% effort starting Z").
2. Send to each named candidate via email + LinkedIn.
3. Track responses in [`phase-ii/letters/README.md`](phase-ii/letters/README.md).
4. When PDFs arrive, file at `phase-ii/letters/{ml-engineer-loi.pdf, sme-consultant-loi.pdf}` and commit.

**When done**: both LoI PDFs committed under `phase-ii/letters/`.

**Gates**: Phase II proposal §5.1 evidence. Also fills in 2 author `\todo{}` placeholders in `paper/main.tex`.

---

### Step 7 — File LoIs for customer-discovery (≥4 ag-industry; ≥2 NASA-center) (~6 weeks elapsed; ~10 hours active)

Per proposal §2 Obj. 5 success criterion. These are the partnership commitments that anchor Phase II commercialization.

**Ag-industry targets** (commit interview notes to `phase-ii/customer-discovery/`):
- OSU Extension (existing contacts)
- Ohio Agricultural Research and Development Center (OARDC)
- American Farm Bureau Federation (documented Gannon impacts in their 2024 survey)
- John Deere Operations Center
- AGCO Fuse
- CNH AFS Connect

**NASA-center targets** (commit engagement notes to `phase-ii/nasa-engagement/`):
- CCMC at GSFC — validation-framework alignment + model-catalog submission
- M2M SWAO at GSFC — DONKI integration
- SRAG at JSC — ARRT-compatibility alignment
- SPoRT Center at MSFC — operational end-user transition

**Steps**:

1. Send courtesy emails with the helios-program companion URL <https://577industries.github.io/helios-program/companion/> + master plan URL. Frame: "We're building public infrastructure that fits your framework; here's how it slots in; we'd value your read on the RFC and any specific gaps."
2. Schedule 30-min discovery calls.
3. After each call, commit interview notes per the README template.
4. When LoI PDFs arrive, file at `phase-ii/letters/<name>.pdf` and commit.

**When done**: ≥4 ag-industry LoIs + ≥2 NASA-center LoIs committed under `phase-ii/letters/`. README inventories updated.

**Gates**: Phase II proposal §2 Obj. 5 success criterion + commercialization plan §6.3 OEM-integration cold open.

---

### Step 8 — Cross-post RFC-0001 to community lists (~1 hour)

RFC-0001 issue is open at <https://github.com/577Industries/helios-provenance-spec/issues/4>. Only people who visit the repo see it; broaden reach.

1. Email **SPASE info list** (<spase-info@googlegroups.com>): subject "RFC: feature-level provenance for heliophysics fusion systems". Body: 3-paragraph intro + issue URL.
2. Email **sunpy-dev** (<https://groups.google.com/g/sunpy>): similar framing — emphasize the SPASE + W3C PROV-JSON composition.
3. Email **CCMC feedback** at <ccmc-feedback@helio.gsfc.nasa.gov> (verify the right CCMC contact based on existing relationships).
4. Cross-post to LinkedIn from the 577 Industries page (or Thomas's personal account). Either repurpose `docs/blog/social/2026-05-17-linkedin.md`'s closing CTA to point at the RFC, or write a separate LinkedIn post.

**When done**: ≥3 cross-posts sent; comments accumulating on the RFC issue.

**Gates**: RFC §6 community-comment phase → informs v0.2 of the provenance schema.

---

### Step 9 — Publish Gannon retrospective blog post + schedule social (~1 hour)

Currently staged at <https://577industries.github.io/helios-program/blog/when-the-sky-stopped-the-tractors/>. Mirror to 577industries.com for the canonical outbound-marketing home.

1. Copy `docs/blog/posts/2026-05-17-when-the-sky-stopped-the-tractors.md` into 577industries.com WordPress (or whatever CMS).
2. Schedule the LinkedIn post — draft at `docs/blog/social/2026-05-17-linkedin.md`. **Preserve the inline climatological-v1 caveat**.
3. Schedule the 9-tweet Twitter/X thread — draft at `docs/blog/social/2026-05-17-twitter-thread.md`.
4. Send courtesy heads-ups to the Step 7 ag-industry contacts.

**When done**: blog post published at the canonical URL; ≥2 social posts scheduled.

**Gates**: customer-discovery interviews (Step 7) — gives them a "click here for the full story" landing page.

---

### Step 10 — (Post-DARPA evaluation) Transfer ASEMA asset to org

**Why**: `asema-feasibility-artifacts` currently lives on the personal account `577-Industries` because URL stability during DARPA evaluation is non-negotiable. Once DARPA closes its evaluation, consolidate to the org.

1. Confirm DARPA evaluation has closed (check email + DARPA portal).
2. Transfer:
   ```bash
   gh api -X POST /repos/577-Industries/asema-feasibility-artifacts/transfer -f new_owner=577Industries
   ```
3. Wait ~30s for transfer to settle:
   ```bash
   until gh api /repos/577Industries/asema-feasibility-artifacts --jq '.full_name' 2>/dev/null | grep -q 577Industries; do sleep 3; done
   ```
4. Update the org profile README at `~/577i-Projects/577Industries.github/profile/README.md`:
   - Move ASEMA section out of "personal-account caveat" framing
   - Update the link to `github.com/577Industries/asema-feasibility-artifacts`
5. Commit + push the profile update.

**When done**: `gh repo view 577Industries/asema-feasibility-artifacts` returns 200; org profile README reflects the move.

**Gates**: nothing internal — purely consolidation hygiene. The personal account becomes 100% dormant (only archived repos remain).

---

## Long arc (informational; no immediate action)

### SBIR Phase I award outcome

Whether or not Phase I lands, HELIOS continues:
- **If awarded**: Phase I work plan kicks in for 6 months (T1-T5 per master plan §3).
- **If rejected**: Phase II re-pitch uses everything in the companion document + `phase-ii/` evidence package.

### Phase II proposal

Per master plan §3.3 — 24-month effort to advance HELIOS to TRL 5-6. The Sprint C-Training results + kill-gate paper + companion document + commercialization-plan-refined become the Phase II evidence base. Scaffold lives at [`phase-ii/phase-ii-proposal-draft.md`](phase-ii/phase-ii-proposal-draft.md).

### npm rebrand for FORGE OS libs

5 forge-* libs were renamed on GitHub but npm packages still publish under `@577-industries/<name>` (lowercase, hyphenated). Future operator-driven decision: deprecate old npm names + publish new `@577industries/forge-<name>` packages, or leave the divergence alone if npm reach isn't a priority.

---

## How this file is maintained

This file is the **operator-facing single source of truth** for what needs human hands. Update statuses as items move ⏳ → ✅. The numbered order encodes dependency — Step N gates Step N+1 where noted.

Cross-references:
- Per-artifact details: [`specs/`](specs/)
- Master plan execution log: [`plan/master-plan.md`](plan/master-plan.md)
- Per-Claude-session context: [`CLAUDE.md`](CLAUDE.md)
- Public-facing companion: [`companion/companion.md`](companion/companion.md)
- Phase II evidence package: [`phase-ii/evidence-package.md`](phase-ii/evidence-package.md)
- Org profile README: <https://github.com/577Industries>
