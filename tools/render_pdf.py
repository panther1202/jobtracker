#!/usr/bin/env python
"""Render an HTML document to PDF using xhtml2pdf (pure Python, no system deps, no TeX).

Usage:
    python tools/render_pdf.py <input.html> [output.pdf]

If output is omitted, writes alongside the input with a .pdf extension.
This is the LaTeX-free replacement for the lualatex/xelatex compile step:
single-column, real text layer (ATS-friendly), no distribution to install.
"""
import sys
from pathlib import Path
from xhtml2pdf import pisa


def render(html_path: Path, pdf_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")
    with pdf_path.open("wb") as out:
        result = pisa.CreatePDF(html, dest=out, encoding="utf-8")
    return not result.err


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    html_path = Path(sys.argv[1]).resolve()
    if not html_path.exists():
        print(f"error: {html_path} not found")
        return 1
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else html_path.with_suffix(".pdf")
    ok = render(html_path, pdf_path)
    if ok:
        print(f"OK  {pdf_path}")
        return 0
    print(f"FAILED  {html_path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
