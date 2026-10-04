---
name: findings-db-synthesizer
description: Close the DB flywheel by turning an engagement's judge-confirmed findings into DB entries, hunt cards, and invariant-library growth. Dedups against the existing DB first so enrichment beats duplication, anonymises client detail, extracts only fuzz/FV-validated invariants, and runs the generation contract honestly. Use after an audit report ships.
argument-hint: "<audit-output-dir>"
context: fork
agent: findings-db-synthesizer
disable-model-invocation: true
---

Synthesize DB growth from the completed audit at `$ARGUMENTS`.

## Verdict per finding

| Verdict | When |
|---------|------|
| `new-entry` | No existing DB entry shares the root cause |
| `enrich <entry-id>` | An entry shares the root cause — add keywords, detection pattern, or example |
| `skip (not generalizable)` | Fails the four-part generalizability test |

In a mature DB, enrichment should outnumber new entries.

## Hard rules

- Only CONFIRMED findings (or triaged HIGH/CRITICAL with a passing PoC) become entries
- Invalidated findings contribute misjudgment notes only
- No client identity in any entry — strip names, addresses, repo URLs
- Only fuzz/FV-validated or exploit-confirmed invariants enter `invariants/`
- Edit `DB/**/*.md` sources only, then regenerate — never hand-edit generated JSON

## Generation contract

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py     # only when hunt-card relationships changed
python3 scripts/db_quality_check.py
python3 -m pytest tests/ -q
```

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — same conventions, external source
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — DB health gate
- [/invariant-indexer](../invariant-indexer/SKILL.md) — invariant library conventions
