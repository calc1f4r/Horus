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
- `scripts/build_db_graph.py` is the canonical DB graph generator — run it after hunt-card/manifest changes that should affect graph traversal
- `scripts/lessons_db.py` manages opt-in cross-audit memory at `~/.horus/lessons.db`
- `scripts/horus_graphify_blockchain/` is the local blockchain DSL extractor package that emits graphify-compatible AST JSON for Phase 0
- `scripts/solodit_fetcher.py` fetches from the Cyfrin Solodit API — never apply quality filters
- `scripts/grep_prune.py` — prunes manifest patterns via grep matching; part of the 4-tier search pipeline
- `scripts/partition_shards.py` — splits audit findings into per-shard files for parallel agent processing
- `scripts/merge_shard_findings.py` — merges shard outputs back into the consolidated report
- `scripts/db_quality_check.py` — validates DB entry structure and frontmatter completeness
- `scripts/generate_entries.py` — generates new DB entries from fetched reports
- Scripts in `scripts/` are utilities: classification, conversion, quality checks
- Do not add dependencies without updating `requirements.txt`
