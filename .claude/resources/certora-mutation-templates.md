# Certora Mutation Templates

## Purpose

Copy-paste templates for configuring and running mutation campaigns with `certoraMutate` and Gambit.

---

## 1) Installation

```bash
python3 -m pip install --upgrade pip
python3 -m pip install certora-cli
certoraRun --version
certoraMutate --help
```

Linux ARM / Windows (no prebuilt Gambit binary):
```bash
git clone https://github.com/Certora/gambit
cd gambit && cargo build --release
export PATH="$PATH:$(pwd)/target/release"
gambit --version
```

---

## 2) Environment Validation

```bash
certoraRun --version
certoraMutate --help
solc --version
echo "CERTORAKEY: ${CERTORAKEY:0:8}..."   # show first 8 chars only
ls -la certora/conf/ certora/specs/       # confirm project layout
```

---

## 3) Baseline-Then-Mutation Command Flow

```bash
# Step 1: baseline verification
certoraRun path/to/prover.conf

# Step 2: generation sanity (after any config change)
certoraMutate path/to/prover.conf --gambit_only

# Step 3: full mutation campaign
certoraMutate path/to/prover.conf --msg "campaign-name-v1"
```

---

## 4) Reuse Existing Original Run

```bash
certoraMutate path/to/prover.conf \
  --orig_run "https://prover.certora.com/output/<job>/<id>/?anonymousKey=<key>" \
  --msg "reuse-executed-original-run"
```

---

## 5) Minimal Gambit Mutation Block

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

---

## 6) Invariant-Driven Gambit Block (recommended default)

Select operators from invariant categories, not arbitrarily.

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
        ],
        "seed": 42
      },
      {
        "filename": "contracts/Vault.sol",
        "num_mutants": 10,
        "mutations": [
          "binary-op-mutation",
          "swap-arguments-operator-mutation",
          "unary-operator-mutation"
        ],
        "seed": 42
      }
    ],
    "msg": "invariant-driven-campaign-arithmetic-and-access-control"
  }
}
```

---

## 7) Access Control Focused Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/Ownable.sol",
        "num_mutants": 8,
        "mutations": ["require-mutation", "if-cond-mutation"]
      }
    ],
    "msg": "access-control-mutation"
  }
}
```

---

## 8) Proxy / Delegatecall Focused Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/Proxy.sol",
        "num_mutants": 6,
        "mutations": ["elim-delegate-mutation", "if-cond-mutation"]
      }
    ],
    "msg": "proxy-delegatecall-mutation"
  }
}
```

---

## 9) Manual Mutants Only Block

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

---

## 10) Combined Gambit + Manual Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/MyContract.sol",
        "num_mutants": 6,
        "mutations": ["require-mutation", "if-cond-mutation"]
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

---

## 11) Reproducible Campaign (fixed seed)

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/Staking.sol",
        "num_mutants": 15,
        "mutations": [
          "binary-op-mutation",
          "assignment-mutation",
          "require-mutation"
        ],
        "seed": 1337
      }
    ],
    "msg": "reproducible-seed-1337"
  }
}
```

---

## 12) Contract-Scoped Mutation Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/MultipleContracts.sol",
        "contract": "LiquidityPool",
        "num_mutants": 10,
        "mutations": ["binary-op-mutation", "require-mutation"]
      }
    ],
    "msg": "scoped-to-LiquidityPool"
  }
}
```

---

## 13) Function-Scoped Mutation Block

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/Lending.sol",
        "functions": ["borrow", "repay"],
        "num_mutants": 12,
        "mutations": ["binary-op-mutation", "assignment-mutation"]
      }
    ],
    "msg": "borrow-repay-scoped"
  }
}
```

---

## 14) Manual Patch Generation

```bash
# Create a manual mutant patch
cp contracts/MyContract.sol contracts/MyContract.mutated.sol
# Edit MyContract.mutated.sol to introduce the mutation manually

# Generate patch
diff -u contracts/MyContract.sol contracts/MyContract.mutated.sol > certora/mutations/manual/mutant-001.patch

# Validate patch applies cleanly
patch --dry-run contracts/MyContract.sol < certora/mutations/manual/mutant-001.patch
```

Manual patch conventions:
- One mutation per `.patch` file for traceability
- File must end with `.patch`
- Prefer small, focused mutations (single expression or condition)

---

## 15) Troubleshooting Commands

```bash
# Generation diagnostics only
certoraMutate path/to/prover.conf --gambit_only --debug

# Capture collection failures
certoraMutate path/to/prover.conf --dump_failed_collects failed_collects.log

# Inspect locally applied mutants
ls -R .certora_internal/applied_mutants_dir

# Replay a single mutant manually
certoraRun certora/conf/SpecName.conf --solc_allow_path .certora_internal/applied_mutants_dir/<mutant_id>

# Standalone Gambit mutation (local inspection)
gambit mutate --filename contracts/MyContract.sol --num_mutants 5

# Gambit human-readable summary
gambit summary
```

---

## 16) Survivor Triage Record Template

Use one record per live mutant:

```text
Mutant ID:
Operator:
Modified file:
Modified line:
Original code:
Mutated code:
Status: live
Classification: equivalent | setup-artifact | true-spec-gap
Reachable Path: <which public function reaches the mutated code>
Evidence: <what the mutation changes that the spec doesn't catch>
Suggested Action:
  equivalent     → document in spec comment; no hardening needed
  setup-artifact → fix compilation/environment; rerun
  true-spec-gap  → add rule or tighten invariant; rerun subset
```

---

## 17) Equivalent Mutant Documentation Comment (CVL)

Add this comment in the spec file for each documented equivalent mutant:

```cvl
// EQUIVALENT MUTANT: mutant-<id>
// Operator: binary-op-mutation
// Modified: src/Pool.sol line 42  (x + fee → x - fee)
// Reason: fee is always 0 in the tested state space due to invariant X.
// Action: none — semantically equivalent for all reachable states.
```

---

## 18) Campaign Report Template

```text
## Mutation Campaign Report: <campaign-name>

### 1. Preflight Status
- certoraRun version:
- certoraMutate version:
- CERTORAKEY present: yes/no
- Remapping validation: pass/fail

### 2. Baseline Run Status
- Run URL:
- Status: Executed / Halted / Problem
- Rules passed / failed:

### 3. Mutation Plan
| Invariant Category | Operators Selected | File | num_mutants |
|-------------------|-------------------|------|-------------|
| access control    | require-mutation  | ...  | 8           |

### 4. Commands Executed
- gambit_only command: certoraMutate ... --gambit_only
- Full campaign command: certoraMutate ...

### 5. Results Summary
- Campaign URL:
- Total mutants: X
- Caught: Y (Z%)
- Live: A
- Failed-invalid: B
- Halted/Problem: C
- Coverage: Z%
- Solo rules: N

### 6. Live Mutant Triage
| Mutant ID | Operator | Classification | Evidence | Action |
|-----------|----------|---------------|----------|--------|

### 7. Hardening Changes
- Gap 1: [description] → [CVL change] → [rerun result]
- Equivalent documented: [mutant IDs]

### 8. Next Run Recommendation
- Remaining gaps:
- Additional operators to add:
- Coverage delta to target: X% → 80%
```

---

## 19) Operator → Invariant Category Quick Reference

| Invariant Category | Primary Operators | Secondary Operators |
|-------------------|-------------------|---------------------|
| access control / guards | `require-mutation`, `if-cond-mutation` | `unary-operator-mutation` |
| arithmetic / precision | `binary-op-mutation`, `assignment-mutation` | `unary-operator-mutation` |
| state machine transitions | `if-cond-mutation`, `if-statement-mutation` | `delete-expression-mutation` |
| conservation of value | `binary-op-mutation`, `assignment-mutation` | — |
| ordering / commutativity | `swap-arguments-operator-mutation` | `binary-op-mutation` |
| delegatecall / proxy | `elim-delegate-mutation` | `if-cond-mutation` |
| storage initialization | `assignment-mutation`, `delete-expression-mutation` | — |
