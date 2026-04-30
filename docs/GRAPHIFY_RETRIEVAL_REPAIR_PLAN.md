# Graphify And Retrieval Repair Plan

Status: Implemented through graph-depth, compliance-detection, mirror-generation, CI, and regression-test phase
Date: 2026-04-30
Scope: Fix false health failures, Graphify graph-contract drift, shallow DB graph expansion, and DB entry metadata issues without hand-editing generated artifacts.

## 0. Purpose

Horus currently has a mostly working retrieval pipeline:

- `python3 scripts/generate_manifests.py` succeeds.
- `python3 scripts/build_db_graph.py` succeeds.
- `graphify query ... --graph DB/graphify-out/graph.json` works.
- Manifests, hunt cards, and sampled line ranges are internally consistent.

The initial problems were not one single broken script. They were interface-contract drift between modules:

- The quality checker reports `BROKEN` for a stale root-level generator path.
- The audit orchestrator can write raw Graphify extraction JSON as `audit-output/graph/graph.json`, which Graphify CLI/MCP cannot load.
- The DB graph is valid but shallow, dominated by category and keyword hub nodes.
- A small set of DB entries still violate metadata/template expectations.
- The local Python environment needed an explicit development dependency surface so regression coverage could run consistently.

This plan is ordered to fix reliability first, then graph correctness, then graph quality.

## Implementation Status

Completed:

- `scripts/db_quality_check.py` now checks the canonical generator path, validates Graphify artifacts, and reports `HEALTHY` with zero warnings on the current DB.
- `scripts/finalize_audit_graph.py` converts raw `.graphify_extract.json` or existing graphify `graph.json` into queryable node-link graph JSON.
- Audit orchestrator Phase 0 now calls `scripts/finalize_audit_graph.py`.
- The known DB frontmatter and invalid severity issues have been fixed.
- `scripts/build_db_graph.py` now emits semantic graph nodes and bounded `related_variant` edges.
- `scripts/build_db_graph.py` now writes a curated graph wiki: the full community set remains in `graph.json` and `GRAPH_REPORT.md`, while `wiki/` is limited to multi-node communities plus god-node articles.
- Regression tests cover the finalizer and semantic DB graph extraction.
- `scripts/db_quality_check.py` now recognizes the current DB schema for root causes, vulnerable examples, secure guidance, and frontmatter-backed keywords instead of relying only on legacy emoji markers.
- `requirements-dev.txt` documents pytest and the pinned `graphifyy==0.5.2` development dependency.
- `scripts/sync_codex_compat.py` now generates and checks the `.github/agents/**` mirror from `.claude/agents/**`, while also enforcing `.claude/resources/**` to `.github/agents/resources/**` parity.
- `.github/workflows/validate-retrieval-pipeline.yml` runs the full retrieval validation pipeline in CI.

Current validation baseline:

```text
python3 scripts/db_quality_check.py
  Full compliance: 218/218 (100%)
  Required frontmatter field coverage: 218/218 for every required field
  Critical issues: 0
  Warnings: 0
  Overall: HEALTHY

python3 scripts/build_db_graph.py
  5270 nodes
  51146 edges
  1038 communities
  58 wiki articles from 43 curated communities

python3 scripts/validate_retrieval_pipeline.py
  Unit tests: 70 passed
  DB quality: HEALTHY
  Graph JSON: OK
  Graphify query/path checks: OK
  Codex/GitHub mirror sync checks: OK
  Audit graph finalizer: OK
```

## 1. Non-Negotiable Guardrails

- Do not hand-edit generated JSON under `DB/manifests/**`.
- Do not hand-edit generated graph artifacts under `DB/graphify-out/**`.
- Do not hand-edit generated Codex files under `.agents/skills/**` or `.codex/**`.
- If DB Markdown changes, run `python3 scripts/generate_manifests.py`.
- If hunt-card or graph relationship inputs change, run `python3 scripts/build_db_graph.py`.
- If Claude playbooks change, run `python3 scripts/sync_codex_compat.py` and `python3 scripts/sync_codex_compat.py --check`.
- Preserve existing untracked work unless explicitly asked to replace it.

## 2. Current Baseline

Observed on 2026-04-29:

```text
python3 scripts/generate_manifests.py
  OK
  218 files indexed
  1972 patterns extracted
  1362 hunt cards generated/enriched

python3 scripts/build_db_graph.py
  OK
  1954 nodes
  10919 edges
  21 communities
  graphify version 0.5.2

python3 scripts/db_quality_check.py
  Reports Overall: BROKEN
  Real generated artifacts are mostly valid
  Main critical is stale root generate_manifests.py path
```

Graphify status:

- Installed CLI: `graphify`
- Python package import: `graphifyy 0.5.2`
- `DB/graphify-out/graph.json` validates with Graphify extraction schema.
- `graphify query "oracle staleness" --graph DB/graphify-out/graph.json` works.
- `graphify query ... --graph DB/graphify-out/.graphify_extract.json` fails because extraction JSON is not node-link graph JSON.

## 3. Target Architecture

The fixed architecture should expose four deeper modules/interfaces:

```text
DB Markdown
  -> RetrievalBuild
  -> GeneratedRetrievalArtifacts
  -> DBGraphBuilder
  -> GraphifyNodeLinkGraph

Audit codebase graphify output
  -> AuditGraphFinalizer
  -> audit-output/graph/graph.json
  -> Graphify CLI/MCP

Generated artifacts
  -> DBQualityChecker
  -> truthful HEALTHY/DEGRADED/BROKEN result

DB graph + retrieval artifacts
  -> GraphAwareExpansion
  -> related hunt-card candidates
```

The important design rule: any file named `graph.json` must be Graphify node-link graph JSON, not raw extraction JSON.

## 4. Phase 1: Make Health Checks Truthful

Goal: make `scripts/db_quality_check.py` report actual operational health.

### 4.1 Fix stale generator path

Files:

- `scripts/db_quality_check.py`

Change the script-health check from root `generate_manifests.py` to canonical `scripts/generate_manifests.py`.

Current problem:

```python
os.path.isfile("generate_manifests.py")
```

Recommended behavior:

```python
GENERATOR = Path("scripts/generate_manifests.py")
```

Classification:

- Missing canonical generator: `CRITICAL`
- Missing root compatibility wrapper: no issue, or at most `INFO`

Definition of done:

- `python3 scripts/db_quality_check.py` no longer reports `BROKEN` solely because root `generate_manifests.py` is absent.
- The summary distinguishes repo drift from runtime breakage.

### 4.2 Stop pretending to run the generator

Files:

- `scripts/db_quality_check.py`

Current output says:

```text
Testing generate_manifests.py...
```

But the checker only validates existing generated JSON.

Recommended solution:

- Rename this section to `Validating generated manifest JSON...`, or
- Add an explicit opt-in flag such as `--run-generator` that executes `python3 scripts/generate_manifests.py`.

Preferred first step:

- Rename the message and keep the checker non-mutating by default.

Definition of done:

- Default quality check does not mutate generated files.
- Any mutating generator execution is opt-in and obvious.

### 4.3 Add Graphify artifact checks

Files:

- `scripts/db_quality_check.py`
- optional helper: `scripts/horus_retrieval/graph_validation.py`

Add a new check:

```text
SKILL 8: GRAPHIFY ARTIFACT HEALTH
```

Validate:

- `DB/graphify-out/graph.json` exists.
- JSON has `nodes`.
- JSON has `links` or `edges`.
- All edge endpoints exist in node IDs.
- `graphify query "oracle staleness" --graph DB/graphify-out/graph.json --budget 200` succeeds when `graphify` is installed.
- Graph node/edge count is nonzero.

Severity:

- Missing graph: `WARNING` unless graph-required mode is requested.
- Invalid graph JSON: `CRITICAL`.
- Graphify CLI absent: `WARNING`, because the DB graph can still be generated if the Python package is available.

Definition of done:

- The quality checker catches malformed graph files.
- The checker does not mark the repo broken when Graphify is merely unavailable and the task can proceed without graph features.

## 5. Phase 2: Fix Audit-Time Graphify Contract

Goal: prevent Phase 0 from creating an invalid `audit-output/graph/graph.json`.

### 5.1 Create `scripts/finalize_audit_graph.py`

New file:

- `scripts/finalize_audit_graph.py`

Interface:

```bash
python3 scripts/finalize_audit_graph.py \
  --codebase <path> \
  --out audit-output/graph/graph.json \
  --blockchain-ast audit-output/graph/blockchain-ast.json
```

Responsibilities:

1. Locate Graphify output:
   - Prefer `<codebase>/graphify-out/graph.json` when present and valid node-link JSON.
   - Fall back to `<codebase>/graphify-out/.graphify_extract.json` only by converting it through `graphify.build.build`.
2. Optionally merge blockchain AST extraction:
   - Deduplicate nodes by `id`.
   - Append edges and hyperedges.
   - Preserve `source_file`, `relation`, `confidence`, and `node_kind`.
3. Convert the merged extraction into Graphify node-link graph JSON if needed.
4. Write `audit-output/graph/graph.json`.
5. Validate the final graph:
   - has nodes and links/edges
   - can be loaded by NetworkX with `edges="links"`
   - can be queried by Graphify CLI if installed

Important behavior:

- A file named `graph.json` must never contain raw extraction JSON only.
- If conversion fails, write a clear warning and return nonzero only when `--strict` is provided.
- Default audit behavior remains soft-gated: Graphify failure should not abort a whole audit.

Definition of done:

- Running the finalizer on a Graphify extraction produces a CLI-queryable graph.
- Running it on an existing Graphify node-link graph preserves queryability.
- Running it with blockchain AST merges additional graph data without corrupting the base graph.

### 5.2 Update audit orchestrator playbooks

Files:

- `.claude/agents/audit-orchestrator.md`
- `.github/agents/audit-orchestrator.md`

Generated after source change:

- `.codex/agents/audit-orchestrator.toml`

Replace the inline Python merge snippet with:

```bash
python3 scripts/finalize_audit_graph.py \
  --codebase "$CODEBASE" \
  --blockchain-ast audit-output/graph/blockchain-ast.json \
  --out audit-output/graph/graph.json
```

Then run:

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --check
```

Definition of done:

- Claude and GitHub audit-orchestrator docs describe the same Phase 0 graph finalization behavior.
- Codex generated agent reflects the `.claude` source.
- Phase 0 no longer documents writing raw extraction JSON as final `graph.json`.

## 6. Phase 3: Deepen DB Graph Semantics

Goal: make `DB/graphify-out/graph.json` useful for related hunt-card expansion, not just category browsing.

### 6.1 Add semantic node types

Files:

- `scripts/build_db_graph.py`
- possibly `scripts/horus_retrieval/graph_inputs.py`

Add nodes for:

- `RootCauseFamily`
- `AttackType`
- `AffectedComponent`
- `ProtocolContext`
- `Manifest`
- `GraphHint`
- `ReportEvidence`
- `Severity`

Potential sources:

- Manifest pattern fields
- Hunt-card fields
- DB Markdown frontmatter
- `reportEvidence`
- `graphHints`
- `scripts/horus_retrieval/protocol_context.py`

Recommended edge examples:

```text
HuntCard -> Manifest                 belongs_to_manifest
HuntCard -> RootCauseFamily          has_root_cause_family
HuntCard -> AttackType               has_attack_type
HuntCard -> AffectedComponent        affects_component
HuntCard -> ProtocolContext          relevant_to_protocol
HuntCard -> GraphHint                hints_variant
HuntCard -> Severity                 has_severity
ProtocolContext -> Manifest          routes_to_manifest
DBEntry -> ReportEvidence            supported_by_report
```

Definition of done:

- Graph report god nodes are less dominated by broad category labels.
- Querying a topic returns related cards through semantic relationships, not only shared grep keywords.

### 6.2 Add related-card edges

Files:

- `scripts/build_db_graph.py`

Create inferred card-to-card edges when two hunt cards share strong signals:

- Same root cause family and affected component.
- Same attack type plus overlapping graph hints.
- Shared reportEvidence category.
- Shared protocol context and high-confidence keyword overlap.

Recommended relation:

```text
HuntCard -> HuntCard  related_variant
```

Confidence:

- `EXTRACTED` only for explicit `graphHints` or direct metadata.
- `INFERRED` for similarity-derived edges.

Definition of done:

- `graphify query "flash loan oracle manipulation" --graph DB/graphify-out/graph.json` surfaces oracle manipulation and flash-loan related cards.
- A path or query from oracle concepts to flash-loan oracle manipulation no longer depends on broad category hubs only.

### 6.3 Add graph-quality checks

Files:

- `scripts/db_quality_check.py`
- `tests/test_db_graph.py`

Check:

- Number of semantic node types.
- Existence of at least one `related_variant` edge.
- Known queries return expected labels.
- No top god node exceeds a chosen domination threshold unless allowlisted.

Example expectations:

```text
Query: oracle flash loan
Expected: flash-loan oracle manipulation card appears

Query: ERC4626 first depositor
Expected: vault inflation / first depositor cards appear

Query: cross-chain replay
Expected: bridge replay cards appear
```

Definition of done:

- Graph quality can regress only by failing a visible test/check.

## 7. Phase 4: Clean DB Entry Metadata

Goal: remove known DB entry compliance failures that pollute routing and generated artifacts.

### 7.1 Fix missing frontmatter

Files:

- `DB/general/reentrancy/reentrancy.md`
- `DB/general/rounding-precision-loss/rounding-precision-loss.md`
- `DB/general/slippage-protection/slippage-protection.md`

Required fields:

```yaml
protocol:
category:
vulnerability_type:
attack_type:
affected_component:
severity:
impact:
```

Definition of done:

- `db_quality_check.py` reports no files missing frontmatter.

### 7.2 Fix invalid severity shape

File:

- `DB/general/perpetuals-derivatives/PERPETUALS_DERIVATIVES_VULNERABILITIES.md`

Current invalid shape:

```yaml
severity: critical|high|medium
```

Recommended decision:

- If entries are pattern collections, prefer a canonical top-level severity policy.
- For quality checker compatibility, use a single canonical severity string unless the parser is intentionally extended.

Conservative first fix:

```yaml
severity: critical
```

Follow-up option:

- Add support for a structured list only if the whole generator and quality checker agree on the schema.

Definition of done:

- No invalid severity warnings remain.
- Regenerated manifests preserve expected severity extraction for section-level patterns.

### 7.3 Regenerate generated artifacts

After DB source changes:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
python3 scripts/build_db_graph.py
```

Definition of done:

- Manifest generation succeeds.
- Quality check no longer reports the fixed metadata issues.
- DB graph rebuild succeeds.

## 8. Phase 5: Make Tests Executable

Goal: make the existing retrieval and graph tests runnable from the default repo workflow.

### 8.1 Choose a test environment policy

Current issue:

```text
python3 -m pytest ...
  No module named pytest
```

Recommended options:

1. Repair `.venv` and install test dependencies there.
2. Add a small `requirements-dev.txt`.
3. Add a `pyproject.toml` test extra if this repo is moving toward package-style Python.

Preferred first step:

```text
requirements-dev.txt
```

Minimum contents:

```text
pytest
```

If Graphify tests are included, document that `graphifyy` must be installed too.

Definition of done:

- A contributor can run the test suite with documented commands.

### 8.2 Add regression tests

Files:

- `tests/test_db_quality_check.py`
- `tests/test_finalize_audit_graph.py`
- `tests/test_db_graph.py`

Required tests:

1. Quality checker recognizes `scripts/generate_manifests.py`.
2. Quality checker does not require root `generate_manifests.py`.
3. Audit graph finalizer converts extraction JSON into node-link graph JSON.
4. Finalized audit graph can be loaded with NetworkX `edges="links"`.
5. DB graph builder emits `links` and `edges` compatibility fields.
6. DB graph contains expected semantic edges after Phase 3.

Definition of done:

- Tests fail on the current bad contracts.
- Tests pass after Phases 1 through 3.

## 9. Phase 6: Documentation And Runtime Surface Sync

Goal: keep human docs, Claude playbooks, GitHub playbooks, and Codex generated surfaces aligned.

Files:

- `docs/codex-architecture.md`
- `.claude/agents/audit-orchestrator.md`
- `.github/agents/audit-orchestrator.md`
- `.claude/resources/orchestration-pipeline.md`
- `.github/agents/resources/orchestration-pipeline.md`
- generated `.codex/agents/audit-orchestrator.toml`

Updates:

- Document that `graph.json` means Graphify node-link graph JSON.
- Document that `.graphify_extract.json` is an intermediate extraction file.
- Document `scripts/finalize_audit_graph.py`.
- Update Phase 0 commands.
- Update Graphify failure handling and validation expectations.

Commands:

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --check
```

Definition of done:

- `.claude` and `.github` Phase 0 instructions agree.
- Codex generated surfaces match `.claude` source.
- Docs no longer imply raw extraction JSON is a valid final graph.

## 10. Suggested Execution Order

### Pass A: Reliability

1. Patch `scripts/db_quality_check.py` generator path check.
2. Rename misleading generator-test output.
3. Add Graphify artifact health check.
4. Run:

```bash
python3 scripts/db_quality_check.py
```

Expected result:

- No false `BROKEN` from missing root generator.
- Real DB metadata warnings remain visible.

### Pass B: Audit Graph Correctness

1. Add `scripts/finalize_audit_graph.py`.
2. Add focused tests for extraction-to-graph conversion.
3. Update `.claude/agents/audit-orchestrator.md`.
4. Update `.github/agents/audit-orchestrator.md`.
5. Regenerate Codex surfaces.

Commands:

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --check
```

Expected result:

- Phase 0 creates queryable `audit-output/graph/graph.json`.

### Pass C: DB Graph Quality

1. Add semantic graph inputs.
2. Add related-card edges.
3. Add known graph-query checks.
4. Rebuild graph.

Commands:

```bash
python3 scripts/build_db_graph.py
graphify query "oracle flash loan" --graph DB/graphify-out/graph.json --budget 2000
```

Expected result:

- Query output includes meaningful oracle/flash-loan variant cards.

### Pass D: DB Source Cleanup

1. Fix the three missing-frontmatter DB entries.
2. Fix invalid severity in perpetuals derivatives entry.
3. Regenerate retrieval artifacts.
4. Rebuild DB graph.

Commands:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
python3 scripts/build_db_graph.py
```

Expected result:

- No missing-frontmatter warnings.
- No invalid severity warning.
- Generated artifacts remain internally consistent.

### Pass E: Test Environment

1. Add or document dev dependencies.
2. Run focused tests.
3. Add CI or local validation command if desired.

Expected command:

```bash
python3 -m pytest tests/test_retrieval_build.py tests/test_huntcards.py tests/test_router_keywords.py tests/test_bundles.py tests/test_protocol_context.py
```

## 11. Done Criteria For The Whole Project

The project is complete when all of the following are true:

- `python3 scripts/generate_manifests.py` succeeds.
- `python3 scripts/db_quality_check.py` reports no false critical issue from root generator drift.
- `python3 scripts/build_db_graph.py` succeeds.
- `graphify query "oracle staleness" --graph DB/graphify-out/graph.json --budget 1000` succeeds.
- `scripts/finalize_audit_graph.py` can produce a queryable `audit-output/graph/graph.json`.
- Phase 0 docs call the finalizer instead of embedding raw merge code.
- DB graph has semantic nodes/edges beyond category and grep keyword hubs.
- Known graph expansion queries surface expected hunt cards.
- Missing-frontmatter and invalid-severity DB entry issues are fixed.
- Focused retrieval/graph tests are executable in the documented dev environment.

## 12. Risks And Mitigations

Risk: Graph changes produce noisy relationships.

Mitigation: start with extracted metadata edges before adding inferred similarity edges. Gate inferred edges behind confidence and tests.

Risk: Quality checker becomes mutating and surprises maintainers.

Mitigation: keep default checks read-only. Put generator execution behind `--run-generator`.

Risk: Audit orchestrator and generated Codex agent drift.

Mitigation: edit `.claude` source, explicitly update `.github`, then run sync/check.

Risk: DB metadata cleanup changes generated artifact counts.

Mitigation: inspect manifest and hunt-card count diffs after regeneration. Count changes are acceptable only if explained by source metadata changes.

Risk: Test environment churn blocks simple maintenance.

Mitigation: keep dependency setup minimal at first: `pytest` plus already-required runtime packages.

## 13. Recommended First Implementation Slice

The first slice should be small and high confidence:

1. Patch `db_quality_check.py` to use `scripts/generate_manifests.py`.
2. Rename the misleading generator-test message.
3. Add a graph artifact validation check that only reads files.
4. Add `scripts/finalize_audit_graph.py` with extraction-to-node-link conversion.
5. Add one test fixture for the finalizer.

This slice removes false `BROKEN` output and prevents the most serious Graphify misuse without changing DB content or graph semantics.
