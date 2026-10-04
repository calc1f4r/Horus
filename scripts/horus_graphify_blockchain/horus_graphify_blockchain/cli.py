"""
CLI entry point for horus-graphify-blockchain.

Usage:
  horus-graphify-blockchain extract <path> [--out FILE] [--language LANG]
  horus-graphify-blockchain languages
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def cmd_extract(args) -> int:
    from .extractor import extract_directory, extract_file
    from .detect import detect_language

    target = Path(args.path)
    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        return 1

    if target.is_file():
        lang = args.language or detect_language(target)
        if not lang:
            print(f"Error: cannot detect language for {target}", file=sys.stderr)
            return 1
        result = extract_file(str(target), language=lang)
    else:
        result = extract_directory(str(target))

    output = json.dumps(result.to_dict(), indent=2)

    if args.out:
        Path(args.out).write_text(output)
        data = result.to_dict()
        print(
            f"Extracted: {len(data['nodes'])} nodes, {len(data['edges'])} edges, "
            f"{len(data['hyperedges'])} hyperedges → {args.out}"
        )
    else:
        print(output)

    return 0


def cmd_languages(args) -> int:
    from .extractor import _LANGUAGE_MODULE_MAP

    print("Supported blockchain languages (Phase 2a):")
    for lang, module in sorted(_LANGUAGE_MODULE_MAP.items()):
        try:
            import importlib
            mod = importlib.import_module(module)
            # Try to load the parser to verify grammar is available
            parser = mod._get_parser() if hasattr(mod, "_get_parser") else None
            status = "tree-sitter OK" if parser else "regex fallback (grammar not installed)"
        except Exception:
            status = "unavailable"
        print(f"  {lang:<15} {module}  [{status}]")

    print("\nComing in Phase 2b: vyper, sway, tact, func")
    print("Languages handled natively by graphify (no extraction needed): rust, go, python, ts, js, ...")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="horus-graphify-blockchain",
        description="Blockchain AST extractor producing graphify-compatible JSON",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_extract = sub.add_parser("extract", help="Extract nodes/edges from a file or directory")
    p_extract.add_argument("path", help="File or directory to extract")
    p_extract.add_argument("--out", "-o", help="Output file (default: stdout)")
    p_extract.add_argument("--language", "-l", help="Override language detection (e.g. solidity, cairo)")

    sub.add_parser("languages", help="List supported languages and grammar status")

    args = parser.parse_args()

    dispatch = {
        "extract": cmd_extract,
        "languages": cmd_languages,
    }
    sys.exit(dispatch[args.cmd](args))


if __name__ == "__main__":
    main()
