---
# Core Classification
protocol: generic
chain: everychain
category: risk_parameters
vulnerability_type: collateral_ratio_miscalculation

# Pattern Identity
root_cause_family: health_factor_computation_error
pattern_key: wrong_collateralization_math | risk_engine | borrow_or_withdraw | ltv_bypass_or_wrong_liquidation_threshold

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - RiskEngine / AccountHealth
  - LendingPool / Market (CDP)
  - Oracle / price feeds
  - Bank position manager (strategy validation)
path_keys:
  - wrong_collateralization_math | borrow() | Pool→oracle | precision_mixing_in_ratio
  - wrong_collateralization_math | _isSolvent() | Market→YieldBox | rate_applied_to_shares
  - wrong_collateralization_math | reducePosition() | Bank→strategyRegistry | unvalidated_strategy_id_bypasses_maxltv
  - wrong_collateralization_math | add_token() | AccountHealth→priceFeed | balance_decimals_ignored

# Attack Vector Details
attack_type: logical_error
affected_component: risk_engine

# Technical Primitives
primitives:
  - userCollateralRatioMantissa
  - collateralizationRate
  - LTV
  - liquidation threshold
  - token decimals normalization
  - shares vs amounts
  - strategyId validation
  - BasisPoints
  - price feed decimals

# Grep / Hunt-Card Seeds
code_keywords:
  - userCollateralRatioMantissa
  - _isSolvent
  - collateralizationRate
  - maxLTV
  - _validateMaxLTV
  - add_token
  - liquidationThreshold
  - toAmount
  - BasisPoints

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - lending
  - risk_parameters
  - ltv
  - health_factor
  - decimals
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [H1] | reports/lending_borrowing_findings/h-1-precision-differences-when-calculating-usercollateralratiomantissa-causes-ma.md | HIGH | Sherlock (Surge) | solodit 18611 / https://github.com/sherlock-audit/2023-02-surge-judging/issues/122 |
| [H2] | reports/lending_borrowing_findings/h-2-precision-differences-when-calculating-usercollateralratiomantissa-causes-ma.md | HIGH | Sherlock (Surge) | solodit 6702 (same root cause, supporting) |
| [H3] | reports/lending_borrowing_findings/account-health-calculations-ignore-token-decimals.md | HIGH | Cantina (Layer N) | solodit 53992 |
| [H4] | reports/lending_borrowing_findings/h-04-incorrect-solvency-check-because-it-multiplies-collateralizationrate-by-sha.md | HIGH | Code4rena (Tapioca DAO) | solodit 27494 |
| [H5] | reports/lending_borrowing_findings/h-22-lack-of-safety-buffer-between-liquidation-threshold-and-ltv-ratio-for-borro.md | HIGH | Code4rena (Tapioca DAO) | solodit 27512 |
| [H6] | reports/lending_borrowing_findings/h-5-users-can-get-around-maxltv-because-of-lack-of-strategyid-validation.md | HIGH | Sherlock (Blueberry) | solodit 6642 / https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/129 |
| [H7] | reports/lending_borrowing_findings/m-4-genericlogicsol-contract-assumes-all-price-feeds-has-the-same-decimals-but-i.md | MEDIUM | Sherlock (ZeroLend One) | solodit 41825 |
| [H8] | reports/lending_borrowing_findings/an-incorrect-collateral-value-with-decimals-18.md | MEDIUM | MixBytes (Threshold Network) | solodit 30192 |
| [H9] | reports/lending_borrowing_findings/h-02-doesnt-calculate-the-current-borrowing-amount-for-the-provider-including-th.md | HIGH | Code4rena (Lybra Finance) | solodit 21139 |

## Health Factor and Collateral Ratio Miscalculation

**The collateralization check that gates borrowing and triggers liquidation computes the ratio with mismatched token precisions, applies rates to shares instead of amounts, trusts user-supplied strategy ids, or collapses LTV and liquidation threshold into one value — so positions borrow past MaxLTV or get liquidated at max LTV.**

### Overview

Health factor / collateral-ratio math is the core safety invariant of every lending market. Nine unique findings (7 HIGH, 2 MEDIUM) from 4 audit firms across 8 protocols show the recurring computation errors: raw native-precision debt divided by raw native-precision collateral (Surge — USDC/SHIB pairs compute ratio 0, making positions unliquidatable), account health that rescales price decimals but ignores balance decimals (Layer N), collateralization rate multiplied by collateral *shares* instead of *amounts* (Tapioca), liquidation threshold identical to the LTV ceiling so max-LTV borrowers are instantly liquidatable and repeatedly re-liquidated (Tapioca BigBang/Singularity), MaxLTV validated against a user-chosen `strategyId` instead of the position's actual strategy (Blueberry), and price feeds assumed to share one decimal count (ZeroLend, Threshold).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the solvency/LTV check computes collateral-to-debt ratios with mismatched precisions, wrong units (shares vs amounts), unvalidated risk-parameter ids, or no buffer between LTV and liquidation threshold, letting positions borrow beyond MaxLTV or become instantly/repeatedly liquidatable."
- Pattern key: `wrong_collateralization_math | risk_engine | borrow_or_withdraw | ltv_bypass_or_wrong_liquidation_threshold`
- Interaction scope: `multi_contract`
- Primary affected component(s): `risk engine / solvency check / LTV validation`
- Contracts / modules involved: `Pool/Market._isSolvent, AccountHealth, Bank._validateMaxLTV, oracle feeds`
- Path keys: `precision_mixing_in_ratio`, `rate_applied_to_shares`, `unvalidated_strategy_id_bypasses_maxltv`, `balance_decimals_ignored`
- High-signal code keywords: `userCollateralRatioMantissa`, `_isSolvent`, `collateralizationRate`, `maxLTV`, `_validateMaxLTV`
- Severity: HIGH — 7/9 unique findings rated HIGH, 2 MEDIUM; dominant consensus HIGH
- Typical sink / impact: `over-borrowing past LTV limits, unliquidatable positions, unfair/instant liquidations, repeated liquidations`
- Validation strength: `strong` (9 unique findings, 4 independent audit firms — Sherlock, Code4rena, Cantina, MixBytes — across 8 protocols)

#### Contract / Boundary Map

- Entry surface(s): `borrow()`, `reducePosition()`, `withdraw()`, `_isSolvent()` (read by liquidation), `add_token()` (health accumulator)
- Contract hop(s): `Pool.borrow -> userCollateralRatioMantissa (native precisions)`; `Market._isSolvent -> YieldBox.toAmount(shares × rate)`; `IchiVaultSpell.reducePosition -> _validateMaxLTV(user strategyId) -> bank.oracle.getPrice`
- Trust boundary crossed: `oracle feed decimals vs token decimals vs mantissa scaling`, `user-supplied risk parameter id`, `share/amount conversion`
- Shared state or sync assumption: `LTV < liquidationThreshold with a safety buffer`; `ratio inputs must be unit-normalized before comparison`

#### Valid Bug Signals

- Signal 1: The ratio's numerator and denominator carry different decimal scales (token decimals, price feed decimals, mantissa exponents) with no normalization step.
- Signal 2: A rate/threshold constant is applied to a share value where the rest of the formula uses amounts (or vice versa).
- Signal 3: A risk-parameter lookup key (strategyId, poolId, market id) comes from user calldata and is never checked against the position's actual configuration.

#### False Positive Guards

- Not this bug when: values are normalized to a common 18-decimal internal unit before every ratio (Aave-style oracle unit accounting) — check the actual normalization, not comments.
- Not this bug when: liquidation threshold intentionally equals LTV by documented design (rare; judges accepted the Tapioca finding because repeated-liquidation churn harms borrowers).
- Safe if: strategy/market ids are derived from position storage, and thresholds are separate state variables strictly greater than LTV.
- Dust guard: sub-basis-point precision skew alone is LOW/QA; flag only when it flips a solvency decision for realistic positions (Surge's 1e6 vs 100,001e18 → ratio 0).

### Vulnerability Description

#### Root Cause

1. **Precision mixing** [H1][H2]: Surge `userCollateralRatioMantissa = debtValue (loan-token precision) / collateralBalance (collateral-token precision)`. For USDC (1e6) debt vs SHIB (100,001e18) collateral: `1e6 * 1e18 / 100,001e18 = 0` — pairs completely broken; some positions impossible to liquidate.
2. **Balance decimals ignored** [H3]: Layer N `AccountHealth::add_token` scales by `price.decimals - BasisPoints.decimals` but never by the token's own balance decimals — 9-decimal ETH counts ~1000x more toward health than 6-decimal USDC per unit.
3. **Rate applied to shares** [H4]: Tapioca `Market._isSolvent` computes `yieldBox.toAmount(collateralId, collateralShare * (EXCHANGE_RATE_PRECISION / FEE_PRECISION) * collateralizationRate, false)` — the rate must apply to the amount; converting a rate-scaled share produces wrong solvency results (confirmed by sponsor).
4. **No LTV/liquidation-threshold buffer** [H5]: BigBang/Singularity use the same `collateralizationRate` as both the max-borrow LTV and the liquidation start threshold — max-LTV borrowers are liquidatable on the smallest adverse move and remain undercollateralized after each partial liquidation.
5. **Unvalidated strategy id** [H6]: Blueberry `reducePosition` accepts any `strategyId` into `_validateMaxLTV(strategyId)`; users pass the most permissive strategy's id and exceed their real strategy's LTV.
6. **Feed-decimal assumption** [H7][H8]: ZeroLend `GenericLogic` assumes all feeds share decimals; Threshold computes incorrect collateral value for decimals != 18.
7. **Debt undercounted** [H9]: Lybra — provider borrowing power check omits the provider's borrowed shares + accrued interest, understating current debt.

#### Attack Scenario / Path Variants

**Path A: Precision mixing makes positions unliquidatable** [H1]
Path key: `wrong_collateralization_math | borrow() | Pool→oracle | precision_mixing_in_ratio`
Entry surface: `borrow()` with mismatched-decimal pair
Contracts touched: `Pool -> userCollateralRatioMantissa`
Boundary crossed: `token decimal normalization`
1. User supplies SHIB (18 dec) collateral, borrows USDC (6 dec).
2. Ratio computed on raw units: tiny debt units vs huge collateral units → mantissa collapses to 0 or wildly wrong scale.
3. Positions enter states where `liquidate` can never satisfy its ratio checks.
4. **Impact**: broken pairs; unliquidatable debt (compounds with bad debt).

**Path B: MaxLTV bypass via user-chosen strategy id** [H6]
Path key: `wrong_collateralization_math | reducePosition() | Bank→strategyRegistry | unvalidated_strategy_id_bypasses_maxltv`
Entry surface: `reducePosition(strategyId, amount)`
Contracts touched: `IchiVaultSpell -> _validateMaxLTV -> bank`
Boundary crossed: `risk parameter id from calldata`
1. User opens a position in a low-LTV strategy.
2. Calls `reducePosition` withdrawing underlying, passing the strategyId of the highest-LTV strategy.
3. `underlyingTokenValue * maxLTV(chosen strategy) > debtValue` passes although the real strategy's LTV is exceeded.
4. **Impact**: leverage far beyond protocol limits; undercollateralization on small moves.

**Path C: Instant + repeated liquidation at max LTV** [H5]
Path key: `wrong_collateralization_math | borrow() at max | Market._isSolvent | missing_threshold_buffer`
Entry surface: borrowing at the maximum allowed by `collateralizationRate`
Contracts touched: `Market._isSolvent` (shared constant for LTV and liquidation)
Boundary crossed: `risk parameter design`
1. Borrower takes the max loan: solvent exactly at `collateralizationRate`.
2. Smallest price move (or interest accrual) makes `_isSolvent` false → instantly liquidatable.
3. After the first partial liquidation the loan is still undercollateralized → liquidated again, churning penalties.
4. **Impact**: unfair liquidations; penalty bleed on borrowers.

**Path D: Health skewed by balance decimals** [H3]
Path key: `wrong_collateralization_math | add_token() | AccountHealth→priceFeed | balance_decimals_ignored`
Entry surface: deposits/withdrawals updating account health
Contracts touched: `AccountHealth -> price feed`
Boundary crossed: `price decimals vs token decimals rescaling`
1. Health value = `balance × weight × price.mantissa` rescaled only by price/BP decimals.
2. 9-decimal ETH balances dominate 6-decimal USDC per real dollar.
3. Withdrawals that should fail the health check pass (or vice versa).
4. **Impact**: undercollateralized withdrawals; insolvency.

#### Vulnerable Pattern Examples

**Example 1: Native-precision ratio (Surge)** [HIGH]
```solidity
// ❌ VULNERABLE: numerator and denominator keep native token decimals
function userCollateralRatioMantissa(address user) public view returns (uint256) {
    uint256 debtValue = loanToken.balanceOf(address(this)) ... ;   // USDC: 1e6 scale
    uint256 collateralBalance = collateralToken.balanceOf(user);   // SHIB: 1e18 scale
    return debtValue * 1e18 / collateralBalance; // @audit 1e6*1e18/100_001e18 = 0
}
// Fix: normalize both sides to 18 decimals before the ratio.
```

**Example 2: Rate applied to shares (Tapioca)** [HIGH]
```solidity
// ❌ VULNERABLE: collateralizationRate scales the SHARE, then converts
return yieldBox.toAmount(
    collateralId,
    collateralShare * (EXCHANGE_RATE_PRECISION / FEE_PRECISION) * collateralizationRate, // @audit rate on shares
    false
) >= (borrowPart * _totalBorrow.elastic * _exchangeRate) / _totalBorrow.base;
// Correct: convert share -> amount FIRST, then apply collateralizationRate to the amount.
```

**Example 3: User-chosen risk parameter id (Blueberry)** [HIGH]
```solidity
// ❌ VULNERABLE: strategyId is calldata, never checked against the position
function reducePosition(uint256 strategyId, uint256 amt) external {
    // ... withdraws underlying, raising LTV ...
    _validateMaxLTV(strategyId); // @audit attacker picks the most permissive strategy
}
function _validateMaxLTV(uint256 strategyId) internal view {
    uint256 maxLTV = strategies[strategyId].maxLTV; // any strategy allowed
    require(collValue * maxLTV > debtValue, "exceeds LTV");
}
```

**Example 4: Health ignores balance decimals (Layer N, Rust)** [HIGH]
```rust
// ❌ VULNERABLE: rescale uses price/BP decimals only; token balance decimals dropped
let mut token_account_value = balance            // token decimals ignored
    .mul(token_weight.value().into())
    .mul(index_price.mantissa().into());
let rescale_decimals = -(index_price.decimals().get() as i32) - BasisPoints::DECIMALS as i32;
// @audit 9-dec ETH vs 6-dec USDC get unequal per-dollar weight
```

**Example 5: One constant for LTV and liquidation threshold (Tapioca)** [HIGH]
```solidity
// ❌ VULNERABLE: max-borrow gate and liquidation gate read the same value
uint256 public collateralizationRate; // LTV ceiling AND liquidation threshold
function _isSolvent(address user, uint256 _exchangeRate) internal view returns (bool) {
    return /* collateral × collateralizationRate */ >= debt; // @audit max-LTV == instantly liquidatable
}
```

### Impact Analysis

#### Technical Impact

- Over-borrowing past MaxLTV / leverage limits (3/9 unique findings: H6, H9, and precision collapses)
- Unliquidatable positions from broken ratio math (2/9: H1, H2)
- Instant and repeated unfair liquidations at max LTV (1/9: H5)
- Wrong solvency outcomes from unit errors (3/9: H3, H4, H7, H8)

#### Business Impact

- Protocol undercollateralization on modest market moves once LTV limits are bypassed
- Borrower churn/penalty bleed when threshold == LTV
- Broken token pairs are unusable or dangerous (Surge fixed via 18-decimal normalization)

#### Affected Scenarios

- Markets listing tokens with divergent decimals (6 vs 18) or odd decimals (9)
- CDP designs sharing one rate constant between borrow gating and liquidation gating
- Position frameworks taking risk-config ids (strategyId) from user calldata
- Multi-oracle setups where feed decimals differ per asset

### Secure Implementation

**Fix 1: Normalize every ratio input to a common unit**
```solidity
// ✅ SECURE: 18-decimal normalization before comparison (Surge fix)
function userCollateralRatioMantissa(address user) public view returns (uint256) {
    uint256 debt = debtInNativePrecision * 10**(18 - debtToken.decimals());     // -> 1e18 scale
    uint256 coll = collInNativePrecision * 10**(18 - collToken.decimals());     // -> 1e18 scale
    return debt.mulDiv(1e18, coll); // price-adjust both sides where units differ
}
```

**Fix 2: Separate LTV and liquidation threshold with a buffer**
```solidity
// ✅ SECURE: two state variables, threshold strictly above LTV
uint256 public collateralizationRate;      // max-borrow LTV
uint256 public liquidationThreshold;       // liquidation start; require(liquidationThreshold > collateralizationRate)
// governance setter enforces the buffer:
function setRates(uint256 ltv, uint256 threshold) external onlyOwner {
    require(threshold > ltv + MIN_BUFFER, "no safety buffer");
}
```

**Fix 3: Derive risk ids from position storage**
```solidity
// ✅ SECURE: never accept the strategy id from calldata
function reducePosition(uint256 amt) external {
    uint256 strategyId = positions[bank.POSITION_ID()].strategyId; // from storage
    _validateMaxLTV(strategyId);
}
```

**Fix 4: Convert before applying rates (Tapioca fix)**
```solidity
// ✅ SECURE: amount first, rate second
uint256 collateralAmount = yieldBox.toAmount(collateralId, collateralShare, false);
return (collateralAmount * collateralizationRate) / EXCHANGE_RATE_PRECISION
    >= (borrowPart * _totalBorrow.elastic * _exchangeRate) / _totalBorrow.base;
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- ratio/division combining values whose decimals come from different tokens or feeds
- rate constants multiplied into share values before a toAmount/convertToAssets call
- risk parameter lookups keyed by calldata (strategyId, marketId, poolId)
- single storage constant feeding both max-borrow gate and liquidation gate
- rescale arithmetic that mentions price/BP decimals but never token decimals
```

#### High-Signal Grep Seeds
```
- userCollateralRatioMantissa
- _isSolvent
- collateralizationRate
- maxLTV
- _validateMaxLTV
- liquidationThreshold
- toAmount
- BasisPoints
- decimals()
```

#### Code Patterns to Look For
```
- Pattern 1: `A * 1e18 / B` where A and B carry `.decimals()` of different tokens
- Pattern 2: `toAmount(id, share * rate, ...)` — rate folded inside the conversion
- Pattern 3: `_validateMaxLTV(strategyId)` with `strategyId` in the external function signature
- Pattern 4: `collateralizationRate` appearing in both borrow validation and `_isSolvent`
- Pattern 5: `10 ** (price.decimals - X)` without a matching `balance` decimal term
```

#### Audit Checklist
- [ ] For every ratio: list the decimals of each operand and the normalization applied.
- [ ] Are rates/thresholds applied to amounts, never to shares, at every use site?
- [ ] Do LTV and liquidation threshold differ by an explicit, enforced buffer?
- [ ] Which risk-config ids come from user calldata, and what validates them against the position?
- [ ] Test extreme decimal pairs (6 vs 18, odd 9) with realistic amounts, not just 18/18.

### Real-World Examples

#### Known Exploits
- Precision-skew solvency errors are a recurring theme in lending incidents (see `DB/general/precision/precision-loss-rounding-vulnerabilities.md` for the general class).

#### Related CVEs/Reports
- Surge fix commit 294aa47 (18-decimal normalization) — [H1]
- Code4rena 2023-07-tapioca issue #1620 family (solvency math) — [H4]

### Prevention Guidelines

#### Development Best Practices
1. One canonical internal unit (1e18) for all value math; convert at the oracle/token boundary only.
2. Keep LTV, liquidation threshold, and close factor as separate governed parameters with enforced ordering `LTV < threshold <= close factor`.
3. Risk configuration for a position must be resolvable from position storage alone.
4. Property-test solvency: for random (decimals, prices, amounts), a position opened at max LTV must not be instantly liquidatable and must be liquidatable once truly underwater.

#### Testing Requirements
- Unit tests for: 6/18 decimal pairs; 9-decimal assets; strategyId taken from storage; threshold > LTV assertion on governance setters
- Integration tests for: borrow at max LTV then small adverse move (expect NO immediate liquidation eligibility)
- Fuzzing targets: `userCollateralRatioMantissa` over decimal/amount grids; monotonicity of health w.r.t. real dollar values

### References

#### Technical Documentation
- Aave V3 oracle unit handling (all assets priced in a common base unit)
- Compound V3 `liquidationFactor` vs `collateralFactor` separation

#### Security Research
- Sherlock 2023-02-surge issue #122 (12 finders — broadest consensus in this set)
- Cantina Layer N report (decimal-aware account health)

### Keywords for Search

`health factor`, `collateral ratio`, `LTV bypass`, `MaxLTV`, `liquidation threshold`, `collateralizationRate`, `userCollateralRatioMantissa`, `token decimals`, `precision mismatch`, `shares vs amounts`, `strategyId validation`, `_isSolvent`, `solvency check`, `unfair liquidation`, `repeated liquidation`, `over-borrowing`, `price feed decimals`, `risk parameters`

### Related Vulnerabilities

- [Bad Debt Socialization and Missing Write-Off](../bad-debt/bad-debt-socialization.md)
- [Oracle-Driven Liquidation Mispricing](../liquidation/oracle-driven-liquidation-mispricing.md)
- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- `DB/general/precision/precision-loss-rounding-vulnerabilities.md` (general precision class)
