---
title: Bonding Curve Oracle and TWAP Vulnerabilities
protocol: Multi-Protocol (Nibbl, Ubiquity, USSD, Unlock)
chain: Ethereum
category: Oracle Manipulation
vulnerability_type: Stale TWAP, TWAP Design Flaws, Oracle Denomination Errors, Collateral Depeg Arbitrage
attack_type: TWAP Manipulation, Oracle Arbitrage, Stale Price Exploitation
primitives: Bonding Curve, TWAP Oracle, Curve Metapool, Uniswap V2 Oracle, Chainlink
severity: MEDIUM to HIGH
impact: Price Manipulation, DoS, Stablecoin Depeg, Collateral Draining
tags:
  - bonding-curve
  - oracle
  - twap
  - twav
  - stale-oracle
  - curve-metapool
  - uniswap-oracle
  - chainlink
  - denomination-mismatch
  - collateral-depeg
  - observation-array
  - time-weighted-average
---

# Bonding Curve Oracle and TWAP Vulnerabilities

## Overview

Bonding curve protocols often use time-weighted average prices (TWAPs) or external oracles to determine exchange rates, trigger rebalancing, or validate operations. Flawed TWAP implementations, stale oracle data, and denomination mismatches create exploitable price discrepancies. This entry covers 6 validated patterns across 4 protocols and 3 independent auditors.

**Pattern Frequency:** Moderate — 6/131 bonding curve reports (4.6%)
**Cross-Auditor Validation:** Strong — confirmed by Code4rena, Sherlock, and multiple independent researchers

## Root Cause

These vulnerabilities exist because **oracle/TWAP implementations fail to provide accurate, timely, and manipulation-resistant price data**. Root causes include: insufficient observation windows, using balance TWAPs as price proxies, denomination mismatches between oracle feeds and protocol expectations, and reliance on external interactions to update oracle state.

## Vulnerability Description

Oracle and TWAP vulnerabilities in bonding curves manifest in several ways:

1. **Insufficient TWAP Window**: Too few observations make the TWAP trivially manipulable within minutes
2. **Stale Oracle**: Oracle only updates when external contracts are interacted with, creating arbitrage windows
3. **Balance vs Price TWAP**: Using time-weighted average *balances* as a proxy for price, which is fundamentally flawed
4. **Denomination Mismatch**: Oracle feeds denominated in wrong units relative to protocol expectations
5. **Depeg Arbitrage**: Slow oracle updates during collateral depeg events allow arbitrage draining

---

### Vulnerable Pattern Examples

#### **Pattern 1: TWAV with Only 4 Observations** [MEDIUM]

**Source:** Nibbl — Code4rena (xiaoming90, hyh)
**File:** `reports/bonding_curve_findings/nibbl_c4rena_ineffective_twav.md`

```solidity
uint8 private constant TWAV_BLOCK_NUMBERS = 4;
TwavObservation[TWAV_BLOCK_NUMBERS] public twavObservations;

function _updateTWAV(uint256 _valuation, uint32 _blockTimestamp) internal {
    twavObservations[twavObservationsIndex] = TwavObservation(
        _blockTimestamp,
        _prevCumulativeValuation + (_valuation * _timeElapsed)
    );
    twavObservationsIndex = (twavObservationsIndex + 1) % TWAV_BLOCK_NUMBERS;
}
```

**Attack:** Block 100: Buy tokens, push valuation to 120 ETH. Blocks 101-103: Call `updateTWAV` each block to overwrite all 4 observations. Block 104: `_getTwav()` returns 120 ETH → buyout rejected. Attacker dumps shares — entire attack within ~1 minute (~4 blocks).

**Root Cause:** Array of 4 observations creates an Observation-Weighted Average, not a Time-Weighted Average. Anyone can call `updateTWAV` each block.

---

#### **Pattern 2: Stale TWAP from Unupdated Curve Metapool** [MEDIUM]

**Source:** Ubiquity — Sherlock (cergyk, rvierdiiev, 0xadrii, osmanozdemir1)
**File:** `reports/bonding_curve_findings/ubiquity_sherlock_stale_twap_metapool.md`

```solidity
// LibTWAPOracle.sol#L134-L136 — fetches metapool values that may be stale
// LibUbiquityPool.sol#L344 — calls update but doesn't poke metapool
// The metapool's internal cumulative balances only update when someone swaps/adds/removes
```

**Attack:** Metapool is idle → TWAP values stale (showing uAD at acceptable peg) → malicious user mints/burns large amounts of uAD at outdated price → pushes uAD further off-peg. Stale TWAP allows mints/burns that should have been rejected.

**Root Cause:** `LibTWAPOracle.update()` doesn't trigger an update on the underlying Curve metapool. Metapool cumulative balances only update on interaction (swap/add/remove liquidity).

---

#### **Pattern 3: Balance TWAP Manipulation via Imbalanced Liquidity** [MEDIUM]

**Source:** Ubiquity — Sherlock (cergyk, evmboi32, cducrest-brainbot, KupiaSec, GatewayGuardians)
**File:** `reports/bonding_curve_findings/ubiquity_sherlock_twap_balance_manipulation.md`

```solidity
// LibTWAPOracle uses IMetapool::get_twap_balances() which returns
// time-weighted average of pool reserves, NOT prices
// Fundamental flaw: balance TWAP ≠ price TWAP
```

**Attack (post-merge, 2 consecutive blocks):**
1. Block N: Update TWAP; add 100 uAD + 200 3CRV (reserves → 110/210)
2. Block N+1: Remove liquidity (reserves back to 10/10) but don't update UbiquityPool TWAP
3. Block N+40: Update TWAP — cumulative still imbalanced (6120 vs 7320)
4. uAD appears overpriced vs 3CRV → redeems blocked for many blocks

**Root Cause:** TWAP of *balances* is not equivalent to TWAP of *prices*. Uniswap V3 correctly TWAPs the price (tick), not the reserves.

---

#### **Pattern 4: Oracle USD Denomination Instead of DAI** [HIGH]

**Source:** USSD (Autonomous Secure Dollar) — Sherlock (WATCHPUG, T1MOH)
**File:** `reports/bonding_curve_findings/ussd_sherlock_oracle_usd_denomination.md`

```solidity
// StableOracleWETH.sol#L12-L27
// Returns prices in USD, but rebalancer treats them as DAI-denominated
// USSD pegs to DAI, not USD — when DAI depegs from $1, rates diverge
```

**Attack (DAI at $1.10):**
1. Mint 1100 USSD with 1000 DAI (oracle says 1 DAI = $1, so 1000 DAI = $1100 worth)
2. Sell 1100 USSD for ~1100 DAI on pool (pushes USSD below DAI peg)
3. Trigger `rebalance()` — sells collateral to DAI, buys back USSD
4. Repeat until all collateral consumed

**Root Cause:** All collateral oracles (WETH, WBTC, WBGL) return USD-denominated prices, but protocol treats them as DAI-denominated. Fix: Change oracle to DAI-denominated feeds or change peg target from DAI to USD.

---

#### **Pattern 5: Collateral Depeg Arbitrage via Stale Chainlink** [MEDIUM]

**Source:** Ubiquity — Sherlock (cergyk, ge6a, cducrest-brainbot, fugazzi, shaka)
**File:** `reports/bonding_curve_findings/ubiquity_sherlock_collateral_depeg_arbitrage.md`

```solidity
// LibUbiquityPool.sol#L358-L364
// Minting/redeeming at Chainlink price minus fee
// No enforcement of collateral ratio between different assets
// When one collateral depegs, Chainlink lags → arbitrage window
```

**Attack (DAI depegging):**
1. DAI begins depegging; Chainlink still shows near-$1 (slow to update)
2. Mint uAD with DAI at stale Chainlink rate (better execution than DEXes)
3. Redeem uAD for LUSD (still well-pegged)
4. LUSD reserves depleted; DAI accumulates → uAD backed by depegging asset → uAD depegs

**Root Cause:** Chainlink oracles update slowly during rapid depeg events. Protocol lacks per-collateral reserve ratios or safety minting caps.

---

#### **Pattern 6: Daily Oracle Update Creates Arbitrage Window** [MEDIUM]

**Source:** Unlock Protocol — Code4rena (itsmeSTYJ)
**File:** `reports/bonding_curve_findings/unlock_c4rena_udt_oracle_arbitrage.md`

```solidity
// Standard Uniswap V2 oracle with updateAndConsult()
// Daily update period too slow to track UDT price volatility
// When exchange price diverges from stale oracle, arbitrage opens
```

**Attack:**
1. UDT exchange price significantly higher than stale `uniswapOracle` value
2. Purchase many keys across many locks → receive UDT referrer rewards at stale low price
3. Sell UDT on exchanges at higher market price
4. Request refund on keys (with or without free trial)
5. Repeat until oracle catches up

**Root Cause:** Single Uniswap V2 oracle with daily update period. Token volatility exceeds oracle update frequency.

---

## Impact Analysis

| Impact | Frequency | Severity |
|--------|-----------|----------|
| Stablecoin/Token depeg | 3/6 patterns | MEDIUM-HIGH |
| Mint/redeem arbitrage | 3/6 patterns | MEDIUM |
| Buyout/governance manipulation | 1/6 patterns | MEDIUM |
| DoS on withdrawals/redeems | 1/6 patterns | MEDIUM |
| Collateral reserve draining | 2/6 patterns | MEDIUM-HIGH |

## Secure Implementation

### Use Proper TWAP with Sufficient Window

```solidity
// SECURE: Use Uniswap V3-style tick TWAP with minimum window
uint32 constant TWAP_WINDOW = 30 minutes;
uint16 constant MIN_OBSERVATIONS = 100;

function getTWAP(address pool) internal view returns (uint256 price) {
    (int24 arithmeticMeanTick,) = OracleLibrary.consult(pool, TWAP_WINDOW);
    price = OracleLibrary.getQuoteAtTick(arithmeticMeanTick, 1e18, token0, token1);
}
```

### Force Oracle Updates Before Reading

```solidity
// SECURE: Poke underlying pool before reading TWAP
function updateAndRead() internal returns (uint256 price) {
    // Force Curve metapool to update cumulative values
    IMetapool(metapool).remove_liquidity(0, [uint256(0), 0]); // zero-amount poke
    price = LibTWAPOracle.consult();
}
```

### Match Oracle Denomination to Peg Target

```solidity
// SECURE: If pegging to DAI, use DAI-denominated oracles
// WETH price = WETH/ETH * ETH/DAI (not WETH/USD)
function getCollateralPriceInDAI(address collateral) internal view returns (uint256) {
    uint256 priceInETH = chainlinkFeed.latestAnswer(); // ETH-denominated
    uint256 daiPerETH = daiEthFeed.latestAnswer();
    return priceInETH * daiPerETH / 1e18;
}
```

---

### Detection Patterns

#### Code Patterns to Look For

```
# Small observation arrays
TWAV_BLOCK_NUMBERS|twavObservations\[.*\]|constant.*=\s*[2-8];
# Balance-based TWAP
get_twap_balances|balanceOf.*twap|reserve.*cumulative
# Missing oracle poke
update\(\).*metapool|update.*cumulative.*(?!remove_liquidity|swap)
# Denomination mismatches
USD.*peg.*DAI|stableOracle.*USD|price.*PRECISION.*USD
# Daily oracle updates
updateAndConsult|updatePeriod.*86400|PERIOD.*1 days
```

#### Preconditions

1. TWAP uses fewer than 30 observations
2. Oracle state depends on external contract interactions
3. Protocol peg target differs from oracle denomination
4. Multiple collateral types with different depeg dynamics
5. Low-frequency oracle updates for volatile assets

---

## Keywords

bonding curve oracle manipulation, TWAP manipulation, TWAV insufficient observations, stale TWAP oracle, Curve metapool stale cumulative, balance TWAP vs price TWAP, oracle denomination mismatch, USD DAI denomination error, collateral depeg arbitrage, Chainlink stale price, Uniswap V2 daily oracle, time weighted average valuation, oracle update frequency, cumulative balance manipulation, poke metapool update

## Related Vulnerabilities

- [BONDING_CURVE_PRICE_MANIPULATION_VULNERABILITIES.md](BONDING_CURVE_PRICE_MANIPULATION_VULNERABILITIES.md) — Spot price manipulation patterns
- [SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md](../SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md) — Front-running oracle updates

## References

| # | Protocol | Auditor | Severity | Report |
|---|----------|---------|----------|--------|
| 1 | Nibbl | Code4rena | MEDIUM | `reports/bonding_curve_findings/nibbl_c4rena_ineffective_twav.md` |
| 2 | Ubiquity | Sherlock | MEDIUM | `reports/bonding_curve_findings/ubiquity_sherlock_stale_twap_metapool.md` |
| 3 | Ubiquity | Sherlock | MEDIUM | `reports/bonding_curve_findings/ubiquity_sherlock_twap_balance_manipulation.md` |
| 4 | USSD | Sherlock | HIGH | `reports/bonding_curve_findings/ussd_sherlock_oracle_usd_denomination.md` |
| 5 | Ubiquity | Sherlock | MEDIUM | `reports/bonding_curve_findings/ubiquity_sherlock_collateral_depeg_arbitrage.md` |
| 6 | Unlock Protocol | Code4rena | MEDIUM | `reports/bonding_curve_findings/unlock_c4rena_udt_oracle_arbitrage.md` |
