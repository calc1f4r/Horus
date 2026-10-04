---
name: "prior-art-matcher"
description: "Answer \"what is already known to be broken in code exactly like this target?\" before discovery starts. Fingerprints protocol lineage (Aave, Compound, Uniswap, Curve, OpenZeppelin, Solmate), mines local reports/ then Solodit for prior audits of that lineage, matches DeFiHackLabs incidents by lineage rather than keyword, and assigns applicability verdicts against the target copy. Use when auditing a fork or before Phase 4 discovery rounds."
---
Use the [prior-art-matcher subagent](../../../.codex/agents/prior-art-matcher.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<codebase-path>`.

Find prior art applicable to `<codebase-path>`.

## Retrieval axis

Hunt cards retrieve by **vulnerability pattern**. This retrieves by **codebase lineage** — it catches bugs pattern search misses, because the pattern may not be in the DB yet while the incident already happened upstream.

## Applicability verdicts

| Verdict | Meaning |
|---------|---------|
| `inherited-unfixed` | Vulnerable code present unmodified — **highest priority Phase 4 seed** |
| `inherited-modified` | Present but changed; needs fresh analysis |
| `fixed-in-target` | Upstream fix or equivalent present |
| `not-applicable` | Vulnerable construct absent |

Every verdict requires target-code evidence, never the report's description.

## Output

- `audit-output/04-prior-art.md` — lineage fingerprint, prior-art items, hunt cards to expand, ranked Phase 4 seeds

## Related skills

- [solodit-fetching](../solodit-fetching/SKILL.md) — Solodit API access
- [defihacklabs-indexer](../defihacklabs-indexer/SKILL.md) — DeFiHackLabs corpus
- [invariant-catcher](../invariant-catcher/SKILL.md) — the pattern axis
