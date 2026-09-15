import json, pathlib

out = pathlib.Path("/home/calc1f4r/Horus/audit-output/vtw-substrate-l1_findings")
rows = json.loads((out / "digest.json").read_text())
dupes = json.loads((out / "dupes.json").read_text())

size = {r["f"]: r["bytes"] for r in rows if r.get("cls") == "text"}
txt = set(size)

drop = {}  # dropped -> canonical
for grp in dupes["exact_dupe_groups"]:
    canon = sorted(grp, key=len)[0]          # prefer shorter human name
    for g in grp:
        if g != canon:
            drop[g] = canon
for a, b, r in dupes["near_dupes"]:
    canon, other = sorted([a, b], key=len)[0], sorted([a, b], key=len)[1]
    drop[other] = canon
# manual soft dupe: same Code4rena Phat Contract Runtime contest
drop["phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md"] = "phala-c4-2401.md"

canonical = sorted(txt - set(drop), key=lambda n: -size[n])

# greedy bin-pack into batches of roughly equal bytes
NB = 12
bins = [[] for _ in range(NB)]
tot = [0] * NB
for n in canonical:
    i = tot.index(min(tot))
    bins[i].append(n)
    tot[i] += size[n]

plan = {"canonical": canonical, "dropped": drop,
        "batches": [{"id": i + 1, "bytes": tot[i], "files": b} for i, b in enumerate(bins)]}
(out / "batches.json").write_text(json.dumps(plan, indent=1))
print("canonical", len(canonical), "dropped", len(drop))
for i, b in enumerate(bins):
    print(f"batch {i+1:>2}  {tot[i]:>7}B  {len(b)} files")
    for f in b:
        print("     ", f)
