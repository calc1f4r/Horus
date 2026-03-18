name: defihacklabs-indexer
description: "Analyze DeFiHackLabs exploit PoCs or exploit folders to build attack-graph-aware DB entries and exploit-derived invariants. Use when indexing DeFiHackLabs cases, especially multi-step or multi-path exploit flows that do not fit flat report clustering."
context: fork
agent: defihacklabs-indexer
argument-hint: <exploit-file-or-folder-or-topic>
---

<!-- AUTO-GENERATED from `.claude/skills/defihacklabs-indexer/SKILL.md`; source_sha256=6cf3c48022f97807ef85183d7cc3c5c71222ad5582a256d3c6370316e2bd204c -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/defihacklabs-indexer/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/defihacklabs-indexer.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Analyze DeFiHackLabs exploit material from `$ARGUMENTS`.

## What this does

1. **Reads PoC code as primary evidence** — including helper contracts, callbacks, setup, and firing flow
2. **Reconstructs the attack graph** — setup stage, execution stage, callbacks, loops, branches, and cross-protocol edges
3. **Classifies the exploit** — by root cause, trigger primitive, path shape, sink, and broken invariant
4. **Creates or migrates DB entries** — choosing between general entries, unique entries, or both
5. **Writes exploit-derived invariants** — into the appropriate `invariants/` category

## Output

- `DB/**` or `DB/unique/defihacklabs/**` — created or migrated attack-pattern entries
- `invariants/**` — exploit-derived invariant files or updates

After DB changes, run `python3 scripts/generate_manifests.py` to refresh manifests and hunt cards.

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — Use for raw report clustering when PoCs are not the primary evidence
- [/invariant-indexer](../invariant-indexer/SKILL.md) — Use for mining canonical invariants from production protocols and formal specs
- [/db-quality-monitor](../db-quality-monitor/SKILL.md) — Use to validate DB integrity after new exploit indexing work