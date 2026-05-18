# CLAUDE.md

> Working context for the **HELIOS** program. Read this first if you're a new Claude session, a developer joining the program, or a future-you returning after a context gap. The program is large enough that working without this orientation has cost real time.

---

## 0. Next-session quick-start

The HELIOS program is **Phase-II-ready** as of 2026-05-18. Four substantive tracks are open in parallel — **each gets a dedicated session** to avoid context-window pressure. **Pick one per session**; don't try to attack multiple in parallel.

| Track | Dispatch spec | Operator prereq | Why this session |
|---|---|---|---|
| **Sprint D — kill-gate execution** | [`specs/2026-05-18-Sprint-D-kill-gate-spec.md`](./specs/2026-05-18-Sprint-D-kill-gate-spec.md) | OSF pre-registration filed | Produces the headline Phase II result |
| **§2 Obj 2 — TFT for TEC forecasting** | [`specs/2026-05-18-TFT-TEC-forecasting-spec.md`](./specs/2026-05-18-TFT-TEC-forecasting-spec.md) | NASA Earthdata credentials | Second proposal objective; upgrades Gannon analysis to real-data v2 |
| **arXiv preprint draft** | [`specs/2026-05-18-arXiv-preprint-draft-spec.md`](./specs/2026-05-18-arXiv-preprint-draft-spec.md) | None (parallel-safe) | Fills §4 from Sprint D when that lands; shortens "result → submission" from weeks to days |
| **Phase II evidence assembly** | [`specs/2026-05-18-PhaseII-evidence-assembly-spec.md`](./specs/2026-05-18-PhaseII-evidence-assembly-spec.md) | None (incremental) | Curated evidence package for Phase II proposal embed |

**Recommended dispatch order** (highest leverage first; lowest blocking risk):

1. **arXiv preprint draft** (no operator prereq; parallel-safe; fillable from any Sprint D outcome)
2. **Sprint D — kill-gate execution** (once OSF is filed)
3. **§2 Obj 2 — TFT for TEC forecasting** (once Earthdata creds set)
4. **Phase II evidence assembly** (continuous — runs once initially, refresh each session)

**Current portfolio state** (also in `companion/footnotes.yaml`):

```
helios-program                  v0.2.0   public
helios-provenance-spec          v0.1.0   public   (RFC issue #4 open)
helios-spaceweather-connectors  v0.2.1   public   (6 adapters live; ISWA registry expanded)
helios-fusion-engine            v0.1.2   public   (Sprint C-Training-v2 shipped)
helios-fusion-internal          —        private  (v2 weights with HeliosTransformationRecord provenance)
gannon-storm-rtk-analysis       v0.1.0   public
```

All 5 Pages sites HTTP 200. All worktrees clean. 0 stale branches across all 6 repos.

**One-instruction onboarding** for a new session: read `## 2. GitHub identity disambiguation` below, then read the dispatch spec for the track you're working on. The master plan (`plan/master-plan.md`) and per-artifact review packs (`specs/`) are reference material — you usually don't need to re-read them.

---

## 1. What HELIOS is

**HELIOS** = Heliophysics-Enhanced Location Integrity and Operations System.

It's a calibrated, provenance-tracked decision-intelligence layer that fuses NASA and NOAA space-weather model outputs and translates them into the specific operational decisions two user communities act on:

- **NASA mission operations** — SRAG SEP all-clear revocation probability + time-to-threshold conformal intervals + ARRT-compatible dose-rate inputs
- **U.S. precision agriculture GNSS** — receiver-family-specific RTK accuracy maps with go/no-go overlays

The technical premise: HELIOS is **not a new space-weather model**. The innovation is a **model-agnostic fusion layer** (Bayesian Model Averaging + isotonic-regression reliability calibration + conformal prediction + severity-stratified validation) paired with industry-native translation modules. Every output traces to its upstream models, data feeds, and calibration history via a feature-level provenance schema.

**Funding context**: NASA SBIR Phase I, subtopic **SPWX.1.S26A** — Advanced Data-Driven Applications for Space Weather Research-to-Operations-to-Research (R2O2R). $150,000 + $6,500 TABA, 6-month period of performance. Submitted; awaiting decision. The program continues regardless of award outcome (Phase II readiness is the open-ended goal).

---

## 2. ⚠️ Critical: GitHub identity disambiguation

This is **the single most common mistake** to make on this program. Read carefully.

| Identity | Type | Where it appears | What goes here |
|---|---|---|---|
| **`577Industries`** *(no hyphen)* | **Organization** | `github.com/577Industries/*`; `gh api orgs/577Industries`; `https://577industries.github.io/*` | **All 577 SBIR public work**, including all 6 HELIOS repos, aegisgraph (DARPA ASEMA), model-router, agent-memory, tool-guardrails, and the private 577i-unified FORGE OS platform. |
| **`577-Industries`** *(with hyphen)* | **User** | `gh auth status` (the CLI's authenticated user identity); historical `github.com/577-Industries/*` URLs auto-redirect | Personal user account; a **member** of the `577Industries` org. **Never create repos here.** |

Both identities exist. The `gh` CLI is authenticated as the **user** (`577-Industries`, with hyphen), but the user has full member access to the **org** (`577Industries`, no hyphen). When creating a repo, you must explicitly target the org:

```bash
# CORRECT
gh repo create 577Industries/<name> --public --source=. --push

# WRONG (creates under user namespace; will need to be transferred)
gh repo create <name> --public --source=. --push
```

If you discover repos under the user account that should be in the org, transfer them:

```bash
gh api -X POST repos/577-Industries/<repo>/transfer -f new_owner=577Industries
```

Then update local origin remotes to point to the new org URL. Old user-account URLs auto-redirect indefinitely, but in-repo references should use the org URL going forward.

**Token scopes** on the user identity: `gist`, `read:org`, `repo`, `workflow`. No `admin:org` — so `gh api orgs/577Industries/*` calls that need org-admin will return 404. Repo-level operations on org repos work fine because the user is an org member.

**Visibility flips**: `gh repo edit --visibility public` may reject `--accept-visibility-change-consequences` on gh CLI < 2.46. Fall back to REST API:

```bash
gh api -X PATCH repos/577Industries/<repo> -f visibility=public
```

**git tag**: in this gh CLI version, `git tag -a` does **not** accept `--quiet`. Omit that flag or you'll silently fail to create the tag (and any subsequent `git push origin <tag>` will fail). If `gh release create <tag>` is run afterward, it will create the tag implicitly — so things sometimes appear to work anyway, but the local tag will be missing.

---

## 3. The six repositories

All live under `github.com/577Industries/`:

| Repo | Visibility | Latest release | Pages | Purpose |
|---|---|---|---|---|
| [`helios-program`](https://github.com/577Industries/helios-program) | public | v0.2.0 | [live](https://577industries.github.io/helios-program/) | **Meta-repo (this one)**. Master plan, proposal companion, orchestration scripts, per-artifact specs, ops guide. |
| [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) | public | v0.1.0 | [live](https://577industries.github.io/helios-provenance-spec/) | JSON Schema (draft 2020-12) for feature-level provenance in heliophysics fusion + pydantic v2 ref impl + RFC-0001. |
| [`helios-spaceweather-connectors`](https://github.com/577Industries/helios-spaceweather-connectors) | public | pre-v0.1 (foundation + DONKI merged; v0.1.0 alpha held until ≥3 adapters live) | [live](https://577industries.github.io/helios-spaceweather-connectors/) | Production-grade Python adapters for DONKI, SEP Scoreboards, NOAA SWPC, CDDIS GIMs, GOES, DSCOVR. |
| [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine) | public | v0.1.0 | [live](https://577industries.github.io/helios-fusion-engine/) | BMA + isotonic/Platt/stratified calibration + split/Mondrian conformal + CCMC-compatible metrics. Public framework. |
| `helios-fusion-internal` | **private** | none | none (private) | Trained BMA priors, isotonic calibrators, equipment transfer functions. Hybrid-IP strategy per master plan §6.6. |
| [`gannon-storm-rtk-analysis`](https://github.com/577Industries/gannon-storm-rtk-analysis) | public | v0.1.0 | [live](https://577industries.github.io/gannon-storm-rtk-analysis/) | Reproducible retrospective of the May 10-12, 2024 Gannon G5 storm. **Headline: 1,302 station-hours over 2.5 cm threshold across 25 NGS CORS stations.** v1 climatological; v2 will use full SPP via the CDDIS adapter. |

**Dependency graph**: A (provenance schema) → B (connectors) → C (fusion engine). D (Gannon) is independent for v1 but will consume B's CDDIS adapter in v2. F (private weights) receives trained artifacts from C.

---

## 4. Local conventions

| Concern | Convention |
|---|---|
| Canonical clone (umbrella) | `git clone --recurse-submodules https://github.com/577Industries/helios-program.git` — fetches the meta-repo with all 4 public HELIOS artifacts as pinned submodules under `submodules/` |
| Local checkout | `~/577i-Projects/<repo>/` for solo work on a single artifact |
| Worktrees | `~/577i-Projects/.worktrees/<repo>-<branch>/` — pre-established user pattern, directory already exists |
| License | Apache 2.0 across all public repos (`helios-fusion-internal` is proprietary) |
| Python | 3.11+/3.12 matrix in CI; develop against 3.12 |
| Lint/format | `ruff` (replaces black + flake8 + isort) — `ruff check .` and `ruff format --check .` in pre-commit and CI |
| Type check | `mypy --strict` for `src/`; `--ignore-missing-imports` permitted on third-party gaps |
| Tests | `pytest`, `pytest-cov`, hypothesis where invariants exist; ≥80% line+branch coverage gate |
| Coverage threshold | 80% for libraries; 85% for `helios-fusion-engine` (per OSF pre-reg discipline) |
| CI/CD | GitHub Actions; Python 3.11+3.12 matrix; nightly integration suite separate from PR suite |
| Release | `git tag -a vX.Y.Z` (no `--quiet`!) → `git push origin vX.Y.Z` → `gh release create` → triggers PyPI publish via trusted publishing |
| Conventional commits | `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:` — enforced by pre-commit |
| Pre-commit | ruff + mypy + conventional-commit lint + secrets scan (detect-secrets) |
| Docs | MkDocs Material; `mkdocs build --strict`; Pages via `actions/configure-pages` + `actions/deploy-pages` |

---

## 5. The master plan and the kill-gate discipline

The **master plan** is `plan/master-plan.md` (this repo). It's the source of truth for sequencing, dependencies, and decisions. **Update its execution log after every substantive session.**

The **kill-gate** for the helios-fusion-engine arXiv preprint is non-negotiable process discipline. It's pre-registered in `orchestration/osf_preregistration.template.md`:

- **H1**: fused all-clear-revocation HSS on the 3-event hold-out exceeds the best-component-model HSS by ≥15% (relative).
- **H2**: reliability-diagram slope within 0.15 of 1.0 across all three Kp severity strata.
- **Hold-out events**: 2022-01-20 (M5.5), 2023-02-17 (X2.2), 2024-05-11 (Gannon G5).
- **Decision rules**: PASS both → full arXiv paper. PASS one → ablation paper. FAIL both → no paper.

**Before any hold-out evaluation runs**:
1. Fill in the `TO_BE_FILLED` fields in `orchestration/osf_preregistration.template.md`.
2. File publicly on OSF.
3. Save the OSF URL to `orchestration/osf_preregistration.url`.
4. Tag `helios-fusion-engine` at the locked commit with `prereg-v1.0`.

The kill-gate runner (`orchestration/kill_gate.py`) currently raises `NotImplementedError` by design — it will refuse to execute without an OSF URL on file. **Do not bypass this.** Pre-registration is the credibility move; bypassing it forfeits the proposition.

---

## 6. Agent dispatch patterns

The HELIOS program is built primarily through dispatched Claude agents in parallel git worktrees. The discipline:

### Four-stage per-artifact agent pipeline

1. **Discover** — `Explore` agents (1-3 in parallel) for state-of-art research, API docs, ecosystem surveys. Provide a focused question per agent; aggregate findings in main session.
2. **Design** — `feature-dev:code-architect` or a thorough `general-purpose` agent produces a per-artifact design spec, written to `specs/YYYY-MM-DD-<artifact>-design.md` in this repo.
3. **Build** — `general-purpose` agents in parallel worktrees, one per independent task chunk per `superpowers:subagent-driven-development`. Each agent commits to `feat/vX.Y-<scope>` and does **not push** — the operator (Thomas) reviews and merges.
4. **Review** — `pr-review-toolkit:code-reviewer` or `feature-dev:code-reviewer` on the integrated branch; `coderabbit:code-review` before merge to main.

### Parallelism budget

**Cap at 5 simultaneous active worktrees.** Beyond that, the operator's review/merge becomes the bottleneck and PRs stack up unmerged.

### Review pack convention

After each agent batch returns, write a per-artifact review pack at `specs/YYYY-MM-DD-<artifact>-review-pack.md`. The pack documents:
- TL;DR + recommendation (merge / refine / reject)
- File-by-file highlights
- Open questions for the operator
- Surface-area decisions worth a human pass
- Merge readiness checklist
- Downstream impact

Review packs are public (visible on the GH Pages site under `/specs/`). They demonstrate program discipline to NASA-center reviewers — keep them honest and substantive.

---

## 7. The submitted NASA proposal

The proposal `.docx` is at `/home/twawe/577i-Projects/SBIR Working Folder/NASA/HELIOS_NASA_SBIR_PhaseI_Proposal.docx` — **locked, do not modify**. That file is the submitted version.

The public mirror is `companion/companion.md` (this repo, served at `https://577industries.github.io/helios-program/companion/`). The companion preserves the proposal structure section-by-section but adds **live citations** to public artifacts as they ship. When new artifacts land or release statuses change, update both:

1. `companion/footnotes.yaml` — machine-readable artifact registry (rebuild via `python -m orchestration.companion_sync`)
2. `companion/companion.md` — human-readable proposal mirror (update the artifact registry table manually if statuses change)

A plaintext extraction of the proposal lives at `/home/twawe/.claude/projects/-home-twawe-577i-Projects-SBIR-Working-Folder-NASA/774be7f5-a036-4889-8afe-4c087e05097c/tool-results/b0awntn99.txt` — useful for sessions that don't want to re-run `python-docx` to read the submitted version.

---

## 8. Working with this program — daily/session-startup checklist

1. **Pull the master plan**: `cat plan/master-plan.md | tail -200` — focus on the execution log to see the last session's state.
2. **Refresh footnotes**: `python -m orchestration.companion_sync` — pulls the latest gh release state across all artifacts; commit if changed.
3. **Check open PRs and CI**: `for r in helios-provenance-spec helios-spaceweather-connectors helios-fusion-engine gannon-storm-rtk-analysis; do gh pr list --repo 577Industries/$r; done`
4. **Check Pages workflow runs** if you've made docs changes: `gh run list --repo 577Industries/helios-program --workflow pages --limit 3`
5. **If picking up agent-dispatched work**: look for `feat/v0.*` branches local on `~/577i-Projects/helios-spaceweather-connectors/` etc. — agents commit but don't push, so the operator might have unreviewed work waiting.

---

## 9. Memory cross-reference

The harness's persistent memory entries at `/home/twawe/.claude/projects/-home-twawe-577i-Projects-SBIR-Working-Folder-NASA/memory/` cover much of this content from a Claude-session perspective:

- `user_profile.md` — Thomas Waweru's role and posture
- `helios-program.md` — program summary (this CLAUDE.md is the in-repo version)
- `helios-conventions.md` — local + GitHub conventions (including the org/user disambiguation)
- `feedback-autonomy-preference.md` — the user's "work without stopping for clarifying questions" directive (with the explicit limit on destructive/irreversible actions)

CLAUDE.md is the **in-repo version** that travels with the codebase; memory entries are the **cross-session inheritance**. When they disagree, the master plan and CLAUDE.md are canonical for code and process; memory is canonical for user posture and preferences.

---

## 10. If you're a new Claude session

You're entering an active program. Things that are easy to get wrong:

1. **Don't create repos under `577-Industries` (user) — always under `577Industries` (org)**. See §2.
2. **Don't bypass the kill-gate pre-registration**. Even if results look promising in informal runs, file OSF first. See §5.
3. **Don't push agent work directly — operator reviews and merges**. See §6.
4. **Don't strip the climatological-v1 disclosure** from any external citation of the Gannon 1,302-station-hours headline. The disclosure is in `gannon-storm-rtk-analysis/docs/methodology.md` and the blog post. Removing it for "marketing simplicity" invites a credibility hit when a sharp reader checks the methodology.
5. **Don't use `git tag -a --quiet`** in this gh CLI version. See §2.
6. **Don't enable GitHub Pages on `helios-fusion-internal`** — it's the IP-gated private repo.

Things that are conventional but worth confirming with the operator (Thomas) before substantive changes:

- New connector adapters: follow the DONKI pattern (`helios-spaceweather-connectors/docs/design.md`); inherit the 7 documented API quirks.
- New schema fields in `helios-provenance-spec`: ship as v0.x (still RFC); open an issue tying the change to RFC-0001 comments.
- Visual changes to Pages: keep the blue/teal palette and the sun-and-horizon logo; deviation breaks portfolio-wide consistency with aegisgraph + model-router + agent-memory + tool-guardrails.

Welcome to HELIOS. The master plan tells you what; this file tells you how.
