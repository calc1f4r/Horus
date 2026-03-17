---
# Core Classification
protocol: Sentiment
chain: arbitrum
category: amm
vulnerability_type: read_only_reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: oracle_manipulation

# Source Information
source: reports/constantproduct/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md
audit_firm: Sherlock
severity: high

# Impact Classification
impact: unfair_liquidations
exploitability: 1.0
financial_impact: high

# Context Tags
tags:
  - read_only_reentrancy
  - curve_virtual_price
  - liquidation_manipulation
  - view_reentrancy

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | oracle_manipulation | read_only_reentrancy

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - attack
  - canLiquidate
  - fallback
  - getPrice
  - liquidate
  - msg.sender
  - receive
  - remove_liquidity
  - totalSupply
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Sentiment] | reports/constantproduct/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md | HIGH | Sherlock | - |


# Sentiment - Curve Read-Only Reentrancy Liquidation Attack

## Unique Protocol Issue

**Protocol**: Sentiment  
**Audit Firm**: Sherlock  
**Severity**: HIGH  
**Source**: `reports/constantproduct/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md`

## Overview

Sentiment used Curve's `virtual_price` to price wstETH-ETH LP tokens as collateral. Through "view-only reentrancy" during Curve's `remove_liquidity`, the attacker could temporarily suppress the virtual_price, making healthy positions appear undercollateralized and trigger unfair liquidations.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | oracle_manipulation | read_only_reentrancy`
- Interaction scope: `single_contract`
- Primary affected component(s): `oracle_manipulation`
- High-signal code keywords: `attack`, `canLiquidate`, `fallback`, `getPrice`, `liquidate`, `msg.sender`, `receive`, `remove_liquidity`
- Typical sink / impact: `unfair_liquidations`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `CrossValidatedOracle.function -> CurveLPOracle.function -> CurveReentrancyAttack.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State variable updated after external interaction instead of before (CEI violation)
- Signal 2: Withdrawal path produces different accounting than deposit path for same principal
- Signal 3: Reward accrual continues during paused/emergency state
- Signal 4: Edge case in state machine transition allows invalid state

#### False Positive Guards

- Not this bug when: Standard security patterns (access control, reentrancy guards, input validation) are in place
- Safe if: Protocol behavior matches documented specification
- Requires attacker control of: specific conditions per pattern

## Why This Is Unique

This vulnerability exploited a novel attack vector:
1. **View-Only Reentrancy**: Read-only calls during callback show inconsistent state
2. **Curve's Native ETH**: `remove_liquidity` sends ETH before updating state
3. **Virtual Price Manipulation**: During callback, `virtual_price` is artificially low
4. **Liquidation Arbitrage**: Attacker liquidates healthy positions during suppressed price

## Attack Mechanics

```
Normal State:
┌─────────────────────────────────────────┐
│ Curve Pool                               │
│ - reserves: 1000 wstETH + 1000 ETH      │
│ - totalSupply: 1000 LP                  │
│ - virtual_price: 1.0                    │
└─────────────────────────────────────────┘

During remove_liquidity callback (ETH sent, state not updated):
┌─────────────────────────────────────────┐
│ Curve Pool                               │
│ - reserves: 1000 wstETH + 500 ETH       │ <- ETH sent out
│ - totalSupply: 1000 LP                  │ <- NOT yet reduced
│ - virtual_price: 0.75                   │ <- SUPPRESSED!
└─────────────────────────────────────────┘
```

## Vulnerable Code Pattern

```solidity
// ❌ VULNERABLE: Oracle uses virtual_price during remove_liquidity callback
contract CurveLPOracle {
    function getPrice(address lpToken) external view returns (uint256) {
        // virtual_price = reserves_value / totalSupply
        // During reentrancy: reserves down, totalSupply unchanged = LOW PRICE
        return ICurve(pool).get_virtual_price() * getUnderlyingPrice() / 1e18;
    }
}

contract RiskEngine {
    function canLiquidate(address account) external view returns (bool) {
        uint256 collateralValue = oracle.getPrice(lpToken) * balance;
        uint256 debtValue = oracle.getPrice(debtToken) * debt;
        
        // During reentrancy: collateralValue is ARTIFICIALLY LOW
        // Healthy positions appear liquidatable!
        return collateralValue < debtValue * minCollateralRatio;
    }
}

// Curve's remove_liquidity (simplified):
function remove_liquidity(uint256 amount, uint256[2] minAmounts) external {
    uint256 ethAmount = calcEthToReturn(amount);
    uint256 wstethAmount = calcWstethToReturn(amount);
    
    // 1. Send ETH first (triggers receive() callback)
    msg.sender.call{value: ethAmount}("");  // REENTRANCY POINT
    
    // 2. State updated AFTER callback returns
    totalSupply -= amount;  // Too late!
    _transfer(wstETH, msg.sender, wstethAmount);
}
```

## Attack Scenario

```solidity
contract CurveReentrancyAttack {
    Sentiment sentiment;
    ICurve curvePool;
    address victim;  // Healthy position with ~150% collateral ratio
    
    function attack() external {
        // 1. Flash loan large amount of LP tokens
        // 2. Call remove_liquidity (triggers receive callback)
        curvePool.remove_liquidity(hugeAmount, [0, 0]);
    }
    
    receive() external payable {
        // 3. During callback, virtual_price is suppressed!
        // Victim's position now appears undercollateralized
        
        // 4. Liquidate "underwater" position
        sentiment.liquidate(victim);
        // Attacker profits from liquidation bonus
        // Victim loses collateral unfairly
    }
    
    // After callback completes:
    // - Curve updates totalSupply
    // - virtual_price returns to normal
    // - But damage is done - victim already liquidated
}
```

## Mathematical Analysis

```
Victim's Position:
- Collateral: 100 wstETH-ETH LP tokens
- Debt: 65 ETH
- Normal virtual_price: 1.0 ETH per LP
- Normal collateral value: 100 ETH
- Collateral ratio: 100/65 = 153.8% (HEALTHY)

During Attack:
- Attacker removes 50% of pool's LP
- ETH sent out but totalSupply not reduced
- Suppressed virtual_price: 0.75 ETH per LP
- Suppressed collateral value: 75 ETH
- Suppressed ratio: 75/65 = 115.4% (LIQUIDATABLE)

Attacker liquidates victim at suppressed price
Profit = liquidation bonus on healthy position
```

## Impact

- **Unfair Liquidations**: Healthy positions liquidated
- **User Fund Loss**: Victims lose collateral + liquidation penalty
- **No Recovery**: Once liquidated, position is closed
- **Flash Loan Amplified**: Large positions make attack more profitable

## Secure Implementation

```solidity
// ✅ SECURE: Multiple mitigations for read-only reentrancy

// Option 1: Check Curve's reentrancy lock
contract SecureOracle {
    ICurve public curve;
    
    function getPrice(address lpToken) external view returns (uint256) {
        // Curve has a withdraw_admin_fees that will revert if reentered
        // Use this as a reentrancy check
        try curve.withdraw_admin_fees() {
            // Revert intentionally - we're just checking
            revert("Expected revert");
        } catch {
            // If it reverts with "Reentrancy", we're in callback
            // Use cached/oracle price instead
        }
        
        return curve.get_virtual_price() * getUnderlyingPrice() / 1e18;
    }
}

// Option 2: Use TWAP or external oracle
contract TWAPOracle {
    function getPrice(address lpToken) external view returns (uint256) {
        // Don't rely on instantaneous virtual_price
        // Use time-weighted average or Chainlink
        return chainlink.getPrice(lpToken);
    }
}

// Option 3: Cross-validate virtual_price
contract CrossValidatedOracle {
    function getPrice(address lpToken) external view returns (uint256) {
        uint256 virtualPrice = curve.get_virtual_price();
        uint256 expectedPrice = calculateExpectedPrice();
        
        // If virtual_price deviates significantly, use fallback
        require(
            virtualPrice > expectedPrice * 90 / 100,
            "Price deviation detected"
        );
        
        return virtualPrice;
    }
}
```

## Detection Patterns

```solidity
// RED FLAGS:

// 1. Using virtual_price for collateral valuation
value = curve.get_virtual_price() * balance;

// 2. Liquidation logic callable in same transaction
function liquidate(address account) external {
    // Can be called during attacker's callback
}

// 3. No reentrancy guards on oracle reads
function getPrice() view returns (uint256) {
    // View functions can be called during reentrancy
}

// 4. Curve pools with native ETH transfers
// These have reentrancy windows during withdrawals
```

## Lessons for Auditors

1. **View Reentrancy Is Real**: `view` functions can return wrong values during reentrancy
2. **Native ETH Transfers**: Any ETH transfer creates a callback opportunity
3. **Curve's virtual_price**: Can be manipulated during `remove_liquidity`
4. **Cross-Validation**: Compare on-chain prices with external oracles
5. **Reentrancy Lock Checks**: Use protocol's own reentrancy locks for validation

## Keywords

`read_only_reentrancy`, `view_reentrancy`, `curve_virtual_price`, `liquidation_manipulation`, `wsteth_eth`, `sentiment`, `LP_token_pricing`, `flash_loan_attack`, `callback_attack`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`amm`, `attack`, `canLiquidate`, `curve_virtual_price`, `fallback`, `getPrice`, `liquidate`, `liquidation_manipulation`, `msg.sender`, `read_only_reentrancy`, `receive`, `remove_liquidity`, `totalSupply`, `view_reentrancy`
