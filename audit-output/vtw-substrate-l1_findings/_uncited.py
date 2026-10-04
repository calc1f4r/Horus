import os, pathlib, json

root = pathlib.Path("/home/calc1f4r/Horus")
rep = root / "reports" / "substrate-l1_findings"
files = sorted(p.name for p in rep.iterdir() if p.is_file())

# Concatenate all DB markdown + json content once
blob = []
for p in (root / "DB").rglob("*"):
    if p.is_file() and p.suffix in (".md", ".json"):
        try:
            blob.append(p.read_text(errors="ignore"))
        except Exception:
            pass
blob = "\n".join(blob)

uncited = [f for f in files if f not in blob]
cited = [f for f in files if f in blob]

out = root / "audit-output" / "vtw-substrate-l1_findings"
(out / "uncited.txt").write_text("\n".join(uncited) + "\n")
(out / "cited.txt").write_text("\n".join(cited) + "\n")
print("total", len(files), "cited", len(cited), "uncited", len(uncited))
