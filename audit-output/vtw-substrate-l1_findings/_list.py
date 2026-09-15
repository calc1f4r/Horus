import json, pathlib
out = pathlib.Path("/home/calc1f4r/Horus/audit-output/vtw-substrate-l1_findings")
rows = json.loads((out / "digest.json").read_text())
txt = [r for r in rows if r.get("cls") == "text"]
txt.sort(key=lambda r: -r["bytes"])
for r in txt:
    sc = r["sevcounts"]
    s = " ".join(f"{k}:{v}" for k, v in sorted(sc.items(), key=lambda x: -x[1])[:5])
    print(f'{r["bytes"]:>8} {r["nlines"]:>6}  {r["f"]}  [{s}]  hd={len(r["headings"])}')
