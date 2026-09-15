# Medusa Harness Templates

## Contents
- [Base harness scaffold](#base-harness-scaffold)
- [Solvency invariants](#solvency-invariants)
- [Access control invariants](#access-control-invariants)
- [State machine invariants](#state-machine-invariants)
- [Arithmetic and precision invariants](#arithmetic-and-precision-invariants)
- [Oracle invariants](#oracle-invariants)
- [Reentrancy guard invariants](#reentrancy-guard-invariants)
- [ERC20 compliance invariants](#erc20-compliance-invariants)
- [ERC4626 vault invariants](#erc4626-vault-invariants)
- [Actor proxy pattern](#actor-proxy-pattern)
- [Ghost variable tracking](#ghost-variable-tracking)
- [Anti-patterns](#anti-patterns)

---

## Base Harness Scaffold

Every Medusa harness follows this structure. The harness contract IS the `targetContract` — Medusa deploys it and fuzzes its public functions.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Import target contracts
import "../../src/TargetContract.sol";
// If using Foundry, console is available for debug (remove before finalizing)
// import "forge-std/console.sol";

contract InvariantHarness {

    // --- Target contract instances ---
    TargetContract target;

    // ---- Ghost variables for tracking ----
    // Ghost variables mirror protocol state for invariant assertions.
    // They are updated by harness wrapper functions, not by the target directly.
    uint256 internal ghost_totalDeposited;
    mapping(address => uint256) internal ghost_userDeposits;
    address[] internal actors;

    // ---- Setup (constructor) ----
    // Medusa calls the constructor once during deployment.
    // Deploy all target contracts here. Order matters.
    constructor() payable {
        target = new TargetContract();

        // Register actor addresses (must match medusa.json senderAddresses)
        actors.push(address(0x10000));
        actors.push(address(0x20000));
        actors.push(address(0x30000));
    }

    // ---- Input bounding helpers (inline — no external deps) ----

    function clampBetween(uint256 value, uint256 low, uint256 high) internal pure returns (uint256) {
        if (value < low || value > high) {
            return low + (value % (high - low + 1));
        }
        return value;
    }

    function clampLte(uint256 value, uint256 upper) internal pure returns (uint256) {
        if (value > upper) {
            return value % (upper + 1);
        }
        return value;
    }

    function clampGte(uint256 value, uint256 lower) internal pure returns (uint256) {
        if (value < lower) {
            return lower;
        }
        return value;
    }

    // ---- Wrapper functions (the fuzzer calls these) ----
    // Wrappers call target functions and update ghost state.
    // The fuzzer generates random inputs for these.

    function handler_deposit(uint256 amount) public {
        amount = clampBetween(amount, 1, address(this).balance);
        if (amount == 0) return; // skip trivial case

        uint256 preBal = target.balances(msg.sender);
        target.deposit{value: amount}();
        uint256 postBal = target.balances(msg.sender);

        // Update ghost state
        ghost_totalDeposited += amount;
        ghost_userDeposits[msg.sender] += amount;

        // Function-level assertion: balance increased by exact amount
        assert(postBal == preBal + amount);
    }

    // ---- System-level property tests ----
    // No parameters. Called by Medusa after each tx in the sequence.
    // Must be view/pure. Use assert() for checks.

    function property_totalDeposited_matches_ghost() public view {
        assert(target.totalDeposited() == ghost_totalDeposited);
    }

    // ---- Function-level property tests ----
    // Accept fuzzed parameters. Medusa generates random values.

    function property_deposit_bounded_by_max(uint256 amount) public {
        amount = clampBetween(amount, 1, address(this).balance);
        if (amount == 0) return;

        target.deposit{value: amount}();
        assert(target.totalDeposited() <= target.MAX_DEPOSIT_AMOUNT());
    }
}
```

---

## Solvency Invariants

Verify that the system cannot create or destroy value.

```solidity
// System-level: sum of all user balances equals contract's tracked total
function property_solvency_sum_equals_total() public view {
    uint256 sum;
    for (uint256 i = 0; i < actors.length; i++) {
        sum += target.balances(actors[i]);
    }
    // Also count the harness itself as a potential depositor
    sum += target.balances(address(this));
    assert(sum == target.totalDeposited());
}

// System-level: contract ETH balance covers all claims
function property_solvency_eth_covers_deposits() public view {
    assert(address(target).balance >= target.totalDeposited());
}

// System-level: no value created from nothing (ghost tracking)
function property_no_free_value() public view {
    assert(ghost_totalDeposited == target.totalDeposited());
}
```

---

## Access Control Invariants

Verify that privileged functions reject unauthorized callers.

```solidity
// Test that a non-owner cannot call an owner-only function.
// This is a function-level property: Medusa fuzzes the caller.
function property_nonOwner_cannot_pause() public {
    // Skip if the caller IS the owner — the invariant is about unauthorized access
    if (msg.sender == target.owner()) return;

    // Attempt the privileged call — it must revert
    try target.pause() {
        // If we reach here, the call succeeded for a non-owner — invariant violated
        assert(false);
    } catch {
        // Expected: call reverted for non-owner
    }
}

// Test that owner CAN call the function (sanity check)
function property_owner_can_pause() public {
    IHevm(0x7109709ECfa91a80626fF3989D68f67F5b1DD12D).prank(target.owner());
    try target.pause() {
        // Expected: call succeeded for owner
    } catch {
        // Owner should not be blocked — invariant violated
        assert(false);
    }
}
```

**Key pattern**: Use `try/catch` to test revert behavior. `assert(false)` inside the `try` block means "this should not have succeeded."

---

## State Machine Invariants

Verify valid state transitions.

```solidity
// Track the previous state via ghost variable
uint8 internal ghost_previousState;

function handler_advanceState() public {
    uint8 stateBefore = uint8(target.currentState());
    target.advanceState();
    uint8 stateAfter = uint8(target.currentState());

    // Assert valid transitions: INIT(0)->ACTIVE(1)->PAUSED(2)->FINALIZED(3)
    if (stateBefore == 0) assert(stateAfter == 1);
    else if (stateBefore == 1) assert(stateAfter == 1 || stateAfter == 2);
    else if (stateBefore == 2) assert(stateAfter == 2 || stateAfter == 3);
    else if (stateBefore == 3) assert(stateAfter == 3); // Terminal — absorbing state

    ghost_previousState = stateAfter;
}

// System-level: state is always within valid range
function property_state_in_valid_range() public view {
    uint8 state = uint8(target.currentState());
    assert(state <= 3);
}

// System-level: finalized state means no further changes
function property_finalized_is_terminal() public view {
    if (ghost_previousState == 3) {
        assert(uint8(target.currentState()) == 3);
    }
}
```

---

## Arithmetic and Precision Invariants

Verify math correctness with fuzzed inputs.

```solidity
// Function-level: multiplication-before-division preserves precision
function property_mulDiv_precision(uint256 a, uint256 b, uint256 c) public pure {
    // Bound to avoid trivial/overflow cases
    a = clampBetween(a, 1, type(uint128).max);
    b = clampBetween(b, 1, type(uint128).max);
    c = clampBetween(c, 1, type(uint128).max);

    // mulDiv should not lose more than 1 unit of precision
    uint256 result = (a * b) / c;
    uint256 reconstructed = (result * c);
    // The error must be less than c (one unit of division rounding)
    assert(a * b - reconstructed < c);
}

// Function-level: percentage calculation stays in bounds
function property_fee_never_exceeds_max(uint256 amount) public view {
    amount = clampBetween(amount, 1, type(uint128).max);
    uint256 fee = target.calculateFee(amount);
    uint256 maxFee = (amount * target.MAX_FEE_BPS()) / 10_000;
    assert(fee <= maxFee);
}

// System-level: exchange rate is monotonically non-decreasing
// (for vault-like contracts where share price should only increase)
uint256 internal ghost_lastSharePrice;

function property_share_price_monotonic() public {
    uint256 currentPrice = target.sharePrice();
    // Skip if no shares exist (price undefined)
    if (target.totalSupply() == 0) return;
    assert(currentPrice >= ghost_lastSharePrice);
    ghost_lastSharePrice = currentPrice;
}
```

---

## Oracle Invariants

Verify oracle data freshness and validity.

```solidity
// System-level: price is never zero
function property_oracle_price_nonzero() public view {
    (, int256 price,,,) = target.priceFeed().latestRoundData();
    assert(price > 0);
}

// System-level: price data is fresh
function property_oracle_price_fresh() public view {
    (,, uint256 startedAt, uint256 updatedAt,) = target.priceFeed().latestRoundData();
    // updatedAt must be within MAX_STALENESS of current block
    assert(block.timestamp - updatedAt <= target.MAX_STALENESS());
    // Round must have started
    assert(startedAt > 0);
}

// System-level: round is complete
function property_oracle_round_complete() public view {
    (uint80 roundId,,, uint256 updatedAt, uint80 answeredInRound) =
        target.priceFeed().latestRoundData();
    assert(answeredInRound >= roundId);
    assert(updatedAt > 0);
}
```

---

## Reentrancy Guard Invariants

Verify reentrancy protection.

```solidity
// Use a callback contract to test reentrancy
contract ReentrancyAttacker {
    TargetContract target;
    bool attacked;

    constructor(TargetContract _target) {
        target = _target;
    }

    function attack(uint256 amount) external payable {
        target.deposit{value: amount}();
        target.withdraw(amount);
    }

    receive() external payable {
        if (!attacked) {
            attacked = true;
            // Attempt reentrant call — should revert if guard works
            try target.withdraw(msg.value) {
                // If this succeeds, the reentrancy guard is broken
                // The property test in the harness will detect this via balance check
            } catch {
                // Expected: reentrancy guard blocks the call
            }
        }
    }
}

// In the harness:
ReentrancyAttacker reentrancyAttacker;

constructor() payable {
    target = new TargetContract();
    reentrancyAttacker = new ReentrancyAttacker(target);
}

function property_no_reentrancy_profit(uint256 amount) public {
    amount = clampBetween(amount, 1 ether, 10 ether);
    if (address(this).balance < amount) return;

    uint256 targetBalBefore = address(target).balance;

    // Fund attacker and attempt reentrancy
    (bool sent,) = address(reentrancyAttacker).call{value: amount}("");
    if (!sent) return;

    try reentrancyAttacker.attack(amount) {} catch {}

    // Invariant: target should not have lost more than the attacker deposited
    assert(address(target).balance >= targetBalBefore);
}
```

---

## ERC20 Compliance Invariants

```solidity
// System-level: total supply equals sum of all balances
function property_erc20_supply_conservation() public view {
    uint256 sum;
    for (uint256 i = 0; i < actors.length; i++) {
        sum += target.balanceOf(actors[i]);
    }
    sum += target.balanceOf(address(this));
    sum += target.balanceOf(address(target));
    assert(sum == target.totalSupply());
}

// Function-level: transfer does not change total supply
function property_transfer_preserves_supply(address to, uint256 amount) public {
    if (to == address(0)) return; // skip zero address
    amount = clampLte(amount, target.balanceOf(address(this)));
    if (amount == 0) return;

    uint256 supplyBefore = target.totalSupply();
    target.transfer(to, amount);
    assert(target.totalSupply() == supplyBefore);
}

// Function-level: self-transfer is neutral
function property_self_transfer_neutral(uint256 amount) public {
    amount = clampLte(amount, target.balanceOf(address(this)));
    uint256 balBefore = target.balanceOf(address(this));
    target.transfer(address(this), amount);
    assert(target.balanceOf(address(this)) == balBefore);
}
```

---

## ERC4626 Vault Invariants

```solidity
// System-level: totalAssets >= convertToAssets(totalSupply)
function property_vault_asset_backing() public view {
    if (target.totalSupply() == 0) return;
    uint256 totalAssets = target.totalAssets();
    uint256 allSharesValue = target.convertToAssets(target.totalSupply());
    assert(totalAssets >= allSharesValue);
}

// Function-level: deposit round-trips within 1 wei tolerance
function property_vault_deposit_roundtrip(uint256 assets) public {
    assets = clampBetween(assets, 1, type(uint128).max);

    uint256 shares = target.previewDeposit(assets);
    uint256 assetsBack = target.previewRedeem(shares);

    // Rounding should favor the vault: depositor gets back at most what they put in
    assert(assetsBack <= assets);
}

// Function-level: rounding favors vault on deposit (fewer shares)
function property_vault_deposit_rounds_down(uint256 assets) public {
    assets = clampBetween(assets, 1, type(uint128).max);

    uint256 shares = target.previewDeposit(assets);
    uint256 exactShares = (assets * target.totalSupply()) / target.totalAssets();

    // previewDeposit should return <= exact mathematical result
    if (target.totalSupply() > 0 && target.totalAssets() > 0) {
        assert(shares <= exactShares + 1); // +1 tolerance for intermediate rounding
    }
}

// System-level: first depositor cannot inflate shares
function property_no_inflation_attack() public view {
    if (target.totalSupply() > 0 && target.totalSupply() < 1000) {
        // If very few shares exist, check that 1 share is worth at most
        // a reasonable amount (prevents donation-based inflation)
        uint256 shareValue = target.convertToAssets(1);
        assert(shareValue < 1e24); // 1M tokens — unreasonable single-share value
    }
}
```

---

## Actor Proxy Pattern

For protocols requiring multiple distinct users, create proxy contracts that act as different users:

```solidity
contract ActorProxy {
    address public target;

    constructor(address _target) {
        target = _target;
    }

    function doDeposit(uint256 amount) external payable returns (bool) {
        (bool success,) = target.call{value: amount}(
            abi.encodeWithSignature("deposit()")
        );
        return success;
    }

    function doWithdraw(uint256 amount) external returns (bool) {
        (bool success,) = target.call(
            abi.encodeWithSignature("withdraw(uint256)", amount)
        );
        return success;
    }

    receive() external payable {}
}

// In the harness constructor:
ActorProxy[] internal proxies;

constructor() payable {
    target = new TargetContract();
    for (uint256 i = 0; i < 3; i++) {
        ActorProxy proxy = new ActorProxy(address(target));
        proxies.push(proxy);
    }
}

// Wrapper that picks a random actor
function handler_deposit_as_actor(uint8 actorIdx, uint256 amount) public {
    actorIdx = uint8(clampLt(uint256(actorIdx), proxies.length));
    amount = clampBetween(amount, 1, address(this).balance);
    if (amount == 0) return;

    // Fund the proxy
    (bool sent,) = address(proxies[actorIdx]).call{value: amount}("");
    if (!sent) return;

    proxies[actorIdx].doDeposit(amount);
    ghost_totalDeposited += amount;
}
```

---

## Ghost Variable Tracking

Ghost variables are harness-only state that mirrors expected protocol behavior. They enable invariant assertions without trusting the target's internal accounting.

**Rules**:
1. Update ghost state in EVERY wrapper function that modifies target state
2. Never read ghost state from the target — derive it independently
3. Ghost variables track the "should be" value; the target holds the "actually is" value

```solidity
// Ghost state
uint256 internal ghost_deposits;
uint256 internal ghost_withdrawals;
mapping(address => uint256) internal ghost_balances;

function handler_deposit(uint256 amount) public {
    // ... call target.deposit ...
    ghost_deposits += amount;
    ghost_balances[msg.sender] += amount;
}

function handler_withdraw(uint256 amount) public {
    // ... call target.withdraw ...
    ghost_withdrawals += amount;
    ghost_balances[msg.sender] -= amount;
}

// Conservation of value: deposits - withdrawals = current balance
function property_conservation_of_value() public view {
    assert(ghost_deposits - ghost_withdrawals == target.totalDeposited());
}
```

---

## Anti-Patterns

### BAD: Admin creates the invariant violation

```solidity
// WRONG — admin sets up the exploit condition
function property_bad_admin_setup() public {
    IHevm(0x7109709ECfa91a80626fF3989D68f67F5b1DD12D).prank(target.owner());
    target.setMaxDeposit(0); // Admin action IS the problem
    assert(target.maxDeposit() > 0); // This "catches" what the admin just did
}
```

**Fix**: Admin prank is allowed ONLY for realistic initial setup (in constructor). Property tests verify invariants hold for all callers.

### BAD: Vague assertion

```solidity
// WRONG — passes trivially, proves nothing
function property_bad_vague() public view {
    assert(target.totalSupply() >= 0); // uint256 is always >= 0
}
```

**Fix**: Assert specific relationships with independent calculations.

### BAD: Tautological assertion

```solidity
// WRONG — compares target output to itself
function property_bad_tautology() public view {
    uint256 a = target.computeShares(100e18);
    uint256 b = target.computeShares(100e18);
    assert(a == b); // Tests determinism, not correctness
}
```

**Fix**: Derive expected value independently (ghost state, math formula, known constant).

### BAD: Missing input bounds

```solidity
// WRONG — unbounded input causes meaningless reverts
function property_bad_unbounded(uint256 amount) public {
    target.deposit{value: amount}(); // amount > balance → always reverts
    assert(target.totalDeposited() > 0);
}
```

**Fix**: Bound all inputs to realistic ranges with `clampBetween`.

### BAD: Using require() instead of assert()

```solidity
// WRONG — require() causes revert, Medusa skips it (not a failure)
function property_bad_require() public view {
    require(target.totalSupply() == ghost_totalMinted, "supply mismatch");
}
```

**Fix**: Always use `assert()` — only `assert` failures (panic 0x01) are caught as property violations.

### BAD: Unnecessary console.log

```solidity
// WRONG — logs in every property call, wastes gas, obscures output
function property_bad_logging() public view {
    console.log("Checking supply:", target.totalSupply());
    console.log("Ghost total:", ghost_totalMinted);
    console.log("Difference:", target.totalSupply() - ghost_totalMinted);
    assert(target.totalSupply() == ghost_totalMinted);
}
```

**Fix**: Remove all logs from final harness. Use only during debugging, then delete.
