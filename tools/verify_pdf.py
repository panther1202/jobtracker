#!/usr/bin/env python
"""Check a rendered CV/cover-letter PDF the way an ATS parser would see it.

Usage:
    python tools/verify_pdf.py <file.pdf> [more.pdf ...]

Reports page count and scans the extracted text layer for encoding damage and
for the contact details that must survive extraction. Requires pdftotext
(poppler) on PATH; without it, only a warning is printed.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

MUST_APPEAR = ["732-824-1460", "panthpatel.aiengg@gmail.com"]


def extract(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(pdf), "-"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout


def check(pdf: Path) -> bool:
    text = extract(pdf)
    pages = text.count("\f")
    cid = len(re.findall(r"\(cid:", text))
    bad = text.count("\ufffd")
    missing = [needle for needle in MUST_APPEAR if needle not in text]
    ok = cid == 0 and bad == 0 and not missing
    print(f"{pdf.name}: pages={pages} cid={cid} replacement_chars={bad} "
          f"missing={missing or 'none'} -> {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if not shutil.which("pdftotext"):
        print("warning: pdftotext not on PATH; skipping text-layer verification")
        return 0
    return 0 if all([check(Path(a)) for a in sys.argv[1:]]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
