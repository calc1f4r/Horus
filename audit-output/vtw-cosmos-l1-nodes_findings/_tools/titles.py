#!/usr/bin/env python3
"""Harvest per-report finding titles + severities from the uncited cosmos corpus.

Two normalization problems in this PDF->md corpus:
  * some files are one-word-per-line (newer Oak Security exports)
  * titles wrap across 2-3 lines before the severity marker
Both are handled before pattern matching.

Layouts covered:
  Halborn        -> "3.1 (HAL-01) TITLE - CRITICAL (10)"
  Informal Sys   -> "<title>\nID IF-FINDING-00N\nSeverity High"
  Oak Security   -> "Summary of Findings" table: "N. <title> <Severity> <Status>"
  Zellic / ToB   -> "<title>\nSeverity: High"
"""
import json
import os
import re

REPORTS = "reports/cosmos-l1-nodes_findings"
BASE = "audit-output/vtw-cosmos-l1-nodes_findings"
UNCITED = f"{BASE}/uncited.txt"

SEV = r"(?:Critical|High|Medium|Major|Minor|Low|Informational|Informative|Gas|None)"


def normalize(txt):
    """Collapse one-word-per-line exports back into real lines."""
    lines = [l for l in txt.splitlines() if l.strip()]
    if not lines:
        return txt
    short = sum(1 for l in lines if len(l.strip()) <= 20)
    if short / len(lines) > 0.75:
        txt = re.sub(r"\s+", " ", txt)
        # re-break before numbered items so titles stay separable
        txt = re.sub(r"(?<![\d.])(\d{1,2}\.)\s", r"\n\1 ", txt)
    return txt


def dedot(s):
    s = re.sub(r"\.{3,}", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def harvest(txt):
    out, seen = [], set()
    n = normalize(txt)

    # --- Halborn ---
    for m in re.finditer(
            r"\d+\.\d+\s*\((HAL-\d+)\)\s*(.+?)\s*[-–]\s*(" + SEV + r")\b",
            n, re.I):
        t = dedot(m.group(2))[:120]
        k = (m.group(1), t.lower())
        if k not in seen:
            seen.add(k)
            out.append({"id": m.group(1), "title": t, "sev": m.group(3).upper()})
    if out:
        return out

    # --- Informal Systems: title lines then "ID ...\nSeverity X" ---
    for m in re.finditer(
            r"([^\n]{8,}\n(?:[^\n]{0,90}\n)?)ID\s+([A-Z0-9\-]{4,24})\s*\n\s*Severity\s+("
            + SEV + r")\b", txt):
        t = dedot(m.group(1).replace("\n", " "))[:130]
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append({"id": m.group(2), "title": t, "sev": m.group(3).upper()})
    if out:
        return out

    # --- Oak Security (modern, word-per-line export): "N. <title> Severity: <sev>" ---
    for m in re.finditer(
            r"(?:^|\n)\s*(\d{1,2})\.\s+(.{10,140}?)\s+Severity:?\s+(" + SEV + r")\b",
            n, re.I):
        t = dedot(m.group(2))[:130]
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append({"id": m.group(1), "title": t, "sev": m.group(3).upper()})
    if out:
        return out

    # --- Zellic (no-space export): "3.N <title>" then bullet "Severity:<sev>" ---
    zl = txt.splitlines()
    for i, line in enumerate(zl):
        hm = re.match(r"^\s*(\d\.\d{1,2})\s+(\S.{8,140})$", line)
        if not hm:
            continue
        sv = ""
        for j in range(i + 1, min(len(zl), i + 10)):
            sm = re.search(r"Severity\s*:\s*(" + SEV + r")\b", zl[j], re.I)
            if sm:
                sv = sm.group(1).upper()
                break
        if not sv:
            continue
        t = dedot(hm.group(2))[:130]
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append({"id": hm.group(1), "title": t, "sev": sv})
    if out:
        return out

    # --- Oak Security: numbered detailed-findings list ---
    for m in re.finditer(r"^\s*(\d{1,2})\.\s+(.{15,150}?)\s*$", n, re.M):
        t = dedot(m.group(2))[:130]
        if re.search(r"^\d", t) or len(t.split()) < 3:
            continue
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append({"id": m.group(1), "title": t, "sev": ""})

    # --- generic "Severity: X" with up-to-3-line title lookback ---
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\s*(?:\*\*)?Severity(?:\*\*)?\s*[:|]\s*(" + SEV + r")\b",
                     line, re.I)
        if not m:
            continue
        buf = []
        for j in range(i - 1, max(-1, i - 6), -1):
            c = lines[j].strip()
            if not c:
                if buf:
                    break
                continue
            if re.match(r"^(impact|likelihood|type|difficulty|status|target|id|"
                        r"category|location|component|finding)\b", c, re.I):
                continue
            if c.count(".") > 12:
                break
            buf.insert(0, c)
            if len(" ".join(buf)) > 40:
                break
        t = dedot(" ".join(buf))[:130]
        k = t.lower()
        if t and k not in seen:
            seen.add(k)
            out.append({"id": "", "title": t, "sev": m.group(1).upper()})
    return out


def main():
    names = [l.strip() for l in open(UNCITED, encoding="utf-8") if l.strip()]
    res = {}
    for nm in names:
        txt = open(os.path.join(REPORTS, nm), encoding="utf-8", errors="ignore").read()
        res[nm] = harvest(txt)
    json.dump(res, open(f"{BASE}/uncited-titles.json", "w", encoding="utf-8"), indent=1)
    empty = [k for k, v in res.items() if not v]
    print("reports", len(res), "titles", sum(len(v) for v in res.values()),
          "empty", len(empty))
    for e in empty:
        print("  EMPTY", e)


main()
