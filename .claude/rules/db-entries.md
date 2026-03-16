---
paths:
  - "DB/**/*.md"
  - "TEMPLATE.md"
  - "Example.md"
---

# Vulnerability Entry Rules

When editing or creating vulnerability entries in `DB/`:

- Follow the structure in `TEMPLATE.md` exactly — all required frontmatter fields and top-of-file low-context sections must be present
- When touching a legacy entry, migrate it to the current template instead of preserving the older layout
- Every entry needs: YAML frontmatter, `root_cause_family`, `pattern_key`, `code_keywords`, description, root cause, detection pattern, vulnerable code, secure code, and real-world references
- Multi-contract or multi-path entries also need `interaction_scope`, `involved_contracts`, and path-level keys / route separation
- Keep section titles and file names stable and specific so generated manifest pattern IDs remain meaningful
- Severity uses Impact × Likelihood matrix: CRITICAL, HIGH, MEDIUM, LOW
- Include concrete `grep`-able code keywords in frontmatter for hunt card generation
- Split materially different exploit routes into explicit path variants instead of blending them into one attack story
- Do not collapse issues that share a root cause but cross different contract boundaries or hop sets into one undifferentiated pattern
- After creating or modifying entries, regenerate manifests: `python3 generate_manifests.py`
- Never read entire vulnerability files when searching — use `DB/index.json` → manifests → line ranges
