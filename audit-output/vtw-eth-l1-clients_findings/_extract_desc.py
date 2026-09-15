import os, re, json

d = "reports/eth-l1-clients_findings"
out = "audit-output/vtw-eth-l1-clients_findings"
rows = []
for f in sorted(os.listdir(d)):
    if not f.endswith(".md"):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding="utf-8", errors="replace").read()
    # immunefi per-finding files
    m = re.search(r'^#\s+(.+)$', t, re.M)
    title = m.group(1).strip() if m else ""
    sev = (re.search(r'\*\*Report severity:\*\*\s*(\w+)', t) or [None,""])[1]
    tgt = (re.search(r'\*\*Target:\*\*\s*<?([^\n>]+)>?', t) or [None,""])[1].strip()
    # first 2 paragraphs of Description section
    desc = ""
    m = re.search(r'## Description\n+(.{0,700})', t, re.S)
    if m:
        desc = re.sub(r'\s+', ' ', m.group(1)).strip()
    # code identifiers mentioned
    idents = sorted(set(re.findall(r'\b(?:0x[0-9a-fA-F]{4,}|[a-z_][a-z0-9_]{5,}\(\))', desc)))
    rows.append(dict(f=f, bytes=len(t), title=title[:140], sev=sev, tgt=tgt[:60], desc=desc[:600]))

json.dump(rows, open(os.path.join(out, "imm-desc.json"), "w"), indent=1)
for r in rows:
    if not re.match(r'^\d{5}-', r["f"]):
        continue
    print(f"### {r['f']}\n  sev={r['sev']} tgt={r['tgt']}\n  title={r['title'][:110]}\n  desc={r['desc'][:420]}\n")
