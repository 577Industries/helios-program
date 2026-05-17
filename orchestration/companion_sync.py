"""Rebuild the companion footnotes registry from each artifact's repo state.

Pulled metadata per artifact:
  - latest GitHub release tag (via `gh release view`)
  - status (derived from release: 0.0.0 -> scaffolding; 0.1.x -> in-development;
    1.0.x+ -> stable; with manual override for "rfc" status)
  - PyPI version (if applicable)
  - arXiv preprint URL (for fusion-engine, manually maintained until paper ships)
  - Blog post URL (for gannon-analysis, manually maintained until post publishes)

The output is written to `companion/footnotes.yaml`. The companion document
`companion/companion.md` reads URLs and status fields from this YAML through
its rendering pipeline (`companion/render.py`).

Usage:
    python -m orchestration.companion_sync                # write/refresh
    python -m orchestration.companion_sync --check        # error if stale
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    print("error: PyYAML not installed. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

LOG = logging.getLogger(__name__)
HERE = Path(__file__).parent
REPO_ROOT = HERE.parent
COMPANION_DIR = REPO_ROOT / "companion"
FOOTNOTES_PATH = COMPANION_DIR / "footnotes.yaml"


@dataclass
class Artifact:
    key: str
    repo: str          # e.g. "577Industries/helios-provenance-spec"
    public: bool
    pypi_name: str | None = None
    cited_in: list[str] = field(default_factory=list)
    extra_keys: dict[str, Any] = field(default_factory=dict)


ARTIFACTS: list[Artifact] = [
    Artifact(
        key="provenance_spec",
        repo="577Industries/helios-provenance-spec",
        public=True,
        pypi_name="helios-provenance",
        cited_in=["§1.4", "§4.2 innovation #2"],
    ),
    Artifact(
        key="connectors",
        repo="577Industries/helios-spaceweather-connectors",
        public=True,
        pypi_name="helios-spaceweather-connectors",
        cited_in=["§2 Obj. 1", "§3 T1"],
    ),
    Artifact(
        key="fusion_engine",
        repo="577Industries/helios-fusion-engine",
        public=True,
        pypi_name="helios-fusion-engine",
        cited_in=["§2 Obj. 2", "§3.1", "§4.2 innovation #1"],
        extra_keys={"preprint": None, "osf_preregistration": None},
    ),
    Artifact(
        key="gannon_analysis",
        repo="577Industries/gannon-storm-rtk-analysis",
        public=True,
        pypi_name=None,
        cited_in=["§1.3 Gannon case study", "§2 Obj. 4", "§4.2 innovation #4"],
        extra_keys={"blog_post": None},
    ),
]


def _gh(*args: str) -> str:
    """Run gh and return stdout, or empty string if the command fails non-fatally."""
    try:
        result = subprocess.run(
            ["gh", *args], capture_output=True, text=True, check=True, timeout=30
        )
        return result.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        LOG.warning("gh command failed: gh %s -> %s", " ".join(args), e)
        return ""


def _latest_release(repo: str) -> str:
    """Latest release tag (e.g., 'v0.1.0') or '0.0.0' if no release exists."""
    out = _gh("release", "view", "--repo", repo, "--json", "tagName")
    if not out:
        return "0.0.0"
    try:
        return json.loads(out).get("tagName", "0.0.0").lstrip("v")
    except json.JSONDecodeError:
        return "0.0.0"


def _derive_status(version: str, manual_override: str | None = None) -> str:
    """Status derivation: 0.0.x -> scaffolding; 0.1.x -> in-development; 1.0+ -> stable."""
    if manual_override:
        return manual_override
    try:
        major, minor, *_ = version.split(".")
        if int(major) >= 1:
            return "stable"
        if int(minor) >= 1:
            return "in-development"
        return "scaffolding"
    except (ValueError, IndexError):
        return "scaffolding"


def build_registry() -> dict[str, Any]:
    """Build the full footnotes registry from upstream state."""
    out: dict[str, Any] = {"artifacts": {}}
    for art in ARTIFACTS:
        version = _latest_release(art.repo)
        entry: dict[str, Any] = {
            "repo": f"https://github.com/{art.repo}",
            "status": _derive_status(version),
            "cited_in": art.cited_in,
            "version": version,
        }
        if art.pypi_name:
            entry["pypi"] = f"https://pypi.org/project/{art.pypi_name}/"
        repo_slug = art.repo.split("/", 1)[1]
        entry["docs"] = f"https://577industries.github.io/{repo_slug}/"
        entry.update(art.extra_keys)
        out["artifacts"][art.key] = entry
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="error nonzero if footnotes.yaml is stale (CI use)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="verbose logging"
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    new = build_registry()
    new_yaml = yaml.safe_dump(
        new, sort_keys=False, default_flow_style=False, allow_unicode=True
    )

    if args.check:
        if not FOOTNOTES_PATH.exists():
            print("error: footnotes.yaml missing", file=sys.stderr)
            return 1
        current = FOOTNOTES_PATH.read_text()
        if current.strip() != new_yaml.strip():
            print("error: footnotes.yaml stale; run companion_sync.py", file=sys.stderr)
            return 1
        print("footnotes.yaml is up to date")
        return 0

    FOOTNOTES_PATH.write_text(new_yaml)
    print(f"wrote {FOOTNOTES_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
