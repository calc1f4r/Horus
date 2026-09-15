"""Extract per-finding records from PDF-extracted Oak Security / misc audit reports.

Usage: python3 extract_findings.py <reports_dir> <out.jsonl> [stats.json]
"""
import json
import os
import re
import sys

SEV_WORDS = r"Critical|Major|Medium|Minor|Informational|High|Low|None"

FIND_RE = re.compile(
    r"(?:(?<=\s)|^)(\d{1,3})\.\s+(?P<title>\S.{4,320}?)\s+Severity:\s*(?P<sev>" + SEV_WORDS + r")\b",
    re.DOTALL,
)


def flatten(text: str) -> str:
    # PDF extraction puts (nearly) one word per line; rebuild flowing text.
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    text = text.replace("ﬃ", "ffi").replace("ﬄ", "ffl")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_frontmatter(text: str):
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw = text[3:end]
            for line in raw.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
            text = text[end + 4 :]
    return fm, text


def detect_auditor(flat: str) -> str:
    checks = [
        ("Oak Security", "Oak Security"),
        ("Informal Systems", "Informal Systems"),
        ("Halborn", "Halborn"),
        ("Trail of Bits", "Trail of Bits"),
        ("Zellic", "Zellic"),
        ("SCV-Security", "SCV Security"),
        ("SCV Security", "SCV Security"),
        ("Certik", "CertiK"),
        ("CertiK", "CertiK"),
        ("Quantstamp", "Quantstamp"),
        ("NCC Group", "NCC Group"),
        ("Least Authority", "Least Authority"),
        ("Coinspect", "Coinspect"),
        ("Ackee Blockchain", "Ackee Blockchain"),
    ]
    head = flat[:6000]
    for needle, name in checks:
        if needle in head:
            return name
    for needle, name in checks:
        if needle in flat:
            return name
    return "unknown"


def detect_protocol(fm, flat, fname) -> str:
    m = re.search(r"Audit Report ([A-Z][\w\-\+\. ]{2,70}?) v\d", flat[:2000])
    if m:
        return m.group(1).strip()
    stem = fname.replace("audit-reports-", "")
    return stem.split("-20")[0].replace("-", " ")


def find_detailed(flat: str) -> str:
    """Return the body starting at the *last* 'Detailed Findings' heading."""
    idxs = [m.start() for m in re.finditer(r"Detailed Findings", flat)]
    if idxs:
        return flat[idxs[-1] :]
    for alt in ("Findings Detail", "Detailed Results", "Issues Found", "Findings"):
        idxs = [m.start() for m in re.finditer(alt, flat)]
        if idxs:
            return flat[idxs[-1] :]
    return flat


def main():
    rdir, out_path = sys.argv[1], sys.argv[2]
    files = sorted(f for f in os.listdir(rdir) if f.endswith(".md"))
    records = []
    stats = []
    for fname in files:
        path = os.path.join(rdir, fname)
        raw = open(path, encoding="utf-8", errors="replace").read()
        fm, body = strip_frontmatter(raw)
        flat = flatten(body)
        auditor = detect_auditor(flat)
        protocol = detect_protocol(fm, flat, fname)
        section = find_detailed(flat)
        matches = list(FIND_RE.finditer(section))
        n = 0
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(section)
            text = section[start:end].strip()
            title = re.sub(r"\s*\d+\s*$", "", m.group("title")).strip()
            # drop TOC-style artefacts
            if len(title) < 5:
                continue
            records.append(
                {
                    "file": fname,
                    "num": int(m.group(1)),
                    "title": title,
                    "severity": m.group("sev"),
                    "auditor": auditor,
                    "protocol": protocol,
                    "body": text[:9000],
                }
            )
            n += 1
        stats.append({"file": fname, "auditor": auditor, "protocol": protocol,
                      "findings": n, "chars": len(flat)})
    with open(out_path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
    if len(sys.argv) > 3:
        json.dump(stats, open(sys.argv[3], "w"), indent=1)
    print("files:", len(files), "findings:", len(records))
    zero = [s["file"] for s in stats if s["findings"] == 0]
    print("files with 0 parsed findings:", len(zero))
    for z in zero:
        print("  ", z)


if __name__ == "__main__":
    main()
