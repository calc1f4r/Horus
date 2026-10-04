import pathlib, re, difflib, sys
rep = pathlib.Path("/home/calc1f4r/Horus/reports/substrate-l1_findings")
def body(n):
    t = (rep / n).read_text(errors="ignore")
    if t.startswith("---"):
        p = t.split("---", 2)
        if len(p) == 3:
            t = p[2]
    return re.sub(r"\s+", " ", t).strip().lower()
pairs = [
  ("phala-c4-2401.md", "phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md"),
  ("publications-audit-reports-peckshield-audit-report-zenlink-v1-0-pdf.md", "zenlink-peckshield.md"),
  ("acala-c4-2401.md", "acala-slowmist-2020.md"),
]
for a, b in pairs:
    ba, bb = body(a), body(b)
    r = difflib.SequenceMatcher(None, ba[:80000], bb[:80000]).ratio()
    print(f"{r:.4f}  {len(ba)} {len(bb)}  {a} <-> {b}")
