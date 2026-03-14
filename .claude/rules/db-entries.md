---
paths:
  - "DB/**/*.md"
---

# Vulnerability Entry Rules

When editing or creating vulnerability entries in `DB/`:

- Follow the structure in `TEMPLATE.md` exactly — all required frontmatter fields must be present
- Every entry needs: YAML frontmatter, description, root cause, detection pattern, vulnerable code, secure code, and real-world references
- Use unique pattern IDs: `<manifest>-<category>-NNN` (e.g., `oracle-staleness-001`)
- Severity uses Impact × Likelihood matrix: CRITICAL, HIGH, MEDIUM, LOW
- Include concrete `grep`-able code keywords in frontmatter for hunt card generation
- After creating or modifying entries, regenerate manifests: `python3 generate_manifests.py`
- Never read entire vulnerability files when searching — use `DB/index.json` → manifests → line ranges
