import re
import sys

p, needle = sys.argv[1], sys.argv[2]
before = int(sys.argv[3]) if len(sys.argv) > 3 else 500
after = int(sys.argv[4]) if len(sys.argv) > 4 else 200
LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}
t = open(p, encoding="utf-8", errors="replace").read()
for k, v in LIG.items():
    t = t.replace(k, v)
t = re.sub(r"\s+", " ", t)
for i, m in enumerate(re.finditer(re.escape(needle), t)):
    print(f"--- hit {i} ---")
    print(t[max(0, m.start() - before): m.end() + after])
    if i >= 2:
        break
