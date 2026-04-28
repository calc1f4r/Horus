# Codex Working Guide

This repository is not a conventional application. It is a security knowledge base plus the automation and agent playbooks that turn that knowledge base into an audit workflow.

Use this file as the Codex entry point. For the full system map, read `docs/codex-architecture.md`.

## What Is Canonical

- `DB/**/*.md`: primary vulnerability content.
- `scripts/generate_manifests.py`: canonical generator for `DB/index.json`, `DB/manifests/*.json`, and `DB/manifests/huntcards/*.json`.
- `scripts/build_db_graph.py`: canonical generator for `DB/graphify-out/graph.json`, `GRAPH_REPORT.md`, and graph wiki artifacts.
- `TEMPLATE.md`: required structure for new or migrated DB entries.
- `scripts/db_quality_check.py`: structural verification for the DB and search artifacts.
- `DB/index.json`: runtime router for search, but generated from DB content plus generator logic.
- `DB/graphify-out/graph.json`: generated DB knowledge graph used for graph-augmented hunt-card expansion.
- `.claude/skills`, `.claude/agents`, `.claude/resources`, `.claude/rules`: source of truth for the portable audit playbooks.
- `.agents/skills/`: generated repo-local Codex skills derived from `.claude/skills/`.
- `.codex/agents/`: generated repo-local Codex custom agents derived from `.claude/agents/`.
- `.codex/resources/`: generated shared Codex references derived from `.claude/resources/`.
- `.codex/rules/`: generated shared Codex rules derived from `.claude/rules/`.
- `.codex/config.toml`: generated repo-local Codex runtime defaults for live web search and nested subagent delegation.

Do not hand-edit generated manifest or hunt-card JSON unless the user explicitly asks for that. Change the source Markdown or the generator instead.
Do not hand-edit generated files under `.agents/skills/` or `.codex/`. Change the source `.claude/` files or the sync script, then regenerate.

## Repo Mental Model

1. Sources
   - `reports/`: raw audit findings corpus.
   - `DeFiHackLabs/`: exploit PoC submodule.
   - `DB/**/*.md`: curated vulnerability patterns.
   - `invariants/`: canonical invariant library used by the audit pipeline.

2. Indexing layer
   - `scripts/generate_manifests.py` parses `DB/**/*.md`.
   - It emits `DB/index.json`, `DB/manifests/*.json`, `DB/manifests/huntcards/*.json`, and keyword routing.
   - `scripts/build_db_graph.py` turns generated hunt cards/manifests into `DB/graphify-out/**` graph artifacts.

3. Consumption layer
   - Agents and tooling start from `DB/index.json`.
   - They then load per-manifest hunt cards or manifests.
   - They may query `DB/graphify-out/graph.json` to expand related hunt cards before grep-pruning.
   - They read targeted line ranges from DB Markdown only after narrowing scope.

4. Audit workflow layer
   - `scripts/grep_prune.py`, `scripts/partition_shards.py`, and `scripts/merge_shard_findings.py` implement the DB-powered hunting loop.
   - `.claude/` and `.github/agents/` contain agent playbooks for the larger multi-phase audit pipeline.
   - `.agents/skills/`, `.codex/agents/`, `.codex/resources/`, `.codex/rules/`, and `.codex/config.toml` are the generated Codex runtime surfaces.

## Start Here By Task

### Search or variant analysis

- Read `DB/index.json` first.
- Prefer `DB/manifests/huntcards/<manifest>-huntcards.json` over reading large Markdown files directly.
- Use `DB/manifests/*.json` for exact `lineStart` and `lineEnd`.
- Read only the relevant lines from the target DB entry.
- If `DB/graphify-out/graph.json` exists, use `graphify query "<topic>" --graph DB/graphify-out/graph.json` to add neighboring hunt cards; do not use graph results to remove baseline cards.

### Add or edit a vulnerability entry

- Read `TEMPLATE.md` and `Example.md`.
- Follow `docs/db-guide.md` for the tiered search and authoring workflow.
- If you touch `DB/**/*.md`, run:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
```

### Change routing, manifests, or hunt-card behavior

- Edit `scripts/generate_manifests.py`.
- Regenerate outputs.
- Rebuild the DB graph if hunt-card relationships should change:

```bash
python3 scripts/build_db_graph.py
```

- Verify the resulting router, manifests, and hunt cards with `scripts/db_quality_check.py`.

### Work on raw reports or report artifacts

- Treat `reports/` as a large corpus, not as normal always-loaded context.
- `scripts/rebuild_report_artifacts.py` rebuilds downloadable artifacts for one fetched report directory.
- `.github/workflows/split-reports.yml` and `scripts/update_codebase_structure.py` maintain the per-category branch strategy and docs table.

### Work on the audit pipeline

- For Codex CLI runtime use, start with `.agents/skills/<name>/SKILL.md`, `.codex/agents/<name>.toml`, and `.codex/config.toml`.
- Read `.codex/resources/*` and `.codex/rules/*` only when the selected skill or agent references them.
- If you are changing the source playbooks, edit `.claude/` and rerun `python3 scripts/sync_codex_compat.py`.
- Read `.github/agents/audit-orchestrator.md` or `.claude/agents/audit-orchestrator.md` when you need to compare the source trees directly.
- Read `invariants/README.md` for the invariant library role.
- Read `scripts/grep_prune.py`, `scripts/partition_shards.py`, and `scripts/merge_shard_findings.py` for the concrete sharded hunt-card loop.
- Read `docs/audit-orchestrator-flow.mmd` for the graph-aware Phase 0 + discovery flow.

## Rules Codex Should Follow Here

- Do not read all of `reports/` or all DB Markdown files when the router/manifests/hunt cards can narrow the search first.
- Do not hand-edit generated manifest or hunt-card files during normal maintenance.
- Do not hand-edit generated files under `.agents/skills/` or `.codex/`; regenerate them from `.claude/` with `python3 scripts/sync_codex_compat.py`.
- If you modify a DB entry, assume manifest regeneration is required.
- If you modify Claude playbooks, regenerate the Codex-facing outputs and verify them with `python3 scripts/sync_codex_compat.py --check`.
- If the GitHub-facing agent docs should match the Claude playbooks, update the corresponding `.github/agents/**` files explicitly; the Codex sync script does not generate `.github/agents`.
- If you modify agent docs, inspect both `.claude/` and `.github/` copies before deciding what to change.
- Prefer `python3` directly unless the virtualenv has been repaired locally.

## Known Inconsistencies

- `.venv` exists, but its Python symlink points to a missing Homebrew Python 3.13 install on this machine. Use system `python3` unless you recreate the venv.
- The real generator is `scripts/generate_manifests.py`, but several docs and workflows still reference a missing root `generate_manifests.py`.
- `.claude/agents` and `.github/agents` are duplicated but not byte-identical.
- `.claude/resources` and `.github/agents/resources` are also not perfectly synchronized.
- `.agents/skills/` and `.codex/` are intentionally generated from `.claude/`, not from `.github/agents/`.
- `scripts/db_quality_check.py` currently checks for a missing root `generate_manifests.py`, so part of its current "BROKEN" summary is repository drift rather than a Codex incompatibility issue.

## Useful Commands

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py
python3 scripts/db_quality_check.py
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --check
python3 scripts/grep_prune.py <target_path> DB/manifests/huntcards/all-huntcards.json
python3 scripts/partition_shards.py audit-output/hunt-card-hits.json
python3 scripts/merge_shard_findings.py audit-output
python3 scripts/update_codebase_structure.py
```

## Deep Reference

- `docs/codex-architecture.md`: Codex-oriented architecture document for this repository.
- `.codex/config.toml`: generated Codex runtime defaults for live web search and nested delegation.
- `.agents/skills/`: generated repo-local Codex skills.
- `.codex/agents/`: generated repo-local Codex custom agents.
- `.codex/resources/`: generated shared Codex references.
- `.codex/rules/`: generated shared Codex rules.
