#!/usr/bin/env python
"""Render an HTML document to PDF using xhtml2pdf (pure Python, no system deps, no TeX).

Usage:
    python tools/render_pdf.py <input.html> [output.pdf]

If output is omitted, writes alongside the input with a .pdf extension.
This is the LaTeX-free replacement for the lualatex/xelatex compile step:
single-column, real text layer (ATS-friendly), no distribution to install.

Fonts
-----
Roboto (assets/fonts/) is registered with reportlab up front and exposed to
xhtml2pdf, so documents can just say `font-family: Roboto` with no @font-face
rule. @font-face is deliberately avoided: on Windows xhtml2pdf copies the TTF
into a still-open NamedTemporaryFile and reportlab then fails to reopen it
(PermissionError -> TTFError). Registering directly sidesteps that entirely.

Roboto has no italic in the vendored set, so italic maps back to the upright
face. The CV templates do not use italics.
"""
import sys
from pathlib import Path

from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = REPO_ROOT / "assets" / "fonts"

# (css family, regular file, bold file)
FONT_FAMILIES = [("Roboto", "Roboto-Regular.ttf", "Roboto-Bold.ttf")]


def register_fonts() -> None:
    """Register vendored TTFs with reportlab and make them visible to xhtml2pdf."""
    for family, regular, bold in FONT_FAMILIES:
        regular_path = FONT_DIR / regular
        bold_path = FONT_DIR / bold
        if not regular_path.exists() or not bold_path.exists():
            print(f"warning: {family} not found in {FONT_DIR}; falling back to Helvetica")
            continue
        bold_name = f"{family}-Bold"
        pdfmetrics.registerFont(TTFont(family, str(regular_path)))
        pdfmetrics.registerFont(TTFont(bold_name, str(bold_path)))
        # (family, bold, italic, registered name) - no italic face, so italic reuses upright
        addMapping(family, 0, 0, family)
        addMapping(family, 1, 0, bold_name)
        addMapping(family, 0, 1, family)
        addMapping(family, 1, 1, bold_name)
        DEFAULT_FONT[family.lower()] = family


def make_link_callback(html_dir: Path):
    """Resolve relative asset paths from the HTML's directory, then the repo root."""

    def link_callback(uri: str, rel):
        if uri.startswith(("http://", "https://", "data:")):
            return uri
        if uri.startswith("file://"):
            uri = uri[len("file://") :]
        candidate = Path(uri)
        if candidate.is_absolute() and candidate.exists():
            return str(candidate)
        for base in (html_dir, REPO_ROOT):
            resolved = (base / uri).resolve()
            if resolved.exists():
                return str(resolved)
        return uri

    return link_callback


def render(html_path: Path, pdf_path: Path) -> bool:
    register_fonts()
    html = html_path.read_text(encoding="utf-8")
    with pdf_path.open("wb") as out:
        result = pisa.CreatePDF(
            html,
            dest=out,
            encoding="utf-8",
            link_callback=make_link_callback(html_path.parent),
        )
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
