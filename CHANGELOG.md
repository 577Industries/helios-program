# Changelog

All notable changes to the HELIOS program meta-repo are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository is documents-first; the version reflects milestone polish or structural shifts in the program-level orchestration, not code releases of the artifact repos (those have their own CHANGELOGs).

## [Unreleased]

### Added
- `CHANGELOG.md` (this file) — back-filled to v0.1.0 from `gh release` history.

## [0.2.0] — 2026-05-17 — Visual polish

### Added
- **Custom MkDocs landing page** with hero (1,302-station-hours headline + climatological-v1 caveat preserved), 4 artifact status cards, 4-up stats strip, Mermaid dependency graph.
- **Custom sun-themed SVG logo + favicon** at `docs/assets/{logo,favicon}.svg` (deployed across all 5 HELIOS Pages sites for portfolio-wide visual consistency).
- **Custom CSS** at `docs/stylesheets/extra.css` covering hero, artifact-card grid, stats strip, dependency-graph section, dark-mode adjustments, print overrides.
- **MkDocs blog plugin** enabled at `docs/blog/` with the first post — the Gannon storm retrospective — and social-post drafts (LinkedIn long-form, 9-tweet thread).
- **New plugins**: `mkdocs-git-revision-date-localized-plugin` (Last-updated stamps), `mkdocs-include-markdown-plugin` (canonical content stays in `companion/`, `plan/`, `specs/` without build-time `cp`), `mkdocs-glightbox` (image lightboxes).
- **CLAUDE.md** at repo root — in-repo working context for future Claude sessions and developer onboarding (the org/user disambiguation, kill-gate discipline, agent dispatch patterns, daily checklist).
- **`.github/workflows/companion-check.yml`** earlier this session — yamllint + footnotes-sync check + lychee link-check.
- Shared meta-file templates at `templates/` (SECURITY.md, CHANGELOG.md.template, .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/{bug,feature}.md, .github/FUNDING.yml) distributed to all 4 public artifact repos.

### Changed
- **Palette refresh**: `deep_purple/amber` → `blue/teal` (better dark-mode contrast; signals "credible engineering" register for the NASA-center + precision-ag audience).
- **Fonts**: Material defaults → Inter (text) + JetBrains Mono (code).
- **Nav restructure**: Home is now the custom landing; Proposal Companion is a dedicated page; Blog added.
- **Workflow refactored**: `.github/workflows/pages.yml` dropped the 9-line `cp` aggregation step in favor of `mkdocs-include-markdown-plugin` directives in `docs/*.md` files. Only `companion/footnotes.yaml` is still copied (referenced as a relative download link in companion.md).
- **`companion/footnotes.yaml`** PyPI URL corrected: `helios-provenance` → `helios-provenance-spec` (the actual package name).

### Fixed
- Master plan `Decisions Locked` table updated to reflect the post-migration `577Industries` org URL (was the historical `577-Industries` user URL).

## [0.1.0] — 2026-05-17 — Initial pages publication

### Added
- Initial Pages publication at <https://577industries.github.io/helios-program/> via MkDocs Material with `actions/configure-pages` + `actions/deploy-pages` (workflow-source deployment, not branch-source Jekyll).
- Master plan committed to `plan/master-plan.md`.
- Proposal companion document at `companion/companion.md` mirroring the submitted NASA SBIR Phase I proposal with live artifact citations.
- Operations runbook at `docs/operations.md`.
- OSF pre-registration template at `orchestration/osf_preregistration.template.md` (binding text; the kill-gate runner refuses to execute without the OSF URL on file at `orchestration/osf_preregistration.url`).
- Four per-artifact Wave 1 review packs at `specs/2026-05-17-{A,B,C,D}-*-review-pack.md`.
- `orchestration/companion_sync.py` — rebuild the artifact registry from upstream GitHub release state; `--check` mode for CI.
- `orchestration/kill_gate.py` — intentional `NotImplementedError` stub until OSF pre-reg + B v0.2 + Sprint C-Training all complete.

### Context
This session completed Wave 1 of the HELIOS program: four public artifacts (helios-provenance-spec v0.1.0 RFC, helios-fusion-engine v0.1.0 framework, gannon-storm-rtk-analysis v0.1.0 retrospective, helios-spaceweather-connectors foundation+DONKI), plus the private helios-fusion-internal scaffolding and this meta-repo. All repos transferred from the user account `577-Industries` (the bootstrap mistake) to the organization `577Industries` (alongside aegisgraph, model-router, agent-memory, tool-guardrails).
