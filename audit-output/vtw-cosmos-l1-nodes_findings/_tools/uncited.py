#!/usr/bin/env python3
"""Reconstruct the uncited-file list for reports/cosmos-l1-nodes_findings/.

A report file is "cited" when its basename appears anywhere under DB/.
"""
import os
import re
import subprocess
import sys

REPORTS = "reports/cosmos-l1-nodes_findings"

md = sorted(f for f in os.listdir(REPORTS) if f.endswith(".md"))

# Collect all DB text once.
db_text = []
for root, dirs, files in os.walk("DB"):
    dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
    for f in files:
        if f.endswith((".md", ".json")):
            p = os.path.join(root, f)
            try:
                db_text.append(open(p, encoding="utf-8", errors="ignore").read())
            except OSError:
                pass
blob = "\n".join(db_text)

cited = [f for f in md if f in blob]
uncited = [f for f in md if f not in blob]

print("total_md", len(md))
print("cited", len(cited))
print("uncited", len(uncited))
out = sys.argv[1] if len(sys.argv) > 1 else None
if out:
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(uncited) + "\n")
    with open(out.replace(".txt", "-cited.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(cited) + "\n")
