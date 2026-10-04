# DB authoring

Use this when you want to add or edit vulnerability entries. The DB holds 337 entries across 18 manifests. Every entry follows `TEMPLATE.md`; `Example.md` shows one done right.

## Where entries come from

Four skills produce entries, each from a different source:

| Skill | Source | Output |
|---|---|---|
| `solodit-fetching` | Solodit API, by topic | Raw findings in `reports/<topic>_findings/` |
| `variant-template-writer` | 5 or more fetched reports per pattern | New entries, cross-report severity consensus |
| `defihacklabs-indexer` | Exploit PoCs in `DeFiHackLabs/` | Attack-graph entries from real exploit flows |
| `findings-db-synthesizer` | Your own confirmed audit findings | Entries and invariants, post-engagement |

The rule that matters most: dedup before you write. Query `DB/index.json` and the manifests for entries with the same root cause. If one exists, enrich it (new keywords, new detection pattern, new exploit example) instead of adding a parallel entry. Enrich beats duplicate. If the corpus has fewer than five reports supporting a pattern, the pattern is not ready and gets skipped.

## Writing an entry

Read `TEMPLATE.md` first. The non-negotiables:

- Frontmatter must be complete: `id`, `severity`, `tags`, `primitives`, `chain`, `protocolFocus`, `root_cause_family`, `pattern_key`, `attack_type`, `affected_component`, `code_keywords`, `impact`.
- Every finding needs concrete code references, a root cause, and an attack scenario. Not summaries.
- False-positive guards are required. An entry without them generates hunt cards that cry wolf.
- References cite real paths: report files, PoC files, or public links. The CI checks that DeFiHackLabs references resolve.

Entries live under `DB/<category>/<subdir>/<NAME>.md`. Pick the category from the existing layout; `scripts/horus_retrieval/taxonomy.py` maps directories to manifests, so a new directory needs a line there plus one in `protocol_context.py` if a protocol context should route to it.

## After writing

```bash
python3 scripts/generate_manifests.py     # rebuild index, manifests, hunt cards
python3 scripts/generate_micro_directives.py  # enrich cards with check/antipattern fields
python3 scripts/db_quality_check.py       # must print HEALTHY
```

Commit only when the quality check passes with zero warnings. The check verifies frontmatter coverage, section structure, hunt-card consistency, and that manifest line ranges actually point at pattern headings in your entry.

## Drafts

Unfinished entries can sit in `DB/_drafts/` without being indexed. They follow the template but carry `status: draft`. Promotion is a manual move into the right category directory, dropping the status field, and regenerating. Nothing in `_drafts/` or `_telemetry/` ever reaches a manifest.
