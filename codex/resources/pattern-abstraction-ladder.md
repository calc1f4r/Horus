<!-- AUTO-GENERATED from `.claude/resources/pattern-abstraction-ladder.md`; source_sha256=266fc4e80e88389a5fdc9ffce51ac120880b9e9baae7b1bc5ac21a3e0bc616f4 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/pattern-abstraction-ladder.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Pattern Abstraction Ladder

Transform specific vulnerability instances into generalized, reusable database patterns. Each finding should be documented at multiple levels.

## Level 0: Exact Instance

The specific vulnerable code from a single exploit or audit report.

- **Sources**: 1 report/exploit
- **Database usage**: Include as numbered example with source reference
- **Example**: BalancerV2's `FixedPoint.mulDown(tokenAmountOut, scalingFactors[tokenIndexOut])` precision loss

## Level 1: Code Pattern Variant

Generalized code structure seen across multiple sources with minor variations.

- **Sources**: 2+ reports/exploits
- **Database usage**: Document all variants as separate examples under one heading
- **Example**: Generic `value.mulDown(scalingFactor)` precision loss in any scaled arithmetic

## Level 2: Vulnerability Class

Family of related vulnerabilities sharing the same root cause.

- **Database usage**: Create major sections, each covering one class
- **Example**: "Precision Loss in Token Scaling" — covers truncation-to-zero, compounding loss, rounding direction

## Level 3: Security Principle

Abstract invariant applicable across protocols and chains.

- **Database usage**: Top-level categorization and cross-linking
- **Example**: "Arithmetic operations in value-bearing code must preserve: conservation (sum inputs == sum outputs), reversibility, dust protection"

## Applying the Ladder

When analyzing a finding:

1. Start at Level 0 — document the exact instance with code + source reference
2. Search for Level 1 variants — are there other reports with the same code shape?
3. Group into Level 2 classes — what root cause family does this belong to?
4. Identify Level 3 principles — what universal invariant does this violate?

**The database entry should contain Level 0 examples organized under Level 2 headings, with Level 3 context in the Overview.**
