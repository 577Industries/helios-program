# helios-program

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![companion-check](https://github.com/577Industries/helios-program/actions/workflows/companion-check.yml/badge.svg)](https://github.com/577Industries/helios-program/actions/workflows/companion-check.yml)

> Meta-repo for **HELIOS** — 577 Industries' NASA SBIR Phase I program on calibrated space-weather decision intelligence (subtopic SPWX.1.S26A). Hosts the public proposal companion document, master plan, cross-repo orchestration scripts, and per-artifact design specs that coordinate the four HELIOS artifact repositories.

The submitted NASA SBIR Phase I proposal "HELIOS: Heliophysics-Enhanced Location Integrity and Operations System" advances a model-agnostic Bayesian-Model-Averaging fusion layer for space-weather model outputs, with two vertical slices (NASA SRAG mission-operations radiation risk and U.S. precision-agriculture GNSS). This meta-repo coordinates the public artifacts that back the proposal's claims with live, citable code.

## Contents

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

Scaffolding committed 2026-05-17; Wave 1 of agent-driven implementation in review. See [`plan/master-plan.md` § Execution Log](./plan/master-plan.md#execution-log) for current state.

## License

Apache 2.0 — see [LICENSE](./LICENSE). Document content (companion, plan, specs, ops) is provided for reference and citation; please attribute 577 Industries Inc. when quoting.

## Contact

Engineering: <engineering@577industries.com>
Principal Investigator: Thomas Waweru, 577 Industries Inc., Columbus OH
