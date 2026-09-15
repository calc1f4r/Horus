import json, pathlib, re, hashlib, difflib

root = pathlib.Path("/home/calc1f4r/Horus")
rep = root / "reports" / "substrate-l1_findings"
out = root / "audit-output" / "vtw-substrate-l1_findings"
rows = json.loads((out / "digest.json").read_text())
txt = [r["f"] for r in rows if r.get("cls") == "text"]

def body(name):
    t = (rep / name).read_text(errors="ignore")
    # strip YAML frontmatter
    if t.startswith("---"):
        parts = t.split("---", 2)
        if len(parts) == 3:
            t = parts[2]
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

bodies = {n: body(n) for n in txt}
hashes = {}
for n, b in bodies.items():
    hashes.setdefault(hashlib.sha1(b.encode()).hexdigest(), []).append(n)

exact = {h: v for h, v in hashes.items() if len(v) > 1}

# near-duplicate detection among remaining
singles = sorted([v[0] for v in hashes.values() if len(v) == 1], key=lambda n: -len(bodies[n]))
near = []
used = set()
for i, a in enumerate(singles):
    if a in used:
        continue
    for b in singles[i + 1:]:
        if b in used:
            continue
        la, lb = len(bodies[a]), len(bodies[b])
        if min(la, lb) / max(la, lb) < 0.9:
            continue
        r = difflib.SequenceMatcher(None, bodies[a][:120000], bodies[b][:120000]).quick_ratio()
        if r > 0.97:
            r2 = difflib.SequenceMatcher(None, bodies[a][:60000], bodies[b][:60000]).ratio()
            if r2 > 0.93:
                near.append((a, b, round(r2, 4)))
                used.add(b)

res = {"exact_dupe_groups": list(exact.values()), "near_dupes": near}
(out / "dupes.json").write_text(json.dumps(res, indent=1))
print("exact groups:", len(exact))
for v in exact.values():
    print("  EXACT", v)
print("near pairs:", len(near))
for a, b, r in near:
    print(f"  NEAR {r} {a}  <->  {b}")
