#!/usr/bin/env python3
"""Summarize existing DB/cosmos entries: pattern_key, category, ref counts."""
import os
import re

KEYS = ("category", "vulnerability_type", "root_cause_family", "pattern_key",
        "interaction_scope", "affected_component", "severity")

for root, dirs, files in os.walk("DB/cosmos"):
    for f in sorted(files):
        if not f.endswith(".md") or f == "README.md":
            continue
        p = os.path.join(root, f)
        txt = open(p, encoding="utf-8").read()
        fm = txt.split("---", 2)
        head = fm[1] if len(fm) > 2 else ""
        vals = {}
        for line in head.splitlines():
            m = re.match(r"^([a-z_]+):\s*(.+)$", line)
            if m and m.group(1) in KEYS:
                vals[m.group(1)] = m.group(2).strip()
        nrefs = len(re.findall(r"reports/[\w./-]+\.md", txt))
        nlines = txt.count("\n")
        print(f"--- {p}  lines={nlines} refs={nrefs}")
        for k in KEYS:
            if k in vals:
                print(f"    {k}: {vals[k]}")
