name: certora-verification
description: "Convert invariant specifications into Certora CVL .spec and .conf files. Handles compilation, Python environment, and configuration issues proactively. Produces general specifications, handles admin conditions correctly, avoids vacuous rules, supports mutation testing via Gambit, and generates satisfy statements. Use when setting up Certora formal verification or converting invariant specs to CVL."
context: fork
agent: certora-verification
argument-hint: <path-to-invariants-file>
---

<!-- AUTO-GENERATED from `.claude/skills/certora-verification/SKILL.md`; source_sha256=e7f9771845fff6bddaa6b98273fe25e34554148b1637e8717f14ae6760fc6d56 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/certora-verification/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/certora-verification.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Generate Certora CVL specs from invariants at `$ARGUMENTS`.

## What this produces

1. **CVL spec files** (`.spec`) — Rules, invariants, ghosts, hooks, and functions
2. **Configuration files** (`.conf`) — Certora Prover settings, contract linking, solc paths
3. **Satisfy statements** — For every rule, to detect vacuity
4. **Gambit config** — Mutation testing configuration (optional)

## Key CVL patterns

```cvl
rule transferPreservesTotalSupply(address from, address to, uint256 amount) {
    uint256 totalBefore = totalSupply();
    transfer(from, to, amount);
    uint256 totalAfter = totalSupply();
    assert totalBefore == totalAfter;
}
```

## Compile-first workflow

Runs `certoraRun` to validate specs. Fixes compilation errors iteratively.

## Output

- `certora/specs/` — CVL specification files
- `certora/conf/` — Configuration files

For CVL reference, see [certora-reference.md](../../resources/certora-reference.md).
For templates, see [certora-templates.md](../../resources/certora-templates.md).

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Alternative: property-based fuzzing
- [/halmos-verification](../halmos-verification/SKILL.md) — Alternative: symbolic testing
- [/certora-mutation-testing](../certora-mutation-testing/SKILL.md) — Downstream: mutation campaigns to validate spec coverage
- [/certora-sui-move-verification](../certora-sui-move-verification/SKILL.md) — Certora for Sui Move
