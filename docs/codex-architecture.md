# Codex-Oriented Architecture

This document describes the repository as Codex should reason about it: what is source data, what is generated, which files are operationally important, and where the current repo has drift that affects maintenance.

For a runtime-neutral system overview, see [`agentic-workflow.md`](./agentic-workflow.md). This file is specifically about how Codex should interpret the repo.

## 1. System Summary

This repository combines seven distinct layers:

1. Horus, the curated vulnerability database in `DB/`.
2. A large raw finding corpus in `reports/`.
3. A supporting exploit corpus in `DeFiHackLabs/`.
4. Python automation in `scripts/` that turns DB Markdown into searchable indexes and hunt cards.
5. Graph artifacts built with graphify for DB traversal and per-audit codebase traversal.
6. Agent playbooks in `.claude/` and `.github/agents/` that use those artifacts for multi-phase audits.
7. Generated Codex-facing surfaces:
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
        scripts/build_db_graph.py
                    |
                    v
DB/graphify-out/graph.json
DB/graphify-out/GRAPH_REPORT.md
DB/graphify-out/wiki/*.md
                    |
                    v
graph-augmented search / variant analysis / sharded hunt-card auditing
                    |
                    v
.claude/* and .github/agents/* audit playbooks
                    |
                    v
generated .agents/skills/* + .codex/agents/* + .codex/resources/* + .codex/rules/* + .codex/config.toml
```

The core design principle is retrieval minimization: route first, then narrow to the smallest manifest or hunt-card set, then read exact line ranges from the Markdown entries only when needed.

The graph layer is additive. Agents still use the router, manifests, and hunt cards as the stable retrieval path, but they may expand topics through `DB/graphify-out/graph.json` before grep-pruning or use `audit-output/graph/graph.json` during a live audit to reason over code paths.

## 3. Directory Roles

### `DB/`

`DB/` is the product. It contains:

- Curated vulnerability entries in Markdown.
- `index.json`, the top-level search router.
- `manifests/*.json`, the pattern-level indexes with exact line ranges.
- `manifests/huntcards/*.json`, compressed detection cards for grep-first auditing.
- `SEARCH_GUIDE.md`, the intended search workflow.
- `graphify-out/`, the generated DB knowledge graph and wiki used for graph-augmented hunting.

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

- `scripts/generate_manifests.py`: builds the search system from DB Markdown.
- `db_quality_check.py`: validates DB structure, manifests, hunt cards, and routing.
- `grep_prune.py`: grep-prunes hunt cards against a target codebase.
- `partition_shards.py`: groups surviving cards into shard payloads.
- `merge_shard_findings.py`: merges and deduplicates shard findings.
- `build_db_graph.py`: builds the graphify DB graph from canonical hunt cards and manifests.
- `lessons_db.py`: stores opt-in cross-audit lessons in `~/.horus/lessons.db`.
- `horus_graphify_blockchain/`: local package for blockchain DSL AST extraction into graphify-compatible JSON.
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

The audit pipeline now also has a soft-gated Phase 0. Phase 0 builds a graphify codebase graph, merges optional `horus-graphify-blockchain` AST output, starts the graphify MCP server when available, initializes coverage logging, and optionally recalls user-approved cross-audit lessons.

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

### `DB/graphify-out/`

`DB/graphify-out/` is the generated graph view of the vulnerability DB.

Current v1 generation is deterministic:

```bash
python3 scripts/build_db_graph.py
```

It emits:

- `graph.json`: graphify-compatible node-link graph for CLI/MCP queries
- `GRAPH_REPORT.md`: god nodes, communities, and surprising connections
- `wiki/index.md`: agent-crawlable curated community index
- `.graphify_version`: pinned graphify package version

The DB graph is built from generated hunt cards plus manifest/frontmatter
metadata. It includes `HuntCard`, `DBEntry`, `Category`, `Manifest`,
`ProtocolContext`, `RootCauseFamily`, `AttackType`, `AffectedComponent`,
`GraphHint`, `ReportEvidence`, and `Severity` nodes. It also includes bounded
`related_variant` edges so graph expansion can move between related hunt cards
without relying only on broad category hubs.

The graph JSON and report preserve the full graph/community set. The wiki is
intentionally bounded to multi-node communities plus god-node articles so normal
graph rebuilds do not create hundreds of singleton community pages.

`graph.json` always means graphify node-link JSON. Raw extraction JSON such as
`.graphify_extract.json` is an intermediate file and must be converted before it
is served by graphify CLI/MCP. Audit-time graph finalization is handled by:

```bash
python3 scripts/finalize_audit_graph.py --codebase <path> --out audit-output/graph/graph.json
```

Do not hand-edit these artifacts. Rebuild them from the canonical DB hunt cards and manifests.

### `docs/`

`docs/` contains architecture, DB guidance, and repo structure explanations. These files are descriptive and useful, but they are not always perfectly synchronized with the generator, workflows, or file layout. When docs and code disagree, prefer the generator and workflows.

## 4. The Retrieval Architecture Codex Should Use

The repo is designed around a four-tier retrieval system plus an additive graph expansion layer.

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

### Graph Expansion Layer

Use `DB/graphify-out/graph.json` after choosing seed topics from the router or scope.

Examples:

```bash
graphify query "oracle staleness" --graph DB/graphify-out/graph.json --budget 2000
graphify path "oracle" "flash-loan" --graph DB/graphify-out/graph.json
```

The graph layer should expand candidate hunt cards and related vulnerability concepts through semantic edges such as root-cause family, attack type, affected component, graph hints, protocol context, report evidence, and `related_variant`. It should not prune away the baseline manifest or hunt-card set.

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

Before step 1, `invariant-catcher` may run graph expansion against `DB/graphify-out/graph.json` and write `audit-output/<id>/d1-graph-expansion.md`. The old grep path remains the fallback.

## 7. The Larger Audit Pipeline

The audit pipeline described in `.github/agents/audit-orchestrator.md` and `.claude/agents/audit-orchestrator.md` has these broad stages:

0. Graph foundation: graphify codebase graph, blockchain AST merge, MCP server, coverage log, optional memory recall
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

`attack-graph-synthesizer` runs after discovery when `audit-output/graph/graph.json` and `02-invariants-reviewed.md` exist. It enumerates graph paths and hyperedge compositions, then hands candidates to `protocol-reasoning`; it does not replace validation.

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
- `scripts/build_db_graph.py`
- `scripts/horus_graphify_blockchain/`
- `scripts/lessons_db.py`
- `docs/audit-orchestrator-flow.mmd`
- `invariants/`

### If the task is about report ingestion or corpus maintenance

Primary files:

- `reports/`
- `scripts/rebuild_report_artifacts.py`
- `.github/workflows/split-reports.yml`
- `.github/workflows/update-codebase-structure.yml`
- `scripts/update_codebase_structure.py`
- `.github/workflows/validate-retrieval-pipeline.yml`

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

## 10. Generated Surface Rules

The repo has multiple generated surfaces. The following contracts should inform future maintenance:

- `.claude/agents/` is the source for `.github/agents/`; regenerate the GitHub mirror with `python3 scripts/sync_codex_compat.py --sync-github-agents`.
- `.claude/resources/` and `.github/agents/resources/` are expected to stay byte-identical; `python3 scripts/sync_codex_compat.py --check` validates that mirror.
- `.agents/skills/` and `.codex/` are generated from `.claude/` plus sync-script defaults, so changes should flow `.claude/` -> `scripts/sync_codex_compat.py` -> generated outputs.
- `.github/agents/` is generated by `scripts/sync_codex_compat.py --sync-github-agents`; do not hand-edit generated mirror changes when `.claude/agents/` should be updated instead.
- `.claude/` is the main agent tree. `.github/agents/` is the GitHub-facing mirror.

## 11. Codex Working Recommendations

When operating in this repo, Codex should default to this workflow:

1. Identify whether the task targets content, retrieval, ingestion, or agent orchestration.
2. Open the narrowest canonical source file for that layer.
3. Avoid bulk reads of `reports/` and large DB Markdown files until a router, manifest, or hunt card narrows the search.
4. Edit authored sources rather than generated outputs.
5. Regenerate `.agents/skills/` and `.codex/` after `.claude/` changes with `python3 scripts/sync_codex_compat.py`.
6. Rebuild `DB/graphify-out/` with `python3 scripts/build_db_graph.py` after hunt-card or manifest changes that should affect graph traversal.
7. Regenerate and run the quality check after DB or generator changes.
8. Treat duplicated agent trees as a synchronization risk and verify the corresponding file in the other tree before finalizing edits.

That is the most accurate Codex-native architecture for the repository in its current state.
