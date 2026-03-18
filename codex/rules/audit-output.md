<!-- AUTO-GENERATED from `.claude/rules/audit-output.md`; source_sha256=088255ce83016993094a8af2a31fae0d170aa41eb5a96318e8d26280ebe5418a -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/audit-output.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "audit-output/**"
---

# Audit Output Rules

When working with files in `audit-output/`:

- This directory is the filesystem-based communication channel between pipeline agents
- `pipeline-state.md` tracks overall pipeline progress — update it as phases complete
- Phase artifacts follow naming: `00-scope.md`, `01-context.md`, `02-invariants.md`, etc.
- `CONFIRMED-REPORT.md` is the final deliverable — only judge-verified findings go here
- Per-shard findings go in `03-findings-shard-<id>.md`
- Persona outputs go in `personas/round-N/<persona>.md`
- PoC files go in `pocs/F-NNN-poc.{ext}`
- Polished issues go in `issues/F-NNN-issue.md`
- Do not delete audit-output during an active pipeline run
