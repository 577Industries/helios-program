# helios-program

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![companion-check](https://github.com/577Industries/helios-program/actions/workflows/companion-check.yml/badge.svg)](https://github.com/577Industries/helios-program/actions/workflows/companion-check.yml)

> Meta-repo for **HELIOS** — 577 Industries' NASA SBIR Phase I program on calibrated space-weather decision intelligence (subtopic SPWX.1.S26A). Hosts the public proposal companion document, master plan, cross-repo orchestration scripts, and per-artifact design specs that coordinate the four HELIOS artifact repositories.

The submitted NASA SBIR Phase I proposal "HELIOS: Heliophysics-Enhanced Location Integrity and Operations System" advances a model-agnostic Bayesian-Model-Averaging fusion layer for space-weather model outputs, with two vertical slices (NASA SRAG mission-operations radiation risk and U.S. precision-agriculture GNSS). This meta-repo coordinates the public artifacts that back the proposal's claims with live, citable code.

## For NASA SBIR Reviewers (5-minute onramp)

This repository orchestrates the public artifact ecosystem for the HELIOS NASA SBIR Phase I proposal (subtopic SPWX.1.S26A). To verify proposal claims:

1. **Start with [`companion/companion.md`](companion/companion.md)** — the canonical index that maps every proposal section (§1.3 Gannon case study, §3 technical objectives, §4 work plan, etc.) to specific files in the public artifact repos.
2. **Pre-registration**: see [`orchestration/kill_gate.py`](orchestration/kill_gate.py) for the kill-gate constants and [`plan/master-plan.md`](plan/master-plan.md) for the sealed hold-out event list (Table 4-2 in the proposal).
3. **Empirical evidence**: see [`gannon-storm-rtk-analysis`](https://github.com/577Industries/gannon-storm-rtk-analysis) for the 25-station NGS CORS analysis (1,302 station-hours headline; `results/quantitative.md`).
4. **Framework code**: [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine) (BMA + isotonic + Mondrian conformal) and [`helios-spaceweather-connectors`](https://github.com/577Industries/helios-spaceweather-connectors) (6 data adapters).
5. **Provenance schema**: [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) (feature-level lineage JSON Schema).

Trained model weights, BMA priors, and equipment transfer functions are held in the private `helios-fusion-internal` repo (commercial-license gated); the framework code is fully open.

## Quick start

```bash
git clone --recurse-submodules https://github.com/577Industries/helios-program.git
```

This umbrella repo bundles the 4 public HELIOS artifacts as git submodules pinned at their latest release tags (see [`submodules/`](./submodules/)). Each submodule is independently usable from its own repo URL.

## Contents

- [`submodules/`](./submodules/) — the 4 public HELIOS artifact repos pinned at release tags:
  - [`helios-provenance-spec`](./submodules/helios-provenance-spec/) @ `v0.1.0`
  - [`helios-spaceweather-connectors`](./submodules/helios-spaceweather-connectors/) @ `v0.2.1`
  - [`helios-fusion-engine`](./submodules/helios-fusion-engine/) @ `v0.2.0`
  - [`gannon-storm-rtk-analysis`](./submodules/gannon-storm-rtk-analysis/) @ `v0.1.0`
- [`companion/`](./companion/) — public-facing companion document mirroring the submitted proposal with live artifact citations; rebuilt automatically from upstream release state via `orchestration/companion_sync.py`. **Read this first** if you're a reviewer or stakeholder.
- [`plan/master-plan.md`](./plan/master-plan.md) — program-level master plan, including the dependency graph across artifacts, the pre-registered kill-gate for the fusion-engine arXiv preprint, and the rolling execution log.
- [`specs/`](./specs/) — per-artifact design specs from each follow-up brainstorm cycle, plus operator-facing review packs for completed agent work.
- [`orchestration/`](./orchestration/) — cross-repo automation: `companion_sync.py` rebuilds the artifact registry from GitHub release state; `kill_gate.py` executes the pre-registered HSS + reliability-slope evaluation on the 3-event hold-out; `osf_preregistration.template.md` is the binding text to file on the Open Science Framework before any hold-out evaluation runs.
- [`docs/operations.md`](./docs/operations.md) — operator runbook: where everything lives, daily checklist, agent dispatch conventions, known gotchas.
- [`results/`](./results/) — kill-gate evaluation results, validation runs.
- [`.github/workflows/`](./.github/workflows/) — CI: yamllint, footnotes-sync check, lychee link-check on the companion document.

## Artifact repositories

| Artifact | Repo | Status |
|---|---|---|
| Provenance schema (JSON Schema 2020-12 + pydantic ref impl + RFC) | [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) | public |
| Space-weather data adapters (DONKI, SEP Scoreboards, NOAA SWPC, CDDIS GIMs, GOES, DSCOVR) | [`helios-spaceweather-connectors`](https://github.com/577Industries/helios-spaceweather-connectors) | public |
| Fusion engine (BMA + isotonic + conformal + severity-stratified validation) | [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine) | public |
| Trained weights, BMA priors, equipment transfer functions | `helios-fusion-internal` | private (IP) |
| May 2024 Gannon storm retrospective on NGS CORS data | [`gannon-storm-rtk-analysis`](https://github.com/577Industries/gannon-storm-rtk-analysis) | public |

## Reading order for first-time visitors

1. [`companion/companion.md`](./companion/companion.md) — what HELIOS is and where the supporting evidence lives
2. [`plan/master-plan.md`](./plan/master-plan.md) — how the program is structured and what gates each artifact passes
3. Whichever artifact repo above matches your interest

## Status

**Phase-II-ready** (2026-05-18). All 4 public HELIOS artifacts have shipped initial releases and are bundled here as submodules. Phase II evidence assembly lives at [`phase-ii/`](./phase-ii/). Four dispatch-ready specs in [`specs/`](./specs/) cover Sprint D kill-gate, TFT-TEC forecasting, the arXiv preprint, and Phase II evidence refresh. See [`plan/master-plan.md` § Execution Log](./plan/master-plan.md#execution-log) for the rolling state.

## License

Apache 2.0 — see [LICENSE](./LICENSE). Document content (companion, plan, specs, ops) is provided for reference and citation; please attribute 577 Industries Inc. when quoting.

## Contact

Engineering: <engineering@577industries.com>
Principal Investigator: Thomas Waweru, 577 Industries Inc., Columbus OH
