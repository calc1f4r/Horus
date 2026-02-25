---
# Core Classification
protocol: generic
chain: everychain
category: arithmetic
vulnerability_type: bonding_curve_math_error

# Attack Vector Details
attack_type: logical_error
affected_component: bonding_curve, pricing_formula, invariant_calculation, AMM_math

# Technical Primitives
primitives:
  - bonding_curve
  - spot_price
  - constant_product
  - invariant
  - reserve_ratio
  - delta
  - utilization_rate
  - binary_search
  - geometric_mean
  - time_decay

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - bonding_curve
  - math_error
  - formula_bug
  - pricing
  - AMM
  - invariant
  - defi
  - arbitrage
  - curve_supply
  - spot_price

# Version Info
language: solidity
version: ">=0.6.0"
---

## References
- [Report-01]: reports/bonding_curve_findings/binary-search-implementation-may-not-always-find-the-optimal-solution.md
- [Report-02]: reports/bonding_curve_findings/calculatespotprice-should-not-use-_normalizedtimeremaining.md
- [Report-03]: reports/bonding_curve_findings/incorrect-calculation-for-linear-curves.md
- [Report-04]: reports/bonding_curve_findings/h-01-the-bonding-curve-implementation-can-not-be-fully-changed.md
- [Report-05]: reports/bonding_curve_findings/h-01-gas-issuance-is-inflated-and-will-halt-the-chain-or-lead-to-incorrect-base-.md
- [Report-06]: reports/bonding_curve_findings/h-1-bonding-curve-logic-can-be-exploited-to-pay-less-for-buying-votes.md
- [Report-07]: reports/bonding_curve_findings/h-1-the-sign-of-delta-hedge-amount-can-be-reversed-by-malicious-user-due-to-inco.md
- [Report-08]: reports/bonding_curve_findings/h-2-utilization-rate-for-bonding-curve-purposes-is-calculated-for-a-total-of-bul.md
- [Report-09]: reports/bonding_curve_findings/h-3-lp-tokens-always-valued-at-3-pts.md
- [Report-10]: reports/bonding_curve_findings/m-01-bonding-curve-check-stepsize-numsteps-may-not-match-curvesupply.md
- [Report-11]: reports/bonding_curve_findings/m-02-in-stable2lut1getratiosfrompriceliquidity-in-extreme-cases-updatereserve-wi.md
- [Report-12]: reports/bonding_curve_findings/m-10-xyk-reflect_curve-is-incorrect-and-decreases-k-over-time-leading-to-loss-of.md
- [Report-13]: reports/bonding_curve_findings/m-2-incorrect-implementation-of-bpf-leads-to-kicker-losing-rewards-in-a-take-act.md
- [Report-14]: reports/bonding_curve_findings/bancor-formula-should-not-be-updated-during-the-batch-fixed.md
- [Report-15]: reports/bonding_curve_findings/error-codes-of-quote-functions-are-unchecked.md
- [Report-16]: reports/bonding_curve_findings/gdacurve-does-not-validate-new-spot-price.md
- [Report-17]: reports/bonding_curve_findings/h-01-value-can-be-extracted-from-the-pool-by-combining-the-burning-of-btoken-and.md
- [Report-18]: reports/bonding_curve_findings/m-02-bonding-curve-invariant-check-incorrectly-validates-sol-balance-due-to-rent.md
- [Report-19]: reports/bonding_curve_findings/h-3-asymmetric-liquidity-provision-to-geometric-pool-can-allow-attacker-to-purch.md
- [Report-20]: reports/bonding_curve_findings/m-6-incorrect-liquidation-mechanics-either-causes-revert-on-liquidation-due-to-i.md
- [Report-21]: reports/bonding_curve_findings/h-9-uniswap-v3-pool-token-balance-proportion-does-not-necessarily-correspond-to-.md

## Vulnerability Title

**Bonding Curve Math and Formula Errors Leading to Incorrect Pricing, Invariant Violations, and Fund Loss**

### Overview

Bonding curves, AMM pricing formulas, and related mathematical implementations are systematically vulnerable to logic errors, incorrect formula transcription, wrong parameter usage, missing edge case handling, and invariant violations. These bugs enable attackers to buy/sell at incorrect prices, drain protocol reserves, manipulate utilization metrics, or cause permanent protocol dysfunction.

### Vulnerability Description

#### Root Cause

The fundamental issues across all 21 findings fall into these categories:

1. **Incorrect formula transcription** — Mathematical formulas from whitepapers/specs implemented with wrong operators, missing terms, or wrong parameter references (Reports 2, 3, 6, 7, 12, 13)
2. **Static vs dynamic valuation** — Using hardcoded constants instead of dynamic on-chain values for pricing (Reports 4, 9, 11)
3. **Non-monotonic assumption violations** — Binary search or optimization algorithms assuming monotonicity when user inputs or curve shapes break this (Reports 1, 16)
4. **Combined metric manipulation** — Aggregate utilization or pricing metrics that can be cheaply manipulated via one side to affect the other (Reports 8, 17)
5. **Invariant check bypasses** — Validation checks that don't account for rent, fees, or precision differences (Reports 5, 18, 20)
6. **Unchecked error codes** — Quote functions returning error codes that callers silently discard (Report 15)
7. **Mid-operation formula changes** — Governance updating pricing formulas during active batches/operations (Report 14)
8. **Geometric/asymmetric pool bypass** — Asymmetric liquidity operations bypassing the intended price impact of curve designs (Report 19)

---

### Vulnerable Pattern Examples

---

#### **Pattern 1: Binary Search Assumes Monotonic Cost Function** [MEDIUM]
**Protocol**: Sudoswap | **Auditor**: Cyfrin | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Binary search assumes cost criteria is monotonic
// User-supplied maxCostPerNumNFTs arrays can break this assumption
function _findMaxFillableAmtForBuy(
    ICurve curve,
    ICurve.Params calldata params,
    uint256 numNFTs,
    uint256[] calldata maxCostPerNumNFTs
) internal view returns (uint256) {
    // Binary search converges on wrong answer when cost function
    // is non-monotonic (volume discounts, GDA error codes, etc.)
    uint256 lo = 1;
    uint256 hi = numNFTs;
    while (lo < hi) {
        uint256 mid = (lo + hi + 1) / 2;
        (,,, uint256 cost,,) = curve.getBuyInfo(params, mid, 0);
        if (cost <= maxCostPerNumNFTs[mid - 1]) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
}
```

**Root Cause**: The binary search in `VeryFastRouter::_findMaxFillableAmtForBuy` and `_findMaxFillableAmtForSell` assumes the cost/output criteria function is monotonic. This breaks with non-monotonic user-supplied `maxCostPerNumNFTs` arrays (e.g., volume discounts) or GDA curves that return error codes for overflow that create non-monotonic return patterns.

**Impact**: Users may trade fewer NFTs than their budget allows, missing optimal fill amounts. Pool quoted price may be wrong.

**Recommended Fix**: Use linear scan fallback when binary search result is suboptimal; validate monotonicity of input arrays.

---

#### **Pattern 2: Wrong Parameter in Spot Price Calculation** [MEDIUM]
**Protocol**: Hyperdrive (Delv) | **Auditor**: Spearbit | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Uses _normalizedTimeRemaining instead of correct formula
// WRONG: dz/dy = z / (y * tr * ts)
// CORRECT: dx/dy = c * (mu * z / y) ** ts
function calculateSpotPrice(
    uint256 _shareReserves,
    uint256 _bondReserves,
    uint256 _initialSharePrice,
    uint256 _normalizedTimeRemaining,
    uint256 _timeStretch
) internal pure returns (uint256 spotPrice) {
    // Missing: _initialSharePrice (c factor)
    // Using: _normalizedTimeRemaining where only _timeStretch should appear
    uint256 base = _shareReserves.divDown(_bondReserves);
    spotPrice = base.mulDown(_normalizedTimeRemaining).mulDown(_timeStretch);
}
```

**Root Cause**: The spot price formula in `HyperdriveMath.sol` uses `_normalizedTimeRemaining` (tr) in the calculation, but the correct YieldSpace curve definition only uses `_timeStretch` (ts). The initial share price factor (c) is also missing. This affects oracles, LP fees, and governance fee calculations.

**Recommended Fix**: `spotPrice = _initialSharePrice * (_shareReserves / _bondReserves) ** _timeStretch`

---

#### **Pattern 3: Wrong Operator in Linear Curve Buy Price** [HIGH]
**Protocol**: Stargaze Infinity | **Auditor**: OtterSec | **Severity**: High

```rust
// ❌ VULNERABLE: Pool buys NFTs at inflated price (spot + delta instead of spot)
PoolType::Trade => match self.bonding_curve {
    BondingCurve::Linear => self.spot_price
        .checked_add(self.delta)  // BUG: should not add delta for buy price
        .map_err(|e| ContractError::Std(StdError::overflow(e))),
    BondingCurve::Exponential => self.spot_price
        .checked_multiply_ratio(self.delta, 100u128)
        .map_err(|e| ContractError::Std(StdError::overflow(e))),
},
```

**Root Cause**: In `get_buy_quote` for Trade pools with Linear bonding curves, the buy price adds delta to spot price (`spot_price + delta`) instead of using just `spot_price`. The pool overpays when buying NFTs, violating the invariant that buy-then-sell shouldn't cause loss.

**Impact**: Pool loses funds on every buy operation. Users can arbitrage by selling NFTs to the pool at the inflated buy price and buying them back at the correct sell price.

**Recommended Fix**: Remove the delta addition in the linear curve buy price calculation for Trade pools.

---

#### **Pattern 4: Hardcoded getOutputPrice Not Updated with Bonding Curve** [HIGH]
**Protocol**: MoarCandy | **Auditor**: Pashov Audit Group | **Severity**: High

```solidity
// ❌ VULNERABLE: getOutputPrice is hardcoded, not part of replaceable AMMFormula
contract ContinuosBondingERC20Token {
    // This function is NOT delegated to AMMFormula contract
    function getOutputPrice(
        uint256 outputAmount,
        uint256 inputReserve,
        uint256 outputReserve
    ) public pure returns (uint256) {
        require(inputReserve > 0 && outputReserve > 0);
        uint256 numerator = inputReserve * outputAmount;
        uint256 denominator = (outputReserve - outputAmount);
        return numerator / denominator + 1;
    }
}

// Admin updates bonding curve but getOutputPrice stays the same:
function updateBondingCurve(address _newFormula) external onlyOwner {
    ammFormula = AMMFormula(_newFormula); // Only updates getInputPrice
}
```

**Root Cause**: `updateBondingCurve` only updates the `AMMFormula` contract used for `getInputPrice`. The `getOutputPrice` function is hardcoded directly in the token contract and never changes, creating pricing inconsistency at the curve's upper range.

**Recommended Fix**: Move `getOutputPrice` into the `AMMFormula` contract so both functions are updated together.

---

#### **Pattern 5: Cumulative Gas Issuance Instead of Incremental** [HIGH]
**Protocol**: Taiko | **Auditor**: Code4rena | **Severity**: High

```solidity
// ❌ VULNERABLE: Issuance is cumulative from lastSyncedBlock, not per-block incremental
uint256 numL1Blocks;
if (lastSyncedBlock > 0 && _l1BlockId > lastSyncedBlock) {
    numL1Blocks = _l1BlockId - lastSyncedBlock; // Grows each block!
}
if (numL1Blocks > 0) {
    uint256 issuance = numL1Blocks * _config.gasTargetPerL1Block;
    excess = excess > issuance ? excess - issuance : 1;
}
// lastSyncedBlock only updated every BLOCK_SYNC_THRESHOLD (5) blocks
// Result: blocks issue 1+2+3+4+5 = 15x target instead of 5x
```

**Root Cause**: `TaikoL2._calc1559BaseFee` calculates gas issuance as `numL1Blocks * gasTargetPerL1Block` where `numL1Blocks` grows each block since `lastSyncedBlock` is only updated every 5 blocks. This leads to 3x gas issuance inflation, potentially halting the chain.

**Impact**: Chain halt if `block.basefee` uses correct math but contract uses inflated; or severely incorrect base fee if both use same flawed logic.

**Recommended Fix**: Issue exactly `gasTargetPerL1Block` per block by tracking the last processed L1 block.

---

#### **Pattern 6: Vote Price Manipulation via Alternating Buy/Sell** [HIGH]
**Protocol**: Ethos Network | **Auditor**: Sherlock | **Severity**: High

```solidity
// ❌ VULNERABLE: Price depends on ratio which can be manipulated
function _calcVotePrice(Market memory market, bool isPositive) private pure returns (uint256) {
    uint256 totalVotes = market.votes[TRUST] + market.votes[DISTRUST];
    return (market.votes[isPositive ? TRUST : DISTRUST] * market.basePrice) / totalVotes;
}
// Alternating trust/distrust purchases keeps ratio near 1:1
// Each trust vote costs ~basePrice/2 instead of increasing price
```

**Root Cause**: The vote price formula `price = (votes_side * basePrice) / totalVotes` allows manipulation by alternating trust and distrust vote purchases to keep the ratio near 1:1, buying votes at approximately half price. Selling distrust votes at the end yields a net discount of ~20-28%.

**Impact**: Attacker buys votes at 20-28% discount. In skewed markets the discount is even larger.

**Recommended Fix**: Add time delay between consecutive buy/sell votes from the same address; or use a different pricing formula that doesn't depend on the ratio of opposing votes.

---

#### **Pattern 7: Absolute Value Check Reverses Hedge Direction** [HIGH]
**Protocol**: Smilee Finance | **Auditor**: Sherlock | **Severity**: High

```solidity
// ❌ VULNERABLE: abs() comparison ignores sign; always sets positive value
if (SignedMath.abs(tokensToSwap) > params.sideTokensAmount) {
    if (SignedMath.abs(tokensToSwap) - params.sideTokensAmount 
        < params.sideTokensAmount / 10000) {
        // BUG: always sets positive regardless of original sign
        tokensToSwap = SignedMath.revabs(params.sideTokensAmount, true);
    }
}
// When tokensToSwap is negative (buy side tokens), sign is reversed to positive (sell)
// Vault hedges in wrong direction — attacker can drain all funds
```

**Root Cause**: `FinanceIGDelta.deltaHedgeAmount` uses `SignedMath.abs()` to compare but always sets a positive value when clamping. If `tokensToSwap` is negative (meaning vault should buy side tokens), the sign reversal causes it to sell instead, enabling vault drainage through repeated manipulation.

**Impact**: Complete vault drainage through repeated cycles of forced wrong-direction hedging.

**Recommended Fix**: Only apply the clamping logic when `tokensToSwap > 0`; preserve original sign in all safety checks.

---

#### **Pattern 8: Combined Bull/Bear Utilization Enables Premium Manipulation** [HIGH]
**Protocol**: Smilee Finance | **Auditor**: Sherlock | **Severity**: High

```solidity
// ❌ VULNERABLE: Single utilization rate for both bull and bear
// Cheap option inflates volatility for expensive option
// getUtilizationRate uses total (bear+bull) used vs initial liquidity
// Premium = f(volatility) = f(utilizationRate)
// Attacker: buy expensive option → cheaply inflate utilization → sell expensive → sell cheap
```

**Root Cause**: Volatility (and thus option premium) is computed from a single utilization rate combining both bull and bear positions. When price is away from strike, one side is much cheaper. Attacker buys the expensive option, pushes total utilization to 75% via the cheap option, then sells the expensive option at inflated premium — profiting ~0.07% of vault per iteration.

**Impact**: Vault drainage at ~0.07% per cycle; ~1500 iterations to drain completely.

**Recommended Fix**: Calculate utilization rate separately for bull and bear positions; or implement vega-weighted utilization.

---

#### **Pattern 9: Static LP Token Valuation Ignores Fee Accrual** [HIGH]
**Protocol**: Napier | **Auditor**: Sherlock | **Severity**: High

```solidity
// ❌ VULNERABLE: LP tokens always valued at N_COINS * 1 PT regardless of actual value
int256 internal constant N_COINS = 3;

// In swap functions — always uses 3x multiplier:
exactBaseLptIn.neg() * N_COINS    // Should use get_virtual_price()
exactBaseLptOut.toInt256() * N_COINS
totalBaseLptTimesN: baseLptUsed * N_COINS,
```

**Root Cause**: The Napier AMM uses `N_COINS = 3` as a static multiplier to convert Curve Base LP Tokens to PT-equivalent amounts. While initially correct (1:1:1:1 deposits), Curve LP tokens appreciate over time via fee accrual. The pool permanently undervalues LP tokens.

**Impact**: LPs shortchanged on deposits; arbitrageurs extract the difference between pool valuation (3 PTs) and actual Curve virtual price (>3 PTs).

**Recommended Fix**: Use `Curve.get_virtual_price()` to dynamically value LP tokens instead of static `N_COINS`.

---

#### **Pattern 10: Bonding Curve Supply Mismatch (stepSize × numSteps ≠ curveSupply)** [MEDIUM]
**Protocol**: Wild Protocol | **Auditor**: Kann | **Severity**: Medium

**Root Cause**: No validation ensures `stepSize * numSteps == curveSupply` during token launch. If `stepSize * numSteps > curveSupply`, the curve promises more tokens than exist. If less, part of the supply is unreachable via the bonding curve.

**Impact**: Over-allocation risks using LP pool tokens; under-allocation permanently locks tokens.

**Recommended Fix**: Add validation `require(stepSize * numSteps == curveSupply)` during token launch configuration.

---

#### **Pattern 11: Extreme Price Range Causes Underflow in Lookup Table** [MEDIUM]
**Protocol**: Basin (Beanstalk) | **Auditor**: Code4rena | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Extreme gap between highPrice and lowPrice in LUT causes underflow
PriceData(
    0.27702e6,   // highPrice
    0,
    9.646e18,
    0.001083e6,  // lowPrice — 250x gap from highPrice
    0,
    2000e18,     // lowPriceJ — massive step size causes overflow
    1e18
);
// When targetPrice near lowPrice: updateReserve attempts 2000e18 corrections → underflow
// Newton's method fails to converge within 255 iterations
```

**Root Cause**: `Stable2LUT1::getRatiosFromPriceLiquidity` has extreme price ranges where `lowPriceJ` step sizes are enormous. At extreme lower bounds, correction attempts underflow or Newton's method doesn't converge, bricking the function.

**Recommended Fix**: Reduce step sizes and narrow estimated price ranges in lookup table entries.

---

#### **Pattern 12: XYK Reflect Curve Uses Initial Reserves Instead of K-Invariant** [MEDIUM]
**Protocol**: Dango DEX | **Auditor**: Sherlock | **Severity**: Medium

```rust
// ❌ VULNERABLE: Uses initial quote_reserve (Q0) instead of sqrt(K/P)
let quote_reserve_div_price = quote_reserve.checked_div_dec(price).ok()?;
let mut size = quote_reserve_div_price.checked_sub(base_reserve).ok()?;
// CORRECT: size = sqrt(K / price) - base_reserve
// where K = base_reserve * quote_reserve (constant product)
```

**Root Cause**: The XYK `reflect_curve` uses the initial `quote_reserve` value when computing passive order sizes instead of deriving from the K-invariant (`sqrt(K/P)`). This causes the pool to overpay on fills, decreasing K over time and continuously draining LP value.

**Impact**: K decreases after every passive order fill; LP providers lose funds continuously.

**Recommended Fix**: Replace `Q₀/P` with `sqrt(K/P)` for bids and `sqrt(K*P)` for asks.

---

#### **Pattern 13: BPF Returns Zero at Neutral Price Boundary** [MEDIUM]
**Protocol**: Ajna | **Auditor**: Sherlock | **Severity**: Medium

```solidity
// ❌ VULNERABLE: val == 0 case leaves sign as 0, setting BPF to 0
int256 val = int256(neutralPrice_) - int256(auctionPrice_);
if (val < 0)       sign = -1e18;
else if (val != 0) sign = 1e18;
// BUG: when val == 0 (auctionPrice == neutralPrice), sign = 0
// Per whitepaper: BPF should equal bondFactor when price <= NP
```

**Root Cause**: The Bond Payment Factor implementation diverges from spec at the exact boundary where `auctionPrice == neutralPrice`. The `else if (val != 0)` condition leaves `sign = 0`, zeroing the BPF. Kicker loses all rewards for takes at the 18-hour auction mark.

**Recommended Fix**: Change `else if (val != 0) sign = 1e18` to `else sign = 1e18`.

---

#### **Pattern 14: Mid-Batch Formula Update Makes Prices Unpredictable** [HIGH]
**Protocol**: AragonBlack Fundraising | **Auditor**: ConsenSys | **Severity**: High

```solidity
// ❌ VULNERABLE: Formula can be changed mid-batch
function updateFormula(IBancorFormula _formula) external auth(UPDATE_FORMULA_ROLE) {
    require(isContract(_formula), ERROR_CONTRACT_IS_EOA);
    _updateFormula(_formula); // Immediate effect — pending batch orders affected
}
```

**Root Cause**: `updateFormula()` takes effect immediately. If called during an active batch, pending orders priced under the old formula execute under the new one, producing unpredictable prices.

**Recommended Fix**: Store formula reference per meta-batch; apply updates starting from the next batch; or use a timelock > batch duration.

---

#### **Pattern 15: Unchecked Error Codes from Quote Functions** [MEDIUM]
**Protocol**: Sudoswap | **Auditor**: Spearbit | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Error code silently discarded in Router
(, , pairOutput, ) = swapList[i].pair.getSellNFTQuote(...);
(, , pairCost, ) = swapList[i].pair.getBuyNFTQuote(...);

// ✅ SECURE: Properly checked in Pair
(error, ...) = _bondingCurve.getBuyInfo(...);
require(error == CurveErrorCodes.Error.OK, "Bonding curve error");
```

**Root Cause**: `LSSVMRouter.sol` discards error return values from `getBuyNFTQuote()` and `getSellNFTQuote()`. Future curve implementations with new error codes would go unhandled, potentially executing swaps with garbage pricing data.

**Recommended Fix**: Check error codes in Router; revert for normal swaps, skip during robust operations.

---

#### **Pattern 16: GDA Spot Price Decays Below MIN_PRICE** [MEDIUM]
**Protocol**: Sudoswap | **Auditor**: Cyfrin | **Severity**: Medium

```solidity
// ❌ VULNERABLE: No MIN_PRICE validation in getBuyInfo/getSellInfo
{
    UD60x18 newSpotPrice_ = spotPrice_.mul(alphaPowN).div(decayFactor);
    if (newSpotPrice_.gt(ud(type(uint128).max))) {
        return (Error.SPOT_PRICE_OVERFLOW, 0, 0, 0, 0, 0);
    }
    // MISSING: if (newSpotPrice_ < MIN_PRICE) return Error
    newSpotPrice = uint128(unwrap(newSpotPrice_));
}
// validateSpotPrice HAS MIN_PRICE check but it's not called here
```

**Root Cause**: GDA spot price can decay below `MIN_PRICE` (1 gwei) with high lambda and low demand. While `validateSpotPrice()` checks `MIN_PRICE`, `getBuyInfo`/`getSellInfo` skip this validation.

**Impact**: Pool continues market-making at near-zero prices indefinitely; NFTs sold for negligible amounts.

**Recommended Fix**: Add `MIN_PRICE` validation in `getBuyInfo` and `getSellInfo`.

---

#### **Pattern 17: External Token Burn Manipulates Constant-Product Reserves** [HIGH]
**Protocol**: PossumLabs V2 | **Auditor**: Shieldify | **Severity**: High

```solidity
// ❌ VULNERABLE: Reserve includes burnable tokens in balance
function quoteBuyPortalEnergy(uint256 _amountInputPSM) public view returns (uint256) {
    uint256 reserve0 = IERC20(PSM_ADDRESS).balanceOf(VIRTUAL_LP);
    // reserve0 includes bToken reward pool — burning bToken changes it
    uint256 reserve1 = CONSTANT_PRODUCT / reserve0;
    amountReceived = (_amountInputPSM * reserve1) / (_amountInputPSM + reserve0);
}
```

**Root Cause**: Portal energy price derives from PSM token balance of VirtualLP via constant-product formula. Burning `bToken` removes PSM tokens from the contract, reducing reserve0 and shifting the price curve. Sell before burn, buy after = profit.

**Impact**: ~139% profit on portal energy per cycle in example scenario.

**Recommended Fix**: Subtract `fundingRewardPool` from PSM balance when calculating swap prices.

---

#### **Pattern 18: Solana Rent Inflates Invariant Check** [MEDIUM]
**Protocol**: Pump Science | **Auditor**: Code4rena | **Severity**: Medium

```rust
// ❌ VULNERABLE: lamports() includes rent-exemption
let sol_escrow_lamports = sol_escrow.lamports(); // Includes rent!
if sol_escrow_lamports < bonding_curve.real_sol_reserves {
    return Err(ContractError::BondingCurveInvariant.into());
}
// rent amount makes check pass when actual reserves are insufficient
```

**Root Cause**: Solana account `lamports()` includes rent-exemption balance. The invariant check compares total lamports against `real_sol_reserves` (which excludes rent), making the check always pass even with slightly insufficient reserves.

**Recommended Fix**: Subtract rent-exemption amount from lamports before comparing.

---

#### **Pattern 19: Asymmetric Deposit Bypasses Geometric Pool Price Bands** [HIGH]
**Protocol**: Dango DEX | **Auditor**: Sherlock | **Severity**: High

```rust
// ❌ VULNERABLE: Geometric pool prices independent of pool balances
// Asymmetric add_liquidity performs virtual swap at flat oracle price
let marginal_price = base_price.checked_div(quote_price)?;
// Bids/asks sized from remaining inventory with fixed geometric ratio
// NOT from actual pool reserves
```

**Root Cause**: The geometric pool's `reflect_curve` generates passive orders centered at oracle price, independent of pool balances. Asymmetric `add_liquidity` performs a virtual swap at flat oracle price, bypassing the geometric price bands (spacing/ratio) the pool is designed to enforce.

**Impact**: Attacker swaps at flat oracle price (0% slippage) vs normal ~2.7% slippage through geometric pool.

**Recommended Fix**: Account for pool balance asymmetry in geometric pool pricing; or restrict asymmetric deposits.

---

#### **Pattern 20: Partial Liquidation Worsens Collateral Ratio** [MEDIUM]
**Protocol**: Numa | **Auditor**: Sherlock | **Severity**: Medium

```solidity
// ❌ VULNERABLE: Each partial liquidation with incentive worsens LTV
// Liquidator repays X debt, receives X * (1 + incentive) collateral
// LTV = debt / collateral increases after each partial liquidation
// Eventually: revert (seize too much) or bad debt (unprofitable)
```

**Root Cause**: Partial liquidations with `liquidationIncentive` (e.g., 12%) give liquidators more collateral value than debt repaid, worsening the LTV ratio each iteration. Combined with `closeFactorMantissa` and minimum borrow thresholds, positions reach states where liquidation reverts or becomes unprofitable.

**Recommended Fix**: If partial liquidation would push into bad debt, require full liquidation with reduced incentive.

---

#### **Pattern 21: Uniswap V3 Balance Proportion ≠ Price** [HIGH]
**Protocol**: Gamma | **Auditor**: Sherlock | **Severity**: High

**Root Cause**: Uniswap V3 pool token balance proportions don't reflect price and are cheaply manipulable unlike V2. Using V3 balance ratios for collateral pricing or decision-making enables attackers to force excessive sells at manipulated prices.

**Recommended Fix**: Use TWAP price from Uniswap V3 oracle instead of balance proportions.

---

### Impact Analysis

#### Technical Impact (Frequency across 21 reports)
- Incorrect pricing leading to arbitrage (12/21 reports)
- Protocol fund drainage through formula bugs (8/21 reports)
- Invariant violations allowing continued operation with insufficient reserves (3/21 reports)
- Chain halt or permanent dysfunction (1/21 reports — Taiko)
- LP value erosion over time (3/21 reports)

#### Business Impact
- Direct financial loss from pricing arbitrage (all patterns)
- Loss of LP provider confidence when K-invariant decreases
- Protocol insolvency from accumulated formula errors
- Governance risk from mid-operation parameter changes

### Secure Implementation

**Fix 1: Validate Formula Implementation Against Specification**
```solidity
// ✅ SECURE: Match specification exactly with comprehensive testing
// For YieldSpace: spotPrice = c * (mu * z / y) ** ts
function calculateSpotPrice(
    uint256 shareReserves,
    uint256 bondReserves,
    uint256 initialSharePrice,
    uint256 timeStretch
) internal pure returns (uint256) {
    uint256 base = shareReserves.divDown(bondReserves);
    return initialSharePrice.mulDown(base.pow(timeStretch));
}
```

**Fix 2: Dynamic Valuation Instead of Static Constants**
```solidity
// ✅ SECURE: Use on-chain virtual price for LP token valuation
function getLPTokenValue(address curvePool) internal view returns (uint256) {
    return ICurvePool(curvePool).get_virtual_price();
}
// NOT: int256 constant N_COINS = 3; // This becomes stale
```

**Fix 3: Validate Curve Parameters at Launch**
```solidity
// ✅ SECURE: Ensure bonding curve parameters are consistent
function createToken(uint256 stepSize, uint256 numSteps, uint256 curveSupply) external {
    require(stepSize * numSteps == curveSupply, "Supply mismatch");
    require(stepSize > 0 && numSteps > 0, "Zero params");
    // ... launch logic
}
```

**Fix 4: Separate Utilization Rates Per Position Type**
```solidity
// ✅ SECURE: Independent utilization for bull and bear
function getUtilizationRate(bool isBull) public view returns (uint256) {
    if (isBull) return bullUsed * 1e18 / initialLiquidity;
    else return bearUsed * 1e18 / initialLiquidity;
}
```

### Detection Patterns

```
- Pattern: Hardcoded multiplier (N_COINS, static ratios) used for token valuation
- Pattern: Binary search without monotonicity guarantee on input
- Pattern: Formula using wrong parameter (timeRemaining vs timeStretch)
- Pattern: abs() comparison that loses sign information in clamping
- Pattern: Combined utilization/metric from independent position types
- Pattern: Solana lamports() used without subtracting rent-exemption
- Pattern: updateFormula/updateCurve without batch/epoch boundary check
- Pattern: Discarded error return values from quote/pricing functions
- Pattern: Spot price validation in constructor but not in runtime functions
- Pattern: Asymmetric deposit performing virtual swap at flat price
- Pattern: stepSize * numSteps not validated against curveSupply
```

### Keywords for Search

`bonding curve`, `formula error`, `math bug`, `invariant violation`, `spot price`, `getOutputPrice`, `getInputPrice`, `binary search`, `monotonic`, `N_COINS`, `get_virtual_price`, `utilization rate`, `delta hedge`, `SignedMath.abs`, `BPF`, `neutralPrice`, `GDACurve`, `MIN_PRICE`, `reflect_curve`, `K-invariant`, `constant product`, `rent-exemption`, `lamports`, `updateFormula`, `batch`, `error codes`, `getBuyInfo`, `getSellInfo`, `calculateSpotPrice`, `timeStretch`, `geometric pool`, `asymmetric liquidity`, `stepSize`, `numSteps`, `curveSupply`, `LP valuation`, `option premium`, `volatility`

### Related Vulnerabilities

- Bonding Curve Rounding/Precision Errors
- Bonding Curve Price Manipulation
- Flash Loan Attacks on Bonding Curves
- AMM Invariant Manipulation
- Oracle Price vs Spot Price Discrepancy
