"""Render the companion document to HTML + PDF via pandoc.

Re-builds `companion.md` against `footnotes.yaml`, emits:
  - `_site/companion.html` — for GitHub Pages
  - `_site/companion.pdf` — for distribution

Run via `python -m companion.render`. Requires `pandoc` and `wkhtmltopdf` on PATH.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "_site"


def main() -> int:
    if not shutil.which("pandoc"):
        print("error: pandoc not found on PATH", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    md = HERE / "companion.md"
    html = OUT / "companion.html"
    pdf = OUT / "companion.pdf"

    subprocess.run(
        ["pandoc", str(md), "-o", str(html), "--standalone", "--toc",
         "--metadata", "title=HELIOS Public Companion",
         "--css", "assets/companion.css"],
        check=True,
    )

    if shutil.which("wkhtmltopdf"):
        subprocess.run(["wkhtmltopdf", str(html), str(pdf)], check=True)
    else:
        print("warning: wkhtmltopdf not found; skipping PDF render")

    print(f"rendered: {html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
