#!/usr/bin/env python3
"""Print harvested titles filtered by severity tier, for bucket formation."""
import json
import sys

BASE = "audit-output/vtw-cosmos-l1-nodes_findings"
TIER = {"CRITICAL": 0, "HIGH": 1, "MAJOR": 1, "MEDIUM": 2, "MINOR": 3, "LOW": 3,
        "INFORMATIONAL": 4, "INFORMATIVE": 4, "GAS": 5, "NONE": 5, "": 6}

maxtier = int(sys.argv[1]) if len(sys.argv) > 1 else 2
only = sys.argv[2] if len(sys.argv) > 2 else ""

d = json.load(open(f"{BASE}/uncited-titles.json", encoding="utf-8"))
n = 0
for f, items in d.items():
    if only and only not in f:
        continue
    keep = [i for i in items if TIER.get(i["sev"], 6) <= maxtier]
    if not keep:
        continue
    print(f"\n### {f}")
    for i in keep:
        n += 1
        print(f"  [{i['sev'] or '?':6s}] {i['title']}")
print(f"\nTOTAL {n}")
