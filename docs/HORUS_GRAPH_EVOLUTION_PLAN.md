# Horus Architecture Evolution Plan — v1

**Status**: DRAFT — pending answers to open questions in §4.
**Owner**: User (calc1f4r). Plan author: Claude (architecture review session, 2026-04-27).
**Audience**: AI agents executing each Doable, and human reviewers.
**Goal of this document**: Be explicit enough that any sub-agent can pick up a Doable and execute it without re-deriving context. If you (executing agent) hit ambiguity, **stop and ask the user** — do not guess. Open questions are flagged inline as `OPEN QUESTION (Qn)` and consolidated in §4.

---

## 0. TL;DR for Executing Agents

You are implementing one of six **Doables** that together evolve Horus from a retrieval-based audit pipeline (grep over manifests) to a graph-traversal-based one (query a knowledge graph of both the DB and the target codebase, with cross-audit memory and self-improving hunt cards).

You inherit:
- A working 11-phase audit pipeline (`audit-orchestrator`)
- A vulnerability DB with 4-tier search (`DB/index.json` → manifests → hunt cards → entries)
- 30+ specialized agents in `.claude/agents/`
- The `graphify` skill (already installed, see `~/.claude/skills/graphify/SKILL.md`)

You are NOT:
- Migrating Horus to Hermes (Hermes is a personal AI platform, wrong abstraction)
- Replacing the judging self-loop (it works — leave it alone)
- Adding any blockchain-specific hard dependency (Slither, anchor-syn, move-prover are all OPT-IN deepeners only)

---

## 1. Goal & Constraints

### 1.1 Primary goal
Lift **recall** of the audit pipeline. Findings are being missed because:
1. Coverage of the target codebase is implicit, not tracked
2. Hunt cards are flat keyword patterns with no relationships
3. Multi-step / cross-contract attacks are found only by persona intuition, not systematic search
4. Each audit starts cold — no learning carries forward

### 1.2 Constraints
- **C1 (universality)**: Horus must remain language- and blockchain-agnostic. No core component may depend on a Solidity-only tool (Slither, Aderyn, Wake, etc.) or any single-ecosystem tool (anchor-syn for Solana, move-prover for Move). These may exist as **optional deepeners** that the user enables per-project, but the floor must work for every blockchain language Horus already covers.
- **C2 (no rewrites)**: Existing agents and the 11-phase pipeline keep working during rollout. Each Doable must be additive, not destructive. Old grep-based hunt-card lookup remains as a fallback until graph-based lookup is proven equivalent or better on a recall benchmark.
- **C3 (filesystem coordination)**: All inter-agent communication goes through files in `audit-output/` or new locations specified herein. No side channels.
- **C4 (no client data leakage)**: Cross-audit memory must respect NDA boundaries. Default opt-in per audit. See §4 Q3.

### 1.3 Definition of done (for the entire plan)
- Recall on a labeled benchmark of past audits (see §15) improves by ≥ 20% over baseline
- No regression in precision (false-positive rate stays within 1.5× of baseline)
- Pipeline completes within 1.5× current wall-clock time

---

## 2. Non-Goals

- Building our own static analyzer
- Replacing graphify with a custom alternative
- Visualizing graphs for human consumption (HTML output is a side effect, not a goal)
- Embedding-based / vector retrieval over the DB (graph cross-refs are a simpler win)
- Multi-tenant / SaaS deployment
- RL training of agents (Hermes does this; we do not)

---

## 3. Architectural Decisions

### 3.1 Substrate
**graphify is the storage and query substrate** for all graph artifacts. We do not build our own graph store. Reasons: graphify already provides AST extraction (tree-sitter), semantic extraction (Claude), confidence-tagged edges (`EXTRACTED|INFERRED|AMBIGUOUS`), Leiden community detection, god-node analysis, hyperedges, MCP server, Neo4j export, and incremental update via SHA256 cache. Reinventing this is wasted work.

### 3.2 Language coverage
Tree-sitter is the universal AST layer. graphify already supports `.py .ts .js .go .rs .java .c .cpp .rb .cs .kt .scala .php` natively. Doable 2 wires in tree-sitter grammars for the blockchain DSLs graphify lacks: Solidity, Vyper, Move (Sui & Aptos), Cairo, Sway, Tact. Solana / NEAR / Polkadot ink! / CosmWasm / Stellar Soroban are Rust → already covered. Cosmos SDK is Go → already covered.

### 3.3 Optional deepeners
Per C1, language-native analyzers are opt-in and detected via `$PATH`. If `slither` is available and the project is Solidity, the orchestrator runs it and merges Slither's call-graph output into the graphify graph via `graphify merge-graphs`. If absent, tree-sitter alone is used. Same pattern for `move-prover`, `anchor-syn`, `cairo-lint`. Horus core never depends on any of these.

### 3.4 Cross-audit memory
SQLite with FTS5. Reasons: zero-deployment (single file at `~/.horus/lessons.db`), built-in full-text search, well-supported in Python stdlib. Honcho-style dialectic modeling is out of scope; plain text lessons indexed by `protocol_type`/`ecosystem` is sufficient.

### 3.5 New agent boundaries
- `attack-graph-synthesizer` is a new agent — it consumes the codebase graph and the invariant suite, emits attack candidates, hands off to existing `protocol-reasoning` for validation. Does NOT do its own validation.
- `db-quality-monitor` is **extended**, not replaced — gains a "DB gap analysis" mode triggered after audits.
- `audit-orchestrator` gains **Phase 0** (graph foundation) before existing Phase 1 (reconnaissance). Existing phase numbering is preserved.

### 3.6 Pipeline cutover strategy
Per C2: dual-track until benchmark proves new path is equal-or-better.
- New path: Phase 0 graph + graph-based hunt-card lookup
- Old path: existing grep-based lookup
- Both run; orchestrator logs which path found which finding
- After 3 consecutive audits with new-path recall ≥ old-path recall, old path is removed

---

## 4. OPEN QUESTIONS (USER MUST ANSWER OR ACCEPT DEFAULTS)

These are decisions where the plan changes shape. Defaults below are what executing agents will use absent override.

### Q1. Where does `horus-graphify-blockchain` live?
- **(a)** Subdirectory inside Horus repo: `Horus/scripts/horus_graphify_blockchain/` — fastest, internal-only
- **(b)** New sibling repo `~/horus-graphify-blockchain/`, published to PyPI — open-source-friendly, slower
- **(c)** Fork of graphify itself with PR upstream — maximum reach, slowest

**Default**: (a) for v1. Promote to (b) once stable. Q1 affects Doable 2.

### Q2. Hunt-card auto-drafting policy (Doable 5)
When a confirmed finding has no matching hunt card, system auto-drafts one. Then:
- **(a)** Auto-merge to `DB/_drafts/`, human reviews and promotes
- **(b)** Open PR, human reviews and merges
- **(c)** Write to `audit-output/db-gap-suggestions.md` only, never auto-touch the DB

**Default**: (a). Drafts in `_drafts/` never load into manifests until promoted; safe.

### Q3. Cross-audit memory privacy (Doable 4)
- **(a)** Opt-out: every audit's lessons go into `~/.horus/lessons.db` unless `--no-memory` flag passed
- **(b)** Opt-in: lessons added only with `--memory` flag
- **(c)** Per-client: `~/.horus/lessons-<client>.db`, isolated

**Default**: (b). NDA-safe. User can flip to (a) for personal repos / public audits.

### Q4. Recall benchmark dataset
We need a labeled benchmark of past audits with confirmed findings to validate "recall improved." Does it exist?
- **(a)** Yes, point me to it
- **(b)** No, build one from `reports/` or past `audit-output/` runs
- **(c)** Defer benchmark to validation phase, ship Doables on judgement first

**Default**: (b). See §15. Without a benchmark, we cannot prove the plan worked.

### Q5. Optional deepeners — fully out, or opt-in allowed?
You said "slither should be out of the picture." Two readings:
- **(a)** Out of CORE only. Opt-in deepeners (Slither, anchor-syn, move-prover) are fine when user has them installed.
- **(b)** Out entirely. Tree-sitter is the only analysis layer, period.

**Default**: (a). Universal floor, optional ceiling. (b) leaves Solidity precision on the table for users who have Slither anyway.

### Q6. Plan execution mode
- **(a)** Each Doable spawned as autonomous agent, runs to completion, reports back
- **(b)** User supervises step-by-step within each Doable
- **(c)** Mixed: D1 + D4 autonomous (low risk), D2 + D3 + D6 supervised (higher risk)

**Default**: (c). Spelled out per-Doable in §6–§11.

### Q7. graphify version pin
- **(a)** Pin to current PyPI version of `graphifyy` at start of plan, freeze for duration
- **(b)** Track main, accept upstream churn
- **(c)** Vendor a copy into Horus repo

**Default**: (a). Capture version in `Horus/.graphify-version`. Re-eval after plan completes.

### Q8. Graph artifact locations
Default scheme used throughout this plan:
- DB graph: `DB/graphify-out/graph.json` (created by `python3 scripts/build_db_graph.py`)
- Per-audit codebase graph: `audit-output/<audit-id>/graph/graph.json`
- Cross-audit memory: `~/.horus/lessons.db`
- Lessons artifacts: `~/.horus/lessons/<audit-id>.md`
- MCP server PID file: `audit-output/<audit-id>/graph/mcp.pid`

Confirm or override.

---

## 5. Conventions for Executing Agents

### 5.1 Read these first
- `/home/calc1f4r/Horus/CLAUDE.md` (project instructions)
- `/home/calc1f4r/Horus/.claude/rules/` (path-scoped conventions)
- `/home/calc1f4r/.claude/skills/graphify/SKILL.md` (graphify command reference)
- This document (§6 onward, plus §13 cross-cutting)

### 5.2 Use these tools
- `Read`, `Edit`, `Write`, `Glob`, `Grep`, `Bash` — standard
- For graphify: invoke via `/graphify ...` slash command — DO NOT shell out to `graphify` binary directly unless documented; the skill handles interpreter detection
- For graph queries from agents: prefer the graphify MCP server (`--mcp`) over direct JSON file parsing

### 5.3 Output discipline
- Each Doable specifies exact output paths and schemas. Stick to them.
- New files: write with `Write`. Modifications: use `Edit`.
- New rules / conventions go in `.claude/rules/` (path-scoped per CLAUDE.md). Doable 6 creates `attack-graph-synthesizer.md` rule.
- DO NOT create new top-level docs unless this plan says so.

### 5.4 Validation discipline
- Each Doable has explicit acceptance criteria. Run them before declaring done.
- If acceptance fails, write a failure report to `audit-output/plan-execution/<doable-id>-failures.md` and stop. Do not proceed to dependent Doables.

### 5.5 When uncertain
- Re-read the relevant Doable section
- Re-read the open questions in §4
- If still uncertain: STOP, write your question to `audit-output/plan-execution/<doable-id>-questions.md`, hand back to user

### 5.6 Commit discipline
- Each Doable produces ONE branch named `plan/d<n>-<slug>` (e.g. `plan/d1-graphify-db`)
- Commits authored by Claude must include `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` (per CLAUDE.md)
- DO NOT commit unless the user explicitly asks — write changes, mark done, let user review

---

## 6. Doable 1 — graphify the vulnerability DB

### 6.1 Goal
Convert `Horus/DB/` into a queryable knowledge graph so agents can find related hunt cards via traversal instead of grep.

### 6.2 Why
Hunt cards today are independent. Matching `oracle-staleness-001` doesn't pull in `oracle-confidence-002` or `oracle-fallback-003` even though they're variants of the same attack class. Graphify's community detection + cross-references close this gap with one command.

### 6.3 Inputs
- `/home/calc1f4r/Horus/DB/` (entire tree: manifests, hunt cards, .md entries)
- graphify skill installed (verify by checking `~/.claude/skills/graphify/SKILL.md` exists)

### 6.4 Outputs
- `Horus/DB/graphify-out/graph.json` — persistent graph
- `Horus/DB/graphify-out/GRAPH_REPORT.md` — god nodes, surprising connections, suggested questions
- `Horus/DB/graphify-out/wiki/index.md` + curated multi-node community/god-node articles (agent-crawlable)
- `Horus/DB/graphify-out/cache/` — SHA256 cache for incremental updates
- `Horus/DB/graphify-out/.graphify_version` — pin from Q7

### 6.5 Step-by-step

1. **Verify graphify installed**:
   ```bash
   python3 -c "import graphify" 2>&1 | head -1
   ```
   If ImportError: `pip install graphifyy && graphify install`. Capture installed version into `Horus/.graphify-version`.

2. **Run graphify on DB**:
   ```bash
   cd /home/calc1f4r/Horus/DB
   ```
   Then in Claude Code: `/graphify . --mode deep --directed --wiki --mcp`

   Flags rationale:
   - `--mode deep`: aggressive INFERRED edges (DB is conceptual; we want speculative relationships flagged for review)
   - `--directed`: hunt-card relationships have direction (`is_variant_of`, `enables`, `precondition_for`)
   - `--wiki`: agent-crawlable markdown index
   - `--mcp`: starts MCP server for live queries from other agents

3. **Verify outputs exist** (acceptance, partial):
   - `DB/graphify-out/graph.json` — open and confirm `nodes` array length > 100, `edges` array length > 200
   - `DB/graphify-out/GRAPH_REPORT.md` — confirm "God Nodes" section lists ≥ 5 entries
   - `DB/graphify-out/wiki/index.md` — confirm exists and references community articles

4. **Inspect god_nodes**: Read GRAPH_REPORT.md "God Nodes" section. Hand-eyeball: do these patterns deserve being central? If a god node is something obviously not-central (e.g., the word "function"), graphify may have over-extracted on stop-words. Flag in execution log; do not proceed to step 5 until confirmed.

5. **Inspect community labels**: graphify auto-labels communities. For each labeled community, sanity-check 3 random member nodes belong to that community. If labels look wrong, run `/graphify . --cluster-only` to re-cluster — sometimes initial clustering is unstable.

6. **Wire into invariant-catcher (pilot)**: Edit `.claude/agents/invariant-catcher.md` to add a new query path:
   - On invocation, BEFORE running grep over manifests, query the graphify MCP server:
     - `get_neighbors(<topic-as-node-id>, depth=2)` to expand the topic into related patterns
     - `shortest_path(<topic>, <other-topic>)` for cross-category links
   - Pass expanded set of hunt-card IDs into the existing grep step
   - Log both expansions to `audit-output/<audit-id>/d1-graph-expansion.md`

   This is **additive** — old grep behavior continues. New behavior expands the search set.

7. **Document the new query API** in `.claude/resources/db-hunting-workflow.md` — add a section "Graph-augmented hunting" with example queries.

### 6.6 Acceptance criteria
- [ ] `DB/graphify-out/graph.json` exists, valid JSON, ≥ 100 nodes, ≥ 200 edges
- [ ] `GRAPH_REPORT.md` lists ≥ 5 god nodes that are recognizable hunt-card concepts
- [ ] `wiki/index.md` exists with ≥ 3 community articles
- [ ] MCP server starts cleanly (`/graphify . --mcp` returns without error)
- [ ] On a benchmark of 5 past confirmed audits (see §15), `invariant-catcher` with graph augmentation surfaces ≥ baseline hunt cards. Specifically: for each finding, the hunt card that caught it (or would have caught it) must be in the augmented set.
- [ ] No regressions in existing `audit-orchestrator` runs (run one full audit; report must complete identically modulo additional graph-expansion log)

### 6.7 Files touched / created
- Created: `DB/graphify-out/**` (graphify writes these)
- Created: `Horus/.graphify-version`
- Edited: `.claude/agents/invariant-catcher.md` (add graph query path)
- Edited: `.claude/resources/db-hunting-workflow.md` (document new query API)
- Created: `audit-output/plan-execution/d1-completion.md` (report)

### 6.8 Failure modes & responses
- **Graphify produces empty graph**: Likely all DB files were skipped as binary or sensitive. Check `.graphify_detect.json`. Resolve and re-run.
- **Too many INFERRED edges, low signal**: Re-run without `--mode deep`. Document tradeoff.
- **MCP server fails to start**: Check `python3 -m graphify.serve` directly. May need to upgrade graphify.
- **invariant-catcher regresses (finds fewer cards)**: Graph expansion is too narrow. Increase `depth` parameter to 3. If still regressing, log it and revert the wire-in — D1 still has value as a one-shot DB analysis even without runtime integration.

### 6.9 Estimated effort
2–4 hours (mostly graphify runtime + benchmark validation).

### 6.10 Dependencies
None. Doable 1 has no upstream dependencies and unblocks Doables 5 and 6.

### 6.11 Execution mode
**Autonomous OK** — low blast radius. Output to `audit-output/plan-execution/d1-completion.md` for review.

---

## 7. Doable 2 — `horus-graphify-blockchain` extension

### 7.1 Goal
Add tree-sitter-based AST extraction to graphify for blockchain DSLs it lacks (Solidity, Vyper, Move-Sui, Move-Aptos, Cairo, Sway, Tact). After this Doable, graphify works on **every** blockchain ecosystem Horus targets.

### 7.2 Why
Tree-sitter grammars exist for all these languages but graphify hasn't wired them in. Without this, Phase 0 (Doable 3) on a Solidity codebase produces only Claude-extracted semantic edges — no precise call graph, no storage-write graph. Tree-sitter gives us those edges deterministically.

### 7.3 Architecture

```
horus-graphify-blockchain/
├── pyproject.toml
├── horus_graphify_blockchain/
│   ├── __init__.py
│   ├── languages/
│   │   ├── __init__.py
│   │   ├── solidity.py      # tree-sitter-solidity bindings
│   │   ├── vyper.py
│   │   ├── move_sui.py
│   │   ├── move_aptos.py
│   │   ├── cairo.py
│   │   ├── sway.py
│   │   └── tact.py
│   ├── extractor.py          # generic walker: tree-sitter parse tree → graphify JSON
│   ├── schema.py             # node/edge types (see §7.5)
│   ├── detect.py             # file extension → language mapping
│   └── cli.py                # `horus-graphify-blockchain extract <path>`
├── tests/
│   ├── fixtures/             # tiny canonical contract per language
│   └── test_extractor.py
└── README.md
```

Per Q1 default: this lives in `Horus/scripts/horus_graphify_blockchain/` for v1. The `pyproject.toml` is still included so it can be pip-installed locally and promoted to a sibling repo later.

### 7.4 Common schema (language-agnostic)

#### Node types
- `Module` — contract / module / namespace (Solidity contract, Move module, Cairo contract)
- `Function` — public/private/internal function or method
- `StateVar` — storage variable / state field
- `LocalVar` — function-local variable (only emitted in `--mode deep`, optional)
- `Modifier` — Solidity modifier, Move attribute, Cairo decorator
- `Event` — emittable event
- `Struct` — user-defined struct / type
- `ExternalCall` — call to external address / unknown module
- `Constant` — top-level constant or enum value

#### Edge types
- `CALLS` — function A calls function B (target may be unresolved → annotated `unresolved: true`)
- `READS_VAR` — function reads state var
- `WRITES_VAR` — function writes state var
- `INHERITS` — module inherits / extends another module
- `EMITS` — function emits event
- `HAS_MODIFIER` — function has modifier / attribute
- `EXTERNAL_CALL` — function makes external call (low-level call, swap, transfer)
- `DECLARES` — module declares function / state var / event / struct
- `RETURNS_TYPE` — function returns type (struct / primitive)
- `PARAM_TYPE` — function parameter has type

All edges include:
- `confidence: "EXTRACTED"` (deterministic from AST) — almost everything emitted by this extension
- `confidence_score: 1.0`
- `source_file`: relative path
- `source_location`: `{line, col}`
- `weight: 1.0` (or higher if the relationship occurs multiple times)

#### Node ID format (must match graphify's convention from SKILL.md line 338)
`{stem}_{entity}` where stem is filename without extension, entity is the symbol name. Both lowercased, non-alphanumeric replaced with `_`. CRITICAL: deterministic from label alone, no chunk numbers. This must match the IDs graphify's semantic extractor produces so cross-references connect.

### 7.5 Step-by-step

1. **Set up repo skeleton** under `Horus/scripts/horus_graphify_blockchain/` with the structure in §7.3. Use `pyproject.toml` (modern Python packaging). Dependencies: `tree-sitter>=0.21`, `tree-sitter-languages>=1.10` (or per-language packages).

2. **Decide grammar source per language** (executing agent must verify each works):
   - Solidity: `tree-sitter-solidity` (PyPI) or build from `JoranHonig/tree-sitter-solidity`
   - Vyper: check PyPI; fallback to build from source
   - Move (Sui): `tree-sitter-move` (verify version)
   - Move (Aptos): same grammar may cover both — verify, or use Aptos-specific fork
   - Cairo: `tree-sitter-cairo`
   - Sway: `tree-sitter-sway`
   - Tact: `tree-sitter-tact` (likely needs source build)

   **OPEN QUESTION (Q9, NEW)**: For each language, document which grammar repo + revision was used in `horus_graphify_blockchain/GRAMMARS.md`. If a grammar is broken or missing for a language, document and SKIP that language from v1. Do not proceed with broken grammars.

3. **Implement `extractor.py`** — generic walker:
   - Parse file with appropriate tree-sitter grammar
   - Walk parse tree, emit nodes per §7.4
   - Run a second pass for call resolution: for each call site, attempt to resolve target by:
     - Same-file lookup (function in same module)
     - Imported module lookup (if imports parsed)
     - Otherwise: emit edge with `unresolved: true`

4. **Implement per-language modules** in `languages/` — each is small (50–150 lines) and exports:
   - `LANGUAGE_NAME: str`
   - `FILE_EXTENSIONS: list[str]`
   - `GRAMMAR: tree_sitter.Language`
   - `node_kind_map: dict` — maps tree-sitter node kinds to schema node types (e.g. Solidity `function_definition` → `Function`)
   - `edge_kind_map: dict` — maps tree-sitter edges to schema edge types

   Start with Solidity. Get tests passing on a minimal ERC20. Then replicate pattern for others.

5. **Detect step**: `detect.py` maps extensions to language modules. `.sol → solidity`, `.vy → vyper`, `.move → move_sui` (or `move_aptos` based on `Move.toml` presence), `.cairo → cairo`, `.sw → sway`, `.tact → tact`.

6. **CLI**: `horus-graphify-blockchain extract <path>` — emits a graphify-compatible JSON to stdout or `--out <file>`. Same shape graphify's own AST extractor produces (see SKILL.md line 222–230).

7. **Integration test**: For each language, place a small fixture contract in `tests/fixtures/<lang>/` with known properties (5 functions, 3 state vars, 2 events). Run extractor, assert node/edge counts.

8. **Integration with graphify**: Two paths supported:
   - **(a)** As a graphify plugin (graphify auto-discovers via entry points). Out of scope for v1 — depends on graphify's plugin API which may not exist yet.
   - **(b)** As a pre-processor: `horus-graphify-blockchain extract <path> --out blockchain-ast.json`, run graphify on the codebase, then finalize with `python3 scripts/finalize_audit_graph.py --codebase <path> --blockchain-ast blockchain-ast.json --out audit-output/graph/graph.json`. **Use this for v1.**

   Doable 3 wires this into Phase 0.

9. **Validate on real codebase**: Pick one Solidity protocol and one Move-Sui protocol from past audits. Run extractor. Compare:
   - Number of functions detected vs `grep -c 'function ' *.sol`
   - Number of state-var writes detected vs hand count on a single contract
   - Acceptable: ±10% for functions, ±20% for writes (tree-sitter sometimes misses unusual patterns)

10. **Document known limitations** in `README.md`:
    - No inter-procedural data flow
    - Inheritance edges declared, not flattened (no virtual function resolution)
    - External calls detected but target not resolved
    - Reentrancy NOT detected at the graph level — that's a separate analysis

### 7.6 Acceptance criteria
- [ ] Package installs cleanly: `pip install -e Horus/scripts/horus_graphify_blockchain/`
- [ ] CLI runs on each supported language fixture and produces valid graphify-compatible JSON
- [ ] Tests pass: `pytest tests/`
- [ ] Validation on real codebase shows function detection within ±10% of grep baseline
- [ ] `scripts/finalize_audit_graph.py` produces a graph that graphify's MCP server can serve without error
- [ ] `README.md` and `GRAMMARS.md` are complete and explicit about supported languages and known limitations

### 7.7 Files touched / created
- All files under `Horus/scripts/horus_graphify_blockchain/` (created)
- No edits to existing Horus files in this Doable

### 7.8 Failure modes & responses
- **Tree-sitter grammar build fails** for a language: drop that language from v1, document in `GRAMMARS.md`, ship without it. Do not block other languages.
- **Call resolution produces too many false edges**: tighten to same-file calls only for v1. Cross-file resolution is a follow-up.
- **graph finalization doesn't accept our JSON shape**: read graphify's `build` and `export` modules to confirm exact schema, adjust `scripts/finalize_audit_graph.py`, and keep `graph.json` as node-link JSON.

### 7.9 Estimated effort
1–2 weeks. Phase 2a (Solidity + Move-Sui + Cairo) = 3–5 days. Phase 2b (rest) = 1 week.

### 7.10 Dependencies
- Independent of Doable 1 (can run in parallel)
- Blocks Doable 3 for non-Rust/Go ecosystems

### 7.11 Execution mode
**Supervised** (per Q6 default). User reviews extractor output on at least one fixture per language before Doable 3 proceeds.

---

## 8. Doable 3 — `audit-orchestrator` Phase 0: Graph Foundation

### 8.1 Goal
Add a new initial phase to `audit-orchestrator` that builds the codebase knowledge graph, starts the MCP server, and passes endpoints to all downstream agents. This is the integration point that makes Doables 1 and 2 useful at audit time.

### 8.2 Why
Without Phase 0, the graph artifacts are orphaned. Every downstream agent must be able to ask "what calls this function?" or "what's the shortest path from this entrypoint to this state mutator?" — and that requires the graph to be built and served before they run.

### 8.3 Inputs
- Output of Doable 2 (or just graphify alone if codebase is in graphify-native languages)
- The target codebase path (orchestrator argument)

### 8.4 Outputs (per audit)
- `audit-output/<audit-id>/graph/graph.json`
- `audit-output/<audit-id>/graph/GRAPH_REPORT.md`
- `audit-output/<audit-id>/graph/wiki/` (agent-readable)
- `audit-output/<audit-id>/graph/mcp.pid` (server PID)
- `audit-output/<audit-id>/graph/mcp.endpoint` (URI)
- `audit-output/<audit-id>/graph/coverage.json` — empty initial; populated by downstream agents as they visit nodes

### 8.5 Step-by-step

1. **Edit `.claude/agents/audit-orchestrator.md`** — insert a new section "Phase 0: Graph Foundation" before existing Phase 1. Pipeline numbering 1–11 stays the same; Phase 0 is the addition.

2. **Phase 0 logic** (specified in audit-orchestrator agent prompt):
   ```
   a. Detect ecosystem from file extensions (.sol → EVM, .move → Sui/Aptos, .rs in anchor → Solana, etc.)
   b. If ecosystem requires the blockchain extension (Doable 2), invoke:
        horus-graphify-blockchain extract <codebase> --out audit-output/<id>/graph/blockchain-ast.json
   c. Run graphify on codebase:
        cd <codebase> && /graphify . --mode deep --directed --no-viz
        (Skip --wiki and --html for codebase — too noisy for agents.)
   d. If blockchain extension was run in step b, merge:
        python3 scripts/finalize_audit_graph.py \
          --codebase <codebase> \
          --blockchain-ast audit-output/<id>/graph/blockchain-ast.json \
          --out audit-output/<id>/graph/graph.json
      Otherwise:
        cp <codebase>/graphify-out/graph.json audit-output/<id>/graph/graph.json
   e. Start MCP server in background:
        python3 -m graphify.serve audit-output/<id>/graph/graph.json &
        Save PID to audit-output/<id>/graph/mcp.pid
        Save endpoint to audit-output/<id>/graph/mcp.endpoint
   f. Initialize coverage tracker:
        echo '{"visited_nodes": []}' > audit-output/<id>/graph/coverage.json
   g. (Optional, per Q5(a)) Run opt-in deepeners detected on $PATH:
        - if Solidity and `slither` available: slither <codebase> --json audit-output/<id>/graph/slither.json,
          then convert + merge into graph.json
        - if Move and `move-prover` available: similar
        - if Solana/Anchor and `anchor` available: anchor idl parse, similar
   ```

3. **Pass graph endpoint to downstream agents**: Update `.claude/resources/inter-agent-data-format.md` schema to include:
   ```json
   {
     "graph": {
       "json_path": "audit-output/<id>/graph/graph.json",
       "mcp_endpoint": "stdio://...",
       "coverage_path": "audit-output/<id>/graph/coverage.json"
     }
   }
   ```
   Every spawned agent receives this in its prompt.

4. **Coverage tracking**: Edit each persona agent (`persona-bfs`, `persona-dfs`, `persona-mirror`, `persona-state-machine`, `persona-working-backward`, `persona-reimplementer`) to append visited node IDs to `coverage.json` as they read functions. Use `Edit` on the JSON file (read-modify-write with file lock — or use a single append-only log file `coverage.jsonl` to avoid races).

   **OPEN QUESTION (Q10, NEW)**: Concurrent writes to `coverage.json` will race when personas run in parallel. Recommend `coverage.jsonl` (append-only) instead, with a post-phase aggregator that merges into `coverage.json`. **Default**: jsonl + aggregator.

5. **Blind-spot detection**: After Phase 4 (Discovery — see existing pipeline), add a sub-step "blind-spot pass":
   ```
   - Read graph.json: list all Function nodes that are externally callable (have no internal-only modifier)
   - Read coverage.jsonl: list visited Function node IDs
   - Diff: uncovered externally callable functions
   - Spawn one focused persona-dfs on top 10 by call-graph centrality
   ```
   This is the recall lift — forces examination of paths nobody touched.

6. **Phase 0 cleanup**: Phase 11 (final reporting) tears down MCP server using PID from `mcp.pid`.

7. **Update `docs/audit-orchestrator-flow.mmd`** (Mermaid diagram already in repo) to include Phase 0.

### 8.6 Acceptance criteria
- [ ] `audit-orchestrator` invocation on a test codebase produces all artifacts in `audit-output/<id>/graph/`
- [ ] MCP server starts and accepts at least one query (test: `python3 -m graphify.client query ...`)
- [ ] All 6 persona agents successfully append to `coverage.jsonl`
- [ ] Blind-spot pass identifies at least 1 uncovered function on a real codebase (sanity check — every audit has *some* blind spots)
- [ ] Phase 11 successfully kills the MCP server (no orphaned processes)
- [ ] No regression in audit wall-clock time exceeding 30% (Phase 0 adds 2–10 min depending on codebase size)
- [ ] Pipeline produces equivalent CONFIRMED-REPORT.md on a known audit (no findings lost)

### 8.7 Files touched / created
- Edited: `.claude/agents/audit-orchestrator.md` (Phase 0 added)
- Edited: `.claude/agents/persona-*.md` (6 files, coverage logging hook)
- Edited: `.claude/resources/inter-agent-data-format.md` (graph endpoint schema)
- Edited: `docs/audit-orchestrator-flow.mmd` (diagram)
- Created: `audit-output/<id>/graph/**` (per-audit artifacts; not committed)

### 8.8 Failure modes & responses
- **MCP server hangs**: timeout in Phase 0 step e at 30s. Fall back to file-only graph (agents read graph.json directly with Read tool).
- **Graph too large for MCP server**: graphify has a 5000-node limit for HTML viz; MCP may have similar issues. If hit, use the aggregated community view (see SKILL.md lines 581–604).
- **Coverage tracking adds latency**: if profiling shows >5% slowdown, batch writes (in-memory deque, flush every 30s).

### 8.9 Estimated effort
2 days for the orchestrator changes + 1 day for persona coverage hooks = 3 days.

### 8.10 Dependencies
- Requires Doable 2 done (or skip blockchain extension for graphify-native ecosystems only)
- Blocks Doable 6 (attack-graph-synthesizer needs the live graph)

### 8.11 Execution mode
**Supervised**. The orchestrator is the most critical agent in Horus. User reviews edits to `audit-orchestrator.md` before they merge.

---

## 9. Doable 4 — Cross-audit memory (FTS5)

### 9.1 Goal
Persist lessons across audits in a queryable SQLite FTS5 index, and inject relevant lessons at the start of each new audit. This is the Hermes "closed learning loop" applied to vuln hunting.

### 9.2 Why
Each Horus audit currently starts cold. If we found a tricky pattern in audit N (e.g., "in Sui Move, hot-potato types can be smuggled through public_share_object to bypass capability checks"), audit N+1 has no awareness. FTS5 provides cheap full-text recall keyed by ecosystem and protocol type.

### 9.3 Inputs
- All past confirmed findings in `audit-output/<id>/CONFIRMED-REPORT.md` (one per audit)
- Judge revision logs in `audit-output/<id>/` (when judges flagged + corrected)

### 9.4 Outputs
- `~/.horus/lessons.db` — SQLite database, schema in §9.5
- `~/.horus/lessons/<audit-id>.md` — per-audit lessons artifact (human-readable)
- New helper script: `Horus/scripts/lessons_db.py`

### 9.5 Schema

```sql
CREATE VIRTUAL TABLE lessons USING fts5(
  audit_id UNINDEXED,
  date UNINDEXED,
  ecosystem,        -- e.g. 'evm', 'sui', 'solana', 'cosmos'
  protocol_type,    -- e.g. 'lending_protocol', 'dex_amm'
  phase,            -- which phase of the pipeline produced this lesson
  category,         -- 'false_negative' | 'judge_revision' | 'novel_pattern' | 'recall_gap'
  finding_id UNINDEXED,
  related_hunt_cards,
  severity,
  lesson,           -- the lesson text itself (full-text searched)
  tokenize='porter unicode61'
);

CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO meta VALUES ('schema_version', '1');
```

### 9.6 Step-by-step

1. **Build `lessons_db.py`** with three subcommands:
   - `init` — creates `~/.horus/lessons.db` with the schema above
   - `ingest <audit-output-dir>` — reads `CONFIRMED-REPORT.md` and judge logs, extracts lessons, inserts rows
   - `query --ecosystem X --protocol-type Y --topic "..." [--limit 10]` — returns top-K lessons

2. **Lesson extraction logic** (in `ingest`):
   For each finding in `CONFIRMED-REPORT.md`:
   - `category = "false_negative"` if grep over the original hunt-card manifests didn't surface this finding's pattern
   - `category = "judge_revision"` if the judge changed severity or marked initially-invalid finding as valid
   - `category = "novel_pattern"` if there's no related hunt card in the DB
   - `category = "recall_gap"` if the finding's pattern exists in DB but in a different manifest than agents searched
   Lesson text is generated by an LLM call summarizing what was learned. Format:
   > "When auditing {protocol_type} on {ecosystem}, watch for {pattern}. Specifically: {2–3 sentences}. Found in audit {audit_id}, severity {severity}."

3. **Wire into `audit-orchestrator`**: Add new step "Phase 1.5: Memory Recall" after Phase 1 (Reconnaissance):
   ```
   - Determine ecosystem and protocol_type from Phase 1 output
   - Call: python3 Horus/scripts/lessons_db.py query --ecosystem <eco> --protocol-type <pt> --limit 10
   - Format results as a markdown block, save to audit-output/<id>/memory-recall.md
   - Inject this block into all discovery-phase persona prompts
   ```

4. **Wire into `report-aggregator`**: After CONFIRMED-REPORT.md is finalized, automatically run:
   ```
   python3 Horus/scripts/lessons_db.py ingest audit-output/<id>/
   ```
   Per Q3 default (opt-in): only run if `--memory` flag was passed to orchestrator. Add this flag to `audit-orchestrator` invocation.

5. **Privacy guardrails** (per Q3 default):
   - Default behavior: lessons are NOT ingested. User must pass `--memory` to opt in.
   - Lessons text generated by `ingest` MUST NOT include client-identifying strings (codebase paths, contract addresses, function names that are clearly client-specific). The extraction prompt enforces this.
   - Add a `--client-tag` flag to ingest so lessons can be later purged: `lessons_db.py purge --client-tag X`

6. **Test on past audits**: Pick 3 past audits from `audit-output/`, run `ingest`, then `query` with synthetic queries. Verify lessons surface relevant past findings.

### 9.7 Acceptance criteria
- [ ] `lessons_db.py init` creates the DB
- [ ] `lessons_db.py ingest` on a past audit produces ≥ 3 lessons
- [ ] `lessons_db.py query --ecosystem evm --topic "oracle"` returns relevant lessons
- [ ] `audit-orchestrator --memory` invocation runs Phase 1.5 and injects lessons into discovery prompts
- [ ] No client-identifying strings in lesson text on a sample of 10 ingested lessons
- [ ] `purge --client-tag` removes the right rows

### 9.8 Files touched / created
- Created: `Horus/scripts/lessons_db.py`
- Created: `~/.horus/lessons.db` (runtime, not committed)
- Created: `~/.horus/lessons/` directory (runtime)
- Edited: `.claude/agents/audit-orchestrator.md` (Phase 1.5 + `--memory` flag)
- Edited: `.claude/agents/report-aggregator.md` (auto-ingest hook)
- Edited: `.claude/resources/orchestration-pipeline.md` (document Phase 1.5)

### 9.9 Failure modes & responses
- **FTS5 not available in user's Python sqlite3**: rare on modern systems. If hit, install `pysqlite3-binary`.
- **Lesson extraction LLM produces noise**: tighten prompt; require structured output.
- **Lessons leak client info despite guardrail**: add a regex post-filter for known sensitive patterns (Ethereum addresses, API keys, etc.).

### 9.10 Estimated effort
2–3 days.

### 9.11 Dependencies
- Independent of D1, D2, D3 (memory is orthogonal to graph)
- Doable 5 may use the same DB

### 9.12 Execution mode
**Autonomous OK** — additive, opt-in by default.

---

## 10. Doable 5 — Self-improving hunt cards

### 10.1 Goal
After every audit, identify hunt-card gaps and auto-draft new hunt cards or refinement suggestions for human review. Hermes-style "skills self-improve during use" applied to the DB.

### 10.2 Why
The DB is currently maintained manually. Audits surface novel patterns that should become hunt cards but rarely do because nobody sits down to extract them. Automating the *draft* step (with human-in-the-loop *promote* step) closes this loop without compromising DB quality.

### 10.3 Inputs
- `audit-output/<id>/CONFIRMED-REPORT.md` (judge-verified findings)
- `DB/index.json`, manifests, hunt cards (existing DB state)
- Lessons DB from Doable 4 (optional, for cross-audit aggregation)

### 10.4 Outputs (per audit)
- `DB/_drafts/<draft-id>.md` — TEMPLATE.md-compliant hunt-card drafts (per Q2 default option (a))
- `audit-output/<id>/db-gap-analysis.md` — human-readable summary

### 10.5 Step-by-step

1. **Extend `db-quality-monitor`**: Add a new mode `--gap-analysis <audit-output-dir>`. Existing modes (4-tier integrity, manifest validation) remain unchanged.

2. **Gap-analysis logic**:
   For each finding in `CONFIRMED-REPORT.md`:
   ```
   a. Extract key signals: ecosystem, protocol type, root cause one-liner, code keywords
   b. Query DB graph (D1 output) for nearest hunt card via shortest_path on relevant terms
   c. If shortest_path distance > 3 OR no path: classify as "gap"
   d. For each gap, generate a TEMPLATE.md-compliant draft using:
      - Title: derived from finding title
      - Severity: from finding
      - Category: best-guess based on signals (or "uncategorized" if unclear)
      - Code keywords: extracted from finding's code references
      - Search keywords: extracted from finding description
      - Pattern body: paraphrased from finding's root cause + attack scenario
   e. Write draft to DB/_drafts/<auto-generated-id>.md
   ```

3. **Hunt-card refinement logic**:
   For each existing hunt card, track usage:
   - When did it last fire (match a confirmed finding)?
   - When did it misfire (match but finding was invalid)?
   - When did it fail to fire (a finding that should have matched but didn't)?

   Maintain a sidecar `DB/_telemetry/<hunt-card-id>.json`:
   ```json
   {
     "hits": 12,
     "misses": 3,
     "false_positives": 1,
     "last_hit": "2026-04-15",
     "last_audit": "audit-2026-04-20",
     "suggested_changes": [...]
   }
   ```
   When a hunt card has `false_positives > hits`, flag for review.

4. **Output report**: Write `audit-output/<id>/db-gap-analysis.md` with:
   - List of new drafts (with paths)
   - List of hunt cards flagged for refinement (with reasons)
   - List of hunt cards that fired correctly (positive feedback)

5. **Promotion workflow** (NOT automated):
   User reviews `DB/_drafts/`. To promote, user moves the file to the right manifest's directory and runs `python3 scripts/generate_manifests.py`. Document this in `DB/_drafts/README.md`.

### 10.6 Acceptance criteria
- [ ] On a past audit with known novel finding (one with no existing hunt card), gap-analysis correctly identifies the gap and produces a draft
- [ ] Drafts pass the TEMPLATE.md schema check (run `db-quality-monitor` against `DB/_drafts/` to verify)
- [ ] Hunt-card telemetry sidecars are created for all hunt cards that fired
- [ ] No drafts are written to manifest directories (only to `_drafts/`)
- [ ] `db-gap-analysis.md` is produced and human-readable

### 10.7 Files touched / created
- Edited: `.claude/agents/db-quality-monitor.md` (add gap-analysis mode)
- Created: `DB/_drafts/` directory + README
- Created: `DB/_telemetry/` directory + README
- Created: `audit-output/<id>/db-gap-analysis.md` per audit
- Edited: `.claude/rules/db-entries.md` (document `_drafts/` and `_telemetry/` conventions)

### 10.8 Failure modes & responses
- **Drafts are too noisy**: tighten the gap classification threshold (require shortest_path distance > 5 instead of 3).
- **TEMPLATE.md schema drift**: keep the draft generator in sync with `TEMPLATE.md`. Run quality monitor in CI.
- **`generate_manifests.py` accidentally indexes `_drafts/`**: add `_drafts/` and `_telemetry/` to the script's ignore list.

### 10.9 Estimated effort
3–5 days.

### 10.10 Dependencies
- Requires Doable 1 done (uses graph for shortest_path)
- Optionally uses Doable 4 (cross-audit lesson aggregation)

### 10.11 Execution mode
**Autonomous OK** for gap analysis itself (writes to `_drafts/` only, never live DB). User-supervised for promotion.

---

## 11. Doable 6 — `attack-graph-synthesizer` agent

### 11.1 Goal
A new agent that systematically searches for multi-step / cross-contract attacks by walking the codebase graph (from Doable 3) and checking each path against the invariant suite (from `invariant-writer`).

### 11.2 Why
Multi-step attacks are where Horus loses the most recall. Personas occasionally find them through intuition. This agent makes the search systematic.

### 11.3 Inputs
- `audit-output/<id>/graph/graph.json` (codebase graph, from Phase 0)
- `audit-output/<id>/invariants/invariants.md` (from invariant-writer)
- MCP endpoint from Phase 0

### 11.4 Outputs
- `audit-output/<id>/attack-candidates.md` — ranked candidate attack chains
- `audit-output/<id>/attack-candidates.json` — structured form for protocol-reasoning to consume

### 11.5 Schema for attack-candidates.json

```json
{
  "candidates": [
    {
      "id": "atk-001",
      "path": [
        {"node_id": "router_swap", "kind": "Function", "ecosystem": "evm"},
        {"node_id": "oracle_getprice", "kind": "Function"},
        {"node_id": "vault_borrow", "kind": "Function"},
        {"node_id": "vault_collateral", "kind": "StateVar", "edge": "WRITES_VAR"}
      ],
      "hypothesized_violation": "Invariant I-7 (collateral always backed by oracle TWAP)",
      "preconditions": ["attacker has flash loan capital", "swap moves spot price > 5%"],
      "severity_estimate": "HIGH",
      "rationale": "Spot-price oracle read inside borrow path allows manipulation by sandwich.",
      "validator": "protocol-reasoning",
      "reachability_proof_path": "audit-output/<id>/attack-proofs/atk-001.md"
    }
  ]
}
```

### 11.6 Step-by-step

1. **Create agent file**: `.claude/agents/attack-graph-synthesizer.md`. Standard agent frontmatter (per `.claude/rules/agents.md`).

2. **Algorithm** (specified in agent prompt):
   ```
   Phase A: Identify primitives
     - Query graph for all Function nodes with edge "EXTERNAL_CALL" → "external"
       OR with no access modifier (open to anyone)
     - These are entry points
     - Query for all StateVar nodes with > 0 incoming WRITES_VAR edges where
       the writer is reachable from an entry point. These are mutable state.

   Phase B: Path enumeration
     - For each (entry_point, mutable_state) pair, run BFS in the graph
       up to depth 5. Collect all paths.
     - Filter: drop paths where every step is gated by access control AND
       attacker cannot meet that access condition (heuristic: presence of
       owner-only / role-only modifier without a match in known compromised
       roles).

   Phase C: Hyperedge expansion
     - For each graphify-extracted hyperedge in graph.json, treat it as a
       candidate composition flow. For each, ask the invariant suite:
       "could the simultaneous invocation of these N functions violate
       any invariant?"

   Phase D: Invariant matching
     - For each candidate path/hyperedge from B and C:
       - Read invariants.md
       - For each invariant, ask via LLM: "does this path/composition violate
         this invariant? Be conservative — only return YES if there's a
         concrete reason."
       - If YES, write to attack-candidates.json with severity_estimate
         based on invariant criticality.

   Phase E: Reachability proofs
     - For each candidate, write a brief reachability sketch:
       - Required attacker capabilities (capital, role, prior state)
       - Sequence of transactions
       - Expected end state (which invariant breaks)
     - Save to audit-output/<id>/attack-proofs/<id>.md
     - These are NOT PoCs — they're hypotheses for protocol-reasoning to validate.

   Phase F: Hand off
     - Write attack-candidates.md (human-readable summary) and .json
     - Spawn protocol-reasoning agent with attack-candidates as input
   ```

3. **Wire into orchestrator**: After Phase 4 (Discovery), spawn `attack-graph-synthesizer`. Its output feeds into `protocol-reasoning` (already in pipeline) for validation.

4. **Skill wrapper**: Create `.claude/skills/attack-graph-synthesizer/SKILL.md` with `context: fork` and `agent: attack-graph-synthesizer`, mirroring existing skill conventions in `.claude/rules/skills.md`.

### 11.7 Acceptance criteria
- [ ] On a past audit known to contain a multi-step attack, the synthesizer surfaces a candidate that maps to the actual finding (path overlap ≥ 70%)
- [ ] Candidate count ≤ 50 per audit (more = too noisy, prune more aggressively)
- [ ] Each candidate has a non-trivial reachability sketch (not just "function A is callable")
- [ ] Hand-off to `protocol-reasoning` works without errors
- [ ] No regression in pipeline wall-clock time exceeding 20% from this agent alone

### 11.8 Files touched / created
- Created: `.claude/agents/attack-graph-synthesizer.md`
- Created: `.claude/skills/attack-graph-synthesizer/SKILL.md`
- Edited: `.claude/agents/audit-orchestrator.md` (insert call to new agent after Phase 4)
- Edited: `.claude/agents/protocol-reasoning.md` (consume attack-candidates.json as additional input)
- Edited: `.claude/resources/inter-agent-data-format.md` (document new artifact)

### 11.9 Failure modes & responses
- **Candidate explosion** (>500 per audit): tighten BFS depth to 3, filter aggressively by access control.
- **Invariant matching is noisy**: require LLM to cite the specific invariant clause; reject candidates without citation.
- **Synthesizer dominates wall-clock**: cap by time budget (e.g., 20 min). Return what it has.

### 11.10 Estimated effort
3–5 days.

### 11.11 Dependencies
- Requires Doable 3 (needs Phase 0 graph)
- Requires invariant-writer to have run (already in pipeline)

### 11.12 Execution mode
**Supervised**. New agent in critical pipeline path; user reviews on first 2–3 audits.

---

## 12. Sequencing & Dependencies

```
Week 1:
  D1 ────────────────────────────────────────┐
  D2 (Phase 2a: Solidity, Move-Sui, Cairo)──┐│
  D4 (start: schema + ingest)               │└─→ DB graph available
                                            │   for D5 to query
Week 2:                                     │
  D2 (Phase 2b: rest of languages) ─────────┤
  D3 (Phase 0 in orchestrator) ─────────────┤   ←─ depends on D2
  D4 (finish: wire into orchestrator)       │
                                            │
Week 3:                                     │
  D6 (attack-graph-synthesizer) ────────────┤   ←─ depends on D3
  D5 (start: gap analysis logic)            │
                                            │
Week 4:                                     │
  D5 (finish + integrate)                   │
  Recall benchmark validation ──────────────┘
  Decision: cutover from grep to graph?
```

Critical path: D2 → D3 → D6 (these block each other). D1, D4, D5 can run in parallel with the critical path.

---

## 13. Cross-cutting: New rules and conventions

### 13.1 New rules files to create

1. **`.claude/rules/graph-artifacts.md`** — conventions for `audit-output/<id>/graph/`
   - File naming: `graph.json`, `coverage.jsonl`, `mcp.pid`, `mcp.endpoint`, `wiki/`
   - When agents may write to this directory (only via the coverage append-log)
   - When agents may read (any time after Phase 0 declares done)

2. **`.claude/rules/lessons-db.md`** — conventions for `~/.horus/lessons.db`
   - Schema location: §9.5 of this plan
   - Privacy guardrails: §9.6 step 5
   - Query API: only via `lessons_db.py`, not direct sqlite3

3. **`.claude/rules/draft-hunt-cards.md`** — conventions for `DB/_drafts/`
   - TEMPLATE.md compliance required
   - Promotion workflow (manual: move + run `generate_manifests.py`)
   - Drafts NEVER load into `index.json` until promoted

### 13.2 Edits to existing rules

- `.claude/rules/audit-output.md`: add subdirectories `graph/`, `attack-proofs/`, `plan-execution/`
- `.claude/rules/db-entries.md`: reference new draft conventions
- `.claude/rules/scripts.md`: document `lessons_db.py` and `horus_graphify_blockchain` package

### 13.3 Edits to CLAUDE.md
Add to the "Key Agents" table:
- `attack-graph-synthesizer` (new in Doable 6)

Add to "Common Commands":
```
# Build/refresh DB graph
cd DB && /graphify . --mode deep --directed --wiki

# Query lessons
python3 scripts/lessons_db.py query --ecosystem <eco> --topic "..."

# Build blockchain AST for codebase
horus-graphify-blockchain extract <path> --out blockchain-ast.json
```

---

## 14. Risk Register

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | Graphify produces too many INFERRED edges, drowning signal | Medium | Medium | Tune `--mode deep` off; filter by `confidence_score >= 0.7` |
| R2 | Tree-sitter grammars for niche languages (Tact, Sway) are buggy | High | Low | Drop language from v1, document in GRAMMARS.md, ship without |
| R3 | Phase 0 doubles audit wall-clock time | Medium | High | Cache graph per codebase commit; reuse across audits if commit unchanged |
| R4 | Lessons DB leaks client info | Low | Critical | Default opt-in (Q3 default (b)); regex post-filter; per-client tagging for purge |
| R5 | attack-graph-synthesizer produces too many candidates | Medium | Medium | Aggressive filtering; time budget cap; require invariant citation |
| R6 | DB drafts pollute the manifest pipeline | Low | High | Explicit `_drafts/` ignore in `generate_manifests.py`; never auto-promote |
| R7 | MCP server crashes mid-audit | Medium | Medium | Fall back to direct graph.json reads (Read tool); detect via heartbeat |
| R8 | Recall benchmark doesn't exist | High | High | Build it as part of D1 acceptance work; see §15 |
| R9 | Plan author (me) misunderstood graphify's plugin API | Medium | Low | D2 step 8 falls back to merge-graphs (path (b)) which is documented |

---

## 15. Validation Strategy / Recall Benchmark

### 15.1 Why we need this
Without a labeled benchmark, "recall improved" is anecdotal. Section 1.3 sets the bar: ≥ 20% recall lift. We must measure this.

### 15.2 Benchmark dataset construction (per Q4 default)

1. Pick 10 past audits from `audit-output/` or `reports/` with confirmed findings.
2. For each finding, label:
   - `severity`
   - `category` (oracle, reentrancy, access control, etc.)
   - `multi_step` (boolean — required >1 transaction or contract)
   - `would_grep_find_it` (boolean — could a grep over the original DB manifests have surfaced the right hunt card?)
3. Save as `tests/benchmark/findings.jsonl`.

### 15.3 Recall measurement

For each Doable that affects recall (D1, D3, D6), re-run on the 10 audits with the new path. Measure:
- **Recall**: % of confirmed findings that any agent flagged as a candidate
- **Precision**: % of agent-flagged candidates that were confirmed

Baseline (pre-plan) values are established by running the current pipeline on the 10 audits before any Doable lands.

### 15.4 Acceptance gate

Before declaring the plan done:
- [ ] Recall improved ≥ 20% over baseline
- [ ] Precision dropped ≤ 33% (from e.g. 0.6 to ≥ 0.4) — some FP increase acceptable for big recall gains
- [ ] Wall-clock ≤ 1.5× baseline
- [ ] No regressions in confirmed-finding count on any individual audit

---

## 16. Glossary

- **CPG (Codebase Property Graph)**: Graph representation of source code with structural and semantic edges. Implemented here via graphify + horus-graphify-blockchain.
- **Hunt card**: A pattern entry in `DB/manifests/huntcards/`. Compressed detection signal.
- **Manifest**: A JSON file in `DB/manifests/` listing patterns at the section level with line ranges into the .md entries.
- **Phase 0**: New initial pipeline phase added by Doable 3. Builds graph, starts MCP server, initializes coverage tracker.
- **God node**: graphify term. Highest-degree node in a graph; a "central concept."
- **Hyperedge**: graphify term. A relationship between 3+ nodes representing a shared flow or pattern. Used by attack-graph-synthesizer.
- **MCP server**: Model Context Protocol server. graphify exposes graph queries this way.
- **Confidence-tagged edge**: An edge in graphify with `EXTRACTED` (deterministic), `INFERRED` (reasonable guess), or `AMBIGUOUS` (flagged for review) confidence.
- **Deepener**: An optional language-specific analyzer (Slither, anchor-syn, move-prover) that adds precision when present but is not required.
- **Coverage tracker**: `coverage.jsonl` log of which graph nodes have been visited by any agent during an audit. Used for blind-spot detection.

---

## 17. Final notes for executing agents

- **Read this file fully before starting your Doable**. Sections you might think don't apply (§5 conventions, §13 cross-cutting) almost certainly do.
- **Don't do the next Doable's work**. Each Doable is intentionally scoped. Resist scope creep.
- **Fail loudly**. Write failure reports to `audit-output/plan-execution/<doable-id>-failures.md` and stop. Better than silently doing the wrong thing.
- **Ask before destructive changes**. Per CLAUDE.md and §5.6: never commit, never delete, never overwrite uncommitted work without explicit user approval. Edits are reversible; commits and deletes aren't.
- **Stay agnostic**. Per C1: every line of code you write should work for any blockchain language. If you're tempted to special-case Solidity, ask yourself: does this work for Move? Cairo? Sway? If no, it goes into an opt-in deepener (§3.3), not core.

---

**End of plan v1.** Re-read §4 (open questions) before starting any Doable. Default answers are fine for autonomous execution; user override is welcome any time.
