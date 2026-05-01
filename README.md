<div align="center">

# Horus

**A portable agentic workflow for smart contract auditing.**

Horus is a security knowledge system built so multiple agent runtimes can work from the same database, the same retrieval discipline, and the same audit playbooks.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Patterns](https://img.shields.io/badge/patterns-1%2C972-brightgreen)](DB/manifests)
[![Manifests](https://img.shields.io/badge/manifests-14-orange)](DB/manifests)
[![Hunt Cards](https://img.shields.io/badge/hunt%20cards-1%2C362-red)](DB/manifests/huntcards)
[![Graph](https://img.shields.io/badge/graph-5%2C270%20nodes-informational)](DB/graphify-out/graph.json)
[![Agents](https://img.shields.io/badge/agents-38-blueviolet)](.github/agents)
[![Reports](https://img.shields.io/badge/raw%20reports-22%2C200%2B-yellow)](reports)

</div>

---

## What This Repo Actually Is

Horus is not a normal app and it is not just a prompt collection.

It is a layered system:

1. Knowledge sources: curated vulnerability entries in `DB/`, raw findings in `reports/`, exploit PoCs in `DeFiHackLabs/`, and reference properties in `invariants/`.
2. Retrieval layer: generated routers, manifests, keyword indexes, hunt cards, and graph artifacts that let agents narrow context before reading long-form content.
3. Workflow layer: reusable audit playbooks, skills, rules, and shared references.
4. Runtime layer: runtime-specific entrypoints and generated surfaces for Claude, Codex, GitHub, Gemini CLI, and editor-based agents.
5. Execution layer: grep-prune, shard partitioning, merge, PoC, fuzzing, formal verification, and judging flows.

The purpose of the repo is to let different agents execute the same audit workflow instead of forcing every runtime to rediscover the methodology from scratch.

---

## Why Horus Exists

Most AI audit systems fail in one of two ways:

- they have a big corpus but no disciplined way to retrieve only what matters
- they have a sophisticated prompt but no durable knowledge substrate or reproducible workflow

Horus couples those pieces together:

- retrieval is route-first and grep-first
- DB entries are indexed into compact machine-usable artifacts
- Graphify-compatible graph output adds related-variant expansion without replacing route-first retrieval
- the audit lifecycle is encoded as reusable agent playbooks
- those playbooks are exposed through multiple runtime surfaces

The result is a repo that can support quick lookups, variant analysis, and full multi-phase audits.

---

## Runtime Compatibility

The compatibility model is deliberate. Some runtimes have native surfaces here; others consume the same playbooks as workspace instructions.

| Runtime | Support Model | Primary Surface |
|---|---|---|
| Claude Code | Native source runtime | [`CLAUDE.md`](CLAUDE.md), [`.claude/agents/`](.claude/agents), [`.claude/skills/`](.claude/skills), [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) |
| Codex CLI | Native generated runtime | [`AGENTS.md`](AGENTS.md), [`.agents/skills/`](.agents/skills), [`.codex/agents/`](.codex/agents), [`.codex/config.toml`](.codex/config.toml) |
| GitHub-facing agent docs | Generated repo-native mirror | [`.github/agents/`](.github/agents) |
| Gemini CLI | Native workspace instructions & skills | [`GEMINI.md`](GEMINI.md), [`.agents/skills/`](.agents/skills) |
| Cursor | Portable workspace consumption | [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), [`.claude/agents/`](.claude/agents) |
| VS Code | Portable workspace consumption | [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), [`GEMINI.md`](GEMINI.md), [`.claude/agents/`](.claude/agents) |

Key rule:

- `.claude/` is the canonical workflow source tree
- `.agents/skills/` and `.codex/` are generated from `.claude/`
- `.github/agents/` is generated from `.claude/agents/` as the GitHub-facing documentation/runtime mirror
- Cursor and VS Code consume the repo through these instruction files and playbooks, not through a dedicated generated integration layer

---

## System Map

```text
Knowledge Sources
DB/ + reports/ + DeFiHackLabs/ + invariants/
            |
            v
Retrieval Generation
scripts/generate_manifests.py
            |
            v
DB/index.json
DB/manifests/*.json
DB/manifests/huntcards/*.json
DB/manifests/keywords.json
            |
            v
Graph Generation
scripts/build_db_graph.py
            |
            v
DB/graphify-out/graph.json
DB/graphify-out/GRAPH_REPORT.md
            |
            v
Audit Workflow Playbooks
.claude/agents/ + .claude/skills/ + .claude/resources/ + .claude/rules/
            |
            +------------------------------+
            |                              |
            v                              v
Runtime Entry Points                  Codex Compatibility Generation
CLAUDE.md                             scripts/sync_codex_compat.py
AGENTS.md                             -> .agents/skills/
GEMINI.md                             -> .codex/agents/
.github/agents/                       -> .codex/resources/
                                       -> .codex/rules/
                                       -> .codex/config.toml
```

---

## Retrieval Architecture

Horus is designed around retrieval minimization.

```text
Tier 1    DB/index.json
Tier 1.5  DB/manifests/huntcards/*.json
Tier 2    DB/manifests/*.json
Tier 2.5  DB/graphify-out/graph.json
Tier 3    DB/**/*.md
```

How agents should use it:

1. Start with [`DB/index.json`](DB/index.json).
2. Resolve relevant manifests from protocol context or keywords.
3. Use hunt cards to grep the target codebase and prune irrelevant patterns.
4. Optionally expand related variants through [`DB/graphify-out/graph.json`](DB/graphify-out/graph.json). Do not use graph results to remove baseline hunt cards.
5. Use manifests to resolve exact `lineStart` and `lineEnd` ranges.
6. Read only those targeted DB Markdown ranges.

This is the central design constraint of the repo. Reading all DB files or all reports directly defeats the architecture.

---

## End-To-End Audit Workflow

The large-scale workflow is encoded in the agent system and concrete helper scripts.

### Foundation

1. Reconnaissance: detect protocol shape, scope, languages, and likely manifests.
2. Context building: analyze contracts/functions and produce system context.
3. Invariant extraction: write and review system properties before discovery deepens.

### Discovery

4. DB-powered hunting: grep-prune hunt cards, shard surviving cards, and run parallel variant hunts.
5. Reasoning discovery: run deeper domain reasoning against the same target.
6. Multi-persona analysis: audit from multiple mental models in parallel.
7. Validation-gap hunting: explicitly search for missing checks and hygiene issues.

### Triage And Proof

8. Merge and triage candidate findings.
9. Generate PoCs where useful.
10. Generate fuzzing or formal verification artifacts where useful.

### Judging And Reporting

11. Pre-judge findings.
12. Polish valid findings.
13. Deep-review polished issues.
14. Assemble a final report containing only findings that survived the verification loop.

The workflow is agent-driven, but it is also script-backed. The sharded hunt-card loop lives in:

- [`scripts/grep_prune.py`](scripts/grep_prune.py)
- [`scripts/partition_shards.py`](scripts/partition_shards.py)
- [`scripts/merge_shard_findings.py`](scripts/merge_shard_findings.py)

Graph-aware audit setup also uses:

- [`scripts/build_db_graph.py`](scripts/build_db_graph.py)
- [`scripts/finalize_audit_graph.py`](scripts/finalize_audit_graph.py)

For a longer walkthrough, see [`docs/agentic-workflow.md`](docs/agentic-workflow.md).

---

## Source Of Truth vs Generated Surfaces

This distinction is critical for maintenance.

### Canonical Inputs

- [`DB/**/*.md`](DB)
- [`TEMPLATE.md`](TEMPLATE.md)
- [`Example.md`](Example.md)
- [`scripts/generate_manifests.py`](scripts/generate_manifests.py)
- [`.claude/agents/`](.claude/agents)
- [`.claude/skills/`](.claude/skills)
- [`.claude/resources/`](.claude/resources)
- [`.claude/rules/`](.claude/rules)

### Generated Outputs

- [`DB/index.json`](DB/index.json)
- [`DB/manifests/*.json`](DB/manifests)
- [`DB/manifests/huntcards/*.json`](DB/manifests/huntcards)
- [`DB/graphify-out/graph.json`](DB/graphify-out/graph.json)
- [`DB/graphify-out/GRAPH_REPORT.md`](DB/graphify-out/GRAPH_REPORT.md)
- [`.agents/skills/`](.agents/skills)
- [`.codex/agents/`](.codex/agents)
- [`.codex/resources/`](.codex/resources)
- [`.codex/rules/`](.codex/rules)
- [`.codex/config.toml`](.codex/config.toml)
- [`.github/agents/`](.github/agents)

Normal maintenance rule:

- do not hand-edit generated manifests or hunt cards
- do not hand-edit generated graph artifacts
- do not hand-edit generated Codex runtime files
- do not hand-edit generated GitHub agent mirrors
- update the source content or source playbooks, then regenerate

---

## Fine-Grained Repo Guide

| Area | Role |
|---|---|
| [`DB/`](DB) | Curated vulnerability database and generated search artifacts |
| [`reports/`](reports) | Large raw finding corpus used for research and entry creation |
| [`DeFiHackLabs/`](DeFiHackLabs) | Exploit corpus submodule used for exploit-derived patterns |
| [`invariants/`](invariants) | Canonical invariant reference library |
| [`scripts/`](scripts) | Generators, validators, shard tools, migration utilities, runtime sync |
| [`.claude/`](.claude) | Canonical playbooks, skills, rules, and shared references |
| [`.github/agents/`](.github/agents) | Generated GitHub-facing agent definitions plus resource parity mirror |
| [`.agents/skills/`](.agents/skills) | Generated Codex repo-local skills |
| [`.codex/`](.codex) | Generated Codex agents, resources, rules, and config |
| [`CLAUDE.md`](CLAUDE.md) | Claude entry instructions |
| [`AGENTS.md`](AGENTS.md) | Codex entry instructions |
| [`GEMINI.md`](GEMINI.md) | Gemini CLI entry instructions |
| [`docs/`](docs) | Architecture, DB, workflow, and repo reference docs |

---

## Main Agent Families

| Family | Representative Agents | Purpose |
|---|---|---|
| Orchestration | `audit-orchestrator`, `audit-context-building`, `system-synthesizer` | Coordinate the full audit lifecycle |
| Invariants | `invariant-writer`, `invariant-reviewer`, `invariant-indexer` | Define and harden expected system properties |
| Discovery | `invariant-catcher`, `protocol-reasoning`, `finding-chain-synthesizer`, `missing-validation-reasoning` | Find issues using DB lookup, reasoning, and confirmed-finding composition |
| Multi-persona | `persona-bfs`, `persona-dfs`, `persona-mirror`, `persona-state-machine` | Attack the same target from different analysis styles |
| Proof / Reporting | `poc-writing`, `issue-writer`, `report-aggregator` | Prove and package findings |
| Formal verification | `chimera-setup`, `medusa-fuzzing`, `halmos-verification`, `certora-verification` | Produce harnesses and formal specs |
| Judging | `sherlock-judging`, `cantina-judge`, `code4rena-judge`, `judge-orchestrator` | Validate reportability and severity |
| DB maintenance | `variant-template-writer`, `defihacklabs-indexer`, `solodit-fetching`, `db-quality-monitor` | Expand and maintain the knowledge base |

The canonical source playbooks live in [`.claude/agents/`](.claude/agents). The Codex-generated mirrors live in [`.codex/agents/`](.codex/agents), and the GitHub-facing mirrors live in [`.github/agents/`](.github/agents).

---

## Start Here By Runtime

### Claude Code

Start with [`CLAUDE.md`](CLAUDE.md). For plugin-oriented usage, the repo also ships [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json).

### Codex CLI

Start with [`AGENTS.md`](AGENTS.md). The generated runtime surface is in [`.agents/skills/`](.agents/skills) and [`.codex/`](.codex).

### GitHub-Facing Agent Docs

Start with [`.github/agents/`](.github/agents). These files are generated from [`.claude/agents/`](.claude/agents); edit the Claude source first when changing behavior.

### Gemini CLI

Start with [`GEMINI.md`](GEMINI.md). Gemini uses these instructions along with the `activate_skill` tool to dynamically load workflows from `.agents/skills/`.

### Cursor / VS Code

Treat the repo as a workspace-local playbook package:

1. start with [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), or [`GEMINI.md`](GEMINI.md)
2. open the relevant source playbook in [`.claude/agents/`](.claude/agents)
3. follow the same tiered retrieval flow from router to hunt cards to exact DB line reads

---

## Start Here By Task

### Search the DB or do variant analysis

1. Read [`DB/index.json`](DB/index.json).
2. Load relevant hunt cards or manifests.
3. Resolve exact line ranges from manifests.
4. Read only the matching DB entry slice.

### Run a full audit

Start from the orchestrator for the runtime you are using:

- Claude: [`.claude/agents/audit-orchestrator.md`](.claude/agents/audit-orchestrator.md)
- Codex: [`.codex/agents/audit-orchestrator.toml`](.codex/agents/audit-orchestrator.toml)
- GitHub-facing docs: [`.github/agents/audit-orchestrator.md`](.github/agents/audit-orchestrator.md)

### Add or edit a DB entry

1. Read [`TEMPLATE.md`](TEMPLATE.md) and [`Example.md`](Example.md).
2. Edit the DB source Markdown.
3. Regenerate manifests and hunt cards.
4. Run quality checks.

### Change routing or manifest behavior

Edit [`scripts/generate_manifests.py`](scripts/generate_manifests.py), then regenerate outputs.

### Change graph behavior

Edit [`scripts/build_db_graph.py`](scripts/build_db_graph.py), then rebuild [`DB/graphify-out/`](DB/graphify-out).

### Change runtime playbooks

Edit the canonical `.claude/` sources, then regenerate the Codex-compatible and GitHub-facing generated surfaces.

---

## Common Commands

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py
python3 scripts/db_quality_check.py
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --sync-github-agents
python3 scripts/sync_codex_compat.py --check
python3 scripts/validate_codex_runtime.py
python3 scripts/validate_retrieval_pipeline.py
python3 scripts/grep_prune.py <target_path> DB/manifests/huntcards/all-huntcards.json
python3 scripts/partition_shards.py audit-output/hunt-card-hits.json
python3 scripts/merge_shard_findings.py audit-output
python3 scripts/update_codebase_structure.py
```

---

## Documentation Map

| Doc | Use It For |
|---|---|
| [`docs/agentic-workflow.md`](docs/agentic-workflow.md) | End-to-end system and workflow overview |
| [`docs/codex-architecture.md`](docs/codex-architecture.md) | Codex-oriented explanation of source, generated, and runtime surfaces |
| [`docs/GRAPHIFY_RETRIEVAL_REPAIR_PLAN.md`](docs/GRAPHIFY_RETRIEVAL_REPAIR_PLAN.md) | Completed Graphify, retrieval, validation, and generated-surface repair plan |
| [`docs/codebase-structure.md`](docs/codebase-structure.md) | Detailed directory-by-directory repo map |
| [`docs/db-guide.md`](docs/db-guide.md) | DB authoring, search, and hunt-card workflows |
| [`AGENTS.md`](AGENTS.md) | Codex working guide |
| [`CLAUDE.md`](CLAUDE.md) | Claude working guide |
| [`GEMINI.md`](GEMINI.md) | Gemini CLI working guide |

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

If you change DB source files, regenerate manifests and rebuild the graph when relationships may change. If you change `.claude/` playbooks, regenerate the Codex-facing outputs and GitHub-facing mirrors. Prefer updating canonical sources over patching generated artifacts directly.

---

## License

MIT. See [`LICENSE`](LICENSE).
