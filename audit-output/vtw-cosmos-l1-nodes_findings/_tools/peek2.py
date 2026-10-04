import sys, re

p = sys.argv[1]
needle = sys.argv[2]
occ = int(sys.argv[3]) if len(sys.argv) > 3 else 2
n = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
t = open(p, encoding="utf-8", errors="replace").read()
# collapse single-word-per-line into flowing text for readability
idxs = [m.start() for m in re.finditer(re.escape(needle), t)]
print("occurrences:", len(idxs))
if not idxs:
    sys.exit()
i = idxs[min(occ, len(idxs)) - 1]
chunk = t[i:i + n]
chunk = re.sub(r"\n(?!\n)", " ", chunk)
print(chunk)
