import json
import sys
from collections import Counter

stats = json.load(open(sys.argv[1]))
c = Counter()
z = Counter()
for s in stats:
    c[s["auditor"]] += 1
    if s["findings"] == 0:
        z[s["auditor"]] += 1
print(f"{'auditor':<22} {'files':>6} {'zero-parse':>11}")
for a, n in c.most_common():
    print(f"{a:<22} {n:>6} {z[a]:>11}")
