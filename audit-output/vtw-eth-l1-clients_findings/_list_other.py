import json, re

rows = json.load(open('audit-output/vtw-eth-l1-clients_findings/raw-index.json'))
o = [r for r in rows if not re.match(r'^\d{5}-', r['f'])]
for r in o:
    print(r['bytes'], '|', r['f'][:80], '|', r['title'][:60])
print(len(o), 'other files')
