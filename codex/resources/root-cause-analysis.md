<!-- AUTO-GENERATED from `.claude/resources/root-cause-analysis.md`; source_sha256=5f38dc44291cae55ead9a0bfe5455cb1e878ff8ba641d0a9df2b3bc80c4bd673 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/root-cause-analysis.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Root Cause Analysis Framework

Shared framework for extracting vulnerability patterns from exploits and audit reports.

## The 5 Critical Questions

For every vulnerability, answer ALL with evidence from source code:

| # | Question | What to extract |
|---|----------|----------------|
| 1 | **What operation is dangerous?** | Specific function call, math operation, or state transition |
| 2 | **What data/condition makes it dangerous?** | Attacker-controlled inputs, timing, state prerequisites |
| 3 | **What's missing?** | Validation, bounds check, access control, invariant enforcement |
| 4 | **What context enables exploitation?** | Protocol state, market conditions, flash loan availability |
| 5 | **What is the actual impact?** | Financial loss, state corruption, permanent damage |

## Root Cause Statement Formula

Formulate one sentence per vulnerability class:

> "This vulnerability exists because **[MISSING VALIDATION / UNTRUSTED DATA]** in **[COMPONENT]** allows **[ATTACK VECTOR]** leading to **[IMPACT]**."

Examples:
- "Missing staleness validation in Pyth oracle integration allows stale price consumption in liquidation logic leading to unfair liquidations"
- "Absent reentrancy guard on withdraw() allows recursive callbacks leading to full vault drain"
- "Unchecked positive exponent from oracle price feed causes integer overflow in scaling calculation leading to fund loss"

This statement becomes the foundation of the database entry's Overview section.

## Confidence Scoring

Rate each finding before including it:

| Confidence | Criteria | Action |
|------------|----------|--------|
| **HIGH** | Code confirms root cause + exploit path is clear + real-world precedent exists | Include with full documentation |
| **MEDIUM** | Code matches vulnerable pattern + theoretical exploit path exists | Include with caveats noted |
| **LOW** | Pattern match only + exploit path unclear or requires unlikely preconditions | Include as "potential" with explicit uncertainty |
| **SPECULATIVE** | No code evidence, only structural similarity | Do NOT include — research more |

## Falsification Protocol

Before finalizing ANY finding, actively attempt to disprove it:

1. **Does a check exist elsewhere?** — Search for validation in callers, modifiers, or upstream functions
2. **Are preconditions realistic?** — Can attacker actually reach this state on mainnet?
3. **Is the impact real?** — Would the numeric impact actually matter (dust vs. significant)?
4. **Does the fix exist already?** — Check if protocol handles this in a non-obvious way
5. **Does another control mitigate?** — Access control, pausing, timelocks, rate limits?

If ANY falsification check succeeds, downgrade or remove the finding.
