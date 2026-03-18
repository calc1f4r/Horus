name: medusa-fuzzing
description: "Convert invariant specifications into compilable Medusa-compatible Solidity test harnesses and medusa.json configuration. Produces property tests (property_ prefix), assertion tests, ghost variable tracking, actor proxies, and bounding utilities. Use when setting up a Medusa fuzzing campaign or converting invariant specs to harness code."
context: fork
agent: medusa-fuzzing
argument-hint: <path-to-invariants-file>
---

<!-- AUTO-GENERATED from `.claude/skills/medusa-fuzzing/SKILL.md`; source_sha256=257bd295f2090ffad5e2a04aaab170500c85496a157b07060d4bda654bcc23f0 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/medusa-fuzzing/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/medusa-fuzzing.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Generate Medusa fuzzing harnesses from invariants at `$ARGUMENTS`.

## What this produces

1. **Property tests** — `property_*` functions that return `bool` for stateless invariant checks
2. **Assertion tests** — Functions with `assert()` for stateful multi-step scenarios
3. **Ghost variables** — Tracking variables for cumulative properties (total deposited, total withdrawn)
4. **Actor proxies** — Multi-user simulation with `ActorProxy` pattern
5. **Bounding utilities** — `clampBetween()`, `clampLte()` for input constraining
6. **medusa.json** — Fuzzing configuration with corpus, coverage, and timeout settings

## Compile-first workflow

All harnesses are validated with `forge build` before being considered complete. If compilation fails, the agent fixes the errors iteratively.

## Output

- `test/fuzzing/` — Harness contracts
- `medusa.json` — Fuzzing configuration

For Medusa API reference, see [medusa-reference.md](../../resources/medusa-reference.md).
For templates, see [medusa-templates.md](../../resources/medusa-templates.md).

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant specs this consumes
- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — Hardens invariants before conversion
- [/chimera-setup](../chimera-setup/SKILL.md) — Alternative: multi-tool scaffold (Medusa + Echidna + Halmos from one harness). Prefer for new suites; use this skill for advanced Medusa-only tuning beyond the template
- [/halmos-verification](../halmos-verification/SKILL.md) — Alternative: symbolic testing
- [/certora-verification](../certora-verification/SKILL.md) — Alternative: formal verification
