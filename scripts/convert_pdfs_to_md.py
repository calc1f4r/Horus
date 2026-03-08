#!/usr/bin/env python3
"""
Convert all OtterSec Move audit PDFs to markdown using pymupdf4llm.
"""

import os
import sys
from pathlib import Path

import pymupdf4llm

PDF_DIR = Path(__file__).resolve().parent.parent / "reports" / "ottersec_move_audits"
MD_DIR = PDF_DIR / "markdown"


def main():
    MD_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs to convert")

    success = 0
    failed = []

    for i, pdf_path in enumerate(pdfs, 1):
        md_name = pdf_path.stem + ".md"
        md_path = MD_DIR / md_name

        if md_path.exists() and md_path.stat().st_size > 100:
            print(f"[{i}/{len(pdfs)}] Already converted: {md_name}")
            success += 1
            continue

        print(f"[{i}/{len(pdfs)}] Converting: {pdf_path.name}...", end=" ", flush=True)
        try:
            md_text = pymupdf4llm.to_markdown(str(pdf_path))
            md_path.write_text(md_text, encoding="utf-8")
            lines = md_text.count("\n")
            print(f"OK ({lines} lines)")
            success += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed.append(pdf_path.name)

    print(f"\nConverted: {success}/{len(pdfs)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")

    # Print line counts
    print("\nMarkdown file sizes:")
    for md in sorted(MD_DIR.glob("*.md")):
        lines = sum(1 for _ in open(md))
        print(f"  {md.name}: {lines} lines")


if __name__ == "__main__":
    main()
