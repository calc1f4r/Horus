import os, re, json

d = "reports/eth-l1-clients_findings"
out = "audit-output/vtw-eth-l1-clients_findings"
rows = []
for f in sorted(os.listdir(d)):
    if not f.endswith(".md"):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding="utf-8", errors="replace").read()
    title = ""
    m = re.search(r'^#\s+(.+)$', t, re.M)
    if m:
        title = m.group(1).strip()
    sev = ""
    m = re.search(r'\*\*Report severity:\*\*\s*(\w+)', t)
    if m:
        sev = m.group(1)
    tgt = ""
    m = re.search(r'\*\*Target:\*\*\s*<?([^\n>]+)>?', t)
    if m:
        tgt = m.group(1).strip().rstrip('>')
    imp = ""
    m = re.search(r'\*\*Impacts:\*\*\n((?:\s*\*.*\n)+)', t)
    if m:
        imp = " ; ".join(x.strip("* \n") for x in m.group(1).strip().split("\n"))
    rows.append(dict(f=f, bytes=len(t), title=title[:120], sev=sev, tgt=tgt[:70], imp=imp[:140]))

json.dump(rows, open(os.path.join(out, "raw-index.json"), "w"), indent=1)
imm = [r for r in rows if re.match(r'^\d{5}-', r["f"])]
print(len(rows), "md files;", len(imm), "immunefi;", len(rows) - len(imm), "other")
for r in imm:
    print("|".join([r["f"][:60], r["sev"], r["tgt"], r["title"][:70]]))
