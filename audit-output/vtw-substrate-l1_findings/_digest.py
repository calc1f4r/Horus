import pathlib, re, json

root = pathlib.Path("/home/calc1f4r/Horus")
rep = root / "reports" / "substrate-l1_findings"
out = root / "audit-output" / "vtw-substrate-l1_findings"

uncited = [l.strip() for l in (out / "uncited.txt").read_text().splitlines() if l.strip()]

SEV = re.compile(r"\b(critical|high|medium|minor|moderate|low|informational|info|severity)\b", re.I)

rows = []
for name in uncited:
    p = rep / name
    if not p.exists():
        rows.append({"f": name, "cls": "MISSING"})
        continue
    size = p.stat().st_size
    if p.suffix == ".pdf":
        sib = name[:-4] + ".md"
        rows.append({"f": name, "bytes": size, "cls": "binary-pdf",
                     "sibling_md": sib if (rep / sib).exists() else None})
        continue
    txt = p.read_text(errors="ignore")
    lines = txt.splitlines()
    head = "\n".join(lines[:30])
    heads = [l.strip() for l in lines if l.lstrip().startswith("#")]
    sevhits = {}
    for m in SEV.finditer(txt):
        k = m.group(1).lower()
        sevhits[k] = sevhits.get(k, 0) + 1
    rows.append({
        "f": name, "bytes": size, "cls": "text",
        "nlines": len(lines),
        "head": head[:900],
        "headings": heads[:120],
        "sevcounts": sevhits,
    })

(out / "digest.json").write_text(json.dumps(rows, indent=1))
n_pdf = sum(1 for r in rows if r.get("cls") == "binary-pdf")
n_txt = sum(1 for r in rows if r.get("cls") == "text")
print("rows", len(rows), "pdf", n_pdf, "text", n_txt)
print("total text bytes", sum(r.get("bytes", 0) for r in rows if r.get("cls") == "text"))
