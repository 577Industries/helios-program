# HELIOS Artifact Buildout — Program Master Plan

## Context

577 Industries' NASA SBIR Phase I proposal "HELIOS: Heliophysics-Enhanced Location Integrity and Operations System" (`/home/twawe/577i-Projects/SBIR Working Folder/NASA/HELIOS_NASA_SBIR_PhaseI_Proposal.docx`) is submitted. The proposal advances a five-objective work plan around a model-agnostic Bayesian-Model-Averaging fusion engine for space-weather model outputs, with two vertical slices: NASA SRAG mission-operations radiation risk and U.S. precision-agriculture GNSS.

The goal of this plan is to convert four of the proposal's strongest claims from paper into citable, deployable, public artifacts:

1. **`helios-spaceweather-connectors`** — Python package + GitHub (Objective 1)
2. **`helios-fusion-engine`** (public framework) + private companion + arXiv preprint (Objective 2 + §3.1 pre-registration)
3. **`gannon-storm-rtk-analysis`** — repo + blog post (§1.3 marquee event + Objective 4 feasibility)
4. **`helios-provenance-spec`** — JSON Schema RFC + reference implementation (§1.4 CONOPS + §4.2 innovation #2)

Each artifact converts a paper claim into a URL reviewers and stakeholders can kick the tires on. They feed a **proposal companion document** maintained in parallel — a public-facing mirror of the submitted proposal with live citations — which becomes Phase II re-pitch material, NASA-center engagement collateral (CCMC, M2M SWAO, SRAG, SPoRT), and the 577industries.com/helios landing page.

Submission has happened; timeline is open-ended. The plan optimizes for **quality and Phase II readiness**, not deadline pressure.

## Decisions Locked

| Decision | Choice | Why it matters |
|---|---|---|
| Timeline | Open-ended, Phase II-oriented | Permits sequential quality gates over parallel speed-runs where the dependency requires it |
| Fusion-engine IP scope | **Hybrid**: public framework, private weights/configs | Matches §6.6 IP strategy; companion private repo `helios-fusion-internal` holds trained weights, BMA priors, equipment transfer functions |
| Execution team | Solo founder (Thomas) + heavy Claude agent delegation | Aggressive parallel agent dispatch across 4 worktrees; you on review/merge/secrets |
| Paper kill-gate | **§2 Obj. 3 criterion (pre-registered)**: fused all-clear-revocation HSS beats best-component-model HSS by ≥15% on 3-event hold-out (2022-01-20 M5.5, 2023-02-17 X2.2, 2024-05-11 Gannon G5) AND reliability slope within 0.15 across all Kp severity strata | Both must pass → full arXiv paper. One fails → honest-negative-result ablation paper (still valuable). Both fail → no paper, fusion engine ships without preprint citation |
| GitHub home | `github.com/577-Industries/` (already authenticated via `gh`) | Matches existing org access; sibling to agent-memory, hashchain-audit, etc. |
| License | Apache 2.0 across all public repos | Preserves patent grant for SBIR data-rights compatibility; broader than MIT for SaaS/OEM downstreams |
| Python baseline | 3.11+ (3.12 preferred) | Pattern matching, exception groups, modern typing |

## Defaults applied (flag any to revise)

- **Local checkout convention**: `~/577i-Projects/<repo>/` matching existing sibling repos (`agent-memory`, `hashchain-audit`, `model-router`, `tool-guardrails`, `workflow-dag`).
- **Worktree convention**: `~/577i-Projects/.worktrees/<repo>-<branch>/` matching the directory you already maintain at `~/577i-Projects/.worktrees/`.
- **Meta-repo**: `~/577i-Projects/helios-program/` (private, on GitHub) holds the proposal companion document source, cross-repo orchestration scripts, the master plan tracker, kill-gate evaluation runner, and per-artifact design specs as they're created.
- **CITATION**: every public repo ships `CITATION.cff` so academic citers don't have to invent one.
- **PyPI**: `helios-spaceweather-connectors`, `helios-fusion-engine`, `helios-provenance` namespace; `helios-fusion-internal` is wheel-only via internal index, never PyPI.
- **DOI**: each public release tagged on GitHub auto-mints a Zenodo DOI (free, accepts arbitrary GitHub repos).

## Scope and Decomposition

The work splits into **one program-level orchestration layer** (this plan, plus the meta-repo `helios-program`) and **five independent execution streams**:

| Stream | Artifact | Public? | Eff. weeks | Critical-path? |
|---|---|---|---|---|
| A | `helios-provenance-spec` | Yes (RFC + ref impl) | 2 | **Yes** — unblocks B's schema |
| B | `helios-spaceweather-connectors` | Yes | 4 | **Yes** — unblocks C's data |
| C | `helios-fusion-engine` (public framework) + `helios-fusion-internal` (private) + arXiv preprint | Hybrid | 8-10 | Yes — paper depends on C |
| D | `gannon-storm-rtk-analysis` | Yes | 3 | No — runs parallel from week 1 (CORS data is public and independent) |
| E | Proposal companion document | Yes (web + PDF) | Continuous | No — updates as A-D ship |

Each stream **gets its own per-artifact brainstorm → spec → plan → execute cycle** as a follow-up once this master plan is approved. This plan does NOT design the internals of each artifact — it sets up the program-level orchestration, conventions, dependency graph, and quality gates that all four streams will inherit.

## Dependency Graph

```
Week:   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
A (spec):       [══ v0.1 RFC ══][refine─►v1.0]
B (conn):    [══ v0.1 ══][══ v0.2 ══][══ v1.0 ══]
                ▲ uses A v0.1 schema
C (fuse):           [skeleton][train Table 3-1][hold-out][kill-gate│paper]
                       ▲ uses B v0.2 data flow                      │
                       └─uses A schema for output provenance        ▼
D (Gannon):  [══ data pull ══][analysis][blog post + repo]
                ▲ uses B's CORS adapter (or builds its own thin fetcher)
E (companion):  [───────── updated weekly ─────────►][publish v1.0 web]
```

**Hard ordering**:
1. A v0.1 RFC schema must exist before B v0.1 final commits (B uses A's `ProvenanceRecord` type).
2. B v0.2 (at least DONKI, SWPC, GOES, Scoreboard A) must be importable before C trains on Table 3-1 events.
3. C kill-gate evaluation runs on the 3-event hold-out **after** Table 3-1 training is locked.
4. Paper write-up only proceeds if kill-gate passes; otherwise pivot to ablation paper or no paper.

**Soft ordering**:
- D can start week 1 (CORS RINEX is public via NGS, no auth needed).
- E updates continuously as A-D ship public URLs.

## Per-Artifact Briefs

### A — `helios-provenance-spec`

**What**: JSON Schema (draft 2020-12) describing how every HELIOS output traces back through fusion to upstream models, plus a Python reference implementation (`pydantic` v2 models that emit/validate provenance records). Issued as an open RFC on GitHub for community comment.

**Architecture (per Phase 1 survey)**: Adopt **SPASE 2.7.1** (heliophysics dataset metadata, spase-group.org) + **W3C PROV-JSON** (feature-level lineage relations: `wasGeneratedBy`, `used`, `wasDerivedFrom`) + **RO-Crate 1.2 JSON-LD** packaging. Novel contribution: a **feature-level transformation chain** record format binding upstream model output values → calibration parameters → fused output value, with confidence-interval provenance. No existing heliophysics project does feature-level lineage today.

**Repo layout**:
```
helios-provenance-spec/
├── schema/
│   ├── helios-provenance-v0.1.json        # JSON Schema 2020-12
│   ├── examples/                          # validated example records
│   └── crosswalks/                        # to SPASE / RO-Crate
├── ref-impl/                              # Python pydantic v2 models
│   └── helios_provenance/
├── docs/                                  # MkDocs site → readthedocs
├── rfc/
│   └── RFC-0001-feature-lineage.md        # community-comment doc
└── tests/
```

**Quality gates (citable when met)**: schema validates ≥10 example records covering each upstream source; pydantic ref impl has ≥95% test coverage; MkDocs site live; RFC issue open and circulated to CCMC/SPASE-list/sunpy-dev; tagged v0.1.0; Zenodo DOI minted.

**Citation in companion doc**: §1.4 (CONOPS provenance affordance) + §4.2 innovation #2 + every other artifact's `ProvenanceRecord` type imports from here.

### B — `helios-spaceweather-connectors`

**What**: Production-grade Python adapters for 6 space-weather data sources, normalized to a common feature schema with feature-level provenance tracking per spec A. Direct fulfilment of Objective 1 in the proposal.

**Architecture (per Phase 1 survey)**: 3 BUILD, 1 EXTEND, 2 WRAP.

| Source | Strategy | Notes |
|---|---|---|
| NASA DONKI | BUILD | nasapy dormant; implement full CME/flare/SEP/HSS/IPS/MPC/GST/RBE coverage with intelligent linkages |
| CCMC SEP Scoreboards A/B/C | BUILD | No read client exists; respect CCMC rate limits per §3 T1 |
| NOAA SWPC | EXTEND | SunPy covers indices; HELIOS adds plasma/mag/SEP forecast JSON endpoints |
| CDDIS GIMs (IONEX) | BUILD | Earthdata auth + IONEX parsing + parquet cache |
| GOES X-ray/proton | WRAP | Thin adapter over PySPEDAS + SWPC near-real-time JSON |
| DSCOVR | WRAP | Thin adapter over PySPEDAS + real-time JSON |

**Excluded**: HESPERIA REleASE (commercial licensing per §3 T1, ref [30]). UMASEP, SEPMOD, MagPy individual model outputs come through SEP Scoreboards, not direct.

**Repo layout**:
```
helios-spaceweather-connectors/
├── src/helios_connectors/
│   ├── adapters/                          # one module per source
│   ├── schema.py                          # imports ProvenanceRecord from helios-provenance
│   ├── cache.py                           # parquet on disk
│   └── ratelimit.py
├── tests/
├── examples/                              # one Jupyter notebook per adapter + a fusion-input recipe
└── docs/
```

**Quality gates**: all 6 adapters importable; each has ≥1 example notebook running end-to-end in CI; integration test against live endpoints in nightly CI (separated from unit tests so they don't break PR signal); ≥80% line coverage; PyPI published; tagged v0.1.0; README badges (CI/PyPI/coverage/license/DOI); rate-limit handling documented; provenance records emit for every fetched data point.

**Citation in companion doc**: §2 Objective 1; §3 T1 ingestion pipeline; every NASA-center engagement deck.

### C — `helios-fusion-engine` (public) + `helios-fusion-internal` (private) + arXiv preprint

**What — public**: BMA orchestrator, isotonic-regression reliability calibrator, conformal-prediction wrappers, severity-stratified validation harness, CCMC-compatible metrics suite (HSS, TSS, POD, FAR, Brier, CRPS). Framework only — no trained weights, no production BMA priors, no equipment transfer functions.

**What — private**: trained weights, BMA priors fitted on Table 3-1 training events, equipment transfer functions for StarFire/Trimble/AgLeader (slated for Phase II refinement). Kept in `helios-fusion-internal` private repo, hosted on internal PyPI mirror or direct git install.

**What — arXiv preprint**: retrospective results on Table 3-1's 7 training events + 3 hold-out events, with pre-registration filed on OSF (Open Science Framework) **before** hold-out evaluation runs. Target venue: **astro-ph.SR** (heliophysics) with **cs.LG** cross-list.

**Kill-gate (pre-registered, do not retune)**:
- Fused HSS on 3-event hold-out > best-component-model HSS × 1.15 (i.e., ≥15% relative improvement, matching proposal §2 Obj. 3 success criterion).
- Reliability-diagram slope within 0.15 of 1.0 across all three Kp severity strata (quiet / moderate / extreme).
- If both pass → full paper (~12 pages, 8 figures).
- If one passes → ablation paper with honest negative result on the failing dimension (still valuable; demonstrates pre-registration discipline).
- If both fail → no paper; ship framework with notebook showing the negative result; cite "calibration achieved on training set; hold-out improvement did not meet pre-registered threshold."

**Repo layout (public)**:
```
helios-fusion-engine/
├── src/helios_fusion/
│   ├── bma/                               # Bayesian model averaging orchestrator
│   ├── calibration/                       # isotonic + Platt (rejected, kept for comparison)
│   ├── conformal/                         # split conformal + Mondrian (severity-stratified)
│   ├── eval/                              # HSS, TSS, POD, FAR, Brier, CRPS + bootstrap CIs
│   └── stratification/                    # Kp-bin severity-stratified validation
├── tests/                                 # synthetic data tests; integration tests use fixtures
├── paper/                                 # arXiv preprint LaTeX source + figures notebook
├── notebooks/
│   └── reproducibility.ipynb              # full Table 3-1 retrospective from public sources
└── docs/
```

**Quality gates (framework)**: ≥85% coverage on core fusion code; benchmark notebook runs reproducibly from public data (via helios-spaceweather-connectors); PyPI published; v0.1.0 tagged; Zenodo DOI; docs site.

**Quality gates (paper)**: pre-registration on OSF (with timestamp) BEFORE hold-out runs; bootstrapped 95% CIs on all metrics; reliability diagrams in supplement; figures reproducible from notebook; arXiv submitted to astro-ph.SR + cs.LG; preprint URL added to companion doc §2 Obj. 2.

**Citation in companion doc**: §2 Objective 2 + §3.1 pre-registered validation + §4.2 innovation #1 (model-agnostic decision-calibrated fusion).

### D — `gannon-storm-rtk-analysis`

**What**: Pull NGS CORS RINEX for Iowa/Illinois/Indiana/Ohio stations covering May 9-13, 2024 (Gannon G5 storm 3-day window). Compute positioning solutions and 2D error envelopes per region. Correlate with SWPC indices (Kp, Dst, NOAA proton flux). Output: GitHub repo with reproducible notebook + blog post on 577industries.com + Twitter/LinkedIn thread with CTAs to the companion document.

**Why this matters**: §1.3 of the proposal is the strongest customer-discovery hook (the Gannon anecdote). Today it's a story; this artifact makes it a citable result with code, data, and a 2D error map a row-crop operator can recognize. It demonstrates the equipment-transfer-function concept on real data, without depending on the full fusion engine.

**Method (v1)**: PPP positioning via RTKLIB or gnss-pylib; 2D horizontal error vs. time, per station, color-coded by Kp severity. Equipment transfer function v0 is climatological/empirical — full receiver-family-specific functions come in Phase II.

**Repo layout**:
```
gannon-storm-rtk-analysis/
├── data/                                  # .gitignore'd; pulled via fetch.py
├── src/
│   └── analysis.py
├── notebooks/
│   ├── 01-fetch-cors.ipynb
│   ├── 02-positioning-solutions.ipynb
│   └── 03-correlate-swpc.ipynb
├── results/                               # figures, error CSVs committed
├── blog-post/                             # markdown source for 577industries.com
└── README.md                              # links to blog + key result figure
```

**Quality gates**: notebook reproducible end-to-end via `make all`; every figure has data + method + timestamp footer; blog post published on 577industries.com; LinkedIn + Twitter posts scheduled with CTA to companion doc; data manifest with NGS CORS station IDs + dates.

**Citation in companion doc**: §1.3 Gannon case study + §2 Objective 4 GNSS slice + §4.2 innovation #4 (equipment-aware GNSS prediction, foreshadowed by transfer-function approach in v1).

### E — Proposal Companion Document (`helios-program/companion/`)

**What**: A public-facing markdown mirror of the submitted proposal, rendered to PDF via pandoc and to web via GitHub Pages or Cloudflare Pages. Identical section structure; every claim that maps to a live artifact gets a URL footnote linking to repo/notebook/preprint/blog.

**Purpose audiences**:
1. **Phase II re-pitch reviewers** (assume rejection of Phase I or routine Phase II application — strongest single piece of evidence)
2. **NASA-center engagement decks**: CCMC validation discussions, M2M SWAO meetings, SRAG ALARA-framework alignment, SPoRT R2O2R conversations
3. **Customer-discovery pre-reads**: OSU Extension intros, OARDC, OEM platform teams (Deere, AGCO, CNH)
4. **Public web presence**: 577industries.com/helios landing page; LinkedIn/Twitter announcement engine

**Repo layout** (in `helios-program/`):
```
helios-program/
├── companion/
│   ├── companion.md                       # source — mirrors proposal sections 1-8
│   ├── footnotes.yaml                     # artifact URL registry, autoincluded
│   ├── render.py                          # pandoc-based PDF + HTML generation
│   └── assets/
├── orchestration/
│   ├── kill_gate.py                       # runs the pre-registered HSS+reliability check
│   ├── schema_diff.py                     # detects A v0.1 → v0.2 breaking changes for B and C
│   └── companion_sync.py                  # rebuilds footnotes from artifact READMEs
├── specs/                                 # per-artifact design docs from follow-up brainstorm cycles
│   ├── 2026-MM-DD-provenance-spec-design.md
│   ├── 2026-MM-DD-connectors-design.md
│   ├── 2026-MM-DD-fusion-engine-design.md
│   └── 2026-MM-DD-gannon-analysis-design.md
└── plan/
    └── master-plan.md                     # this document, mirrored from ~/.claude/plans/
```

**Quality gates**: companion.md updates on every artifact merge to main (via GitHub Action triggered by repository_dispatch from artifact repos); PDF auto-publishes to GitHub Pages; mobile-readable web view; SEO-clean (Open Graph tags so LinkedIn previews render); every URL footnote works (link-checker CI).

## Shared Repository Conventions

Applied identically to all 4 public artifacts (A, B, C-public, D):

| Concern | Convention |
|---|---|
| Layout | PEP-621 `pyproject.toml`, `src/<package>/` layout |
| Python | 3.11+ (3.12 preferred), full typing with strict `mypy` |
| Lint/format | `ruff` (replaces black + flake8 + isort + most pylint), `ruff check` and `ruff format` in pre-commit and CI |
| Type check | `mypy --strict` for `src/`; `--ignore-missing-imports` permitted on third-party gaps |
| Tests | `pytest`, `pytest-cov`, hypothesis where invariants exist; ≥80% line coverage gate in CI |
| CI/CD | GitHub Actions; matrix on 3.11 + 3.12; nightly integration suite separate from PR suite |
| Release | Trusted publishing to PyPI on tagged release; auto Zenodo DOI mint |
| Docs | MkDocs (Material theme), readthedocs hosting, autoref to docstrings |
| License | Apache 2.0 with NOTICE file |
| Versioning | SemVer; v0.x while pre-stable; pre-1.0 reserved until A v1.0 RFC closes |
| Pre-commit | ruff, mypy, conventional-commit lint, secrets scan (`detect-secrets`) |
| Security | `pip-audit` + `safety` in CI; GitHub Dependabot enabled |
| Code review | `pr-review-toolkit:review-pr` agent runs on every PR; `coderabbit:code-review` for major merges |
| Citation | `CITATION.cff` per repo |
| Community | `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` (lightweight; "open an issue first for substantive changes") |
| Badges | CI, PyPI version, coverage, license, DOI, "made with Claude Code" optional |

## Worktree Topology and Agent Dispatch Model

**Directory layout**:
```
~/577i-Projects/
├── helios-program/                        # meta-repo (private GitHub)
├── helios-provenance-spec/                # public GitHub repo
├── helios-spaceweather-connectors/        # public GitHub repo
├── helios-fusion-engine/                  # public GitHub repo
├── helios-fusion-internal/                # private GitHub repo
├── gannon-storm-rtk-analysis/             # public GitHub repo
└── .worktrees/                            # existing convention
    ├── helios-provenance-spec-<branch>/
    ├── helios-connectors-<branch>/
    └── ...
```

**Per-artifact agent pipeline** (run by you-as-conductor from main session):

1. **Discover** — dispatch 1-3 `Explore` agents in parallel for state-of-art + API docs + library-survey questions
2. **Design** — dispatch one `feature-dev:code-architect` agent against a fresh worktree to produce per-artifact design spec; spec lands at `helios-program/specs/YYYY-MM-DD-<artifact>-design.md`
3. **Build** — decompose design into independent task chunks via `superpowers:writing-plans`; dispatch `general-purpose` agents in **parallel worktrees** for each chunk per `superpowers:subagent-driven-development`
4. **Review** — `pr-review-toolkit:code-reviewer` or `feature-dev:code-reviewer` against the integrated branch; `coderabbit:code-review` before merge to main

**Cross-artifact orchestration** (run from main session in `helios-program`):
- Weekly: pull artifact READMEs, regenerate companion footnotes, push to gh-pages
- On provenance-spec breaking change: dispatch a `general-purpose` agent in connectors + fusion-engine worktrees to update consumers; surface as a PR
- On B v0.2 merge: dispatch fusion-engine agent to wire connector data into eval harness
- On kill-gate evaluation day: I (Claude in main session) run `orchestration/kill_gate.py`, render result, decide paper branch

**Parallelism budget**: with solo + heavy Claude delegation, target 3-5 simultaneous worktrees active at any time. More than 5 → context-switching cost on review exceeds parallelism gains.

## Critical Files To Be Created

| Path | Purpose |
|---|---|
| `~/577i-Projects/helios-program/` (NEW repo) | Meta-repo: companion doc source, orchestration scripts, master plan, per-artifact specs |
| `~/577i-Projects/helios-provenance-spec/` (NEW repo) | Public RFC + ref impl |
| `~/577i-Projects/helios-spaceweather-connectors/` (NEW repo) | Public Python package |
| `~/577i-Projects/helios-fusion-engine/` (NEW repo) | Public fusion framework |
| `~/577i-Projects/helios-fusion-internal/` (NEW PRIVATE repo) | Trained weights, BMA priors, eq transfer functions |
| `~/577i-Projects/gannon-storm-rtk-analysis/` (NEW repo) | Public analysis + blog |
| `~/577i-Projects/helios-program/companion/companion.md` | Public-facing proposal mirror |
| `~/577i-Projects/helios-program/specs/` (4 files) | Per-artifact design specs from follow-up brainstorms |

Nothing in `/home/twawe/577i-Projects/SBIR Working Folder/NASA/` is modified by this plan. The submitted proposal `.docx` stays as-is; the companion document is the public live mirror.

## Verification & Quality Gates

**Per-artifact "citable"-readiness checklist** (all must be true before companion doc cites the artifact URL):

- [ ] CI green on main (lint + type + test + coverage gate)
- [ ] README with badges and ≥1 working quick-start example
- [ ] LICENSE (Apache 2.0) + NOTICE + CITATION.cff
- [ ] Tagged v0.1.0 release
- [ ] For Python packages: published to PyPI
- [ ] DOI minted via Zenodo
- [ ] For A: RFC issue open and circulated to SPASE-list + sunpy-dev + ccmc-feedback
- [ ] For C-paper: pre-registration timestamped on OSF before hold-out evaluation runs
- [ ] For D: blog post published; social posts scheduled

**Program-level end-to-end verification**:
1. `git clone` any of the 4 public repos into a fresh container; `pip install -e .`; `pytest` passes
2. Run the connectors example notebook → produces normalized records → validates against helios-provenance-spec schema
3. Run the fusion engine reproducibility notebook → recovers headline retrospective numbers from Table 3-1 events ±5%
4. Open companion doc on web → every artifact footnote URL returns 200 + repo readme renders
5. `gh pr view` shows the pr-review-toolkit + coderabbit reviews ran on each merge

**Kill-gate verification** (specific to C-paper):
- Pre-registration on OSF includes: exact HSS formula, severity-strata definitions, hold-out event list, bootstrap protocol — frozen before hold-out runs
- `helios-program/orchestration/kill_gate.py` executes once, prints PASS/FAIL with all metrics, commits result to `helios-program/results/YYYY-MM-DD-killgate.json`

## Risks Specific to the Program-Level Plan

(Per-artifact risks belong in each artifact's own design spec; these are the cross-cutting ones.)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Provenance spec churns mid-build, breaks connectors and fusion engine repeatedly | Medium | High | A ships v0.1 as **RFC, not stable**; consumers pin to a specific v0.x; breaking changes ship as v0.(N+1) with a documented migration; `schema_diff.py` flags incompatible changes pre-merge |
| Fusion-engine kill-gate fails on hold-out; user emotional pressure to rerun | Low (process-mitigated) | High to credibility | Pre-registration on OSF makes "retune" detectable; ablation-paper branch is pre-defined so failure has a graceful exit |
| Agent dispatch fan-out exceeds review capacity; PRs stack up unmerged | Medium | Medium | Cap simultaneous active worktrees at 5; weekly merge-day; small focused PRs over large omnibus PRs |
| CCMC rate-limiting trips during nightly integration tests, looks like outage in CI | Medium | Low | Integration suite uses recorded fixtures by default; live-endpoint job runs once daily with backoff |
| Companion doc drifts from artifact reality | Medium | Medium | `companion_sync.py` rebuilds footnotes from artifact READMEs on every artifact merge; link-checker CI on companion repo |
| Phase II review timing forces premature artifact citations | Low (open-ended timeline) | Medium | Companion supports per-artifact `status: rfc | in-development | stable` field; status renders next to URL so reviewers know maturity |
| `helios-fusion-internal` private repo secrets leak into public framework | Low | High | `.gitignore` of weights/configs paths is duplicated in `pre-commit` hook with `detect-secrets`; CI fails on any `.npy`/`.pkl` in public repo |

## What Happens Immediately After This Plan Is Approved

1. **Initialize `helios-program` meta-repo** locally and on GitHub (private). Commit this plan to `helios-program/plan/master-plan.md`.
2. **Bootstrap the 5 GitHub repos** (4 public + 1 private) with shared scaffolding: `pyproject.toml`, GH Actions templates, pre-commit, LICENSE, CITATION.cff, MkDocs skeleton, README placeholder.
3. **Brainstorm + spec Artifact A** (`helios-provenance-spec`) first using `superpowers:brainstorming` → spec → `superpowers:writing-plans` → `superpowers:subagent-driven-development`. Ship v0.1 RFC.
4. **Start Artifact D** (`gannon-storm-rtk-analysis`) in parallel — independent of A and B; brainstorm-spec-build cycle.
5. As A v0.1 lands: **start Artifact B** brainstorm-spec-build. Connectors phase first wave (DONKI, SWPC, GOES, DSCOVR, Scoreboard A).
6. As B v0.2 lands: **start Artifact C** brainstorm-spec-build. Fusion engine framework first, then training on Table 3-1, then hold-out, then kill-gate, then paper-or-ablation.
7. Continuous: companion document updated weekly; LinkedIn/Twitter announcements as each artifact's v0.1.0 ships.

Each of those follow-up cycles is its own brainstorm → spec → plan → execute sequence with its own user-approval gate. This master plan only orchestrates the program.
