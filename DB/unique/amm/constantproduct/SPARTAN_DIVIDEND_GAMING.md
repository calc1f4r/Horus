---
# Core Classification
protocol: Spartan Protocol
chain: bsc
category: amm
vulnerability_type: dividend_gaming

# Attack Vector Details
attack_type: economic_exploit
affected_component: fee_distribution

# Source Information
source: reports/constantproduct/h-08-dividend-reward-can-be-gamed.md
audit_firm: Code4rena
severity: high

# Impact Classification
impact: reserve_drainage
exploitability: 1.0
financial_impact: high

# Context Tags
tags:
  - dividend
  - fee_manipulation
  - averaging_attack
  - reserve_drainage

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | fee_distribution | dividend_gaming

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - addDividend
  - addLiquidity
  - addTradeFee
  - block.timestamp
  - calculateDividend
  - drainReserve
  - micro
  - receive
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Spartan Protocol] | reports/constantproduct/h-08-dividend-reward-can-be-gamed.md | HIGH | Code4rena | - |


# Spartan Protocol - Dividend Reward Gaming Vulnerability

## Unique Protocol Issue

**Protocol**: Spartan Protocol  
**Audit Firm**: Code4rena  
**Severity**: HIGH  
**Source**: `reports/constantproduct/h-08-dividend-reward-can-be-gamed.md`

## Overview

Spartan Protocol's dividend distribution system used a rolling average of the last 20 trades to determine fee distribution. This design allowed attackers to manipulate the average by executing micro-trades, then capture disproportionate dividends by becoming the dominant LP in curated pools.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | fee_distribution | dividend_gaming`
- Interaction scope: `single_contract`
- Primary affected component(s): `fee_distribution`
- High-signal code keywords: `addDividend`, `addLiquidity`, `addTradeFee`, `block.timestamp`, `calculateDividend`, `drainReserve`, `micro`, `receive`
- Typical sink / impact: `reserve_drainage`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
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

## Why This Is Unique to Spartan

Unlike standard fee collection, Spartan:
1. **Rolling Average**: Uses only last 20 trades for fee baseline
2. **Curated Pools**: Only specific pools receive dividends from reserve
3. **Daily Allocation**: Reserve distributes based on fee comparison
4. **Manipulable Baseline**: Micro-trades can zero out the average

## Vulnerable Code Pattern

```solidity
// ❌ VULNERABLE: Rolling average based on trade count, not volume/time
function addDividend(uint256 _fees) external {
    // normalAverageFee is average of last 20 trade fees
    // Can be zeroed by 20 micro-trades!
    uint256 feeDividend = _fees * dailyAllocation / (_fees + normalAverageFee);
    
    // If normalAverageFee = 0, feeDividend = dailyAllocation / 2
    // Attacker gets 50% of daily allocation per trade!
    reserve.transfer(pool, feeDividend);
}

function addTradeFee(uint256 fee) internal {
    // Rolling window of 20 trades
    fees[feeIndex] = fee;
    feeIndex = (feeIndex + 1) % arrayFeeSize;  // arrayFeeSize = 20
    
    // Calculate average
    normalAverageFee = sum(fees) / arrayFeeSize;
}
```

## Attack Scenario

1. **Become Dominant LP**: Provide liquidity to smallest curated pool
2. **Zero the Average**: Execute 20 trades of 1 wei each
   - Each trade generates 0 fees
   - normalAverageFee becomes 0
3. **Execute Fee-Generating Trade**: Make one normal trade
   - feeDividend = dailyAllocation / 2
   - Half of reserve's daily allocation sent to pool
4. **Repeat**: Zero average again, extract more
5. **Redeem LP**: Withdraw share of profits

```solidity
// Attack execution
function drainReserve() external {
    // Step 1: Provide LP to smallest curated pool
    pool.addLiquidity(amount0, amount1);
    
    // Step 2: Zero the average with 20 micro-trades
    for (uint i = 0; i < 20; i++) {
        pool.buyTo(1);  // 1 wei trade, 0 fees
    }
    
    // Step 3: Normal trade to capture dividend
    pool.buyTo(normalAmount);  // Captures dailyAllocation / 2
    
    // Step 4: Repeat until reserve is empty
    // Step 5: Redeem LP tokens for profit
}
```

## Impact

- **Reserve Drainage**: Entire reserve can be systematically emptied
- **Daily Allocation Theft**: Attacker captures majority of each day's distribution
- **LP Dilution**: Legitimate LPs lose expected dividend share
- **Low Cost Attack**: Only gas costs for micro-trades

## Secure Implementation

```solidity
// ✅ SECURE: Volume-weighted average over time period
function calculateDividend(uint256 _fees) internal view returns (uint256) {
    // Use volume-weighted average, not trade-count average
    uint256 volumeWeightedAvgFee = getVolumeWeightedFee(TIME_WINDOW);
    
    // Or use time-based minimum
    require(block.timestamp >= lastDividendTime + MIN_INTERVAL, "Too soon");
    
    return _fees * dailyAllocation / (_fees + volumeWeightedAvgFee);
}

// Alternative: Use cumulative volume
mapping(uint256 => uint256) public dailyVolume;
mapping(uint256 => uint256) public dailyFees;

function addTradeFee(uint256 volume, uint256 fee) internal {
    uint256 today = block.timestamp / 1 days;
    dailyVolume[today] += volume;
    dailyFees[today] += fee;
}
```

## Detection Patterns

Look for these anti-patterns:

```
- Rolling averages based on trade count (not volume/time)
- Fee calculations that can be zeroed
- Dividend distributions without minimum thresholds
- No minimum trade size requirements
- Easily manipulated baseline metrics
```

## Lessons for Auditors

1. **Trade-Count Averages Are Dangerous**: Always prefer volume-weighted or time-weighted
2. **Minimum Trade Sizes**: Prevent micro-trade manipulation
3. **Time-Based Windows**: Use time periods, not transaction counts
4. **Reserve Protection**: Implement maximum distribution limits
5. **Economic Modeling**: Calculate attack profitability vs gas costs

## Keywords

`dividend_gaming`, `rolling_average`, `micro_trade_manipulation`, `fee_distribution`, `reserve_drainage`, `spartan`, `curated_pools`, `daily_allocation`

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

`addDividend`, `addLiquidity`, `addTradeFee`, `amm`, `averaging_attack`, `block.timestamp`, `calculateDividend`, `dividend`, `dividend_gaming`, `drainReserve`, `fee_manipulation`, `micro`, `receive`, `reserve_drainage`
