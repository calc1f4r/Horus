# Agentic Workflow

This document explains Horus as a full system rather than as a single runtime integration.

If you want the short version, start with [`README.md`](../README.md). If you want Codex-specific operating guidance, read [`AGENTS.md`](../AGENTS.md). If you want DB authoring and search guidance, read [`docs/db-guide.md`](./db-guide.md).

## 1. The System In One Sentence

Horus is a portable audit workflow that combines:

- a curated vulnerability database
- a retrieval layer that minimizes unnecessary context
- a graph layer that connects DB patterns and live code paths
- a reusable multi-agent audit pipeline
- runtime-specific delivery surfaces for different agent environments

## 2. The Main Layers

### Layer 1: Knowledge Sources

These are the long-lived inputs:

- `DB/`: curated vulnerability entries
- `reports/`: raw audit-finding corpus
- `DeFiHackLabs/`: exploit PoC corpus
- `invariants/`: reusable invariant references

These are not all consumed the same way. `DB/` is the primary runtime knowledge source. `reports/` and `DeFiHackLabs/` are slower-moving research corpora.

### Layer 2: Retrieval And Indexing

The main generator is [`scripts/generate_manifests.py`](../scripts/generate_manifests.py). It turns DB Markdown into machine-usable retrieval artifacts:

- `DB/index.json`
- `DB/manifests/*.json`
- `DB/manifests/huntcards/*.json`
- `DB/manifests/keywords.json`

This layer exists so agents can navigate the DB without loading the full corpus.

### Layer 2.5: Graph Foundation

Horus now maintains graph artifacts for both the vulnerability DB and each live
audit.

DB graph:

- built by `python3 scripts/build_db_graph.py`
- stored at `DB/graphify-out/graph.json`
- summarized in `DB/graphify-out/GRAPH_REPORT.md`
- browsable by agents through `DB/graphify-out/wiki/index.md`

Per-audit graph:

- built during `audit-orchestrator` Phase 0
- stored at `audit-output/graph/graph.json`
- optionally enriched by `horus-graphify-blockchain`
- served through graphify MCP when available
- tracked by `audit-output/graph/coverage.jsonl`

The graph layer is additive. It expands candidate patterns and attack paths, but
the router/manifests/hunt cards remain the baseline retrieval path.

### Layer 3: Canonical Workflow Playbooks

The canonical playbooks live in [`.claude/`](../.claude):

- `.claude/agents/`
- `.claude/skills/`
- `.claude/resources/`
- `.claude/rules/`

This is the source of truth for the workflow logic. When the playbook changes, this is the place to edit.

### Layer 4: Runtime Delivery

The same workflow is exposed through multiple surfaces:

- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `.github/agents/`
- `.agents/skills/`
- `.codex/`

These surfaces are not equal in status. Some are canonical inputs and some are generated outputs.

### Layer 5: Execution Utilities

The repo includes concrete helpers for the workflow:

- `scripts/grep_prune.py`
- `scripts/partition_shards.py`
- `scripts/merge_shard_findings.py`
- `scripts/db_quality_check.py`
- `scripts/sync_codex_compat.py`

These make the workflow operational rather than purely descriptive.

## 3. Canonical vs Generated

### Canonical

- `DB/**/*.md`
- `TEMPLATE.md`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/resources/`
- `.claude/rules/`
- generator logic in `scripts/`

### Generated

- `DB/index.json`
- `DB/manifests/*.json`
- `DB/manifests/huntcards/*.json`
- `.agents/skills/`
- `.codex/agents/`
- `.codex/resources/`
- `.codex/rules/`
- `.codex/config.toml`
- `DB/graphify-out/**`
- `.github/agents/*.md`

Operational rule: change the source, then regenerate the generated surfaces.

## 4. Runtime Model

### Claude Code

Claude uses the source playbook tree directly:

- `CLAUDE.md`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/resources/`
- `.claude/rules/`

### Codex CLI

Codex gets a generated compatibility layer built from `.claude/` by [`scripts/sync_codex_compat.py`](../scripts/sync_codex_compat.py):

- `AGENTS.md`
- `.agents/skills/`
- `.codex/agents/`
- `.codex/resources/`
- `.codex/rules/`
- `.codex/config.toml`

### GitHub-Facing Agent Docs

GitHub-facing agents live in [`.github/agents/`](../.github/agents). They are generated from [`.claude/agents/`](../.claude/agents) by `python3 scripts/sync_codex_compat.py --sync-github-agents`. Do not hand-edit them for behavior changes.

### Gemini CLI

Gemini uses [`GEMINI.md`](../GEMINI.md) as the workspace-local instruction surface, and dynamically loads generated workflows via the `activate_skill` tool from `.agents/skills/`.

### Cursor And VS Code

These editor-based agents consume the repo through the instruction files and source playbooks rather than through a dedicated generated runtime layer.

## 5. Retrieval Architecture

The retrieval stack has four tiers plus graph expansion:

```text
Tier 1    DB/index.json
Tier 1.5  DB/manifests/huntcards/*.json
Tier 2    DB/manifests/*.json
Graph     DB/graphify-out/graph.json
Tier 3    DB/**/*.md
```

### Tier 1: Router

[`DB/index.json`](../DB/index.json) tells the agent:

- which manifests exist
- which protocol contexts map to which manifests
- where hunt cards live
- where keyword routing lives

This should be the first read for almost every search task.

### Tier 1.5: Hunt Cards

Hunt cards are compressed detection units for grep-first auditing. A card typically carries:

- a `grep` pattern
- a short detection statement
- micro-directive verification steps
- a pointer back to the source DB entry and line range

This is the preferred interface for full audits against an external codebase.

### Tier 2: Manifests

Manifests bridge semantic lookup and exact DB reads. They contain exact line ranges, titles, IDs, severity, and keywords for patterns.

### Tier 3: DB Markdown

Long-form DB entries are the richest source of vulnerability knowledge, but they should only be read after narrowing through the earlier tiers.

### Graph Expansion

The DB graph is queried after a topic, protocol type, or likely vulnerability
class is known:

```bash
graphify query "<topic>" --graph DB/graphify-out/graph.json --budget 2000
graphify path "<topic>" "<candidate>" --graph DB/graphify-out/graph.json
```

Agents use it to pull neighboring hunt cards and related concepts into the
working set. They must log expansions and continue without graph features if the
graph is unavailable.

## 6. The Full Audit Pipeline

The full pipeline is orchestrated by the `audit-orchestrator` family of playbooks.

### Phase 0: Graph Foundation

Build `audit-output/graph/graph.json` before the classic audit phases. The
orchestrator runs graphify on the target codebase, merges optional blockchain DSL
AST extraction, starts graphify MCP when possible, initializes coverage logging,
and optionally writes `audit-output/memory-recall.md`.

This is a soft gate: if graphify or MCP fails, the audit continues through the
existing retrieval and discovery pipeline.

### Phase 1: Reconnaissance

Identify:

- target structure
- protocol type
- key components
- likely relevant manifests

### Phase 2: Context Building

Build local and global code understanding through:

- function-level analysis
- contract-level notes
- system synthesis

### Phase 3: Invariant Extraction

Write and review system properties before deeper hunting. This improves later triage and formal verification.

### Phase 4: Discovery Fan-Out

Run multiple discovery streams:

- DB-powered hunting with optional graph expansion
- reasoning-based discovery
- multi-persona analysis
- validation-gap hunting
- attack-graph synthesis when Phase 0 graph and reviewed invariants exist

### Phase 5: Merge And Triage

Merge findings from parallel streams, deduplicate them, and falsify weak claims.

### Phase 6: PoC

When justified, write and execute proof-of-concept artifacts.

### Phase 7: Fuzzing / Formal Verification

Generate and possibly execute:

- Medusa harnesses
- Chimera setups
- Halmos specs
- Certora specs
- Sui prover artifacts

### Phase 8-10: Judging Loop

The pipeline contains a judging self-loop:

1. pre-judge
2. polish
3. deep review

This is designed to filter findings before final reporting.

### Phase 11: Report Assembly

Assemble a final report containing only findings that survived the earlier filters.

## 7. Script-Backed Hunt Loop

The hunt-card audit loop is not just conceptual. It is implemented directly:

1. [`scripts/grep_prune.py`](../scripts/grep_prune.py): keep hunt cards with code hits and preserve critical `neverPrune` cards
2. [`scripts/partition_shards.py`](../scripts/partition_shards.py): split surviving cards into workable shard payloads
3. [`scripts/merge_shard_findings.py`](../scripts/merge_shard_findings.py): combine and deduplicate shard findings

This is the main bridge from retrieval artifacts to scalable agent execution.

## 8. What To Edit For Common Changes

### If you are adding or editing vulnerability content

Edit:

- `DB/**/*.md`
- `TEMPLATE.md` if the schema itself needs to change

Then run:

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py
python3 scripts/db_quality_check.py
```

### If you are changing routing or hunt-card behavior

Edit:

- `scripts/generate_manifests.py`
- `scripts/build_db_graph.py` if graph relationships need to change

Then regenerate and validate.

### If you are changing the workflow logic or agent behavior

Edit:

- `.claude/agents/`
- `.claude/skills/`
- `.claude/resources/`
- `.claude/rules/`

Then run:

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --sync-github-agents
python3 scripts/sync_codex_compat.py --check
python3 scripts/validate_codex_runtime.py
```

The GitHub-facing agent mirror is generated from `.claude/agents/`; resources under `.github/agents/resources/**` are checked for parity with `.claude/resources/**`.

### If you are updating graph artifacts

Run:

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py
python3 scripts/db_quality_check.py
```

Commit `DB/graphify-out/graph.json`, `GRAPH_REPORT.md`, and `wiki/` only when
the generated graph should be shared with other agents from the repository.

### If you are doing report-corpus maintenance

Look at:

- `reports/`
- `scripts/rebuild_report_artifacts.py`
- `scripts/update_codebase_structure.py`
- `.github/workflows/split-reports.yml`

## 9. Common Mistakes

- Reading all DB Markdown files instead of routing first
- Treating `reports/` as normal always-on context
- Editing generated manifests or hunt cards directly
- Editing generated Codex surfaces instead of the `.claude/` sources
- Editing generated `.github/agents/` mirrors instead of the `.claude/` sources
- Forgetting to regenerate after changing DB or `.claude/` sources

## 10. Recommended Reading Order

### If you are new to the repo

1. [`README.md`](../README.md)
2. [`docs/codebase-structure.md`](./codebase-structure.md)
3. [`docs/db-guide.md`](./db-guide.md)
4. [`docs/codex-architecture.md`](./codex-architecture.md)

### If you want to run or extend agent workflows

1. `AGENTS.md` or `CLAUDE.md` depending on runtime
2. `.claude/agents/audit-orchestrator.md`
3. `scripts/sync_codex_compat.py`
4. `scripts/grep_prune.py`, `scripts/partition_shards.py`, `scripts/merge_shard_findings.py`

### If you want to maintain the DB

1. `TEMPLATE.md`
2. `Example.md`
3. `docs/db-guide.md`
4. `scripts/generate_manifests.py`
5. `scripts/db_quality_check.py`
