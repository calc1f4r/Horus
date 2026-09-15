# Invariants and formal verification

Use this when you want to state what a protocol must never do, then prove it holds (or find out it does not).

## Step 1: extract invariants

`invariant-writer` reads the codebase and writes `02-invariants.md`. It works in two modes at once. The positive mode specifies what should happen, pulled from standards and reference implementations: ERC-4626 rounding rules, solvency, share accounting. The adversarial mode writes out multi-call attack sequences for what must never happen.

`invariant-reviewer` then re-derives the protocol from scratch, checks the spec against canonical invariants for the protocol type, and hardens bounds that are too loose or too tight. Use these two as a pair; the reviewer exists because first drafts of invariants are usually half right.

## Step 2: turn invariants into harnesses

Three skills consume the reviewed spec, one per tool:

| Skill | Tool | Shape of the output |
|---|---|---|
| `chimera-setup` | Echidna + Medusa + Halmos from one codebase | `test/recon/` with Setup, BeforeAfter, Properties, targets |
| `medusa-fuzzing` | Medusa | `property_` prefix tests, ghost variables, actor proxies, `medusa.json` |
| `halmos-verification` | Halmos | `check_` prefix symbolic tests with `svm.createUint256` style cheatcodes |
| `certora-verification` | Certora | CVL `.spec` and `.conf` under `certora/` |

All of them compile first. A harness that does not build is not a harness.

`chimera-setup` is the starting point when you want all three fuzzers on the same properties without writing three harnesses. Go straight to a single-tool skill when you already know which one you need.

## Step 3: run and read results

Violations map back to the invariant they broke. Each one is either a real finding (the code is wrong) or a spec bug (the invariant was wrong or vacuous). `certora-mutation-testing` helps separate those: it mutates the code under test and checks whether the spec catches the mutants. Survivors point at spec gaps.

## Sui Move

For Move targets there are two options: `certora-sui-move-verification` for CVLM specs and `sui-prover-verification` for requires/ensures style specs with ghost variables and loop invariants.
