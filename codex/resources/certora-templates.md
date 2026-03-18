<!-- AUTO-GENERATED from `.claude/resources/certora-templates.md`; source_sha256=7b07e840fd7f5d97ebaf70d436037119c837d25c6c7424fca39cc0c03f9bbd33 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/certora-templates.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Certora CVL Spec Templates

## Contents
- [Base spec scaffold](#base-spec-scaffold)
- [Solvency: sum-of-balances invariant](#solvency-sum-of-balances-invariant)
- [Solvency: conservation of value (transfer)](#solvency-conservation-of-value-transfer)
- [Access control: privileged function restriction](#access-control-privileged-function-restriction)
- [State machine: monotonic state transitions](#state-machine-monotonic-state-transitions)
- [Arithmetic safety with mathint](#arithmetic-safety-with-mathint)
- [Reentrancy detection via persistent ghost](#reentrancy-detection-via-persistent-ghost)
- [ERC20 compliance suite](#erc20-compliance-suite)
- [ERC4626 vault share accounting](#erc4626-vault-share-accounting)
- [No unexpected reverts (DoS resistance)](#no-unexpected-reverts-dos-resistance)
- [Parametric rule with filter](#parametric-rule-with-filter)
- [Hyperproperty: monotonicity via storage snapshots](#hyperproperty-monotonicity-via-storage-snapshots)
- [Multi-contract linking](#multi-contract-linking)
- [Preserved block patterns](#preserved-block-patterns)
- [Conf files per use case](#conf-files-per-use-case)
- [Anti-patterns (DO NOT USE)](#anti-patterns-do-not-use)

---

## Base Spec Scaffold

Every spec file should start with this skeleton. Adapt the methods block and imports.

```cvl
// SPDX-License-Identifier: MIT
// Spec: MainContract

using MainContract as mainContract;
// using Token as token;  // uncomment for multi-contract

/*//////////////////////////////////////////////////////////////
                        METHODS BLOCK
//////////////////////////////////////////////////////////////*/

methods {
    // --- Primary contract (envfree where possible) ---
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;

    // --- External contract summaries ---
    // function _.extFunc(uint256) external => NONDET;
}

/*//////////////////////////////////////////////////////////////
                        BUILT-IN RULES
//////////////////////////////////////////////////////////////*/

use builtin rule sanity;

/*//////////////////////////////////////////////////////////////
                        GHOSTS & HOOKS
//////////////////////////////////////////////////////////////*/

// Ghost declarations and hooks here

/*//////////////////////////////////////////////////////////////
                        INVARIANTS
//////////////////////////////////////////////////////////////*/

// Invariants here

/*//////////////////////////////////////////////////////////////
                        RULES
//////////////////////////////////////////////////////////////*/

// Rules with satisfy statements here
```

---

## Solvency: Sum-of-Balances Invariant

Proves that the sum of all individual balances equals the tracked totalSupply. Uses ghost + hook pattern for precise tracking.

```cvl
/*//////////////////////////////////////////////////////////////
                        GHOSTS & HOOKS
//////////////////////////////////////////////////////////////*/

ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sstore _balances[KEY address user] uint256 newVal (uint256 oldVal) {
    sumOfBalances = sumOfBalances + newVal - oldVal;
}

hook Sload uint256 val _balances[KEY address user] {
    require ghostBalances[user] == val;
}

/*//////////////////////////////////////////////////////////////
                   SUM-OF-BALANCES INVARIANT
//////////////////////////////////////////////////////////////*/

/// @title Total supply equals sum of all balances
invariant totalSupplyIsSumOfBalances()
    to_mathint(totalSupply()) == sumOfBalances
    {
        preserved with (env e) {
            require e.msg.sender != 0;
        }
    }

/// @title Anti-vacuity: positive supply is reachable
rule totalSupplyCanBePositive() {
    satisfy totalSupply() > 0;
}
```

### Generalizations for edge cases
- Use `mathint` for the ghost to prevent phantom overflows
- The `init_state axiom` aligns with constructor where balances start at 0
- The `preserved` block restricts sender to nonzero (realistic)
- Add Sload hook for bidirectional consistency
- Add `satisfy` rule to prove non-vacuity

---

## Solvency: Conservation of Value (Transfer)

Proves that transfers don't create or destroy tokens.

```cvl
/// @title Transfer conserves total supply
rule transferConservesTotalSupply(address from, address to, uint256 amount) {
    env e;
    require e.msg.sender == from;
    require from != to;  // avoid self-transfer edge case masking

    mathint supplyBefore = totalSupply();
    mathint fromBefore = balanceOf(from);
    mathint toBefore = balanceOf(to);

    transfer(e, to, amount);

    mathint supplyAfter = totalSupply();
    mathint fromAfter = balanceOf(from);
    mathint toAfter = balanceOf(to);

    assert supplyAfter == supplyBefore,
        "total supply must not change on transfer";
    assert fromAfter == fromBefore - amount,
        "sender balance must decrease by amount";
    assert toAfter == toBefore + amount,
        "receiver balance must increase by amount";

    satisfy amount > 0;
}
```

---

## Access Control: Privileged Function Restriction

Parametric rule that proves ONLY the owner/admin can call privileged functions.

```cvl
/// @title Only owner can call admin functions
rule onlyOwnerCanCallPrivileged(method f)
filtered { f -> f.selector == sig:pause().selector
             || f.selector == sig:unpause().selector
             || f.selector == sig:setFee(uint256).selector }
{
    env e;
    calldataarg args;

    require e.msg.sender != owner();

    f@withrevert(e, args);

    assert lastReverted,
        "non-owner call to privileged function must revert";

    // Anti-vacuity
    env e2;
    require e2.msg.sender == owner();
    f@withrevert(e2, args);
    satisfy !lastReverted;
}
```

### Important: Admin condition handling
- NEVER test that admin actions revert — the admin SHOULD be able to execute them
- Always filter: `require e.msg.sender != owner()` for unauthorized-access tests
- Test the positive case separately: admin CAN execute
- For time-locked admin, require `block.timestamp < unlockTime` for the unauthorized path

---

## State Machine: Monotonic State Transitions

Proves that state can only move forward through defined transitions.

```cvl
/// @title State transitions follow defined order
rule stateTransitionsAreMonotonic(method f) {
    env e;
    calldataarg args;

    uint8 stateBefore = getState();

    f(e, args);

    uint8 stateAfter = getState();

    // State can only increase or stay the same
    assert stateAfter >= stateBefore,
        "state must not go backwards";

    // Define valid transitions: 0→1, 1→2, 2→3 only
    assert (stateBefore == stateAfter)
        || (stateBefore == 0 && stateAfter == 1)
        || (stateBefore == 1 && stateAfter == 2)
        || (stateBefore == 2 && stateAfter == 3),
        "only defined state transitions allowed";

    satisfy stateAfter > stateBefore;
}
```

---

## Arithmetic Safety with mathint

Demonstrates overflow-free arithmetic in specifications.

```cvl
/// @title Deposit correctly updates shares using mathint
rule depositShareCalculation(uint256 assets) {
    env e;

    mathint totalAssetsBefore = totalAssets();
    mathint totalSharesBefore = totalSupply();
    mathint userSharesBefore = balanceOf(e.msg.sender);

    uint256 shares = deposit(e, assets);

    mathint totalAssetsAfter = totalAssets();
    mathint totalSharesAfter = totalSupply();
    mathint userSharesAfter = balanceOf(e.msg.sender);

    // All arithmetic in mathint — no overflow possible
    mathint expectedShares;
    if (totalSharesBefore == 0 || totalAssetsBefore == 0) {
        expectedShares = to_mathint(assets);
    } else {
        expectedShares = (to_mathint(assets) * totalSharesBefore) / totalAssetsBefore;
    }

    assert to_mathint(shares) == expectedShares,
        "shares must match expected calculation";
    assert totalSharesAfter == totalSharesBefore + to_mathint(shares),
        "total shares must increase by minted amount";
    assert userSharesAfter == userSharesBefore + to_mathint(shares),
        "user shares must increase by minted amount";
    assert totalAssetsAfter == totalAssetsBefore + to_mathint(assets),
        "total assets must increase by deposited amount";

    satisfy assets > 0 && shares > 0;
}
```

---

## Reentrancy Detection via Persistent Ghost

Uses a persistent ghost + CALL opcode hook to detect reentrancy.

```cvl
persistent ghost bool reentrancyDetected {
    init_state axiom !reentrancyDetected;
}

persistent ghost uint256 callDepth {
    init_state axiom callDepth == 0;
}

hook CALL(uint g, address addr, uint value, uint argsOff, uint argsLen,
          uint retOff, uint retLen) uint rc {
    if (executingContract == currentContract && addr == currentContract) {
        reentrancyDetected = true;
    }
}

/// @title No function re-enters the contract
rule noReentrancy(method f) {
    env e;
    calldataarg args;

    require !reentrancyDetected;

    f(e, args);

    assert !reentrancyDetected,
        "reentrancy detected: contract called itself during execution";

    satisfy true;
}
```

---

## ERC20 Compliance Suite

```cvl
methods {
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function allowance(address, address) external returns (uint256) envfree;
    function transfer(address, uint256) external returns (bool);
    function transferFrom(address, address, uint256) external returns (bool);
    function approve(address, uint256) external returns (bool);
}

ghost mathint sumBalances {
    init_state axiom sumBalances == 0;
}

hook Sstore _balances[KEY address a] uint256 newVal (uint256 oldVal) {
    sumBalances = sumBalances + newVal - oldVal;
}

/// @title Total supply equals sum of balances
invariant totalSupplyIsSumOfBalances()
    to_mathint(totalSupply()) == sumBalances;

/// @title Transfer moves exact amount between accounts
rule transferIntegrity(address to, uint256 amount) {
    env e;
    require e.msg.sender != to;

    mathint balFromBefore = balanceOf(e.msg.sender);
    mathint balToBefore = balanceOf(to);

    transfer(e, to, amount);

    assert balanceOf(e.msg.sender) == balFromBefore - amount;
    assert balanceOf(to) == balToBefore + amount;

    satisfy amount > 0;
}

/// @title TransferFrom respects allowance
rule transferFromRespectsAllowance(address from, address to, uint256 amount) {
    env e;
    require from != to;

    mathint allowanceBefore = allowance(from, e.msg.sender);
    require allowanceBefore < max_uint256; // skip infinite allowance

    transferFrom(e, from, to, amount);

    mathint allowanceAfter = allowance(from, e.msg.sender);
    assert allowanceAfter == allowanceBefore - amount,
        "allowance must decrease by transferred amount";

    satisfy amount > 0;
}

/// @title Approve sets exact allowance
rule approveIntegrity(address spender, uint256 amount) {
    env e;

    approve(e, spender, amount);

    assert allowance(e.msg.sender, spender) == amount,
        "allowance must equal approved amount";

    satisfy amount > 0;
}

/// @title Transfer to self preserves balance
rule selfTransferPreservesBalance(uint256 amount) {
    env e;

    mathint balBefore = balanceOf(e.msg.sender);

    transfer(e, e.msg.sender, amount);

    assert balanceOf(e.msg.sender) == balBefore,
        "self-transfer must not change balance";

    satisfy amount > 0;
}

/// @title Zero transfer always succeeds
rule zeroTransferAlwaysSucceeds(address to) {
    env e;
    require e.msg.value == 0;

    transfer@withrevert(e, to, 0);

    assert !lastReverted,
        "zero transfer must not revert";

    satisfy to != e.msg.sender;
}

/// @title No method changes third-party balance
rule noThirdPartyBalanceChange(method f, address third) {
    env e;
    calldataarg args;
    require third != e.msg.sender;

    mathint balBefore = balanceOf(third);

    f(e, args);

    mathint balAfter = balanceOf(third);

    assert balAfter != balBefore =>
        (f.selector == sig:transfer(address, uint256).selector && third == to)
        || f.selector == sig:transferFrom(address, address, uint256).selector
        || f.selector == sig:mint(address, uint256).selector
        || f.selector == sig:burn(address, uint256).selector,
        "only transfer/transferFrom/mint/burn may change third-party balance";

    satisfy true;
}
```

---

## ERC4626 Vault Share Accounting

```cvl
methods {
    function totalAssets() external returns (uint256) envfree;
    function totalSupply() external returns (uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function deposit(uint256, address) external returns (uint256);
    function withdraw(uint256, address, address) external returns (uint256);
    function redeem(uint256, address, address) external returns (uint256);
    function convertToShares(uint256) external returns (uint256) envfree;
    function convertToAssets(uint256) external returns (uint256) envfree;
}

/// @title Deposit-withdraw round trip: user gets back no more than deposited
rule depositWithdrawRoundTrip(uint256 depositAmount) {
    env e;

    uint256 shares = deposit(e, depositAmount, e.msg.sender);
    uint256 withdrawnAssets = redeem(e, shares, e.msg.sender, e.msg.sender);

    assert withdrawnAssets <= depositAmount,
        "user must not profit from deposit-redeem round trip";

    satisfy depositAmount > 0 && shares > 0;
}

/// @title Share price can only increase (no vault inflation attack)
rule sharePriceNonDecreasing(method f)
filtered { f -> !f.isView }
{
    env e;
    calldataarg args;

    mathint assetsBefore = totalAssets();
    mathint sharesBefore = totalSupply();
    require sharesBefore > 0;

    f(e, args);

    mathint assetsAfter = totalAssets();
    mathint sharesAfter = totalSupply();
    require sharesAfter > 0;

    // Share price = assets / shares. Cross-multiply to avoid division.
    assert assetsAfter * sharesBefore >= assetsBefore * sharesAfter,
        "share price must not decrease";

    satisfy assetsAfter > assetsBefore;
}

/// @title convertToShares and convertToAssets are inverses (approximate)
rule conversionConsistency(uint256 assets) {
    require totalSupply() > 0;
    require totalAssets() > 0;

    uint256 shares = convertToShares(assets);
    uint256 roundTrip = convertToAssets(shares);

    // Due to rounding, roundTrip <= assets
    assert roundTrip <= assets,
        "conversion rounding must favor vault";

    satisfy assets > 0 && shares > 0;
}
```

---

## No Unexpected Reverts (DoS Resistance)

```cvl
/// @title Core user functions do not revert under normal conditions
rule withdrawDoesNotRevert(uint256 amount) {
    env e;
    require e.msg.value == 0;              // non-payable
    require e.msg.sender != 0;             // valid sender
    require balanceOf(e.msg.sender) >= amount;  // has funds
    require amount > 0;

    withdraw@withrevert(e, amount);

    assert !lastReverted,
        "withdraw must not revert when user has sufficient balance";

    satisfy amount > 0;
}
```

---

## Parametric Rule with Filter

```cvl
/// @title View functions do not change state
rule viewFunctionsDoNotChangeState(method f)
filtered { f -> f.isView }
{
    env e;
    calldataarg args;

    mathint supplyBefore = totalSupply();

    f(e, args);

    assert totalSupply() == supplyBefore,
        "view function must not change total supply";

    satisfy true;
}

/// @title All non-view functions preserve the sum-of-balances invariant
rule nonViewPreservesSolvency(method f)
filtered { f -> !f.isView && !f.isFallback }
{
    env e;
    calldataarg args;

    requireInvariant totalSupplyIsSumOfBalances();

    f(e, args);

    assert to_mathint(totalSupply()) == sumOfBalances,
        "non-view function must maintain solvency";

    satisfy true;
}
```

---

## Hyperproperty: Monotonicity via Storage Snapshots

Proves that depositing more always gives ≥ shares.

```cvl
/// @title Depositing more assets yields more or equal shares
rule depositMonotonicity(uint256 smallAmt, uint256 largeAmt) {
    env e;
    require smallAmt <= largeAmt;

    storage initial = lastStorage;

    uint256 sharesSmall = deposit(e, smallAmt, e.msg.sender) at initial;
    uint256 sharesLarge = deposit(e, largeAmt, e.msg.sender) at initial;

    assert sharesLarge >= sharesSmall,
        "more assets must yield more or equal shares";

    satisfy smallAmt < largeAmt && sharesLarge > sharesSmall;
}
```

---

## Multi-Contract Linking

When the main contract references another deployed contract:

### Spec file
```cvl
using Token as token;
using MainContract as main;

methods {
    // Main contract methods
    function main.deposit(uint256) external returns (uint256);
    function main.getBalance(address) external returns (uint256) envfree;

    // Token methods — used directly
    function token.balanceOf(address) external returns (uint256) envfree;
    function token.totalSupply() external returns (uint256) envfree;

    // External unknowns — summarize
    function _.onTokenTransfer(address, uint256) external => NONDET;
}
```

### Conf file
```json
{
    "files": [
        "src/MainContract.sol",
        "src/Token.sol"
    ],
    "verify": "MainContract:certora/specs/MainContract.spec",
    "link": [
        "MainContract:token=Token"
    ]
}
```

---

## Preserved Block Patterns

### Generic preserved block
```cvl
invariant alwaysPositive()
    totalSupply() > 0
    {
        preserved with (env e) {
            require e.msg.sender != 0;
            require e.msg.value == 0;
        }
    }
```

### Method-specific preserved block
```cvl
invariant supplyBounded()
    totalSupply() <= MAX_SUPPLY()
    {
        preserved mint(address to, uint256 amount) with (env e) {
            require e.msg.sender == owner();
            requireInvariant totalSupplyIsSumOfBalances();
        }
        preserved with (env e) {
            require e.msg.sender != 0;
        }
    }
```

### Wildcard contract preserved block
```cvl
invariant crossContractInvariant()
    main.getTotal() == token.totalSupply()
    {
        preserved with (env e) {
            requireInvariant totalSupplyIsSumOfBalances();
        }
        preserved _.transfer(address to, uint256 amt) with (env e) {
            require amt <= balanceOf(e.msg.sender);
        }
    }
```

---

## Conf Files Per Use Case

### Development iteration
```json
{
    "files": ["src/Contract.sol"],
    "verify": "Contract:certora/specs/Contract.spec",
    "optimistic_loop": true,
    "loop_iter": "2",
    "rule_sanity": "basic",
    "msg": "dev iteration",
    "rule": ["mySpecificRule"]
}
```

### Full verification
```json
{
    "files": ["src/Contract.sol"],
    "verify": "Contract:certora/specs/Contract.spec",
    "optimistic_loop": false,
    "loop_iter": "5",
    "rule_sanity": "advanced",
    "multi_assert_check": true,
    "msg": "full verification"
}
```

### Multi-contract with linking
```json
{
    "files": [
        "src/MainContract.sol",
        "src/Token.sol",
        "src/Oracle.sol"
    ],
    "verify": "MainContract:certora/specs/MainContract.spec",
    "link": [
        "MainContract:token=Token",
        "MainContract:oracle=Oracle"
    ],
    "optimistic_loop": true,
    "loop_iter": "3",
    "rule_sanity": "basic",
    "packages": [
        "@openzeppelin/contracts=node_modules/@openzeppelin/contracts"
    ]
}
```

### Mutation testing
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
                "mutations": [
                    "binary-op-mutation",
                    "require-mutation",
                    "assignment-mutation",
                    "if-statement-mutation"
                ]
            }
        ],
        "msg": "mutation coverage"
    }
}
```

---

## Anti-Patterns (DO NOT USE)

### 1. Vacuous rule (contradictory requires)
```cvl
// BAD: x > 10 AND x < 5 is impossible — rule passes trivially
rule vacuousExample(uint256 x) {
    require x > 10;
    require x < 5;
    assert false; // This "passes" because no model satisfies both requires
}
```
**Fix**: Always add `satisfy true;` and enable `rule_sanity: basic`.

### 2. Tautological assertion
```cvl
// BAD: This is always true regardless of contract behavior
rule tautology(uint256 x) {
    require x > 0;
    assert x > 0; // Just re-states the require
}
```
**Fix**: Assert a property of the CONTRACT, not the input.

### 3. Reusing env across incompatible calls
```cvl
// BAD: Same env for payable and non-payable calls
rule badEnvReuse() {
    env e;
    payableDeposit(e);     // needs msg.value > 0
    nonPayableWithdraw(e); // needs msg.value == 0
    // One of these always reverts → rule is vacuous
}
```
**Fix**: Use separate `env` variables for payable vs non-payable calls.

### 4. Testing admin does bad things
```cvl
// BAD: Testing that admin can drain funds — admin CAN do this by design
rule adminShouldNotDrain() {
    env e;
    require e.msg.sender == owner();
    adminWithdraw(e);
    assert totalAssets() > 0; // Admin CAN set this to zero
}
```
**Fix**: Admin tests should verify that NON-admins cannot do admin things.

### 5. Filtering out critical methods
```cvl
// BAD: Filtering out the very method that can break the invariant
invariant supplyBounded()
    totalSupply() <= MAX_SUPPLY()
    filtered { f -> f.selector != sig:mint(address, uint256).selector }
    // mint is the most likely method to violate this!
```
**Fix**: Never filter methods that are most likely to violate the property.

### 6. Missing init_state axiom for ghost
```cvl
// BAD: Ghost starts at arbitrary value — invariant may fail base case
ghost mathint sum;
// Missing: init_state axiom sum == 0;

hook Sstore balances[KEY address a] uint256 newV (uint256 oldV) {
    sum = sum + newV - oldV;
}
```
**Fix**: Always set `init_state axiom` matching the constructor state.

### 7. Using uint256 for intermediate arithmetic
```cvl
// BAD: Overflow possible in intermediate calculation
rule overflowRisk(uint256 a, uint256 b) {
    uint256 product = a * b; // Can overflow!
    assert product >= a;
}
```
**Fix**: Use `mathint` for all intermediate arithmetic.

### 8. Invariant expression that can revert
```cvl
// BAD: Division by zero when totalSupply() == 0
invariant pricePositive()
    totalAssets() / totalSupply() > 0;
```
**Fix**: Add `require totalSupply() > 0;` in preserved block, or rewrite as multiplication: `totalAssets() > 0 => totalSupply() > 0`.
