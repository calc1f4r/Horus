---
paths:
  - "reports/**/*.md"
---

# Reports Directory Rules

When working with vulnerability reports in `reports/`:

- Reports are raw findings fetched from Solodit via `solodit_fetcher.py`
- Organized by topic: `reports/<topic>_findings/`
- Naming convention: `[severity]-[issue-number]-[description].md`
- Do not modify fetched reports — they are source data
- To add reports for a new topic, use the `solodit-fetching` skill or run `python3 solodit_fetcher.py`
- Reports are consumed by `variant-template-writer` to create DB entries
