#!/usr/bin/env python3
"""
Merge Shard Findings with Root-Cause Deduplication
===================================================
Reads all per-shard finding files (03-findings-shard-*.md), merges them,
groups by a root-cause text heuristic (same code location + same root cause),
assigns intermediate IDs (M-001, M-002...), and preserves every input in a JSON
lineage sidecar. Grouping is not proof of semantic root-cause equivalence.

Usage:
    python3 scripts/merge_shard_findings.py <audit_output_dir>

Options:
    --output <path>     Merged findings path (default: <dir>/03-findings-raw.md)
    --log <path>        Merge log path (default: <dir>/03-merge-log.md)
    --lineage <path>    JSON lineage (default: <dir>/03-merge-lineage.json)
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys


HEADER = re.compile(r"^### (F-[A-Za-z0-9][A-Za-z0-9_-]*):[ \t]*(\S.*)$")
FINDING_LIKE = re.compile(r"^\s{0,3}#{1,6}\s+.*(?:\bF-|\bFinding\b)", re.I)
FIELD = re.compile(r"^\s*\|\s*(?:\*\*)?(Affected Code|Root Cause|Severity|Confidence)(?:\*\*)?\s*\|\s*(.*?)\s*\|\s*$")


def _outside_fences(content):
    """Yield physical line numbers/text outside Markdown fenced examples."""
    fence = None
    for number, line in enumerate(content.split("\n")):
        line = line.removesuffix("\r")
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", line):
                fence = None
            continue
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            continue
        yield number, line
    if fence:
        raise ValueError("Unclosed Markdown fence in shard findings")


def _headers_and_preamble(content, shard_id):
    headers = []
    for number, line in _outside_fences(content):
        match = HEADER.fullmatch(line)
        if match:
            headers.append((number, match[1], line))
        elif FINDING_LIKE.match(line):
            raise ValueError(f"Unsupported finding header in shard {shard_id}, line {number + 1}")
        elif not headers and FIELD.fullmatch(line):
            raise ValueError(f"Unparsed finding fields before first header in shard {shard_id}")
    lines = content.split("\n")
    preamble = "\n".join(lines[:headers[0][0]]) + ("\n" if headers and headers[0][0] else "") if headers else content
    return headers, preamble


def parse_findings(content, shard_id="unknown"):
    """Extract individual findings from a shard findings markdown file."""
    findings = []
    headers, _ = _headers_and_preamble(content, shard_id)
    lines = content.split("\n")
    original_ids = set()
    for index, (start, original_id, header) in enumerate(headers):
        if original_id in original_ids:
            raise ValueError(f"Repeated finding ID in shard {shard_id}: {original_id}")
        original_ids.add(original_id)
        end = headers[index + 1][0] if index + 1 < len(headers) else len(lines)
        body = "\n".join(lines[start + 1:end]).strip()
        fields = {}
        for _, line in _outside_fences(body):
            match = FIELD.fullmatch(line)
            if match:
                if match[1] in fields:
                    raise ValueError(f"Repeated {match[1]} field in shard {shard_id}, finding {original_id}")
                fields[match[1]] = match[2]
        affected_code = fields.get("Affected Code", "")
        root_cause = fields.get("Root Cause", "")
        findings.append({
            "input_id": f"{shard_id}:{len(findings) + 1:04d}",
            "members": [f"{shard_id}:{len(findings) + 1:04d}"],
            "original_id": original_id,
            "block_sha256": hashlib.sha256(f"{header}\n\n{body}".encode("utf-8")).hexdigest(),
            "header": header,
            "body": body,
            "full": f"{header}\n\n{body}",
            "shard": shard_id,
            "affected_code": affected_code,
            "root_cause": root_cause,
            "severity": fields.get("Severity", ""),
            "confidence": fields.get("Confidence", ""),
            "dedup_key": f"{affected_code}::{root_cause}".lower().strip(),
        })

    return findings


def confidence_rank(conf):
    """Rank confidence for dedup comparison (higher = keep)."""
    return {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(conf.upper(), 0)


def severity_rank(sev):
    """Rank severity for dedup comparison (higher = keep)."""
    return {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(sev.upper(), 0)


def main():
    parser = argparse.ArgumentParser(description="Merge shard findings with deduplication")
    parser.add_argument("audit_output_dir", help="Path to audit-output/ directory")
    parser.add_argument("--output", default=None)
    parser.add_argument("--log", default=None)
    parser.add_argument("--lineage", default=None)
    args = parser.parse_args()

    output_dir = args.audit_output_dir
    output_path = args.output or os.path.join(output_dir, "03-findings-raw.md")
    log_path = args.log or os.path.join(output_dir, "03-merge-log.md")
    lineage_path = args.lineage or os.path.join(output_dir, "03-merge-lineage.json")

    # Find shard files
    shard_files = sorted(glob.glob(os.path.join(output_dir, "03-findings-shard-*.md")))
    if not shard_files:
        print(f"No shard files found in {output_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(shard_files)} shard files")

    # Parse all findings
    all_findings = []
    shard_stats = []
    source_artifacts = []
    for shard_file in shard_files:
        shard_id = os.path.basename(shard_file).replace("03-findings-shard-", "").replace(".md", "")
        with open(shard_file, "rb") as f:
            source_bytes = f.read()
        content = source_bytes.decode("utf-8")
        findings = parse_findings(content, shard_id)
        _, preamble = _headers_and_preamble(content, shard_id)
        preamble_bytes = preamble.encode("utf-8")
        source_artifacts.append({"path": os.path.basename(shard_file), "sha256": hashlib.sha256(source_bytes).hexdigest(),
                                 "preamble_sha256": hashlib.sha256(preamble_bytes).hexdigest(),
                                 "preamble_bytes": len(preamble_bytes), "parsed_count": len(findings)})
        all_findings.extend(findings)
        shard_stats.append({"shard": shard_id, "findings": len(findings), "file": shard_file})
        print(f"  {shard_id}: {len(findings)} findings")

    # Deduplicate by root cause
    seen = {}  # dedup_key → best finding
    duplicates = []
    for f in all_findings:
        key = f["dedup_key"]
        if not key or key == "::":
            # No dedup key — keep as unique
            seen[f"unique:{f['input_id']}"] = f
            continue
        if key in seen:
            existing = seen[key]
            # Keep the one with higher confidence, then higher severity
            if (confidence_rank(f["confidence"]) > confidence_rank(existing["confidence"]) or
                (confidence_rank(f["confidence"]) == confidence_rank(existing["confidence"]) and
                 severity_rank(f["severity"]) > severity_rank(existing["severity"]))):
                duplicates.append({"kept_shard": f["shard"], "dropped_shard": existing["shard"],
                                   "reason": f"Same root cause: {f['root_cause'][:60]}"})
                f["members"] = existing["members"] + f["members"]
                seen[key] = f
            else:
                duplicates.append({"kept_shard": existing["shard"], "dropped_shard": f["shard"],
                                   "reason": f"Same root cause: {f['root_cause'][:60]}"})
                existing["members"].extend(f["members"])
        else:
            seen[key] = f

    unique_findings = list(seen.values())
    # Sort by severity (CRITICAL first)
    unique_findings.sort(key=lambda x: -severity_rank(x["severity"]))

    # Renumber
    merged_content = "# DB-Powered Hunting Findings (Phase 4 — Merged)\n\n"
    merged_content += f"**Total unique findings**: {len(unique_findings)} (from {len(all_findings)} across {len(shard_files)} shards, {len(duplicates)} deduplicated)\n\n---\n\n"
    for i, f in enumerate(unique_findings, 1):
        # Replace old finding ID with new sequential ID
        new_header = re.sub(r"### F-[^\s:]+", f"### M-{i:03d}", f["header"])
        merged_content += f"{new_header}\n\n{f['body']}\n\n---\n\n"

    lineage = {
        "schema_version": 1,
        "heuristic_only": True,
        "intermediate_namespace": "M",
        "source_artifacts": source_artifacts,
        "input_records": [{"id": f["input_id"], "original_id": f["original_id"], "block_sha256": f["block_sha256"],
                           "severity": f["severity"], "confidence": f["confidence"], "shard": f["shard"]} for f in all_findings],
        "inputs": [f["input_id"] for f in all_findings],
        "routes": [{"input_id": member, "candidate_ids": [f"M-{i:03d}"]}
                   for i, f in enumerate(unique_findings, 1) for member in f["members"]],
    }
    if not all_findings:
        lineage["no_shard_inputs"] = "No finding headers in supplied shards; preambles retained by hash and length"
    # Reconcile before emitting; confidence selection must never erase provenance.
    from horus_review.core import check_lineage
    issues = check_lineage(lineage, {f"M-{i:03d}" for i in range(1, len(unique_findings) + 1)})
    if issues:
        raise ValueError(f"Shard merge lineage failed: {issues}")
    with open(lineage_path, "w", encoding="utf-8") as out:
        json.dump(lineage, out, indent=2)
        out.write("\n")

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(merged_content)

    # Write merge log
    log = "# Shard Merge Log\n\n"
    log += "## Shard Results\n"
    log += "| Shard | Findings |\n|-------|----------|\n"
    for s in shard_stats:
        log += f"| {s['shard']} | {s['findings']} |\n"
    log += f"\n## Deduplication\n"
    if duplicates:
        log += "| Kept From | Dropped From | Reason |\n|-----------|-------------|--------|\n"
        for d in duplicates:
            log += f"| {d['kept_shard']} | {d['dropped_shard']} | {d['reason']} |\n"
    else:
        log += "No duplicates found.\n"
    log += f"\n## Summary\n- Total findings across shards: {len(all_findings)}\n"
    log += f"- Unique findings after merge: {len(unique_findings)}\n"
    log += f"- Deduplicated: {len(duplicates)}\n"

    with open(log_path, "w", encoding="utf-8") as out:
        out.write(log)

    print(f"\nMerged: {len(unique_findings)} unique findings (from {len(all_findings)}, {len(duplicates)} deduped)")
    print(f"Written: {output_path}")
    print(f"Log: {log_path}")
    print(f"Lineage: {lineage_path}")


if __name__ == "__main__":
    main()
