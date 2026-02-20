#!/usr/bin/env python3
"""
Merge Shard Findings with Root-Cause Deduplication
===================================================
Reads all per-shard finding files (03-findings-shard-*.md), merges them,
deduplicates by root cause (same code location + same root cause), renumbers
sequentially (F-001, F-002...), and writes merged output.

Usage:
    python3 scripts/merge_shard_findings.py <audit_output_dir>

Options:
    --output <path>     Merged findings path (default: <dir>/03-findings-raw.md)
    --log <path>        Merge log path (default: <dir>/03-merge-log.md)
"""

import argparse
import glob
import os
import re
import sys


def parse_findings(content, shard_id="unknown"):
    """Extract individual findings from a shard findings markdown file."""
    findings = []
    # Split on finding headers: ### F-<shard>-NNN: or ### F-NNN:
    pattern = r"(### F-[^\n]+)"
    parts = re.split(pattern, content)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            header = parts[i].strip()
            body = parts[i + 1].strip()

            # Extract key fields for dedup
            affected_code = ""
            root_cause = ""
            severity = ""
            confidence = ""

            for line in body.split("\n"):
                line_stripped = line.strip().strip("|").strip()
                if "Affected Code" in line and "|" in line:
                    affected_code = line_stripped.split("|")[-1].strip()
                elif "Root Cause" in line and "|" in line:
                    root_cause = line_stripped.split("|")[-1].strip()
                elif "Severity" in line and "|" in line:
                    severity = line_stripped.split("|")[-1].strip()
                elif "Confidence" in line and "|" in line:
                    confidence = line_stripped.split("|")[-1].strip()

            findings.append({
                "header": header,
                "body": body,
                "full": f"{header}\n\n{body}",
                "shard": shard_id,
                "affected_code": affected_code,
                "root_cause": root_cause,
                "severity": severity,
                "confidence": confidence,
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
    args = parser.parse_args()

    output_dir = args.audit_output_dir
    output_path = args.output or os.path.join(output_dir, "03-findings-raw.md")
    log_path = args.log or os.path.join(output_dir, "03-merge-log.md")

    # Find shard files
    shard_files = sorted(glob.glob(os.path.join(output_dir, "03-findings-shard-*.md")))
    if not shard_files:
        print(f"No shard files found in {output_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(shard_files)} shard files")

    # Parse all findings
    all_findings = []
    shard_stats = []
    for shard_file in shard_files:
        shard_id = os.path.basename(shard_file).replace("03-findings-shard-", "").replace(".md", "")
        with open(shard_file, "r", encoding="utf-8") as f:
            content = f.read()
        findings = parse_findings(content, shard_id)
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
            seen[f"{key}_{id(f)}"] = f
            continue
        if key in seen:
            existing = seen[key]
            # Keep the one with higher confidence, then higher severity
            if (confidence_rank(f["confidence"]) > confidence_rank(existing["confidence"]) or
                (confidence_rank(f["confidence"]) == confidence_rank(existing["confidence"]) and
                 severity_rank(f["severity"]) > severity_rank(existing["severity"]))):
                duplicates.append({"kept_shard": f["shard"], "dropped_shard": existing["shard"],
                                   "reason": f"Same root cause: {f['root_cause'][:60]}"})
                seen[key] = f
            else:
                duplicates.append({"kept_shard": existing["shard"], "dropped_shard": f["shard"],
                                   "reason": f"Same root cause: {f['root_cause'][:60]}"})
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
        new_header = re.sub(r"### F-[^\s:]+", f"### F-{i:03d}", f["header"])
        merged_content += f"{new_header}\n\n{f['body']}\n\n---\n\n"

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


if __name__ == "__main__":
    main()
