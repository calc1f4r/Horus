#!/usr/bin/env python3
"""Peek at raw-index.json structure and a sample report file."""
import json
import os
import sys

p = "audit-output/vtw-cosmos-l1-nodes_findings/raw-index.json"
if os.path.exists(p):
    d = json.load(open(p, encoding="utf-8"))
    print("TYPE", type(d).__name__)
    if isinstance(d, dict):
        print("KEYS", list(d.keys())[:30])
        k = list(d.keys())[0]
        print("SAMPLE", k, json.dumps(d[k])[:800])
    elif isinstance(d, list):
        print("LEN", len(d))
        print(json.dumps(d[0], indent=1)[:1200])
