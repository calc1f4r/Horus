---
title: Bonding Curve Price Manipulation Vulnerabilities
protocol: Multi-Protocol (Flayer, USSD, Dango, Frax, TokenBox, Paladin, PossumLabs, Maverick, Zivoe, Malt, GTE, Computable, 1inch)
chain: Ethereum, Solana, Multi-Chain
category: Price Manipulation
vulnerability_type: Spot Price Manipulation, Reserve Manipulation, Callback Exploitation, Timing Attacks
attack_type: Sandwich Attack, Flash Loan, Front-Running, Price Oracle Manipulation
affected_component: bonding_curve_pricing|pool_reserves|price_discovery
primitives: Bonding Curve, AMM, Uniswap V2/V3/V4, DEX, Price Discovery
severity: critical
impact: Fund Theft, Price Distortion, LP Losses, Reserve Draining
tags:
  - bonding-curve
  - price-manipulation
  - spot-price
  - uniswap
  - flash-loan
  - sandwich-attack
  - reserve-manipulation
  - callback-exploitation
  - delta-accounting
  - maker-hooks
  - bin-movement
  - dutch-auction
  - rounding-exploitation
  - listing-fee
  - concentrated-liquidity
  - virtual-LP

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | unknown | Spot Price Manipulation, Reserve Manipulation, Callback Exploitation, Timing Attacks

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AMM
  - Bonding Curve
  - DEX
  - Price Discovery
  - Uniswap V2/V3/V4
  - _getQuoteAmount
  - balanceOf
  - deposit
  - execute
  - extraction
  - mint
  - msg.sender
  - receive
  - spotPriceOHM
  - swap
---

# Bonding Curve Price Manipulation Vulnerabilities

## Overview

Bonding curve protocols derive token prices from on-chain state (pool reserves, spot prices, oracle readings). When these prices are read without manipulation resistance, attackers can temporarily distort them via flash loans, large swaps, or callback exploitation to buy/sell at favorable rates. This entry covers 13 validated patterns across 13 protocols and 8+ independent auditors.

**Pattern Frequency:** Common — 13/131 bonding curve reports (10%)
**Cross-Auditor Validation:** Strong — patterns confirmed by Sherlock, Code4rena, Cyfrin, Trail of Bits, Spearbit, ConsenSys, Shieldify, Pashov



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | unknown | Spot Price Manipulation, Reserve Manipulation, Callback Exploitation, Timing Attacks`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `AMM`, `Bonding Curve`, `DEX`, `Price Discovery`, `Uniswap V2/V3/V4`, `_getQuoteAmount`, `balanceOf`, `deposit`
- Typical sink / impact: `Fund Theft, Price Distortion, LP Losses, Reserve Draining`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

## Root Cause

These vulnerabilities exist because **manipulable spot prices or reserves** are used in pricing logic instead of time-weighted or manipulation-resistant alternatives. The fundamental issue is that bonding curve pricing functions read instantaneous on-chain state that can be atomically modified within the same transaction or block, allowing attackers to profit from temporary price distortions.

## Vulnerability Description

Bonding curve price manipulation takes several forms:

1. **Spot Price Reads**: Using `getSlot0()`, `getReserves()`, or `balanceOf()` for pricing instead of TWAPs
2. **Reserve-Based Pricing**: Computing prices from pool balances that can be inflated/deflated via flash loans
3. **Callback Exploitation**: Using protocol callbacks (hooks, routers) to manipulate state mid-execution
4. **Timing Attacks**: Exploiting delayed state updates (bin movements, fee claims) to trade at stale prices
5. **Rounding Exploitation**: Using small trades to compound integer division truncation for systematic underpricing

---

### Vulnerable Pattern Examples

#### **Pattern 1: Spot Price Used in beforeSwap Fee Conversion** [HIGH]

**Source:** Flayer — Sherlock (ComposableSecurity, Thanos, BugPull, AuditorPraise, KingNFT, zzykxx)
**File:** `reports/bonding_curve_findings/flayer_sherlock_beforeswap_price_manipulation.md`

```solidity
// UniswapImplementation.sol — beforeSwap() uses current spot price
(uint160 sqrtPriceX96,,,) = poolManager.getSlot0(poolId); // ← manipulable
(, ethIn, tokenOut, ) = SwapMath.computeSwapStep({
    sqrtPriceCurrentX96: sqrtPriceX96, // attacker-controlled
    ...
});
```

**Attack:** Sell collectionTokens → price drops → swap pending fees at discounted price → buy back tokens. PoC shows cost drops from ~1.11 ETH to ~0.41 ETH. UniswapV4's delta accounting eliminates flash loan requirement.

---

#### **Pattern 2: V3 Pool Balances Used as Price Proxy** [HIGH]

**Source:** USSD (Autonomous Secure Dollar) — Sherlock (VAD37, curiousapple, Bahurum, simon135, n33k)
**File:** `reports/bonding_curve_findings/ussd_sherlock_uniswap_v3_balance_proportion.md`

```solidity
// USSDRebalancer.sol#L83-L107
// Uses pool.balanceOf(token) to determine price proportion
// WRONG for Uniswap V3 — concentrated liquidity means reserves ≠ price
if (USSDamount < DAIamount) // L97 — underflow revert if manipulated
```

**Attack:** Add single-sided DAI liquidity at extreme range → manipulate WETH/DAI pool → trigger `rebalance()` → protocol mints/sells excessive USSD → crash stablecoin. Fundamental flaw: V3 pool `balanceOf()` does NOT correspond to price due to concentrated liquidity.

---

#### **Pattern 3: Asymmetric LP Bypasses Geometric Pool Price Bands** [HIGH]

**Source:** Dango DEX — Sherlock (haxagon, axelot, blockace)
**File:** `reports/bonding_curve_findings/dango_sherlock_asymmetric_geometric_pool.md`

```rust
// geometric.rs#L211-L294 — reflect_curve()
let marginal_price = base_price.checked_div(quote_price)?;
// Orders always centered at oracle marginal_price, independent of pool balances
// Asymmetric add_liquidity performs "virtual swap" at flat oracle price
```

**Attack:** Pool has 10 ETH / 20000 USDC, oracle says 1 ETH = 2000 USDC. Attacker calls `add_liquidity` with 2.222 ETH → burns LP → receives ~1.22 ETH + ~1999 USDC. Effectively trades 1 ETH at flat 2000 USDC, bypassing geometric spacing/ratio price bands.

---

#### **Pattern 4: Uniswap V2 Spot Reserves in Collateral Valuation** [HIGH]

**Source:** Frax Solidity (OHM_AMO) — Trail of Bits (Samuel Moelius, Maximilian Krüger, Troy Sargent)
**File:** `reports/bonding_curve_findings/frax_tob_spot_price_ohm_manipulation.md`

```solidity
function spotPriceOHM() public view returns (uint256 frax_per_ohm_raw, uint256 frax_per_ohm) {
    (uint256 reserve0, uint256 reserve1,) = (UNI_OHM_FRAX_PAIR.getReserves());
    frax_per_ohm = reserve1.mul(PRICE_PRECISION).div(reserve0.mul(10 ** missing_decimals_ohm));
}
// Feeds into globalCollateralValue() → unlocks buyBackFXS and recollateralize
```

**Attack:** Flash-loan FRAX → buy OHM (inflate spot) → `buyBackFXS` (protocol burns FXS, pays USDC) → sell OHM → `recollateralize` (receive newly minted FXS + bonus). Repeat until 200k hourly cap reached.

---

#### **Pattern 5: getAmountsIn Spot Price for Minting** [HIGH/CRITICAL]

**Source:** Forgottenplayland (TokenBox) — Pashov Audit Group
**File:** `reports/bonding_curve_findings/tokenbox_pashov_uniswap_oracle_manipulation.md`

```solidity
// Uses uniswapV2Router.getAmountsIn() for paymentToken price
// Trivially manipulable via large swap in underlying V2 pair
```

**Attack:** Flashloan referenceToken → sell in V2 pair (price drops to ~0) → mint TokenBox at manipulated near-zero price → return flash loan. Pure profit extraction.

---

#### **Pattern 6: FullRangeHook Tick Boundary Gap** [HIGH]

**Source:** Paladin Valkyrie — Cyfrin (Draiakoo, Giovanni Di Siena)
**File:** `reports/bonding_curve_findings/paladin_cyfrin_fullrangehook_tick_gap.md`

```solidity
// FullRangeHook.sol — narrower range than TickMath
int24 internal constant MIN_TICK = -887220; // FullRangeHook
int24 internal constant MAX_TICK = -MIN_TICK;
// vs TickMath.sol: MIN_TICK = -887272, MAX_TICK = 887272
// Gap of 52 ticks on each side allows price to escape liquidity range
```

**Attack:** After pool init (before LP), swap price outside -887220..887220 range → `getLiquidityForAmounts` returns ~5 instead of ~100e18 → first depositor cannot meet `MINIMUM_LIQUIDITY` (DoS), or LP deposits at out-of-range price and attacker steals value when price returns. `_rebalance()` reverts from division by zero.

---

#### **Pattern 7: Front-Running convert() for Portal Energy Price** [MEDIUM]

**Source:** PossumLabs V2 — Shieldify (Elhaj)
**File:** `reports/bonding_curve_findings/possumlabs_shieldify_psm_portal_energy_manipulation.md`

```solidity
// VirtualLP.sol#L502 — convert() increases PSM reserves
// PortalV2MultiAsset.sol#L556 — buyPortalEnergy() at current price
// PortalV2MultiAsset.sol#L608 — sellPortalEnergy() at new higher price
```

**Attack:** Buy portalEnergy → call `convert()` (adds PSM to LP, raising PE price) → sell portalEnergy at inflated price. `LP_PROTECTION_HURDLE` limits but doesn't prevent extraction.

---

#### **Pattern 8: Stale Bin Position After Swap** [MEDIUM]

**Source:** Maverick — Code4rena (gzeon)
**File:** `reports/bonding_curve_findings/maverick_c4rena_bin_movement_manipulation.md`

```solidity
// Pool.sol#L305-L306 — bins moved AFTER swap, not before
emit Swap(...);
_moveBins(currentState.activeTick, startingTick, lastTwa);
// In low-activity pools, bin position stale until next swap
```

**Attack:** Buy 10 tokens → wait for TWAP to shift (e.g., 1 hour) → execute 0-token swap to trigger bin movement → sell 10 tokens at better price. PoC: 3.22 extra tokens received.

---

#### **Pattern 9: Manipulable fetchBasis() in Yield Forwarding** [MEDIUM]

**Source:** Zivoe — Sherlock (cergyk, lemonmon, AllTooWell, Audinarey, 0xpiken)
**File:** `reports/bonding_curve_findings/zivoe_sherlock_forward_yield_manipulation.md`

```solidity
(uint256 amount, uint256 lp) = fetchBasis(); // based on Uniswap V2 LP value
if (amount > basis) { _forwardYield(amount, lp); }
(basis,) = fetchBasis(); // set to manipulated LOW value
```

**Attack:** Flash-loan → buy pairAsset from V2 pool (shrinks fetchBasis return) → call `forwardYield` (amount < basis, no yield sent; basis set to tiny value) → restore pool → 30 days later: call again (amount >> basis), draining excess yield.

---

#### **Pattern 10: Dutch Auction Commitment Manipulation** [MEDIUM]

**Source:** Malt Finance — Code4rena (gzeon)
**File:** `reports/bonding_curve_findings/malt_c4rena_dutch_auction_manipulation.md`

```solidity
// Auction.sol#L212 — _endAuction only triggers when commitments >= maxCommitments
// purchaseAndBurn reverts for 1 wei swap due to AMM rounding
```

**Attack:** Purchase `maxCommitments - 1 wei` → auction can't end (1-wei purchase reverts in AMM). Auction continues decaying price for 5+ minutes before `stabilize()` can intervene. Attacker guarantees purchase at ≤ `(startingPrice + endingPrice) / 2`.

---

#### **Pattern 11: Integer Division Truncation in Quote Calculations** [MEDIUM]

**Source:** GTE Launchpad — Code4rena (VAD37, harry, Ayomiposi233, Manga, oracle-script)
**File:** `reports/bonding_curve_findings/gte_c4rena_rounding_quote_calculations.md`

```solidity
function _getQuoteAmount(uint256 baseAmount, uint256 quoteReserve, uint256 baseReserve, bool isBuy)
    internal pure returns (uint256 quoteAmount)
{
    uint256 baseReserveAfter = isBuy ? baseReserve - baseAmount : baseReserve + baseAmount;
    return (quoteReserve * baseAmount) / baseReserveAfter; // ← truncates
}
```

**Attack:** Select `baseAmount` values that maximize truncation → each buy underpays → compound error across repeated buys → purchase at systematic discount until curve drained or bonding phase ends.

---

#### **Pattern 12: Listing Fee Claim Timing Manipulation** [HIGH]

**Source:** The Computable Protocol — Trail of Bits (Gustavo Grieco, Rajeev Gopalakrishna, Josselin Feist)
**File:** `reports/bonding_curve_findings/computable_tob_listing_fee_timeout.md`

```python
def claimBytesAccessed(hash: bytes32):
    assert msg.sender == self.listings[hash].owner
    accessed: uint256 = self.datatrust.getBytesAccessed(hash)
    maker_fee: wei_value = (self.parameterizer.getCostPerByte() * accessed * ...) / 100
    price: wei_value = self.reserve.getSupportPrice()
    minted: uint256 = (maker_fee * 1000000000) / price
    self.market_token.mint(minted)
```

**Attack:** Create legitimate listing → let fees accumulate (no timeout) → strategically batch-claim when it maximally manipulates market token price. No timeout means unlimited accumulation of mintable tokens.

---

#### **Pattern 13: Malicious Maker Hooks Override Taking Amount** [HIGH]

**Source:** 1inch AggregationRouter V5 — ConsenSys Diligence (George Kobakhidze, Chingiz Mardanov)
**File:** `reports/bonding_curve_findings/1inch_consensys_malicious_maker_hooks.md`

```solidity
actualMakingAmount = _getMakingAmount(...);
if (actualMakingAmount > remainingMakingAmount) {
    actualMakingAmount = remainingMakingAmount;
    actualTakingAmount = _getTakingAmount(...); // ← maker controls this
    // Threshold check: makingAmount * order.takingAmount <= takingAmount * order.makingAmount
    // Passes because order has large takingAmount
}
```

**Attack:** Maker creates order 100 ETH for 100 DAI with malicious hooks. Taker tries partial fill (100 DAI). `_getMakingAmount` returns 100.1 (triggers recompute). `_getTakingAmount` returns 10000 DAI — taker spends 10000 DAI instead of 100 DAI, up to balance/approval limit.

---

## Impact Analysis

| Impact | Frequency | Severity |
|--------|-----------|----------|
| Direct fund theft via price manipulation | 8/13 patterns | HIGH-CRITICAL |
| LP/depositor losses from incorrect pricing | 5/13 patterns | MEDIUM-HIGH |
| Protocol reserve draining | 4/13 patterns | HIGH |
| DoS/system disruption | 2/13 patterns | MEDIUM-HIGH |
| Oracle consumers receive wrong data | 3/13 patterns | MEDIUM |

**Financial Impact Range:** From small rounding profits (Pattern 11) to complete protocol drain (Patterns 4, 5, 13).

## Secure Implementation

### Use TWAP Instead of Spot Price

```solidity
// SECURE: Use TWAP oracle (e.g., Uniswap V4 truncated oracle hook)
(int24 arithmeticMeanTick, ) = oracle.consult(poolId, TWAP_PERIOD);
uint160 sqrtPriceX96 = TickMath.getSqrtRatioAtTick(arithmeticMeanTick);
// Use sqrtPriceX96 for fee conversion instead of getSlot0()
```

### Round Up for Protocol-Favorable Operations

```solidity
// SECURE: Round up for buys (protocol receives more)
function _getQuoteAmount(uint256 baseAmount, uint256 quoteReserve, uint256 baseReserve)
    internal pure returns (uint256)
{
    uint256 baseReserveAfter = baseReserve - baseAmount;
    return (quoteReserve * baseAmount + baseReserveAfter - 1) / baseReserveAfter; // round up
}
```

### Validate Callback Return Values

```solidity
// SECURE: Cap taker spending to intended amount
actualTakingAmount = _getTakingAmount(...);
require(actualTakingAmount <= takingAmount, "Taking amount exceeds limit");
```

---

### Detection Patterns

#### Code Patterns to Look For

```
# Spot price reads in pricing logic
getSlot0|getReserves|balanceOf.*price|spotPrice
# Missing TWAP usage
# Callback-controlled amounts without caps
_getMakingAmount|_getTakingAmount|actualTakingAmount
# Bin/state updates after swap instead of before
emit Swap.*\n.*_moveBins|_updateState
# No timeout on claimable rewards/fees
claimBytesAccessed|claimFees.*assert msg.sender
```

#### Preconditions

1. Protocol reads spot price or pool balances for pricing
2. No TWAP or manipulation-resistant oracle used
3. Flash loans available for the pricing token
4. Callbacks or hooks allow mid-execution state changes
5. Integer division used without rounding compensation

---

## Keywords

bonding curve price manipulation, spot price manipulation, Uniswap V2 getReserves manipulation, Uniswap V3 balanceOf price, Uniswap V4 beforeSwap hook, getSlot0 manipulation, TWAP bypass, flash loan price oracle, concentrated liquidity reserves, geometric pool asymmetric deposit, delta accounting, maker hooks exploitation, dutch auction commitment, bin movement timing, fetchBasis manipulation, listing fee timeout, rounding truncation quote, virtual LP price manipulation, fullrange hook tick gap, callback return value exploitation

## Related Vulnerabilities

- [BONDING_CURVE_ORACLE_TWAP_VULNERABILITIES.md](BONDING_CURVE_ORACLE_TWAP_VULNERABILITIES.md) — Oracle-specific manipulation patterns
- [SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md](../SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md) — MEV/sandwich attack patterns
- [BONDING_CURVE_SLIPPAGE_PROTECTION_VULNERABILITIES.md](../BONDING_CURVE_SLIPPAGE_PROTECTION_VULNERABILITIES.md) — Missing slippage protection

## References

| # | Protocol | Auditor | Severity | Report |
|---|----------|---------|----------|--------|
| 1 | Flayer | Sherlock | HIGH | `reports/bonding_curve_findings/flayer_sherlock_beforeswap_price_manipulation.md` |
| 2 | USSD | Sherlock | HIGH | `reports/bonding_curve_findings/ussd_sherlock_uniswap_v3_balance_proportion.md` |
| 3 | Dango DEX | Sherlock | HIGH | `reports/bonding_curve_findings/dango_sherlock_asymmetric_geometric_pool.md` |
| 4 | Frax (OHM_AMO) | Trail of Bits | HIGH | `reports/bonding_curve_findings/frax_tob_spot_price_ohm_manipulation.md` |
| 5 | TokenBox | Pashov | HIGH | `reports/bonding_curve_findings/tokenbox_pashov_uniswap_oracle_manipulation.md` |
| 6 | Paladin Valkyrie | Cyfrin | HIGH | `reports/bonding_curve_findings/paladin_cyfrin_fullrangehook_tick_gap.md` |
| 7 | PossumLabs V2 | Shieldify | MEDIUM | `reports/bonding_curve_findings/possumlabs_shieldify_psm_portal_energy_manipulation.md` |
| 8 | Maverick | Code4rena | MEDIUM | `reports/bonding_curve_findings/maverick_c4rena_bin_movement_manipulation.md` |
| 9 | Zivoe | Sherlock | MEDIUM | `reports/bonding_curve_findings/zivoe_sherlock_forward_yield_manipulation.md` |
| 10 | Malt Finance | Code4rena | MEDIUM | `reports/bonding_curve_findings/malt_c4rena_dutch_auction_manipulation.md` |
| 11 | GTE | Code4rena | MEDIUM | `reports/bonding_curve_findings/gte_c4rena_rounding_quote_calculations.md` |
| 12 | Computable | Trail of Bits | HIGH | `reports/bonding_curve_findings/computable_tob_listing_fee_timeout.md` |
| 13 | 1inch | ConsenSys | HIGH | `reports/bonding_curve_findings/1inch_consensys_malicious_maker_hooks.md` |

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

`AMM`, `Bonding Curve`, `DEX`, `Price Discovery`, `Price Manipulation`, `Spot Price Manipulation, Reserve Manipulation, Callback Exploitation, Timing Attacks`, `Uniswap V2/V3/V4`, `_getQuoteAmount`, `balanceOf`, `bin-movement`, `bonding-curve`, `callback-exploitation`, `concentrated-liquidity`, `delta-accounting`, `deposit`, `dutch-auction`, `execute`, `extraction`, `flash-loan`, `listing-fee`, `maker-hooks`, `mint`, `msg.sender`, `price-manipulation`, `receive`, `reserve-manipulation`, `rounding-exploitation`, `sandwich-attack`, `spot-price`, `spotPriceOHM`, `swap`, `uniswap`, `virtual-LP`
