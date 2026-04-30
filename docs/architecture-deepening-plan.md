# Architecture Deepening Plan

This plan captures the recommended refactor sequence for making Horus easier to maintain without destabilizing the generated retrieval artifacts.

## Goal

Improve locality and leverage in the Horus maintenance code by moving repeated domain concepts behind deeper modules:

- DB document parsing and line-range extraction
- Protocol context taxonomy
- Retrieval artifact generation
- Runtime surface synchronization

The plan deliberately favors byte-stable, low-blast-radius steps over a large rewrite.

## Progress

- Started: extracted the shared protocol context taxonomy into `scripts/horus_retrieval/protocol_context.py`.
- Started: updated router generation, partition bundle generation, and DB quality required-context checks to consume the shared taxonomy.
- Started: added `tests/test_protocol_context.py` to lock the shared taxonomy interface.
- Started: added a narrow DB document parser in `scripts/horus_retrieval/documents.py` and migrated manifest-file parsing to it.
- Started: added fixture-level manifest output coverage in `tests/test_generate_manifest_fixture.py`.
- Started: moved category and general-subcategory taxonomy into `scripts/horus_retrieval/taxonomy.py`.
- Started: introduced `scripts/horus_retrieval/build.py` with `build_retrieval_db` orchestration and made `scripts/generate_manifests.py` delegate through it.
- Started: added temp-directory orchestration coverage in `tests/test_retrieval_build.py`.
- Started: extracted router builders into `scripts/horus_retrieval/router.py`.
- Started: extracted keyword-index builders into `scripts/horus_retrieval/keywords.py`.
- Started: extracted manifest builders into `scripts/horus_retrieval/manifests.py`, with `scripts/generate_manifests.py` retaining thin compatibility wrappers.
- Started: extracted hunt-card builders into `scripts/horus_retrieval/huntcards.py`, with focused regression coverage for filtering, grep selection, identifier extraction, and file writes.
- Started: extracted partition-bundle builders into `scripts/horus_retrieval/bundles.py`, keeping protocol shard generation testable without writing real DB artifacts.
- Started: migrated `scripts/db_quality_check.py` and `scripts/huntcard_enrichment.py` entry parsing paths onto shared `DBDocument`/frontmatter helpers while preserving their public result shapes.
- Started: added `.github/agents` surface validation to `scripts/sync_codex_compat.py --check`, covering missing, extra, and identity metadata drift against `.claude/agents`.
- Started: moved standard retrieval-build dependency wiring into `scripts/horus_retrieval/build.py`, so `build_retrieval_db(db_dir=...)` is now the main interface and `scripts/generate_manifests.py` is a thin compatibility CLI.
- Started: extracted retrieval artifact writing and summary reporting into `scripts/horus_retrieval/writers.py`, reducing filesystem mechanics inside the build orchestrator.
- Started: extracted optional hunt-card micro-directive enrichment into `scripts/horus_retrieval/enrichment.py`, keeping `build.py` responsible only for deciding whether the phase runs.

## Current Friction

### Retrieval build module

`scripts/generate_manifests.py` owns Markdown parsing, manifest shaping, router creation, keyword indexing, hunt-card creation, enrichment, partition bundles, file writes, and console output. Its implementation is broad enough that maintainers need to understand unrelated phases to safely change one phase.

### Protocol context duplication

Protocol mappings are repeated in router generation, partition bundle generation, and quality checks. The same domain concept is spread across multiple scripts, which makes drift likely.

### DB document parsing duplication

Frontmatter, headings, sections, line ranges, references, and metadata are parsed separately in multiple scripts. Each caller has to know parsing details rather than consuming a stable document interface.

### Runtime surface drift

`.claude/` is the source of truth for Codex generation, but `.github/agents/` remains a manually maintained parallel surface. That makes agent workflow changes easy to partially synchronize.

## Revised Sequence

### 1. Add golden regression tests first

Before moving code, add tests that make output stability explicit.

Recommended checks:

- Manifest generation remains byte-stable for committed fixtures or a representative fixture DB.
- Router, keywords, hunt cards, and bundle structures preserve counts and key fields.
- Existing generated artifacts do not change unless the refactor intentionally changes behavior.

This creates the test surface for later refactors.

### 2. Extract `ProtocolContext` first

This is the lowest-risk, highest-signal extraction.

Create a canonical module, for example:

```text
scripts/horus_retrieval/protocol_context.py
```

It should own:

- protocol names
- descriptions
- manifest lists
- focus patterns
- bundle inputs
- required validation contexts

Consumers:

- `scripts/generate_manifests.py` router generation
- `scripts/generate_manifests.py` partition bundle generation
- `scripts/db_quality_check.py` protocol context checks

Success criteria:

- No duplicate protocol mapping dicts remain in generation or quality checks.
- Generated artifacts are unchanged.
- Quality checks still validate every protocol context against existing manifests.

### 3. Extract a narrow `DBDocument` interface inside generation only

Create a document module, but migrate only `generate_manifests.py` at first.

Recommended module:

```text
scripts/horus_retrieval/documents.py
```

The interface should expose:

- frontmatter
- headings and section ranges
- section text access
- report references
- derived section signals used by manifest generation

Do not put compliance logic in `DBDocument`; compliance belongs to quality checks. Keeping compliance separate prevents the document module from becoming a broad god object.

Success criteria:

- `generate_manifests.py` consumes `DBDocument`.
- Manifest and hunt-card outputs remain unchanged.
- `db_quality_check.py` and `huntcard_enrichment.py` are not migrated yet.

### 4. Split `RetrievalBuild` into orchestration plus pure builders

After parsing and protocol taxonomy are stable, introduce the deeper build interface.

Recommended public interface:

```python
build_retrieval_db(
    db_root=Path("DB"),
    output_root=Path("DB/manifests"),
    enrich_huntcards=True,
    build_bundles=True,
)
```

Recommended module shape:

```text
scripts/horus_retrieval/
  build.py
  documents.py
  manifests.py
  router.py
  keywords.py
  huntcards.py
  bundles.py
  writers.py
  protocol_context.py
```

Keep `scripts/generate_manifests.py` as a thin CLI wrapper.

Important seam discipline:

- Pure builders return structured data.
- Writers perform filesystem writes.
- CLI code handles printing and process-level behavior.

Success criteria:

- `generate_manifests.py` is a thin interface.
- Builders can be tested without touching the real `DB/` output tree.
- Existing regeneration commands still work.

### 5. Migrate quality and enrichment to shared parsing later

Only after the generation pipeline is stable should other scripts consume `DBDocument`.

Later consumers:

- `scripts/db_quality_check.py`
- `scripts/huntcard_enrichment.py`

Success criteria:

- Quality checks no longer duplicate frontmatter and section parsing.
- Hunt-card enrichment reads sections through the same document interface.
- Existing tests pass and generated artifacts remain stable.

### 6. Treat runtime sync as a separate track

`RuntimeSurfaceSync` is useful, but it is not coupled to retrieval generation and should not block that work.

Recommended first step:

- Add GitHub-facing validation before adding generation.

Do not immediately auto-generate `.github/agents/`; that changes repo policy and may be surprising.

Potential module shape:

```text
scripts/horus_runtime_sync/
  source_tree.py
  codex_adapter.py
  github_adapter.py
  links.py
  check.py
```

Success criteria:

- Existing `.claude -> .agents/.codex` generation remains unchanged.
- `.github/agents` drift becomes explicit in validation output.
- No generated Codex artifacts change unexpectedly.

## Guardrails

- Do not hand-edit generated manifests, hunt cards, DB graph output, `.agents/`, or `.codex/`.
- Keep behavior byte-stable unless a change is explicitly intended.
- Do not make `DBDocument` responsible for quality policy.
- Do not make `RetrievalBuild` another large implementation module; it should orchestrate narrower builders.
- Keep `CATEGORY_MAP`, `GENERAL_SUBCATEGORIES`, and `PROTOCOL_CONTEXTS` in taxonomy/config modules.
- Keep `auditChecklist` separate unless it becomes data-driven as part of a later change.
- Start `.github/agents` work with validation, not automatic generation.

## Recommended Milestones

### Milestone 1: Safety net

- Add golden or fixture-based output tests.
- Ensure refactors can prove no output drift.

### Milestone 2: Protocol taxonomy

- Extract protocol context data.
- Update router, bundle generation, and quality checks to consume it.
- Verify generated output parity.

### Milestone 3: Document parsing

- Add `DBDocument`.
- Migrate only manifest generation.
- Verify output parity.

### Milestone 4: Retrieval build split

- Introduce `build_retrieval_db`.
- Move pure builders and writers into focused modules.
- Keep the existing CLI command working.

### Milestone 5: Shared parsing adoption

- Migrate quality checks and enrichment onto `DBDocument`.
- Expand tests for compliance and enrichment behavior.

### Milestone 6: Runtime sync validation

- Add validation for `.github/agents` parity.
- Keep Codex generation behavior stable.
