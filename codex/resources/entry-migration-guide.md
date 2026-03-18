<!-- AUTO-GENERATED from `.claude/resources/entry-migration-guide.md`; source_sha256=5bf57021d9a749d7470a8cc089c9dab325357147243522a966b7ddfac0b84413 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/entry-migration-guide.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Entry Migration Guide

Shared guidance for upgrading existing `DB/**/*.md` entries to the current `TEMPLATE.md` format without losing evidence or creating duplicate patterns.

## When Migration Is Required

Migrate an entry when any of the following is true:

- You touch an existing DB entry for any substantive edit.
- A legacy entry is missing required frontmatter such as `root_cause_family`, `pattern_key`, or `code_keywords`.
- A legacy entry lacks the low-context agent sections near the top of the file.
- A new report cluster overlaps an existing DB entry strongly enough that creating a second file would duplicate the pattern.
- `db-quality-monitor` flags template drift, missing grep seeds, or missing triage sections.

## Migration Goals

- Preserve all real evidence, references, and working code examples.
- Upgrade the entry in-place when possible instead of creating a near-duplicate file.
- Front-load the entry so low-context agents can triage it from the first `~150` lines.
- Normalize the structure so manifest generation, hunt cards, and report indexing all see the same signals.

## Required Migration Steps

1. **Check for overlap first**
   - Search `DB/**/*.md` for the same root cause family, affected component, and sink.
   - If an existing file already covers the pattern, migrate that file instead of creating a new duplicate.

2. **Preserve the canonical file path when possible**
   - Keep the existing path if the entry is already in the right DB category.
   - Move only when the current location is clearly wrong and the migration plan is explicit.

3. **Upgrade frontmatter**
   - Add or normalize: `chain`, `root_cause_family`, `pattern_key`, `code_keywords`, `primitives`, `severity`, `impact`, and other required template fields.
   - For cross-contract or multi-path issues, also add `interaction_scope`, `involved_contracts`, and `path_keys`.
   - Keep `code_keywords` grep-able: function names, modifiers, selectors, storage vars, error names, critical identifiers.

4. **Upgrade the top-of-file triage layer**
   - Add `References & Source Reports` near the top.
   - Add `Agent Quick View`.
   - Add `Valid Bug Signals`.
   - Add `False Positive Guards`.
   - Add `High-Signal Grep Seeds` under `Detection Patterns`.

5. **Split materially distinct exploit paths**
   - Replace one blended attack story with `Path A / Path B / Path C` when the trigger, component, contract hop set, or sink differs.
   - For multi-contract findings, add a `Contract / Boundary Map` and give each path a `path_key`.

6. **Preserve and reorganize evidence**
   - Keep real-world examples, code snippets, and references.
   - Move verbose appendix-style material lower in the file rather than deleting it.
   - If legacy content conflicts with the current pattern definition, rewrite the summary and clearly scope the examples.

7. **Regenerate downstream artifacts**
   - Run `python3 scripts/generate_manifests.py` after migration so manifests and hunt cards pick up the new structure.

## Migration Acceptance Checklist

- The entry follows the current `TEMPLATE.md` structure.
- The first `~150` lines are sufficient for low-context triage.
- `root_cause_family`, `pattern_key`, and `code_keywords` are present and specific.
- Multi-contract or multi-path findings also include `interaction_scope`, `involved_contracts`, and `path_keys`.
- `Valid Bug Signals` and `False Positive Guards` are evidence-backed.
- Distinct exploit paths are split instead of blended.
- No duplicate DB entry remains for the same pattern unless there is a justified category boundary.
- Manifests were regenerated after the migration.

## Safety Rules

- Do not delete evidence-rich legacy content unless it is clearly duplicate filler.
- Do not create a new file if the existing file can be migrated in-place.
- Do not silently merge two entries with materially different `pattern_key` values.
- If category placement or duplicate consolidation is ambiguous, prefer migration notes and cross-links over destructive cleanup.