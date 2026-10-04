"""Multi-format finding extractor for reports/cosmos-l1-nodes_findings/.

Formats handled:
  oak       -- "N. <title> Severity: <Sev>"                     (Oak Security)
  zellic    -- "N.M. <title> Target .. Category .. Severity <S>" (Zellic)
  halborn   -- "N.M (HAL-0N) <TITLE> - <SEV> (score) Description:"(Halborn)
  informal  -- "<title> Project .. Type .. Severity .. Status .. Issue"
  informal21-- "IF-XXX-NN: <title> Severity <Sev> Type .."
Everything else is reported as unparsed for manual classification.

Usage: python3 extract_v2.py <reports_dir> <out.jsonl> <stats.json>
"""
import json
import os
import re
import sys

SEV_ORDER = ["CRITICAL", "HIGH", "MAJOR", "MEDIUM", "MINOR", "LOW",
             "INFORMATIONAL", "INFORMATIVE", "NONE"]

OAK_RE = re.compile(
    r"(?:(?<=\s)|^)(\d{1,3})\.\s+(?P<title>\S.{4,320}?)\s+Severity:\s*"
    r"(?P<sev>Critical|Major|Medium|Minor|Informational|High|Low|None)\b")

ZELLIC_RE = re.compile(
    r"(?:(?<=\s)|^)(\d{1,2}\.\d{1,2})\.\s+(?P<title>\S.{4,220}?)\s+"
    r"T\s?arget\s+.{0,80}?\s+Category\s+.{0,60}?\s+Severity\s+"
    r"(?P<sev>Critical|High|Medium|Low|Informational)\s+Likelihood")

HALBORN_RE = re.compile(
    r"(?:(?<=\s)|^)(\d{1,2}\.\d{1,2})\s+\((?P<id>HAL-\d{2,3})\)\s+"
    r"(?P<title>[A-Z0-9][^()]{4,220}?)\s+-\s+"
    r"(?P<sev>CRITICAL|HIGH|MEDIUM|LOW|INFORMATIONAL)\s*\(?[\d.]*\)?\s+Description:")

INFORMAL_RE = re.compile(
    r"(?P<pre>.{0,220}?)\s+Project\s+.{0,90}?\s+Type\s+"
    r"(?P<type>(?:PROTOCOL|IMPLEMENTATION|DOCUMENTATION|DESIGN|PROCESS|TESTING)"
    r"(?:\s*/\s*[A-Z]+)*)\s+Severity\s+(?P<sevblob>.{0,160}?)\s+Status\s+"
    r"(?P<status>[A-Z ]{3,30}?)\s+Issue\b")

INFORMAL21_RE = re.compile(
    r"(?P<id>IF-[A-Z0-9]+-\d{1,3})\s*:\s*(?P<title>\S.{4,240}?)\s+Severity\s+"
    r"(?P<sev>Potentially High|Informative|Informational|Critical|High|Medium|Low)\s+Type\b")

LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
       "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"}


def flatten(text):
    for k, v in LIG.items():
        text = text.replace(k, v)
    return re.sub(r"\s+", " ", text).strip()


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


AUDITORS = [
    ("Oak Security", "Oak Security"), ("oaksecurity", "Oak Security"),
    ("Informal Systems", "Informal Systems"),
    ("Halborn", "Halborn"), ("Zellic", "Zellic"),
    ("Trail of Bits", "Trail of Bits"), ("Atredis", "Atredis Partners"),
    ("Sherlock", "Sherlock"), ("Least Authority", "Least Authority"),
    ("Coinfabrik", "CoinFabrik"), ("CoinFabrik", "CoinFabrik"),
    ("Binary Builders", "Binary Builders"), ("binary.builders", "Binary Builders"),
    ("Nethermind", "Nethermind"), ("NCC Group", "NCC Group"),
    ("Quantstamp", "Quantstamp"), ("CertiK", "CertiK"),
    ("Ackee Blockchain", "Ackee Blockchain"), ("SCV", "SCV Security"),
]


def detect_auditor(flat):
    head = flat[:8000]
    for needle, name in AUDITORS:
        if needle in head:
            return name
    for needle, name in AUDITORS:
        if needle in flat:
            return name
    return "unknown"


def detect_protocol(flat, fname):
    m = re.search(r"Audit Report ([A-Z][\w\-\+\. ]{2,70}?) v\d", flat[:2500])
    if m:
        return m.group(1).strip()
    stem = fname.replace("audit-reports-", "").replace("audits-", "")
    stem = re.sub(r"-\d{4}-\d{2}-\d{2}.*$", "", stem)
    return stem.replace("-pdf.md", "").replace(".md", "").replace("-", " ")[:60]


def pick_sev(blob):
    up = blob.upper()
    for s in SEV_ORDER:
        if re.search(r"\b" + s + r"\b", up):
            return s.capitalize()
    return "Unknown"


def section_after(flat, names, last=True):
    for nm in names:
        idxs = [m.start() for m in re.finditer(re.escape(nm), flat)]
        if idxs:
            return flat[(idxs[-1] if last else idxs[0]):]
    return flat


def collect(rx, section, sev_from, title_from, fmt):
    out = []
    ms = list(rx.finditer(section))
    for i, m in enumerate(ms):
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(section)
        body = section[start:end].strip()
        title = title_from(m)
        if not title or len(title) < 6:
            continue
        out.append({"num": m.group(1) if rx not in (INFORMAL_RE, INFORMAL21_RE)
                    else (m.group("id") if rx is INFORMAL21_RE else str(i + 1)),
                    "title": title, "severity": sev_from(m), "body": body[:9000],
                    "format": fmt})
    return out


def clean_informal_title(pre):
    t = pre
    t = re.sub(r".*?(?:Findings|Overview|Appendix)\s+\d+\s*", "", t)
    t = re.sub(r"^[\s•\d\.•/]+", "", t)
    t = re.sub(r"^©\s*\d{4}\s+Informal Systems\s*", "", t)
    return t.strip()


def parse_file(path, fname):
    raw = open(path, encoding="utf-8", errors="replace").read()
    flat = flatten(strip_frontmatter(raw))
    auditor = detect_auditor(flat)
    protocol = detect_protocol(flat, fname)
    recs = []

    sec = section_after(flat, ["Detailed Findings", "Findings Detail",
                               "FINDINGS & TECH DETAILS", "Detailed Results"])
    recs = collect(OAK_RE, sec, lambda m: m.group("sev"),
                   lambda m: re.sub(r"\s*\d+\s*$", "", m.group("title")).strip(), "oak")
    if len(recs) >= 2:
        return auditor, protocol, recs, flat

    recs = collect(ZELLIC_RE, flat, lambda m: m.group("sev"),
                   lambda m: m.group("title").strip(), "zellic")
    if len(recs) >= 1:
        return auditor, protocol, recs, flat

    recs = collect(HALBORN_RE, flat, lambda m: m.group("sev").capitalize(),
                   lambda m: re.sub(r"\s+", " ", m.group("title")).strip(), "halborn")
    if len(recs) >= 1:
        return auditor, protocol, recs, flat

    recs = collect(INFORMAL_RE, flat, lambda m: pick_sev(m.group("sevblob")),
                   lambda m: clean_informal_title(m.group("pre")), "informal")
    if len(recs) >= 1:
        return auditor, protocol, recs, flat

    recs = collect(INFORMAL21_RE, flat, lambda m: m.group("sev"),
                   lambda m: m.group("title").strip(), "informal21")
    if len(recs) >= 1:
        return auditor, protocol, recs, flat

    return auditor, protocol, [], flat


def main():
    rdir, out_path, stats_path = sys.argv[1], sys.argv[2], sys.argv[3]
    files = sorted(f for f in os.listdir(rdir) if f.endswith(".md"))
    records, stats = [], []
    for fname in files:
        auditor, protocol, recs, flat = parse_file(os.path.join(rdir, fname), fname)
        for r in recs:
            r.update({"file": fname, "auditor": auditor, "protocol": protocol})
            records.append(r)
        stats.append({"file": fname, "auditor": auditor, "protocol": protocol,
                      "findings": len(recs),
                      "format": recs[0]["format"] if recs else "none",
                      "chars": len(flat)})
    with open(out_path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
    json.dump(stats, open(stats_path, "w"), indent=1)
    zero = [s for s in stats if s["findings"] == 0]
    print("files:", len(files), "findings:", len(records), "unparsed:", len(zero))
    for z in zero:
        print(f"  {z['auditor']:<18} {z['chars']:>7}  {z['file']}")


if __name__ == "__main__":
    main()
