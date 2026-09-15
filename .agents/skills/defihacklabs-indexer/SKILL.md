---
name: "defihacklabs-indexer"
description: "Analyze DeFiHackLabs exploit PoCs or exploit folders to build attack-graph-aware DB entries and exploit-derived invariants. Use when indexing DeFiHackLabs cases, especially multi-step or multi-path exploit flows that do not fit flat report clustering."
---
Use the [defihacklabs-indexer subagent](../../../.codex/agents/defihacklabs-indexer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<exploit-file-or-folder-or-topic>`.

Analyze DeFiHackLabs exploit material from `<exploit-file-or-folder-or-topic>`.

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

- [variant-template-writer](../variant-template-writer/SKILL.md) — Use for raw report clustering when PoCs are not the primary evidence
- [invariant-indexer](../invariant-indexer/SKILL.md) — Use for mining canonical invariants from production protocols and formal specs
- [db-quality-monitor](../db-quality-monitor/SKILL.md) — Use to validate DB integrity after new exploit indexing work