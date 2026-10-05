#!/usr/bin/env python3
"""Offline JSON decision integrity CLI. Never executes reviewed code or URLs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from horus_review.core import bundle_digests, check_bundle, check_sources, flag_contradiction, reconcile_tally, remap_lineage, resolve_contradiction, tally, transition
from horus_review.serialization import load_json
from horus_review.schema import validate_shape


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "gate", "ledger", "digest", "tally", "contradict", "resolve", "transition", "remap"):
        p = sub.add_parser(command)
        p.add_argument("input", type=Path)
        if command in {"check", "gate", "ledger", "contradict", "resolve", "transition"}:
            p.add_argument("--evidence-root", required=True, type=Path)
        if command == "contradict":
            p.add_argument("--entry-id", required=True)
            p.add_argument("--source-id", required=True)
            p.add_argument("--premise", required=True)
            p.add_argument("--actor-id", required=True)
        if command == "transition":
            p.add_argument("--id", required=True)
            p.add_argument("--state", required=True)
            p.add_argument("--reason", required=True)
            p.add_argument("--actor-id", required=True)
        if command == "resolve":
            p.add_argument("--fingerprint", required=True)
            p.add_argument("--basis-id", action="append", required=True)
            p.add_argument("--actor-id", required=True)
            p.add_argument("--reason", required=True)
        if command == "remap":
            p.add_argument("--mapping", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        bundle = load_json(args.input)
        if args.command != "remap":
            validate_shape(bundle)
        if args.command == "tally":
            result = tally(bundle.get("policy"), bundle.get("records"))
            if "recorded_supported_ids" in bundle:
                result["reconciliation"] = reconcile_tally(result, bundle["recorded_supported_ids"])
                result["ok"] = result["reconciliation"]["ok"]
        elif args.command == "digest":
            result = bundle_digests(bundle)
        elif args.command == "remap":
            result = remap_lineage(bundle, load_json(args.mapping))
        elif args.command == "transition":
            result = transition(bundle, args.id, args.state, args.reason, args.evidence_root, args.actor_id)
        elif args.command == "resolve":
            selected = [s for s in bundle["sources"] if s.get("id") in args.basis_id]
            issues, verified = check_sources(selected, bundle["revisions"], args.evidence_root)
            if issues or verified != set(args.basis_id):
                print(json.dumps({"ok": False, "issues": issues or [{"code": "RESOLUTION_BASIS", "detail": "Missing resolution evidence"}]}))
                return 1
            result = resolve_contradiction(bundle, args.fingerprint, args.actor_id, args.reason, args.basis_id)
        elif args.command == "contradict":
            # A new artifact intentionally makes old approvals stale. Do not
            # require fresh approvals before allowing a certainty-reducing flag.
            selected = [s for s in bundle["sources"] if s.get("id") == args.source_id]
            if len(selected) != 1:
                raise ValueError("Contradiction needs exactly one declared source")
            issues, verified = check_sources(selected, bundle["revisions"], args.evidence_root)
            if issues or args.source_id not in verified:
                print(json.dumps({"ok": False, "issues": issues}))
                return 1
            result = flag_contradiction(bundle, args.entry_id, args.source_id, args.premise, args.actor_id)
        else:
            result = check_bundle(bundle, args.evidence_root, publication=args.command == "gate")
            if args.command == "ledger":
                result = {"ok": result["ok"], "issues": result["issues"], "ledger": result["ledger"]}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if args.command in {"digest", "remap", "transition", "resolve", "contradict"} or result.get("ok", True) else 1
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError) as exc:
        print(json.dumps({"ok": False, "issues": [{"code": "MALFORMED_INPUT", "detail": str(exc)}]}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
