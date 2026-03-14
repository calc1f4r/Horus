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
