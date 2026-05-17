"""Rebuild companion footnotes from each artifact's README + latest release.

Triggered by a repository_dispatch event from each artifact repo on merge to main.
Updates `companion/footnotes.yaml` with the latest version, status, and any new
URLs (preprint, blog post, etc.). Commits and pushes the update to gh-pages.

Implementation pending; for now the YAML is manually maintained.
"""
from __future__ import annotations


def sync() -> None:
    raise NotImplementedError("Companion sync implementation pending — manual updates for now.")
