<!-- AUTO-GENERATED from `.claude/resources/halmos-reference.md`; source_sha256=5124ce37324ab0dd764bbf8d0055997a1fd89759c929e88670462784d5e4174e -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/halmos-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Halmos Symbolic Testing Reference

Halmos is a symbolic execution tool for Solidity smart contracts that runs inside Foundry.
It exhaustively verifies properties over all possible inputs within bounded loops.

Repo: https://github.com/a16z/halmos
Docs: https://github.com/a16z/halmos/blob/main/docs/

## Installation

```bash
pip install halmos
# or
uv tool install halmos
```

## Symbolic Variable Creation

```python
# svm = SymbolicVM cheatcodes — halmos-specific
from halmos.cheatcodes import SVM
```

In Solidity tests, use the `SVM` interface via `vm`:

```solidity
// Symbolic inputs — halmos resolves all possible values
uint256 amount   = svm.createUint256("amount");
address user     = svm.createAddress("user");
bool   flag      = svm.createBool("flag");
int256 delta     = svm.createInt256("delta");
bytes32 hash     = svm.createBytes32("hash");
bytes  calldata_ = svm.createBytes(32, "calldata");
```

## Test Function Convention

```solidity
// Prefix: check_ (NOT test_ — that runs in Foundry, not Halmos)
function check_invariantName() public {
    // 1. Create symbolic inputs
    uint256 amount = svm.createUint256("amount");
    // 2. Constrain inputs (vm.assume — NOT precondition/require)
    vm.assume(amount > 0 && amount <= type(uint128).max);
    // 3. Set up state
    vm.prank(user);
    contract.deposit(amount);
    // 4. Assert invariant
    assert(contract.totalAssets() >= contract.totalLiabilities());
}
```

## Chimera Integration: HalmosAsserts

When using Chimera with Halmos, the `HalmosAsserts` backend:
- Uses `vm.assume(in range)` for `between()` — constrains rather than wraps
- Uses `vm.assume(p)` for `precondition()` — prunes search space
- Uses `assertXxx` from forge-std for all assert methods

```solidity
// In CryticToFoundry (which uses FoundryAsserts, NOT HalmosAsserts):
// Halmos runs check_ functions — but between() from FoundryAsserts wraps
// For true Halmos symbolic behavior, use svm directly in check_ functions
```

## Running Halmos

```bash
# Run all check_ functions
halmos

# Run specific function
halmos --function check_invariantName

# Run on specific contract
halmos --contract MyHalmosTests

# Set loop bound (higher = more thorough, slower)
halmos --loop 3

# With Chimera's CryticToFoundry:
halmos --contract CryticToFoundry --loop 3

# Verbose output
halmos -vvv

# Parallel jobs
halmos --jobs 4
```

## Halmos-Specific Patterns

### Symbolic Caller
```solidity
function check_onlyOwnerCanCall() public {
    address caller = svm.createAddress("caller");
    vm.assume(caller != owner);  // constrain: not the owner
    vm.prank(caller);
    try contract.privilegedFunction() {
        assert(false);  // should not succeed
    } catch {}
}
```

### Symbolic Amount with Bounds
```solidity
function check_depositWithdrawRoundtrip() public {
    uint256 amount = svm.createUint256("amount");
    vm.assume(amount > 0);
    vm.assume(amount <= contract.maxDeposit(address(this)));

    uint256 sharesBefore = contract.balanceOf(address(this));
    contract.deposit(amount, address(this));
    contract.withdraw(amount, address(this), address(this));
    uint256 sharesAfter = contract.balanceOf(address(this));

    assert(sharesAfter >= sharesBefore);  // no loss on roundtrip
}
```

### Symbolic State Transitions
```solidity
function check_stateTransitionSafety() public {
    uint8 action = svm.createUint8("action");
    vm.assume(action < 3);  // 3 possible actions

    if (action == 0) contract.deposit(100);
    else if (action == 1) contract.withdraw(50);
    else contract.accrueInterest();

    // Invariant must hold after any single action
    assert(contract.totalBorrows() <= contract.totalDeposits());
}
```

## Limitations

- **Loops**: Must bound loops with `--loop N`. Unbounded loops are not verifiable.
- **External calls**: Cross-contract calls are modeled symbolically — complex protocol interactions may require summaries.
- **Cryptography**: Hash preimage resistance is not modeled. Do not test hash-dependent invariants symbolically.
- **Gas**: Halmos does not model gas. Out-of-gas conditions are not captured.
- **`startPrank`**: Supported. `prank` is also supported.
- **Fork mode**: Partial support — live state can be forked but symbolic interaction with arbitrary mainnet contracts is limited.

## Output Interpretation

```
[PASS] check_invariantName (paths: 42, time: 1.2s)   — all paths verified
[FAIL] check_invariantName (paths: 7, time: 0.8s)    — counterexample found
  Counterexample: amount=0xffffffff..., user=0xdeadbeef...
[ERROR] check_invariantName                           — analysis error (loop bound hit, etc.)
```

## Halmos vs Medusa vs Certora

| Dimension | Halmos | Medusa | Certora |
|-----------|--------|--------|---------|
| Approach | Symbolic (exhaustive in bounds) | Fuzzing (probabilistic) | Formal proof (complete) |
| Loop handling | Bounded | Unbounded sequences | Inductive |
| Setup cost | Low | Low | High |
| Counterexample quality | Exact | Minimized sequence | CEX trace |
| Best for | Arithmetic bugs, access control | State machine bugs, reentrancy | Proofs of absence |
| Speed | Slow on complex code | Fast | Very slow |
