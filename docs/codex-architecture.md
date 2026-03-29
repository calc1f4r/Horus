# Codex-Oriented Architecture

This document describes the repository as Codex should reason about it: what is source data, what is generated, which files are operationally important, and where the current repo has drift that affects maintenance.

## 1. System Summary

This repository combines five distinct layers:

1. Horus, the curated vulnerability database in `DB/`.
2. A large raw finding corpus in `reports/`.
3. A supporting exploit corpus in `DeFiHackLabs/`.
4. Python automation in `scripts/` that turns DB Markdown into searchable indexes and hunt cards.
5. Agent playbooks in `.claude/` and `.github/agents/` that use those artifacts for multi-phase audits.
6. Generated Codex-facing surfaces:
   - `.agents/skills/` for repo-local Codex skills
   - `.codex/agents/` for repo-local Codex custom agents
   - `.codex/resources/` for shared Codex references
   - `.codex/rules/` for shared Codex rules
   - `.codex/config.toml` for repo-local Codex defaults such as live web search and nested delegation

The repo is therefore best understood as a knowledge system, not as a deployable app.

## 2. Architecture At A Glance

```text
reports/ + DeFiHackLabs/ + curated DB/*.md + invariants/
                    |
                    v
        scripts/generate_manifests.py
                    |
                    v
DB/index.json
DB/manifests/*.json
DB/manifests/huntcards/*.json
DB/manifests/keywords.json
                    |
                    v
search / variant analysis / sharded hunt-card auditing
                    |
                    v
.claude/* and .github/agents/* audit playbooks
                    |
                    v
generated .agents/skills/* + .codex/agents/* + .codex/resources/* + .codex/rules/* + .codex/config.toml
```

The core design principle is retrieval minimization: route first, then narrow to the smallest manifest or hunt-card set, then read exact line ranges from the Markdown entries only when needed.

## 3. Directory Roles

### `DB/`

`DB/` is the product. It contains:

- Curated vulnerability entries in Markdown.
- `index.json`, the top-level search router.
- `manifests/*.json`, the pattern-level indexes with exact line ranges.
- `manifests/huntcards/*.json`, compressed detection cards for grep-first auditing.
- `SEARCH_GUIDE.md`, the intended search workflow.

The unusual part of the DB architecture is that the physical folder layout and the logical search layout are not identical. In particular, `DB/general/` is split by the generator into four logical manifests:

- `general-security`
- `general-defi`
- `general-infrastructure`
- `general-governance`

That split is defined in `GENERAL_SUBCATEGORIES` inside `scripts/generate_manifests.py`, not by the folder tree alone.

### `reports/`

`reports/` is the raw corpus. It contains thousands of Markdown findings grouped by topic. It is an input corpus for research, entry creation, and evidence gathering, but it is too large to treat as normal always-on context.

The repo also uses a branch-splitting strategy for `reports/`:

- `.github/workflows/split-reports.yml` pushes each category to its own `reports/<branch>` branch.
- `scripts/update_codebase_structure.py` regenerates the branch table embedded in `docs/codebase-structure.md`.
- `scripts/rebuild_report_artifacts.py` rebuilds downloaded artifacts for a fetched report directory.

For Codex, the correct mental model is: `reports/` is archival source material, not the primary runtime surface.

### `DeFiHackLabs/`

`DeFiHackLabs/` is a git submodule pointing to the upstream exploit PoC repository. It acts as a second source corpus alongside `reports/`, especially for exploit-derived pattern extraction.

### `scripts/`

`scripts/` is the operational backbone of the repo. The most important scripts are:

- `generate_manifests.py`: builds the search system from DB Markdown.
- `db_quality_check.py`: validates DB structure, manifests, hunt cards, and routing.
- `grep_prune.py`: grep-prunes hunt cards against a target codebase.
- `partition_shards.py`: groups surviving cards into shard payloads.
- `merge_shard_findings.py`: merges and deduplicates shard findings.
- `migrate_to_new_template.py`: migrates legacy DB entries toward the current template.
- `generate_entries.py`: generates DB content from classified source data.
- `update_codebase_structure.py`: refreshes the report-branch section in docs.

For most maintenance tasks, if a change affects retrieval behavior, search semantics, or DB outputs, the real edit point is in `scripts/`, not in the generated JSON.

### `.claude/` and `.github/agents/`

These directories contain the audit-agent layer:

- agent definitions
- resource documents
- rules
- skills
- settings

They describe an 11-phase audit pipeline with context building, invariant extraction, DB-powered hunting, multi-persona reasoning, PoC writing, formal verification, and judging.

For Codex, these directories should be treated as procedural playbooks and specification documents, not as a runtime framework that Codex itself must obey automatically.

### `.agents/skills/`

`.agents/skills/` is the generated runtime discovery surface for Codex repo-local skills.

Each generated skill is derived from a `.claude/skills/<name>/SKILL.md` source and rewritten so Codex CLI can discover it directly.

### `.codex/agents/`

`.codex/agents/` is the generated runtime discovery surface for Codex custom agents.

Each generated TOML file is derived from a `.claude/agents/<name>.md` source and carries the delegated workflow as `developer_instructions`.

### `.codex/config.toml`

`.codex/config.toml` is the generated repo-level Codex runtime config.

It currently enables live web search for Codex sessions in this repo and raises agent nesting depth so spawned custom agents can delegate one level deeper.

### `.codex/resources/` and `.codex/rules/`

`.codex/resources/` and `.codex/rules/` are generated shared references that back the runtime skills and agents.

- `.claude/resources/` -> `.codex/resources/`
- `.claude/rules/` -> `.codex/rules/`

The source of truth remains `.claude/`. All generated Codex-facing runtime surfaces are regenerated by `scripts/sync_codex_compat.py`.

### `invariants/`

`invariants/` is a canonical invariant library used by the invariant-writing phase of the audit pipeline. It is reference material for audit generation, not part of the DB index build itself.

### `docs/`

`docs/` contains architecture, DB guidance, and repo structure explanations. These files are descriptive and useful, but they are not always perfectly synchronized with the generator, workflows, or file layout. When docs and code disagree, prefer the generator and workflows.

## 4. The Retrieval Architecture Codex Should Use

The repo is designed around a four-tier retrieval system.

### Tier 1: Router

Start with `DB/index.json`.

This file answers:

- which manifests exist
- which protocol contexts map to which manifests
- which focus patterns are relevant to each protocol type
- where the hunt cards live
- where the keyword index lives

It is the correct first read for search and audit tasks.

### Tier 1.5: Hunt Cards

Use `DB/manifests/huntcards/*.json` when auditing an external codebase or doing grep-first variant analysis.

Each hunt card compresses:

- a grep pattern
- a short detection statement
- micro-directive verification steps
- quick false-positive filters
- a pointer back to the full DB entry and exact line range

This is the most efficient audit interface when searching a target codebase.

### Tier 2: Manifests

Use `DB/manifests/*.json` when browsing patterns, filtering by severity, or locating exact content.

Each pattern entry contains:

- `id`
- `title`
- `lineStart`
- `lineEnd`
- `severity`
- `codeKeywords`
- `searchKeywords`
- `rootCause`

These files are the bridge between semantic lookup and exact Markdown reads.

### Tier 3: DB Markdown

Read `DB/**/*.md` only after the router or manifest has already narrowed the search to exact ranges.

The repo is explicitly designed to avoid full-file reads wherever possible.

## 5. How Generation Works

The generator parses DB Markdown and emits the searchable layers above it.

Key generator behaviors verified from `scripts/generate_manifests.py`:

- Markdown headings are parsed into section-level patterns.
- YAML frontmatter contributes grep-friendly and semantic search keywords.
- Structural headings are filtered out so they do not become search patterns.
- Some H3 and H4 sections are promoted when a top-level wrapper heading is too generic.
- `general/` content is split into multiple logical manifests via `GENERAL_SUBCATEGORIES`.
- `protocolContext` and `auditChecklist` are hard-coded in the generator.
- `keywords.json` is built from file paths, titles, code keywords, and search keywords.

This means that search behavior is partly data-driven and partly generator-driven. If retrieval looks wrong, inspect both the relevant DB entry and `scripts/generate_manifests.py`.

## 6. The Hunt-Card Audit Loop

The repo's concrete sharded audit loop is implemented in scripts, not just in prose:

1. `grep_prune.py`
   - runs each hunt-card grep pattern against a target repo
   - keeps cards with hits
   - also keeps `neverPrune` cards as a critical safety net

2. `partition_shards.py`
   - groups surviving cards by category tags
   - splits large groups into multiple shards
   - duplicates critical cards into every shard

3. `merge_shard_findings.py`
   - merges `03-findings-shard-*.md`
   - deduplicates by affected code plus root cause
   - renumbers findings for downstream use

This is the operational core of the DB-powered hunting system.

## 7. The Larger Audit Pipeline

The audit pipeline described in `.github/agents/audit-orchestrator.md` and `.claude/agents/audit-orchestrator.md` has these broad stages:

1. Reconnaissance
2. Context building
3. Invariant extraction and review
4. Iterative parallel discovery
5. Merge and triage
6. Optional PoC generation and execution
7. Optional formal verification generation and execution
8. Pre-judging
9. Issue polishing
10. Deep review
11. Final report assembly

For Codex, the important point is that the agent layer depends on the DB retrieval layer and the sharded hunt-card utilities. The DB is not an appendix to the agent system; it is the substrate that those agents consume.

## 8. Source Of Truth By Task

### If the task is about DB content

Primary files:

- `TEMPLATE.md`
- `Example.md`
- `docs/db-guide.md`
- `DB/**/*.md`
- `scripts/generate_manifests.py`

Validation:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
```

### If the task is about search accuracy or routing

Primary files:

- `scripts/generate_manifests.py`
- `DB/index.json`
- `DB/manifests/*.json`
- `DB/manifests/huntcards/*.json`

Generated files should usually be regenerated, not hand-patched.

### If the task is about audit orchestration

Primary files:

- `.agents/skills/*/SKILL.md`
- `.codex/agents/*.toml`
- `.codex/resources/**`
- `.codex/rules/**`
- `.codex/config.toml`
- `.claude/agents/*.md`
- `.github/agents/*.md`
- `.claude/resources/*`
- `.github/agents/resources/*`
- `scripts/grep_prune.py`
- `scripts/partition_shards.py`
- `scripts/merge_shard_findings.py`
- `invariants/`

### If the task is about report ingestion or corpus maintenance

Primary files:

- `reports/`
- `scripts/rebuild_report_artifacts.py`
- `.github/workflows/split-reports.yml`
- `.github/workflows/update-codebase-structure.yml`
- `scripts/update_codebase_structure.py`

## 9. What Is Generated Versus Authored

### Authored or manually maintained

- `DB/**/*.md`
- `TEMPLATE.md`
- `Example.md`
- `scripts/*.py`
- `.claude/**`
- `.github/**`
- `docs/**`
- `invariants/**`

### Generated or regeneration-derived

- `DB/index.json`
- `DB/manifests/*.json`
- `DB/manifests/huntcards/*.json`
- `DB/manifests/keywords.json`
- `.agents/**`
- `.codex/**`
- parts of `docs/codebase-structure.md` updated by script
- report artifact outputs under fetched report directories

Codex should prefer changing the authored source and regenerating the derivative files.

## 10. Verified Repo Drift And Caveats

The repo is workable, but the following drift is real and should inform future maintenance:

- The checked-in `.venv` points to a missing Homebrew Python 3.13 path on this machine. System `python3` works; `.venv/bin/python3` does not.
- The canonical generator is `scripts/generate_manifests.py`, but several docs and workflows still refer to a missing root `generate_manifests.py`.
- `scripts/db_quality_check.py` still checks for that missing root file, so part of its output is stale-path drift.
- `.claude/agents/` and `.github/agents/` are duplicated but not synchronized byte-for-byte.
- `.claude/resources/` and `.github/agents/resources/` also diverge in at least some files.
- `.agents/skills/` and `.codex/` are generated from `.claude/` plus sync-script defaults, so changes should flow `.claude/` -> `scripts/sync_codex_compat.py` -> generated outputs.
- Documentation alternates between treating `.claude/` and `.github/agents/` as the main agent tree, so Codex should inspect both when making cross-cutting agent changes.

## 11. Codex Working Recommendations

When operating in this repo, Codex should default to this workflow:

1. Identify whether the task targets content, retrieval, ingestion, or agent orchestration.
2. Open the narrowest canonical source file for that layer.
3. Avoid bulk reads of `reports/` and large DB Markdown files until a router, manifest, or hunt card narrows the search.
4. Edit authored sources rather than generated outputs.
5. Regenerate `.agents/skills/` and `.codex/` after `.claude/` changes with `python3 scripts/sync_codex_compat.py`.
6. Regenerate and run the quality check after DB or generator changes.
7. Treat duplicated agent trees as a synchronization risk and verify the corresponding file in the other tree before finalizing edits.

That is the most accurate Codex-native architecture for the repository in its current state.
