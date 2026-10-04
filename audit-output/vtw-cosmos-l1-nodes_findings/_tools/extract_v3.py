"""Multi-format finding extractor for reports/cosmos-l1-nodes_findings/.

Formats handled (in priority order per file):
  oak         "N. <title> Severity: <Sev>"                            Oak Security
  zellic      "N.M. <title> Target .. Category .. Severity <S>"       Zellic
  halborn     "N.M (HAL-0N) <TITLE> - <SEV> (score) Description:"     Halborn
  informal-a  "<title> Project .. Type .. Severity .. Issue"          Informal (2023-2025)
  informal-b  "<title> ID IF-XXX Severity <S> Impact .."              Informal (2022)
  informal-c  "IF-XXX-NN: <title> [Category ..] Severity <S> .."      Informal (2021)

Usage: python3 extract_v3.py <reports_dir> <out.jsonl> <stats.json>
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

INFORMAL_A_RE = re.compile(
    r"(?P<pre>.{0,260}?)\s+Project\s+(?P<proj>.{0,90}?)\s+Type\s+"
    r"(?P<type>(?:PROTOCOL|IMPLEMENTATION|DOCUMENTATION|DESIGN|PROCESS|TESTING|"
    r"SECURITY|USABILITY|PERFORMANCE)(?:\s*/\s*[A-Z]+)*)\s+Severity\s+"
    r"(?P<sevblob>.{0,220}?)\s+(?:Issue\b|Involved artifacts\b|Description\b)")

INFORMAL_B_RE = re.compile(
    r"(?P<pre>.{0,240}?)\s+ID\s+(?P<id>IF-[A-Z0-9\-]{4,60})\s+Severity\s+"
    r"(?P<sev>Critical|High|Medium|Low|Informational|Informative|None)\s+"
    r"(?:Impact|Type|Exploitability)\b")

INFORMAL_C_RE = re.compile(
    r"(?P<id>IF-[A-Z0-9]+-\d{1,3})\s*:\s*(?P<title>\S.{4,240}?)\s+"
    r"(?:Category\s+.{0,50}?\s+)?Severity\s+"
    r"(?P<sev>Potentially High|Informative|Informational|Critical|High|Medium|Low)\s+"
    r"(?:Type|Issue|Impact|Category|Involved)\b")

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


def section_after(flat, names):
    for nm in names:
        idxs = [m.start() for m in re.finditer(re.escape(nm), flat)]
        if idxs:
            return flat[idxs[-1]:]
    return flat


def clean_title(pre):
    t = pre
    if " Title " in t:
        t = t.rsplit(" Title ", 1)[1]
    else:
        t = re.sub(r".*?(?:Findings|Overview|Appendix|Dashboard)\s+\d+\s*", "", t)
        t = re.sub(r".*?©\s*\d{4}\s+Informal Systems\s+", "", t)
    t = re.sub(r"^[\s•\-\d\.•/]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:220]


def collect(rx, section, sev_from, title_from, fmt, id_from=None):
    out = []
    ms = list(rx.finditer(section))
    for i, m in enumerate(ms):
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(section)
        body = section[start:end].strip()
        title = title_from(m)
        if not title or len(title) < 6:
            continue
        out.append({"num": id_from(m, i) if id_from else str(i + 1),
                    "title": title, "severity": sev_from(m),
                    "body": body[:9000], "format": fmt})
    return out


def parse_file(path, fname):
    raw = open(path, encoding="utf-8", errors="replace").read()
    flat = flatten(strip_frontmatter(raw))
    auditor = detect_auditor(flat)
    protocol = detect_protocol(flat, fname)

    sec = section_after(flat, ["Detailed Findings", "Findings Detail",
                               "FINDINGS & TECH DETAILS", "Detailed Results"])
    recs = collect(OAK_RE, sec, lambda m: m.group("sev"),
                   lambda m: re.sub(r"\s*\d+\s*$", "", m.group("title")).strip(),
                   "oak", lambda m, i: m.group(1))
    if len(recs) >= 2:
        return auditor, protocol, recs, flat

    for rx, sev_f, title_f, fmt, id_f in (
        (ZELLIC_RE, lambda m: m.group("sev"), lambda m: m.group("title").strip(),
         "zellic", lambda m, i: m.group(1)),
        (HALBORN_RE, lambda m: m.group("sev").capitalize(),
         lambda m: re.sub(r"\s+", " ", m.group("title")).strip(), "halborn",
         lambda m, i: m.group("id")),
        (INFORMAL_A_RE, lambda m: pick_sev(m.group("sevblob")),
         lambda m: clean_title(m.group("pre")), "informal-a", None),
        (INFORMAL_B_RE, lambda m: m.group("sev"),
         lambda m: clean_title(m.group("pre")), "informal-b",
         lambda m, i: m.group("id")),
        (INFORMAL_C_RE, lambda m: m.group("sev"),
         lambda m: m.group("title").strip(), "informal-c",
         lambda m, i: m.group("id")),
    ):
        recs = collect(rx, flat, sev_f, title_f, fmt, id_f)
        if recs:
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
