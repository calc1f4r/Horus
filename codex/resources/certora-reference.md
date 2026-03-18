<!-- AUTO-GENERATED from `.claude/resources/certora-reference.md`; source_sha256=1990e0dee2a5a0502ec6147f77981597998e9477b8f3d1f60cb4c8c34058c427 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/certora-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Certora Prover Reference

## Contents
- [CVL type system](#cvl-type-system)
- [Methods block patterns](#methods-block-patterns)
- [Summary types](#summary-types)
- [Ghost and hook patterns](#ghost-and-hook-patterns)
- [Built-in rules](#built-in-rules)
- [Key CVL statements](#key-cvl-statements)
- [Conf file template](#conf-file-template)
- [CLI options quick reference](#cli-options-quick-reference)
- [Loop unrolling](#loop-unrolling)
- [Rule sanity checks](#rule-sanity-checks)
- [Mutation testing with Gambit](#mutation-testing-with-gambit)
- [Known pitfalls and mitigations](#known-pitfalls-and-mitigations)
- [Environment variable setup](#environment-variable-setup)

---

## CVL Type System

### Core types

| Type | Purpose | Notes |
|------|---------|-------|
| `mathint` | Arbitrary-precision integer | Cannot overflow. Use for ALL intermediate arithmetic. |
| `env` | Transaction context | Fields: `e.msg.sender`, `e.msg.value`, `e.block.number`, `e.block.timestamp`, `e.block.basefee`, `e.block.coinbase`, `e.block.difficulty`, `e.block.gaslimit`, `e.tx.origin` |
| `method` | Arbitrary contract method | Fields: `f.selector`, `f.isPure`, `f.isView`, `f.isFallback`, `f.numberOfArguments`, `f.contract` |
| `calldataarg` | Arbitrary method arguments | Cannot be inspected, only passed to method calls |
| `storage` | EVM state snapshot | Use with `at` keyword for hyperproperties. `lastStorage` gives post-call state |
| Solidity types | `uint256`, `int256`, `address`, `bool`, `bytes32` etc. | Standard Solidity value types |

### Type conversion rules
- `mathint` ← any integer type (implicit upcast)
- Integer type ← `mathint` (requires explicit `assert_uint256()`, `require_uint256()`, or cast)
- Contract/interface types → represented as `address`
- Structs must be qualified: `ContractName.StructType`

---

## Methods Block Patterns

### Exact entry (single method, single contract)
```cvl
methods {
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function transfer(address, uint256) external returns (bool);
}
```

### Wildcard entry (all contracts with matching signature)
```cvl
methods {
    function _.transfer(address, uint256) external => NONDET;
    function _.balanceOf(address) external => NONDET;
}
```

### Catch-all entry (all methods of a specific contract)
```cvl
methods {
    function ExternalLib._ external => NONDET;
}
```

### `envfree` annotation
Marks a method as not depending on `env`. Calls from CVL skip the `env` argument:
```cvl
// In methods block:
function totalSupply() external returns (uint256) envfree;
// In rule:
uint256 supply = totalSupply(); // No env needed
```

### `optional` annotation
Use when a method may not exist on all implementations:
```cvl
function mint(address, uint256) external optional;
```

### `using` statement
Bind a contract instance to a variable:
```cvl
using ERC20 as token;
```

---

## Summary Types

| Summary | Side Effects | Return Value | Use Case |
|---------|-------------|--------------|----------|
| `NONDET` | None | Arbitrary per call | External view/pure calls whose result doesn't matter |
| `ALWAYS(v)` | None | Always `v` | Known constant return |
| `CONSTANT` | None | Same across ALL calls | Deterministic external view |
| `PER_CALLEE_CONSTANT` | None | Same per receiver contract | Multi-instance view calls |
| `HAVOC_ECF` | Havocs external contracts only | Arbitrary | Non-reentrant external calls |
| `HAVOC_ALL` | Havocs ALL storage | Arbitrary | Sound but imprecise (last resort) |
| `DISPATCHER(true)` | Dispatches to known contracts | Depends on implementation | Multi-implementation interfaces (e.g., ERC20) |
| `AUTO` | Depends on opcode | Depends on call type | Default for unresolved calls |

### Expression summaries
Replace a call with a CVL function:
```cvl
methods {
    function _.foo(uint256 x) external => myGhost[calledContract] expect uint256;
}
```

The `calledContract` keyword gives the address of the call target. The `executingContract` keyword gives the caller address.

---

## Ghost and Hook Patterns

### Ghost variable declaration
```cvl
ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
}
ghost mapping(address => mathint) ghostBalances;
```

### Persistent ghosts (survive havoc and reverts)
```cvl
persistent ghost bool reentrancyDetected {
    init_state axiom !reentrancyDetected;
}
```

### Store hook (track writes)
```cvl
hook Sstore _balances[KEY address user] uint256 newVal (uint256 oldVal) {
    sumBalances = sumBalances + newVal - oldVal;
    ghostBalances[user] = newVal;
}
```

### Load hook (track reads)
```cvl
hook Sload uint256 val _balances[KEY address user] {
    require ghostBalances[user] == val;
}
```

### Nested struct hooks
```cvl
hook Sstore users[KEY address user].balance uint256 newBal (uint256 oldBal) {
    ghostTotalBalance = ghostTotalBalance + newBal - oldBal;
}
```

### Opcode hooks
```cvl
hook CALL(uint g, address addr, uint value, uint argsOff, uint argsLen,
          uint retOff, uint retLen) uint rc {
    if (addr == currentContract) {
        reentrancyDetected = reentrancyDetected || executingContract == currentContract;
    }
}
```

### Ghost axioms
```cvl
ghost mathint positiveGhost {
    axiom forall uint256 x. positiveGhost > 0;
}
```

### Init state axioms (constructor state for invariant base case)
```cvl
ghost mathint counter {
    init_state axiom counter == 0;
}
```

---

## Built-in Rules

Include with `use builtin rule <name>;` in the spec file.

| Rule | What It Checks | Extra Config |
|------|---------------|--------------|
| `sanity` | At least one non-reverting path per function | None |
| `deepSanity` | Reachability of interior program points | Requires `multi_assert_check: true` |
| `viewReentrancy` | Read-only reentrancy: view state consistency at external call sites | None |
| `hasDelegateCalls` | Detects functions that use delegatecall | None |
| `msgValueInLoopRule` | Detects msg.value or delegatecall inside loops | None |
| `safeCasting` | Out-of-bounds explicit type casts | Requires `safe_casting_builtin: true` in conf |
| `uncheckedOverflows` | Overflows inside unchecked blocks | Requires `unchecked_overflow_builtin: true` in conf |

### Recommended setup
Always include `sanity` first to validate your env/config before writing custom rules:
```cvl
use builtin rule sanity;
use builtin rule viewReentrancy;
```

---

## Key CVL Statements

### assert and require
```cvl
require e.msg.sender != 0;                    // Precondition — filters models
assert balance_after >= balance_before,        // Property — Prover tries to violate
    "balance must not decrease";
```

### satisfy (positive witness)
```cvl
satisfy balance_after > balance_before;        // Prover must find a model where this holds
```
**Critical for anti-vacuity**: Always add `satisfy` statements to confirm your rules are not vacuously true.

### requireInvariant
```cvl
requireInvariant totalSupplyIsSumOfBalances(); // Safe to use in preserved blocks
```
Assumes a proven invariant holds. Evaluated in pre-state and after unresolved calls (for strong invariants).

### havoc assuming
```cvl
havoc sumBalance assuming sumBalance@new() == sumBalance@old() + newVal - oldVal;
```
Useful inside hooks for ghost function updates.

### @withrevert
```cvl
f@withrevert(e, args);
assert !lastReverted, "should not revert";
// OR
assert lastReverted, "should always revert";
```

### storage snapshots (hyperproperties)
```cvl
storage initial = lastStorage;
stake(e, less) at initial;
stake(e, more) at initial;    // Both start from same state
```

---

## Conf File Template

```json
{
    "files": [
        "src/MainContract.sol",
        "src/Token.sol"
    ],
    "verify": "MainContract:certora/specs/MainContract.spec",
    "link": [
        "MainContract:token=Token"
    ],
    "optimistic_loop": true,
    "loop_iter": "3",
    "rule_sanity": "basic",
    "msg": "MainContract verification",
    "solc": "solc",
    "packages": [
        "@openzeppelin/contracts=node_modules/@openzeppelin/contracts"
    ]
}
```

### Key conf fields

| Field | Type | Purpose |
|-------|------|---------|
| `files` | list | Solidity source files |
| `verify` | string | `ContractName:path/to/spec.spec` |
| `link` | list | `Contract:field=OtherContract` — link contract addresses |
| `optimistic_loop` | bool | Assume loops don't exceed unroll count (unsound) |
| `loop_iter` | int/string | Number of loop unrollings (default: 1) |
| `rule_sanity` | string | `none`, `basic`, or `advanced` |
| `multi_assert_check` | bool | Check each assert independently |
| `rule` | list | Run only specific rules |
| `method` | string | Restrict to specific method |
| `parametric_contracts` | list | Limit parametric rule scope |
| `solc` | string | Solidity compiler path |
| `packages` | list | Package remappings |
| `msg` | string | Run description |
| `smt_timeout` | int | Solver timeout in seconds |
| `prover_args` | list | Additional prover arguments |
| `safe_casting_builtin` | bool | Enable safeCasting built-in rule |
| `unchecked_overflow_builtin` | bool | Enable uncheckedOverflows built-in rule |

### Configuration recipes

**Tight verification (sound)**:
```json
{
    "optimistic_loop": false,
    "loop_iter": "5",
    "rule_sanity": "advanced",
    "multi_assert_check": true
}
```

**Fast iteration (development)**:
```json
{
    "optimistic_loop": true,
    "loop_iter": "2",
    "rule_sanity": "basic",
    "smt_timeout": "600"
}
```

**Mutation testing ready**:
```json
{
    "optimistic_loop": true,
    "loop_iter": "3",
    "rule_sanity": "basic",
    "mutations": {
        "gambit": [
            {
                "filename": "src/MainContract.sol",
                "num_mutants": 10
            }
        ],
        "msg": "mutation test run"
    }
}
```

---

## CLI Options Quick Reference

```bash
# Basic verification
certoraRun certora/conf/MainContract.conf

# Run specific rule only
certoraRun certora/conf/MainContract.conf --rule myRule

# Run with mutation testing
certoraMutate certora/conf/MainContract.conf

# Generate conf file from CLI args
certoraRun src/Contract.sol --verify Contract:spec.spec --generate_conf_file out.conf
```

---

## Loop Unrolling

### Pessimistic mode (default, sound)
Reports violation if ANY path exceeds loop_iter. Use for final verification.

### Optimistic mode (`optimistic_loop: true`, unsound)
Ignores paths exceeding loop_iter. Use during development. Always validate with pessimistic mode before final sign-off.

### Guidelines
- Start with `loop_iter: 1` + `optimistic_loop: true`
- If sanity check fails, increase `loop_iter`
- Typical values: 1-5 for most contracts, up to 10 for heavy iterators
- If a function has unbounded loops, consider summarizing it

---

## Rule Sanity Checks

Enable with `"rule_sanity": "basic"` or `"rule_sanity": "advanced"`.

| Check | What It Catches | Level |
|-------|----------------|-------|
| Vacuity | Rules that pass because `require` rules out ALL models | basic |
| Trivial invariant | Invariants true in ALL states (not just reachable) | basic |
| Assert tautology | Assertions that are always true regardless of requires | advanced |
| Assertion structure | Unnecessarily complex assertions (vacuous premises) | advanced |
| Redundant require | `require` statements that add no filtering | advanced |

**Always run with at least `"rule_sanity": "basic"`** to catch vacuous rules.

---

## Mutation Testing with Gambit

### Setup
1. Install: `pip install certora-cli` (includes `certoraMutate`)
2. Add `mutations` key to conf file
3. Run: `certoraMutate path/to/conf.conf`

### Gambit mutation operators
- `require-mutation`: Changes `require` conditions
- `assignment-mutation`: Changes assignment values
- `binary-op-mutation`: Changes binary operators (`+` → `-`, `>` → `>=`)
- `delete-expression-mutation`: Removes statements
- `if-statement-mutation`: Changes branch conditions
- `swap-arguments-mutation`: Swaps function arguments
- `unary-operator-mutation`: Changes unary operators

### Conf example with mutations
```json
{
    "files": ["src/Contract.sol"],
    "verify": "Contract:certora/specs/Contract.spec",
    "optimistic_loop": true,
    "loop_iter": "3",
    "rule_sanity": "basic",
    "mutations": {
        "gambit": [
            {
                "filename": "src/Contract.sol",
                "num_mutants": 10,
                "mutations": ["binary-op-mutation", "require-mutation"]
            }
        ],
        "manual_mutants": [
            {
                "file_to_mutate": "src/Contract.sol",
                "mutants_location": "certora/mutations"
            }
        ],
        "msg": "mutation coverage assessment"
    }
}
```

### Interpreting results
- **Caught mutant**: A rule broke → specification detected the bug → good
- **Live mutant**: No rule broke → specification gap → write stronger rules
- **Coverage metric**: Caught / Total. Target ≥ 80%
- **Solo rules**: Rules that uniquely catch a mutant. High solo count = non-redundant spec

### Avoiding false mutation survivors
A mutant survives NOT because the spec is weak, but because:
1. **Mutation is semantically equivalent** (e.g., `x + 0` → `x * 1`). Ignore it.
2. **Mutation breaks compilation.** The tool skips it.
3. **Rule is vacuous.** Fix the rule (add `satisfy` statements).
4. **Mutation only affects admin-only paths.** Your spec correctly doesn't test admin-fabricated scenarios.

Always review live mutants manually. Dismiss equivalent mutants. Write new rules for genuine gaps.

---

## Known Pitfalls and Mitigations

### 1. Path explosion / Timeouts
**Symptom**: Prover times out or runs for hours.
**Cause**: Complex branching, unbounded loops, nested external calls.
**Fix**:
- Summarize complex external functions with `NONDET` or `HAVOC_ECF`
- Reduce `loop_iter`
- Use `optimistic_loop: true` during development
- Increase `smt_timeout` if close to finishing
- Split large specs into multiple smaller spec files
- Use `--method` to verify one function at a time
- Use `DELETE` summaries for irrelevant methods

### 2. Havoc producing false counterexamples
**Symptom**: Counterexample shows impossible storage values after external calls.
**Cause**: Unresolved external calls get `AUTO` summary (which havocs storage).
**Fix**:
- Link contracts: `"link": ["A:token=Token"]`
- Add method summaries: `function _.foo() external => NONDET;`
- Use `DISPATCHER(true)` for known interface implementations
- Use `HAVOC_ECF` instead of `HAVOC_ALL` for non-reentrant calls
- Add `requireInvariant` to re-establish ghost state after havoc points

### 3. Vacuity (false sense of security)
**Symptom**: All rules pass but specifications are actually untested.
**Cause**: Contradictory `require` statements, reused `env` variables, reverting functions.
**Fix**:
- Always run `use builtin rule sanity;`
- Set `"rule_sanity": "basic"` minimum
- Add `satisfy` statements to EVERY rule
- Don't reuse `env` across payable/non-payable calls
- Check for vacuous preserved blocks in invariants
- Use `assert true;` in rules with only `satisfy` to trigger pessimistic assertions

### 4. Invariants that revert causing unsoundness
**Symptom**: Invariant passes but property can be violated.
**Cause**: Invariant expression reverts in pre-state (e.g., array out of bounds), discarding counterexamples.
**Fix**:
- Avoid invariants that call reverting functions
- Use `view` functions only in invariant expressions
- Prefer writing as parametric rules if the expression may revert

### 5. Unsound filters and preserved blocks
**Symptom**: Invariant verified but method can violate it.
**Cause**: Method filtered out, or preserved block adds incorrect `require`.
**Fix**:
- Minimize filtered methods — each exclusion is potential unsoundness
- Only `requireInvariant` proven invariants in preserved blocks
- Document every `require` in preserved blocks with justification

### 6. Strong vs Weak invariants
- **Weak invariant** (default): Holds before/after each external method call
- **Strong invariant**: Also asserted before/assumed after unresolved external calls
- Use `strong invariant` for contracts that may be called back during external calls (reentrancy scenarios)

---

## Environment Variable Setup

```bash
# Set Certora API key
export CERTORAKEY="your_api_key_here"

# Verify it's set
echo $CERTORAKEY

# Install Certora CLI
pip install certora-cli

# Verify installation
certoraRun --version
```

The `CERTORAKEY` must be set before running any `certoraRun` or `certoraMutate` commands. Without it, jobs cannot be submitted to the Certora cloud.
