<!-- AUTO-GENERATED from `.claude/rules/reports.md`; source_sha256=a23eb78bb75d22bbd59387355fc0ba77fbc7c343bdfa6e4919e97eda52e3669a -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/reports.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "reports/**/*.md"
---

# Reports Directory Rules

When working with vulnerability reports in `reports/`:

- Reports are raw findings fetched from Solodit via `scripts/solodit_fetcher.py`
- Organized by topic: `reports/<topic>_findings/`
- Naming convention: `[severity]-[issue-number]-[description].md`
- Do not modify fetched reports — they are source data
- To add reports for a new topic, use the `solodit-fetching` skill or run `python3 scripts/solodit_fetcher.py`
- Reports are consumed by `variant-template-writer` to create DB entries
