# Certora Mutation Templates

## Purpose

Copy-paste templates for configuring and running mutation campaigns with `certoraMutate` and Gambit.

## 1) Installation Template

```bash
python3 -m pip install --upgrade pip
python3 -m pip install certora-cli
certoraRun --version
certoraMutate --help
```

## 2) Baseline-Then-Mutation Command Template

```bash
# baseline run
certoraRun path/to/prover.conf

# generation sanity pass
certoraMutate path/to/prover.conf --gambit_only

# full mutation campaign
certoraMutate path/to/prover.conf --msg "mutation-campaign-name"
```

## 3) Reuse Existing Original Run Template

```bash
certoraMutate path/to/prover.conf \
  --orig_run "https://prover.certora.com/output/<job>/<id>/?anonymousKey=<key>" \
  --msg "reuse-executed-original-run"
```

## 4) Minimal Gambit Mutation Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/MyContract.sol",
        "num_mutants": 8
      }
    ],
    "msg": "minimal-gambit-mutation"
  }
}
```

## 5) Invariant-Driven Gambit Block

Use this when mutation operators are selected from invariant categories.

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/Pool.sol",
        "num_mutants": 12,
        "mutations": [
          "require-mutation",
          "if-cond-mutation",
          "binary-op-mutation",
          "assignment-mutation"
        ]
      },
      {
        "filename": "contracts/Vault.sol",
        "num_mutants": 10,
        "mutations": [
          "binary-op-mutation",
          "swap-arguments-operator-mutation",
          "unary-operator-mutation"
        ]
      }
    ],
    "msg": "invariant-driven-mutation"
  }
}
```

## 6) Manual Mutants Only Block

```json
{
  "mutations": {
    "manual_mutants": [
      {
        "file_to_mutate": "contracts/MyContract.sol",
        "mutants_location": "certora/mutations/manual"
      }
    ],
    "msg": "manual-mutants-only"
  }
}
```

## 7) Combined Gambit + Manual Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/MyContract.sol",
        "num_mutants": 6,
        "mutations": [
          "require-mutation",
          "if-cond-mutation"
        ]
      }
    ],
    "manual_mutants": [
      {
        "file_to_mutate": "contracts/MyContract.sol",
        "mutants_location": "certora/mutations/manual"
      }
    ],
    "msg": "combined-gambit-and-manual"
  }
}
```

## 8) Manual Patch Generation Template

```bash
diff -u contracts/MyContract.sol contracts/MyContract.mutated.sol > certora/mutations/manual/mutant-001.patch
```

## 9) Troubleshooting Command Template

```bash
# mutation generation diagnostics
certoraMutate path/to/prover.conf --gambit_only --debug

# capture collection failures
certoraMutate path/to/prover.conf --dump_failed_collects failed_collects.log

# inspect locally applied mutants
ls -R .certora_internal/applied_mutants_dir
```

## 10) Survivor Triage Template

```text
Mutant ID:
Status: live
Classification: equivalent | setup-artifact | true-spec-gap
Reasoning:
Reachable Path:
Suggested Action:
- equivalent: document and ignore
- setup-artifact: fix config/build and rerun
- true-spec-gap: patch spec/conf and rerun target subset
```

## 11) Suggested Invariant to Operator Mapping

This mapping is a practical heuristic for campaign construction.

- access control or guard invariants:
  - `require-mutation`, `if-cond-mutation`
- arithmetic or precision invariants:
  - `binary-op-mutation`, `assignment-mutation`, `unary-operator-mutation`
- state-machine invariants:
  - `if-cond-mutation`, `delete-expression-mutation`
- non-commutative ordering invariants:
  - `swap-arguments-operator-mutation`
- delegatecall or call semantics invariants:
  - `elim-delegate-mutation`

## 12) Campaign Report Template

```text
1. Preflight Status
2. Baseline Run Status
3. Mutation Plan
4. Commands Executed
5. Results Summary
6. Live Mutant Triage
7. Hardening Changes
8. Next Run Recommendation
```
