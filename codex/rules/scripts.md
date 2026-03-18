<!-- AUTO-GENERATED from `.claude/rules/scripts.md`; source_sha256=1ccede4996ebac8807a2a73fac56cfe07ee5bea1f082df90f16658f4908537d2 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/scripts.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "scripts/**/*.py"
  - "generate_manifests.py"
---

# Python Script Rules

When editing Python scripts in this repo:

- Use `python3` explicitly (not `python`)
- Always activate venv first: `source .venv/bin/activate`
- `scripts/generate_manifests.py` is the canonical manifest generator — changes here affect the entire 4-tier search system
- `scripts/solodit_fetcher.py` fetches from the Cyfrin Solodit API — never apply quality filters
- `scripts/grep_prune.py` — prunes manifest patterns via grep matching; part of the 4-tier search pipeline
- `scripts/partition_shards.py` — splits audit findings into per-shard files for parallel agent processing
- `scripts/merge_shard_findings.py` — merges shard outputs back into the consolidated report
- `scripts/db_quality_check.py` — validates DB entry structure and frontmatter completeness
- `scripts/generate_entries.py` — generates new DB entries from fetched reports
- Scripts in `scripts/` are utilities: classification, conversion, quality checks
- Do not add dependencies without updating `requirements.txt`
