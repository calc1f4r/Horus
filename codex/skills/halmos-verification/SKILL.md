name: halmos-verification
description: "Convert invariant specifications into compilable Halmos symbolic test suites (.t.sol) that run inside Foundry. Produces check_ prefix functions using halmos-cheatcodes (svm.createUint256, svm.createAddress) for exhaustive verification over all possible inputs. Use when setting up Halmos formal verification or converting invariant specs to symbolic tests."
context: fork
agent: halmos-verification
argument-hint: <path-to-invariants-file>
---

<!-- AUTO-GENERATED from `.claude/skills/halmos-verification/SKILL.md`; source_sha256=8e414a5a1e53f7d48c1213b86f2222ed74fbb2ae335c71f77cdc198295c88544 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/halmos-verification/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/halmos-verification.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Generate Halmos symbolic tests from invariants at `$ARGUMENTS`.

## What this produces

1. **Symbolic test functions** — `check_*` prefix functions with `svm.create*` symbolic inputs
2. **Multi-path coverage** — Tests that explore all branches exhaustively
3. **Cross-function composition** — Tests that combine multiple function calls symbolically
4. **Arithmetic safety** — Overflow/underflow checks with symbolic bounds
5. **Access control verification** — Symbolic sender with role checks
6. **State machine tests** — Symbolic state transitions

## Key patterns

```solidity
function check_invariant_name() public {
    uint256 amount = svm.createUint256("amount");
    address user = svm.createAddress("user");
    // ... setup and action ...
    assert(/* invariant holds */);
}
```

## Compile-first workflow

All tests validated with `forge build` then `halmos --function check_*`.

## Output

- `test/halmos/` — Symbolic test contracts

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/chimera-setup](../chimera-setup/SKILL.md) — Alternative: multi-tool scaffold that covers Halmos alongside Medusa + Echidna from a single shared harness
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Alternative: property-based fuzzing
- [/certora-verification](../certora-verification/SKILL.md) — Alternative: CVL formal verification
