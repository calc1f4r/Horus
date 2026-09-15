---
name: chimera-setup
description: "Scaffold a complete Chimera property testing suite from an invariant-writer spec. Generates Setup, BeforeAfter, Properties, TargetFunctions, target modules (Admin/Doomsday/Managers), CryticTester, CryticToFoundry, plus echidna.yaml, medusa.json, and foundry.toml. Produces a compile-ready harness that runs on Echidna, Medusa, Foundry invariant tests, and Halmos from the same codebase. Use after invariant-writer and before any fuzzing campaign."
context: fork
agent: chimera-setup
argument-hint: <invariant-spec-path-or-codebase-path> [--fork=<rpc-url>] [--fork-block=<N>] [--no-echidna] [--medusa-only]
---

Scaffold a Chimera test suite for `$ARGUMENTS`.

## What gets generated

```
test/recon/
  Setup.sol             — deploys all contracts; actor/asset management; prank modifiers
  BeforeAfter.sol       — ghost variable structs + __before()/__after() snapshots
  Properties.sol        — invariant_ functions mapped from the invariant spec
  targets/
    AdminTargets.sol    — privileged/admin function wrappers (asAdmin)
    DoomsdayTargets.sol — extreme state drivers (warp, roll, max drain, donations)
    ManagersTargets.sol — actor + asset switching
  TargetFunctions.sol   — all handlers with try/catch + inline transition assertions
  CryticTester.sol      — Echidna + Medusa entry point
  CryticToFoundry.sol   — Foundry invariant suite + Halmos entry point
foundry.toml            — default + invariants profile (1M runs)
echidna.yaml            — assertion mode, symbolic execution via Bitwuzla
medusa.json             — 16 workers, assertion + property testing, Slither integration
```

## Chimera class hierarchy

```
BaseSetup → BaseProperties → BaseTargetFunctions (+ Asserts)
                                    └── TargetFunctions
                                          ├── CryticTester   + CryticAsserts  (Echidna/Medusa)
                                          └── CryticToFoundry + FoundryAsserts (Foundry/Halmos)
```

## Key patterns used

| Pattern | Purpose |
|---------|---------|
| `updateGhosts` modifier | Snapshot state before/after every handler call |
| `asAdmin` / `asActor` | Prank modifiers for role-based call routing |
| `between(value, lo, hi)` | Clamp fuzzer inputs; `vm.assume` in Halmos |
| `precondition(bool)` | Skip invalid states (`require` in Medusa, `vm.assume` in Halmos) |
| `checkError(err, "X")` | Match expected revert reasons in catch blocks |
| `Panic.arithmeticPanic` | Match compiler-inserted arithmetic panic |
| `t(bool, "reason")` | Inline assertion; `assert(false)` in Echidna/Medusa |

## Run commands (printed on completion)

```bash
# Medusa — fastest feedback, 16 workers
medusa fuzz

# Echidna — assertion mode + symbolic execution
echidna . --contract CryticTester --config echidna.yaml --format text --workers 16

# Foundry — 1M invariant runs
FOUNDRY_PROFILE=invariants forge test --match-contract CryticToFoundry -vv --show-progress

# Debug a repro (paste call sequence into test_crytic)
forge test --match-contract CryticToFoundry --match-test test_crytic -vvv

# Halmos — symbolic, bounded
halmos --contract CryticToFoundry --loop 3
```

## Related skills

- [/invariant-writer](../invariant-writer/SKILL.md) — produces the invariant spec consumed here
- [/invariant-reviewer](../invariant-reviewer/SKILL.md) — hardens spec before scaffolding
- [/medusa-fuzzing](../medusa-fuzzing/SKILL.md) — advanced Medusa harness configuration
- [/halmos-verification](../halmos-verification/SKILL.md) — symbolic verification specs
- [/certora-verification](../certora-verification/SKILL.md) — formal verification with CVL
