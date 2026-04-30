# Horus — Claude Code Instructions

This repository is **Horus**, a curated vulnerability database for smart contract security audits, optimized for AI-agent-driven bulk scanning and pattern matching across blockchain ecosystems.

## Quick Reference

- **DB Router**: `DB/index.json` — START HERE for any vulnerability lookup
- **Hunt Cards**: `DB/manifests/huntcards/all-huntcards.json` — combined enriched hunt-card corpus; prefer per-manifest cards when context is tight
- **Manifests**: `DB/manifests/*.json` — full pattern-level indexes with line ranges
- **DB Graph**: `DB/graphify-out/graph.json` — additive related-variant expansion after initial routing
- **Template**: `TEMPLATE.md` — structure for new and migrated vulnerability entries
- **Example**: `Example.md` — reference implementation of an entry

## Architecture: 4-Tier Search + Graph Expansion

```
Tier 1:   DB/index.json                          ← Router (~350 lines). Start here.
Tier 1.5: DB/manifests/huntcards/*-huntcards.json ← Compressed detection cards
Tier 2:   DB/manifests/<name>.json                ← Full pattern-level index with line ranges
Graph:    DB/graphify-out/graph.json             ← Additive related-card expansion
Tier 3:   DB/**/*.md                              ← Vulnerability content. Read ONLY targeted line ranges.
```

**Never read entire vulnerability files** — use hunt cards or manifests to find exact line ranges, then read only those ranges with `Read`.

## Agents System

All agents live in `.claude/agents/`. The entry point for a full audit is `audit-orchestrator`.

### Key Agents

| Agent | Purpose |
|-------|---------|
| `audit-orchestrator` | **ENTRY POINT** — 11-phase audit pipeline with configurable modes |
| `audit-context-building` | Deep line-by-line codebase analysis coordinator |
| `function-analyzer` | Per-contract ultra-granular function analysis (spawned by audit-context-building) |
| `system-synthesizer` | Synthesizes per-contract context into global context document |
| `multi-persona-orchestrator` | 6 parallel auditing personas with cross-verification |
| `protocol-reasoning` | Deep reasoning-based vulnerability discovery |
| `missing-validation-reasoning` | Input validation and hygiene scanner |
| `invariant-writer` / `invariant-reviewer` | Invariant extraction and hardening |
| `invariant-catcher` | DB-powered vulnerability pattern hunting |
| `invariant-indexer` | Indexes canonical invariants from production DeFi protocols |
| `poc-writing` | Exploit test generation |
| `issue-writer` | Polishes findings into submission-ready write-ups |
| `report-aggregator` | Assembles judge-verified findings into final Sherlock-format report |
| `variant-template-writer` | Converts audit reports into TEMPLATE.md-compliant DB entries |
| `defihacklabs-indexer` | Attack-graph-aware indexing of DeFiHackLabs PoCs into DB entries and invariants |
| `judge-orchestrator` | Cross-platform consensus — runs all 3 judges in parallel |
| `sherlock-judging` / `cantina-judge` / `code4rena-judge` | Platform-specific finding validation (single-platform) |
| `chimera-setup` | Multi-tool property testing scaffold — Echidna + Medusa + Halmos |
| `medusa-fuzzing` / `certora-verification` / `halmos-verification` | Formal verification suites (single-tool) |
| `certora-mutation-testing` | Mutation campaigns with Gambit + certoraMutate |
| `certora-sui-move-verification` / `sui-prover-verification` | Sui Move formal verification |
| `db-quality-monitor` | Monitors 4-tier architecture integrity and auto-remediates |
| `solodit-fetching` | Fetches raw findings from Solodit/Cyfrin API |
| `attack-graph-synthesizer` | BFS + hyperedge multi-step attack chain enumeration against invariant suite |

### Invoking the Audit Pipeline

```
/agent audit-orchestrator <codebase-path> [protocol-hint] [--static-only] [--judge=sherlock|cantina|code4rena] [--discovery-rounds=N]
```

### Skills

Each agent has a corresponding skill in `.claude/skills/<agent-name>/SKILL.md`. Skills are thin invocation wrappers (`context: fork` + `agent: <name>`) — agents hold the full instructions. Skills provide:
- `$ARGUMENTS` substitution for dynamic task input
- `argument-hint` for autocomplete
- `user-invocable: false` to hide sub-agent-only skills from the `/` menu
- Cross-links to related upstream/downstream skills

### Resources

Shared reference material lives in `.claude/resources/` (global, not per-skill):
- Templates (audit reports, invariants, PoCs, Medusa, Certora)
- References (Certora CVL, Sui Move, Medusa API)
- Knowledge bases (vulnerability taxonomy, reasoning skills, domain decomposition)
- Pipeline specs (data formats, orchestration, output requirements)
- Judging criteria (Sherlock, Cantina, Code4rena)
- Static analysis rules (CodeQL `.ql`, Semgrep `.yaml`)

### Rules

Path-scoped rules in `.claude/rules/` auto-load when Claude works with matching files:
- `db-entries.md` — DB vulnerability entry conventions (`DB/**/*.md`, `TEMPLATE.md`, `Example.md`)
- `manifests.md` — Manifest/index generation rules (`DB/manifests/**`)
- `invariants.md` — Invariant library format and ID conventions (`invariants/**/*.md`)
- `scripts.md` — Python script conventions (`scripts/**/*.py`, root scripts)
- `agents.md` — Agent file conventions (`.claude/agents/*.md`)
- `skills.md` — Skill file conventions (`.claude/skills/*/SKILL.md`)
- `reports.md` — Reports directory rules (`reports/**/*.md`)
- `audit-output.md` — Pipeline output conventions (`audit-output/**`)
- `resources.md` — Shared resource management (`.claude/resources/**`)
- `chimera.md` — Chimera framework conventions (`test/recon/**`)
- `rules.md` — Rules file conventions (`.claude/rules/*.md`)
- `settings.md` — Settings and permissions conventions (`.claude/settings*.json`)
- `claude-md.md` — CLAUDE.md editing conventions (`CLAUDE.md`)
- `graph-artifacts.md` — Conventions for `audit-output/graph/` and attack-candidates (`audit-output/graph/**`)
- `lessons-db.md` — Conventions for `~/.horus/lessons.db` cross-audit memory (`scripts/lessons_db.py`)
- `draft-hunt-cards.md` — Conventions for `DB/_drafts/` and `DB/_telemetry/` (`DB/_drafts/**`, `DB/_telemetry/**`)

## Common Commands

```bash
# Regenerate manifests after DB changes
python3 scripts/generate_manifests.py

# Fetch vulnerability reports from Solodit
python3 scripts/solodit_fetcher.py <topic>

# Run DB quality checks
python3 scripts/db_quality_check.py

# Run full retrieval/graph validation
python3 scripts/validate_retrieval_pipeline.py

# Generate entries from reports
python3 scripts/generate_entries.py

# Build/refresh DB knowledge graph (run from repo root)
python3 scripts/build_db_graph.py

# Validate generated Codex/GitHub runtime surfaces
python3 scripts/sync_codex_compat.py --check
python3 scripts/validate_codex_runtime.py

# Query cross-audit lessons
python3 scripts/lessons_db.py query --ecosystem evm --topic "price manipulation"

# Extract blockchain AST for a codebase (Solidity/Move/Cairo)
horus-graphify-blockchain extract <path> --out audit-output/graph/blockchain-ast.json

# Finalize audit-time graphify output into queryable node-link graph JSON
python3 scripts/finalize_audit_graph.py --codebase <path> --out audit-output/graph/graph.json
```

## Conventions

- Vulnerability entries follow `TEMPLATE.md` structure, and touched legacy entries should be migrated to the current layout
- Severity uses Impact × Likelihood matrix: CRITICAL, HIGH, MEDIUM, LOW
- Every finding must have: concrete code references, root cause, attack scenario
- DB patterns use unique IDs: `<manifest>-<category>-NNN` (e.g., `oracle-staleness-001`)
- All agent communication goes through `audit-output/` filesystem — no side channels
- Pipeline state tracked in `audit-output/pipeline-state.md`

## Protocol Contexts

Auto-detected or specified: `lending_protocol`, `dex_amm`, `vault_yield`, `governance_dao`, `cross_chain_bridge`, `cosmos_appchain`, `solana_program`, `perpetuals_derivatives`, `token_launch`, `staking_liquid_staking`, `nft_marketplace`.
