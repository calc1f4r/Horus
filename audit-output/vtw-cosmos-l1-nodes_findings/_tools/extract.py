#!/usr/bin/env python3
"""Extract a richer canonical index for the uncited cosmos-l1-nodes reports.

For each file emit: bytes, auditor guess, doc-kind guess, severity histogram,
and candidate finding titles harvested from the report body.
"""
import json
import os
import re

REPORTS = "reports/cosmos-l1-nodes_findings"
UNCITED = "audit-output/vtw-cosmos-l1-nodes_findings/uncited.txt"

AUDITORS = [
    ("Informal Systems", "informal systems"),
    ("Halborn", "halborn"),
    ("Zellic", "zellic"),
    ("Oak Security", "oak security"),
    ("Trail of Bits", "trail of bits"),
    ("Binary Builders", "binary builders"),
    ("CoinFabrik", "coinfabrik"),
    ("Sherlock", "sherlock"),
    ("Timewave", "timewave"),
    ("Certik", "certik"),
    ("Least Authority", "least authority"),
    ("NCC Group", "ncc group"),
    ("Quantstamp", "quantstamp"),
    ("Ackee", "ackee"),
    ("SCV", "scv-security"),
    ("Nethermind", "nethermind"),
    ("Spearbit", "spearbit"),
    ("Code4rena", "code4rena"),
]

SEV_PAT = re.compile(
    r"\b(critical|high|medium|minor|low|informational|informative|gas)\b", re.I)

# Informal Systems style finding ids, Halborn style ids, Oak style ids
ID_PATTERNS = [
    re.compile(r"\b([A-Z]{2,8}-\d{1,3})\b"),          # e.g. IF-CELESTIA-01, OS-XXX-01
    re.compile(r"\b(HAL-\d{2})\b"),
    re.compile(r"\b(\d+\.\d+\s+[A-Z][^\n]{10,90})"),
]


def sniff_kind(name, txt):
    low = name.lower()
    head = txt[:4000].lower()
    if low.endswith("security-md.md") or "security-md" in low:
        return "noise"
    if "-adr-" in low or "-spec-" in low or "docs-architecture" in low:
        return "analysis"
    if "incident" in low:
        return "analysis"
    if "review-md" in low:
        return "analysis"
    if "audit report" in head or "security audit" in head or "findings" in txt[:20000].lower():
        return "finding"
    return "analysis"


def main():
    names = [l.strip() for l in open(UNCITED, encoding="utf-8") if l.strip()]
    out = []
    for n in names:
        p = os.path.join(REPORTS, n)
        txt = open(p, encoding="utf-8", errors="ignore").read()
        low = txt.lower()
        aud = next((a for a, k in AUDITORS if k in low), "")
        sev = {}
        for m in SEV_PAT.finditer(txt):
            k = m.group(1).lower()
            sev[k] = sev.get(k, 0) + 1
        ids = sorted(set(ID_PATTERNS[0].findall(txt)))[:40]
        out.append({
            "f": n,
            "bytes": len(txt),
            "auditor": aud,
            "kind": sniff_kind(n, txt),
            "sev": {k: v for k, v in sorted(sev.items(), key=lambda x: -x[1])},
            "ids": ids,
        })
    json.dump(out, open(
        "audit-output/vtw-cosmos-l1-nodes_findings/uncited-index.json", "w",
        encoding="utf-8"), indent=1)
    kinds = {}
    for o in out:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    print("files", len(out), kinds)
    for o in out:
        print(f"{o['kind']:9s} {o['bytes']:7d} {o['auditor'][:18]:18s} {o['f']}")


main()
