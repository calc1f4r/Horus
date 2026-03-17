name: variant-template-writer
description: "Analyze security audit reports from reports/<topic>/ to identify cross-report vulnerability patterns and create TEMPLATE.md-compliant database entries optimized for vector search. Synthesizes 5-10+ reports per pattern. Use when synthesizing audit findings into DB entries, performing variant analysis, or creating vulnerability templates."
context: fork
agent: variant-template-writer
argument-hint: <topic>
---

Create DB entries from reports in `reports/$ARGUMENTS/`.

## What this does

1. **Read reports** — Loads all findings from `reports/$ARGUMENTS/`
2. **Pattern clustering** — Groups findings by root cause across auditors
3. **Severity consensus** — Determines severity from cross-auditor agreement
4. **Template generation** — Creates TEMPLATE.md-compliant entries with:
   - Frontmatter (title, severity, keywords, category)
   - Description and root cause analysis
   - Detection patterns (grep, code keywords)
   - Vulnerable and secure code examples
   - Real-world references from the source reports
5. **Vector search optimization** — Ensures entries are discoverable by hunt cards

## Output

- `DB/<category>/<subcategory>/<ENTRY_NAME>.md` — New vulnerability entries

After creating entries, run `python3 scripts/generate_manifests.py` to update manifests and hunt cards.

## Related skills

- [/solodit-fetching](../solodit-fetching/SKILL.md) — Fetches the reports this skill consumes
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — Validates the entries this skill creates
