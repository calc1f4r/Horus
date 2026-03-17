---
title: "Tick, Range, and Position Vulnerabilities in Concentrated Liquidity AMMs"
vulnerability_class: concentrated-liquidity-tick-range-position
category: amm/concentrated-liquidity
severity_range: "MEDIUM to HIGH"
consensus_severity: HIGH

affected_protocols:
  - "Uniswap V3/V4 and forks"
  - "PancakeSwap V3"
  - "Sushi Concentrated Liquidity"
  - "Sorella Angstrom/L2"
  - "Ramses V3"
  - "Superposition"
  - "Canto Ambient"
  - "Revert Lend"
  - "RealWagmi"
  - "Good Entry"
  - "Ajna Protocol"
  - "Particle Protocol"
  - "Maia DAO"
  - "Vii Finance"

pattern_frequency:
  total_reports_analyzed: 80
  patterns_identified: 14
  critical_patterns: 5

root_causes:
  - "Missing tick boundary validation (lower < upper)"
  - "Incorrect handling of underflow/overflow in fee growth calculations"
  - "Wrong inequality operators at tick boundaries"
  - "Tick alignment issues with tickSpacing"
  - "Position accounting mismatches between contracts"
  - "TWAP tick calculation rounding errors"
  - "Unbounded array growth in tick tracking"

audit_sources:
  - "Code4rena"
  - "Sherlock"
  - "Cyfrin"
  - "Cantina"
  - "ConsenSys Diligence"

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - allowance
  - block.timestamp
  - crossTicks
  - deposit
  - getFeeGrowthInside
  - getTwapTick
  - mintPosition
  - swap
---

## Overview

Concentrated liquidity AMMs introduced complex tick-based price ranges that enable capital-efficient liquidity provision but also create a new attack surface. This vulnerability class encompasses issues related to **tick validation**, **range boundary handling**, **position accounting**, and **fee growth calculations**.

**Root Cause Statement:**
> These vulnerabilities exist because concentrated liquidity protocols rely on precise tick arithmetic, underflow-dependent fee calculations, and careful boundary condition handling that developers frequently misimplement, allowing attackers to exploit tick boundary edge cases, manipulate fee growth accounting, or cause DoS.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | unknown | unknown`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `allowance`, `block.timestamp`, `crossTicks`, `deposit`, `getFeeGrowthInside`, `getTwapTick`, `mintPosition`, `swap`
- Typical sink / impact: `fund_loss`
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

## Vulnerable Pattern Examples

### Pattern 1: Missing Lower < Upper Tick Validation

**Severity:** HIGH | **Source:** Superposition (Code4rena)

```rust
// H-03: Missing lower/upper check in mint_position
pub fn mint_position(&mut self, lower: i32, upper: i32) -> Result<U256, Error> {
    // BUG: No validation that lower < upper
    self.positions.setter(id).set(Position { lower, upper });
}
```

**Impact:** "An attacker could open positions with arbitrary liquidity assigned to them. This allows fee theft from all existing positions."

**Reference:** [h-03-missing-lowerupper-check-in-mint_position.md](../../reports/constant_liquidity_amm/h-03-missing-lowerupper-check-in-mint_position.md)

---

### Pattern 2: Fee Growth Underflow Without unchecked{}

**Severity:** HIGH | **Sources:** Superposition (Code4rena), Particle Protocol, Maia DAO

Uniswap V3 fee growth calculations intentionally rely on underflow wrapping.

```rust
// H-06: get_fee_growth_inside should allow underflow but doesn't
fee_growth_global_0
    .checked_sub(fee_growth_below_0)  // BUG: Should use wrapping_sub
    .ok_or(Error::FeeGrowthSubTick)?  // Reverts on underflow!
```

**Correct:**
```solidity
unchecked {
    feeGrowthInside0 = feeGrowthGlobal0 - feeGrowthBelow0 - feeGrowthAbove0;
}
```

**References:**
- [h-06-get_fee_growth_inside-in-tickrs-should-allow-for-underflowoverflow-but-does.md](../../reports/constant_liquidity_amm/h-06-get_fee_growth_inside-in-tickrs-should-allow-for-underflowoverflow-but-does.md)
- [h-04-underflow-could-happened-when-calculating-uniswap-v3-positions-fee-growth-a.md](../../reports/constant_liquidity_amm/h-04-underflow-could-happened-when-calculating-uniswap-v3-positions-fee-growth-a.md)

---

### Pattern 3: Wrong Inequality at Tick Boundaries

**Severity:** HIGH | **Sources:** Sushi (Sherlock), Sorella Angstrom (Cyfrin)

```solidity
// H-08: Wrong inequality - uses < instead of <=
if (currentTick < lowerTick || currentTick >= upperTick) {
    // Position is out of range - WRONG!
}
```

**References:**
- [h-08-wrong-inequality-when-addingremoving-liquidity-in-current-price-range.md](../../reports/constant_liquidity_amm/h-08-wrong-inequality-when-addingremoving-liquidity-in-current-price-range.md)
- [all-rewards-can-be-stolen-due-to-incorrect-active-liquidity-calculations-when-th.md](../../reports/constant_liquidity_amm/all-rewards-can-be-stolen-due-to-incorrect-active-liquidity-calculations-when-th.md)

---

### Pattern 4: Tick Tracking Array DoS

**Severity:** HIGH | **Source:** Canto (Code4rena)

```solidity
// H-01: tickTracking_ array grows unbounded
tickTracking_[poolIdx][entryTick].push(tickTrackingData);  // Unbounded!

// Gas exhaustion when looped
while (tickTrackingIndex < numTickTracking) { tickTrackingIndex++; }
```

**Attack:** "Execute multiple small swaps bouncing price across tick boundary."

**Reference:** [h-01-array-length-of-ticktracking_-can-be-purposely-increased-to-brick-minting-a.md](../../reports/constant_liquidity_amm/h-01-array-length-of-ticktracking_-can-be-purposely-increased-to-brick-minting-a.md)

---

### Pattern 5: Tick Iteration Infinite Loop

**Severity:** HIGH | **Source:** OpenZeppelin (Cantina)

```solidity
// Infinite loop when currentTick not aligned with tickSpacing
int24 nextTick = currentTick - tickSpacing;  // Never hits initialized ticks
```

**Reference:** [infinite-loop-in-tick-iteration-due-to-misaligned-current-tick.md](../../reports/constant_liquidity_amm/infinite-loop-in-tick-iteration-due-to-misaligned-current-tick.md)

---

### Pattern 6: Negative TWAP Tick Rounding Error

**Severity:** HIGH | **Source:** Revert Lend (Code4rena)

```solidity
// H-05: Missing round-down for negative tick deltas
int24 tick = int24(tickCumulativesDelta / int56(uint56(twapSeconds)));
// BUG: Need to round down for negative

// Correct:
if (tickCumulativesDelta < 0 && (tickCumulativesDelta % period != 0)) tick--;
```

**Reference:** [h-05-_getreferencepoolpricex96-will-show-incorrect-price-for-negative-tick-delta.md](../../reports/constant_liquidity_amm/h-05-_getreferencepoolpricex96-will-show-incorrect-price-for-negative-tick-delta.md)

---

### Pattern 7: Position Debt Calculation Sign Error

**Severity:** HIGH | **Source:** Ramses V3 (ConsenSys)

```solidity
// Debt should be SUBTRACTED but is ADDED
periodSecondsInsideX96 + uint256(secondsDebtX96);  // BUG: Should be -
```

**Reference:** [debt-is-added-instead-of-subtracted-in-positionperiodsecondsinrange-fixed.md](../../reports/constant_liquidity_amm/debt-is-added-instead-of-subtracted-in-positionperiodsecondsinrange-fixed.md)

---

### Pattern 8: Position State Desync Between Contracts

**Severity:** HIGH | **Sources:** Ajna (Code4rena), Vii Finance (Cyfrin)

```solidity
// PositionManager uses full balance
positionState[tokenId].lps += lpBalance;  // Uses FULL balance

// Pool uses minimum of allowance and balance
lenderInfo[from] -= Maths.min(allowance, balance);  // Only decreases by ALLOWANCE
```

**Reference:** [h-07-user-can-exponentially-increase-the-value-of-their-position-through-the-mem.md](../../reports/constant_liquidity_amm/h-07-user-can-exponentially-increase-the-value-of-their-position-through-the-mem.md)

---

### Pattern 9: Hardcoded Fee Tier

**Severity:** HIGH | **Source:** RealWagmi (Sherlock)

```solidity
// BUG: Assumes all pools use 500 fee tier
IUniswapV3Pool(underlyingTrustedPools[500].poolAddress);
```

**Reference:** [h-1-wrong-calculation-of-tickcumulatives-due-to-hardcoded-pool-fees.md](../../reports/constant_liquidity_amm/h-1-wrong-calculation-of-tickcumulatives-due-to-hardcoded-pool-fees.md)

---

### Pattern 10: Price Movement During Range Operations

**Severity:** HIGH | **Source:** Good Entry (Code4rena)

```solidity
// Fee calculation breaks when price moves outside range
if (token1Amount + fee1 > 0) newFee1 = n1 * fee1 / (token1Amount + fee1);
// When token1Amount = 0, newFee1 = n1 (100% fee!)
```

**Reference:** [h-01-when-price-is-within-positions-range-deposit-at-tokenisablerange-can-cause-.md](../../reports/constant_liquidity_amm/h-01-when-price-is-within-positions-range-deposit-at-tokenisablerange-can-cause-.md)

---

## Secure Implementation Patterns

### Secure Pattern 1: Proper Tick Validation

```solidity
function mintPosition(int24 tickLower, int24 tickUpper, uint128 amount) external {
    require(tickLower < tickUpper, "tickLower >= tickUpper");
    require(tickLower % tickSpacing == 0, "tickLower not aligned");
    require(tickUpper % tickSpacing == 0, "tickUpper not aligned");
    require(tickLower >= TickMath.MIN_TICK, "tickLower too low");
    require(tickUpper <= TickMath.MAX_TICK, "tickUpper too high");
}
```

### Secure Pattern 2: Fee Growth with unchecked{}

```solidity
function getFeeGrowthInside() internal view returns (uint256, uint256) {
    unchecked {
        feeGrowthInside0X128 = feeGrowthGlobal0X128 - feeGrowthBelow0X128 - feeGrowthAbove0X128;
        feeGrowthInside1X128 = feeGrowthGlobal1X128 - feeGrowthBelow1X128 - feeGrowthAbove1X128;
    }
}
```

### Secure Pattern 3: Correct TWAP Tick Calculation

```solidity
function getTwapTick(uint32 twapDuration) internal view returns (int24) {
    int24 tick = int24(tickCumulativesDelta / int56(int32(twapDuration)));
    if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(int32(twapDuration)) != 0)) {
        tick--;  // Round down for negative ticks
    }
    return tick;
}
```

### Secure Pattern 4: Bounded Tick Tracking

```solidity
uint256 constant MAX_TICK_TRACKING_ENTRIES = 1000;

function crossTicks(bytes32 poolIdx, int24 entryTick) internal {
    require(tickTracking_[poolIdx][entryTick].length < MAX_TICK_TRACKING_ENTRIES, "Limit reached");
    tickTracking_[poolIdx][entryTick].push(TickTracking(uint32(block.timestamp), 0));
}
```

---

## Impact Analysis

| Impact Category | Severity | Frequency | Description |
|----------------|----------|-----------|-------------|
| Fee Theft | HIGH | Common | Incorrect fee growth allows stealing from LPs |
| DoS | HIGH | Common | Unbounded loops/arrays block operations |
| Incorrect Rewards | MEDIUM-HIGH | Common | Reward calculations off due to math errors |
| Position Corruption | HIGH | Moderate | State desync allows position inflation |
| Price Manipulation | MEDIUM | Moderate | TWAP/tick errors enable arbitrage |

---

## Detection Checklist

- [ ] `tickLower < tickUpper` validated in all position minting
- [ ] All tick arithmetic aligned with tickSpacing
- [ ] Fee growth calculations use `unchecked{}` for underflow
- [ ] TWAP tick calculations round down for negative deltas
- [ ] Tick tracking arrays have maximum size bounds
- [ ] Cross-contract position state synchronized
- [ ] Tick boundary conditions use correct inequalities
- [ ] Price movement during execution handled

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Superposition | Missing lower/upper check | HIGH | Code4rena | 2024 |
| Superposition | Fee growth needs unchecked | HIGH | Code4rena | 2024 |
| Sushi | Wrong inequality at boundary | HIGH | Sherlock | 2023 |
| Canto | Tick tracking DoS | HIGH | Code4rena | 2023 |
| Revert Lend | Negative TWAP tick rounding | HIGH | Code4rena | 2024 |
| Ramses V3 | Debt sign error | HIGH | ConsenSys | 2024 |
| Sorella Angstrom | Boundary liquidity calc | HIGH | Cyfrin | 2025 |
| RealWagmi | Hardcoded fee tier | HIGH | Sherlock | 2023 |
| Good Entry | Price movement during deposit | HIGH | Code4rena | 2023 |
| Ajna | Position state desync | HIGH | Code4rena | 2023 |

---

## Related Vulnerabilities

- [Slippage and Sandwich Attacks](./slippage-sandwich-frontrun.md)
- [Oracle Price Manipulation](../oracle/)

---

## Keywords

**Primary:** tick validation, tickLower, tickUpper, tick boundary, tick spacing, fee growth, position range, concentrated liquidity, CLMM, tick math

**Technical:** feeGrowthInside, feeGrowthOutside, crossTick, tickBitmap, getSqrtRatioAtTick, secondsPerLiquidity

**Vulnerability:** tick underflow, tick overflow, boundary condition, range boundary, tick iteration, position accounting

**Protocols:** uniswap_v3, uniswap_v4, pancakeswap_v3, sushi_clmm, ramses_v3, superposition, canto_ambient

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

`allowance`, `amm/concentrated-liquidity`, `block.timestamp`, `crossTicks`, `deposit`, `getFeeGrowthInside`, `getTwapTick`, `mintPosition`, `swap`
