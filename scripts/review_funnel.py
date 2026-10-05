#!/usr/bin/env python3
"""Check a saved case-level evaluation ledger against its external inventory."""
import argparse
import hashlib
import json
from pathlib import Path

from horus_review.funnel import evaluate
from horus_review.serialization import load_json, parse_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--evidence-root', type=Path, required=True)
    args = parser.parse_args()
    try:
        inventory_bytes = args.inventory.read_bytes()
        result = evaluate(load_json(args.ledger), parse_json(inventory_bytes),
                          hashlib.sha256(inventory_bytes).hexdigest(), args.evidence_root)
    except (ValueError, TypeError, KeyError, OSError, RecursionError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
