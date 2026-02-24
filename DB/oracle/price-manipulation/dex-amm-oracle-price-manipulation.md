---
# Core Classification
protocol: generic
chain: everychain
category: oracle
vulnerability_type: dex_amm_oracle_price_manipulation

# Attack Vector Details
attack_type: economic_exploit
affected_component: dex_based_price_oracle

# Oracle-Specific Fields
oracle_provider: uniswap_twap
oracle_attack_vector: manipulation

# Technical Primitives
primitives:
  - twap_oracle
  - spot_price
  - uniswap_v3_twap
  - lp_reserve_price
  - getReserves
  - totalSupply
  - concentrated_liquidity
  - bin_movement
  - fee_growth
  - implied_volatility
  - low_tvl_pool
  - flash_loan_manipulation
  - sandwich_attack
  - reserve_ratio

# Impact Classification
severity: high
impact: incorrect_pricing
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - oracle
  - twap
  - uniswap
  - price_manipulation
  - liquidation
  - lending
  - dex
  - amm
  - low_tvl
  - implied_volatility
  - lp_token

# Version Info
language: solidity
version: all

# Source
source: solodit + audit-reports
---

## Reference

| # | Report File | Protocol | Severity | Auditor |
|---|-------------|----------|----------|---------|
| 1 | [m-06-uniswap-oracle-prices-can-be-manipulated.md](reports/dex_aggregator_findings/m-06-uniswap-oracle-prices-can-be-manipulated.md) | Ouroboros 2024 | MEDIUM | Pashov Audit Group |
| 2 | [h-04-oracle-price-can-be-manipulated.md](reports/dex_aggregator_findings/h-04-oracle-price-can-be-manipulated.md) | Abracadabra Money | HIGH | Code4rena |
| 3 | [pools-can-be-subject-to-price-manipulation-leading-to-early-liquidations-or-arbi.md](reports/dex_aggregator_findings/pools-can-be-subject-to-price-manipulation-leading-to-early-liquidations-or-arbi.md) | f(x) v2 | HIGH | OpenZeppelin |
| 4 | [m-5-uniswap-aggregated-fees-can-be-increased-at-close-to-zero-cost.md](reports/dex_aggregator_findings/m-5-uniswap-aggregated-fees-can-be-increased-at-close-to-zero-cost.md) | Aloe | MEDIUM | Sherlock |
| 5 | [m-27-attacker-can-inflate-lp-position-value-to-create-a-bad-debt-loan.md](reports/dex_aggregator_findings/m-27-attacker-can-inflate-lp-position-value-to-create-a-bad-debt-loan.md) | Salty.IO | MEDIUM | Code4rena |
| 6 | [m-03-trader-can-manipulate-price-because-bin-only-moved-after-swap.md](reports/dex_aggregator_findings/m-03-trader-can-manipulate-price-because-bin-only-moved-after-swap.md) | Maverick | MEDIUM | Code4rena |

---

# DEX AMM Oracle Price Manipulation — Short TWAP Windows, Spot Price Abuse, and Low-TVL Pool Bypass

## Overview

Protocols that use DEX AMM prices (Uniswap V2/V3 TWAP, Curve pool reserves, concentrated liquidity TWAP, LP reserve ratios) as their primary price oracle are vulnerable to price manipulation attacks when: (1) TWAP windows are too short to resist economic attacks, (2) spot prices from low-TVL pools are used directly or can bypass deviation checks, (3) LP token prices are derived from manipulable pool reserves/ratios, or (4) the timing of pool state updates creates exploitable windows.

**Root Cause Statement**: This vulnerability exists because on-chain AMM price sources are manipulable by sufficiently capitalized attackers — short TWAP windows can be manipulated across multiple blocks, single low-TVL spot pools can bypass multi-pool deviation checks, and LP token valuations using `getReserves()` enable single-transaction flash loan price distortion, leading to incorrect collateral valuations, premature liquidations, or undercollateralized loans.

**Pattern Frequency**: Common — 6/32 DEX aggregator reports (19%)
**Consensus Severity**: MEDIUM-HIGH (2/6 HIGH, 4/6 MEDIUM; use MEDIUM as conservative consensus)
**Cross-Auditor Validation**: STRONG — 5 independent auditors (Pashov, Code4rena, OpenZeppelin, Sherlock, Code4rena)

---

## Vulnerability Description

### Variant A — Short TWAP Window on Low-Liquidity Pools (2 reports)

Protocols use Uniswap V3 TWAP oracles with insufficient observation window duration. When the liquidity in the pool is low, the capital required to shift the TWAP meaningfully decreases, making it economically viable for attackers to manipulate the price across multiple blocks within the window.

**Affected Reports**: Ouroboros 2024 (Pashov, MEDIUM), Aloe (Sherlock, MEDIUM — fee-based IV manipulation)

### Variant B — LP Token Price Using Manipulable Pool Reserves (2 reports)

LP aggregator oracle contracts compute fair value of LP tokens using `pair.getReserves()` directly. A flash loan can temporarily inflate reserves within a single transaction, artificially elevating the price returned by the oracle. This is used to borrow against an inflated LP position.

**Affected Reports**: Abracadabra Money (Code4rena, HIGH), Salty.IO (Code4rena, MEDIUM)

### Variant C — Multi-Pool Deviation Check Bypass via Single Low-TVL Pool (1 report)

A protocol uses multiple spot price sources and compares them against a Chainlink anchor price; if no pool deviates >1%, the spot prices are used. An attacker targets the single lowest-TVL pool, manipulates its price by exactly 1% (just within the tolerance), and the system uses the manipulated price wholesale for liquidations and redemptions.

**Affected Reports**: f(x) v2 (OpenZeppelin, HIGH)

### Variant D — Price Bin Updated After Swap Creates Manipulation Window (1 report)

In concentrated liquidity AMMs (Maverick), the active liquidity bin is only moved **after** the swap completes — not before. This creates a window where the price read from the protocol before the bin movement is the "old" price, allowing traders to exploit stale pricing for favorable trades.

**Affected Reports**: Maverick (Code4rena, MEDIUM)

---

## Attack Scenarios

### Scenario 1 — Flash Loan Attack on LP Reserve-Based Oracle (Abracadabra)

1. Attacker takes flash loan of large amounts of base or quote token
2. Deposits into the MagicLP pool, inflating `baseReserve` or `quoteReserve`
3. `MagicLpAggregator.latestAnswer()` calls `pair.getReserves()` → returns inflated values
4. Computed LP price is significantly elevated
5. Attacker borrows against inflated LP collateral → undercollateralized loan
6. Flash loan repaid; LP price returns to normal; attacker keeps borrowed funds

```
Proof: latestAnswer = minAnswer * (baseReserve + quoteReserve) / totalSupply
       If baseReserve is 10x inflated via flash → price is 5.5x expected → 
       borrow 5.5x normal → net profit = 4.5x collateral value
```

### Scenario 2 — Single Low-TVL Pool Bypasses Multi-Pool Anchor Check (f(x) v2)

1. Protocol uses three spot price pools + Chainlink anchor; any spot within 1% of anchor is used
2. Attacker identifies Pool C (lowest TVL): costs $50K to manipulate 1%
3. Attacker manipulates Pool C price downward by exactly 0.99%
4. `getPrice()` uses Pool C's `minPrice` (which is manipulated) for liquidations
5. Positions that were healthy are now below liquidation threshold → attacker liquidates
6. Attack cost: ~$50K manipulation + gas; gain: liquidation bonuses on forced liquidations

### Scenario 3 — Short TWAP Window on Low-Liquidity Collateral (Ouroboros/Aloe)

1. Protocol uses 30-minute TWAP window on ETH/TITANX pool (low liquidity)
2. Attacker allocates large capital to gradually shift pool price over 30 minutes
3. TWAP reflects manipulated prices after full window passes
4. At 8% price increase: formula `0.005 ETH * actual_price > 0.05 ETH * marketPriceRatio + 3 BOBA` becomes satisfied
5. Attacker repeatedly executes arbitrage against the stale protocol price
6. Attack profitable whenever TWAP window < cost of manipulation / arbitrage opportunity

### Scenario 4 — Uniswap Fee Manipulation to Inflate Implied Volatility (Aloe)

1. Protocol uses Uniswap V3 fee accumulation as a proxy for implied volatility (IV)
2. Attacker deposits large amount at the active tick (gaining >99% of in-range liquidity)
3. Attacker executes wash trades within the tick range via flashbots bundle (self-cancelling P&L)
4. Fee growth at the active tick spikes → IV calculation inflated
5. Higher IV → LTV decreased → existing borrowers' positions become liquidatable
6. Attacker back-runs to liquidate forced-liquidation positions at a profit

---

## Vulnerable Pattern Examples

**Example 1: LP Reserve Price Oracle — Flash Loan Attack** [HIGH — Abracadabra Money, Code4rena]

Reference: [h-04-oracle-price-can-be-manipulated.md](reports/dex_aggregator_findings/h-04-oracle-price-can-be-manipulated.md)

```solidity
// ❌ VULNERABLE: uses live pool reserves — manipulable via flash loan in same tx
contract MagicLpAggregator {
    function _getReserves() internal view virtual returns (uint256, uint256) {
        // ← direct pool reserves; no TWAP, no time-weighting
        (uint256 baseReserve, uint256 quoteReserve) = pair.getReserves();
        return (baseReserve, quoteReserve);
    }

    function latestAnswer() public view override returns (int256) {
        uint256 baseAnswerNormalized = uint256(baseOracle.latestAnswer())
            * (10 ** (WAD - baseOracle.decimals()));
        uint256 quoteAnswerNormalized = uint256(quoteOracle.latestAnswer())
            * (10 ** (WAD - quoteOracle.decimals()));
        uint256 minAnswer = Math.min(baseAnswerNormalized, quoteAnswerNormalized);

        // ← getReserves() can be inflated via flash loan
        (uint256 baseReserve, uint256 quoteReserve) = _getReserves();
        baseReserve = baseReserve * (10 ** (WAD - baseDecimals));
        quoteReserve = quoteReserve * (10 ** (WAD - quoteDecimals));

        return int256(minAnswer * (baseReserve + quoteReserve) / pair.totalSupply());
    }
}
```

**Example 2: Short TWAP Window on Low-Liquidity Pool** [MEDIUM — Ouroboros, Pashov Audit Group]

Reference: [m-06-uniswap-oracle-prices-can-be-manipulated.md](reports/dex_aggregator_findings/m-06-uniswap-oracle-prices-can-be-manipulated.md)

```solidity
// ❌ VULNERABLE: TWAP window too short for low-liquidity pools
contract PriceOracle {
    uint32 public constant TWAP_PERIOD = 15 minutes;  // ← too short for manipulation resistance

    function getPrice(address pool) external view returns (uint256) {
        // With low liquidity in pool, this TWAP can be shifted profitably
        // within the 15-minute window at relatively low cost
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = TWAP_PERIOD;
        secondsAgos[1] = 0;

        (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        int24 arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(TWAP_PERIOD)));

        return _getQuoteAtTick(arithmeticMeanTick, BASE_AMOUNT, token0, token1);
    }
}
```

**Example 3: Single-Pool Spot Bypass of Multi-Pool Anchor Check** [HIGH — f(x) v2, OpenZeppelin]

Reference: [pools-can-be-subject-to-price-manipulation...](reports/dex_aggregator_findings/pools-can-be-subject-to-price-manipulation-leading-to-early-liquidations-or-arbi.md)

```solidity
// ❌ VULNERABLE: only one pool needs to be manipulated to affect minPrice/maxPrice
// An attacker targets the lowest-TVL pool and manipulates within 1% tolerance
function getPrice() external view returns (uint256 minPrice, uint256 maxPrice) {
    for (uint i = 0; i < spotPools.length; i++) {
        uint256 spotPrice = _getSpotPrice(spotPools[i]);

        // ← Any single pool within 1% of anchor becomes the effective min/maxPrice
        if (spotPrice < anchorPrice * 99 / 100) {
            spotPrice = anchorPrice;  // clamp low outliers to anchor
        }
        if (spotPrice > anchorPrice * 101 / 100) {
            spotPrice = anchorPrice;  // clamp high outliers to anchor
        }

        if (spotPrice < minPrice) minPrice = spotPrice;  // ← attacker sets this
        if (spotPrice > maxPrice) maxPrice = spotPrice;
    }
    // minPrice used for liquidation → attacker can force premature liquidations
}
```

**Example 4: Maverick Bin Moved After Swap** [MEDIUM — Maverick, Code4rena]

Reference: [m-03-trader-can-manipulate-price...](reports/dex_aggregator_findings/m-03-trader-can-manipulate-price-because-bin-only-moved-after-swap.md)

```solidity
// ❌ VULNERABLE: _moveBins() called AFTER swap, not before
// Creates a price manipulation window at the start of each swap
function swap(
    address recipient,
    uint256 amount,
    bool tokenAIn,
    bool exactOutput,
    uint256 sqrtPriceLimit,
    bytes calldata data
) external returns (int256 delta0, int256 delta1) {
    // ... swap logic using current bin state ...
    emit Swap(msg.sender, recipient, tokenAIn, exactOutput, amountIn, amountOut, currentState.activeTick);

    // ← Bin update happens AFTER the swap; stale bin state was used for pricing
    _moveBins(currentState.activeTick, startingTick, lastTwa);
}
```

**Example 5: LP Reserve Ratio Manipulation for Undercollateralized Loan** [MEDIUM — Salty.IO, Code4rena]

Reference: [m-27-attacker-can-inflate-lp-position-value-to-create-a-bad-debt-loan.md](reports/dex_aggregator_findings/m-27-attacker-can-inflate-lp-position-value-to-create-a-bad-debt-loan.md)

```solidity
// ❌ VULNERABLE: LP value computed from manipulable reserve ratio
// Attacker inflates one side of the pool to boost apparent LP value
function getLPTokenValue(address pool, uint256 lpAmount) public view returns (uint256) {
    (uint256 reserveA, uint256 reserveB) = IPool(pool).getReserves();
    uint256 totalSupply = IPool(pool).totalSupply();

    // ← Both reserves are live and manipulable; no TWAP on the ratio
    uint256 valueA = (reserveA * lpAmount / totalSupply) * priceA / 1e18;
    uint256 valueB = (reserveB * lpAmount / totalSupply) * priceB / 1e18;
    return valueA + valueB;
    // Attacker adds massive one-sided liquidity → huge reserveA → LP value inflated
}
```

---

## Impact Analysis

### Technical Impact
- Premature/forced liquidations of healthy positions (2/6 reports)
- Undercollateralized loan creation via inflated LP collateral value (2/6 reports)
- Incorrect implied volatility → LTV manipulation → forced liquidations (1/6 reports)
- Stale price bin enabling favorable trade execution at expense of LPs (1/6 reports)

### Business Impact
- Protocol insolvency via bad debt accumulation from undercollateralized loans
- Liquidation cascade: attacker-induced liquidations trigger further price drops
- LP token holder losses when their collateral value is manipulated downward
- Competitive fairness violations when traders exploit stale pricing

### Affected Scenarios
- **Lending protocols** using Uniswap V3 TWAP or LP reserve prices as collateral oracle
- **Concentrated liquidity AMMs** with delayed bin/tick state updates
- **Multi-pool oracle systems** where a single low-TVL pool can control min/max price
- **Protocols accepting LP tokens as collateral** with reserve-based valuation

---

## Secure Implementation

**Fix 1: Use Longer TWAP Windows and Validate Against Chainlink** [Recommended]

```solidity
// ✅ SECURE: longer TWAP window + Chainlink cross-validation
contract PriceOracle {
    uint32 public constant MIN_TWAP_PERIOD = 30 minutes;  // minimum; adjust up for low-liquidity pools
    // Rule of thumb: TWAP period should resist attacks costing > protocol's TVL in collateral

    function getPrice(address pool) external view returns (uint256) {
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = MIN_TWAP_PERIOD;
        secondsAgos[1] = 0;
        (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
        int24 arithmeticMeanTick = int24(
            (tickCumulatives[1] - tickCumulatives[0]) / int56(uint56(MIN_TWAP_PERIOD))
        );
        uint256 twapPrice = _getQuoteAtTick(arithmeticMeanTick, BASE_AMOUNT, token0, token1);

        // Cross-validate TWAP against Chainlink; revert if deviation > threshold
        uint256 chainlinkPrice = _getChainlinkPrice();
        uint256 deviation = twapPrice > chainlinkPrice
            ? ((twapPrice - chainlinkPrice) * 1e18 / chainlinkPrice)
            : ((chainlinkPrice - twapPrice) * 1e18 / chainlinkPrice);
        require(deviation <= MAX_PRICE_DEVIATION, "oracle deviation too high");

        return twapPrice;
    }
}
```

**Fix 2: Use Invariant-Based LP Token Pricing (Not Live Reserves)**

```solidity
// ✅ SECURE: price LP tokens using external price feeds, not pool reserves
// This removes the flash-loan attack vector entirely
contract SecureLpAggregator {
    function latestAnswer() public view override returns (int256) {
        // Use Chainlink prices for both underlying assets (not pool reserves)
        uint256 basePrice = uint256(baseOracle.latestAnswer())
            * (10 ** (WAD - baseOracle.decimals()));
        uint256 quotePrice = uint256(quoteOracle.latestAnswer())
            * (10 ** (WAD - quoteOracle.decimals()));

        // Compute fair LP value using external prices + total supply
        // Formula: LP_price = 2 * sqrt(basePrice * quotePrice) * k^(1/2) / totalSupply
        // (Chainlink-style LP pricing using invariant k, not live reserves)
        uint256 totalSupply = pair.totalSupply();
        uint256 k = _getInvariant();  // k = reserveA * reserveB (not manipulable via flash)
        return int256(2 * Math.sqrt(basePrice * quotePrice * k) / totalSupply);
    }
}
```

**Fix 3: Multi-Pool Oracle with Minimum Agreement (Not Single-Pool Min/Max)**

```solidity
// ✅ SECURE: require majority of pools to agree within tolerance
function getPrice() external view returns (uint256 price) {
    uint256[] memory spotPrices = new uint256[](spotPools.length);
    uint256 anchorPrice = _getChainlinkAnchorPrice();
    uint256 validCount = 0;
    uint256 priceSum = 0;

    for (uint i = 0; i < spotPools.length; i++) {
        uint256 spotPrice = _getSpotPrice(spotPools[i]);
        uint256 deviation = spotPrice > anchorPrice
            ? (spotPrice - anchorPrice) * 1e18 / anchorPrice
            : (anchorPrice - spotPrice) * 1e18 / anchorPrice;

        if (deviation <= MAX_DEVIATION) {
            priceSum += spotPrice;
            validCount++;
        }
    }
    // Require majority of pools to be within tolerance
    require(validCount >= (spotPools.length * 2 / 3), "insufficient price consensus");
    price = priceSum / validCount;  // average of valid pools, not min/max
}
```

**Fix 4: Move Bins Before Swap (Maverick Pattern)**

```solidity
// ✅ SECURE: update bin state BEFORE executing swap logic
function swap(...) external returns (int256 delta0, int256 delta1) {
    uint256 currentState = _getCurrentState();
    int24 startingTick = currentState.activeTick;
    uint256 lastTwa = _getTwa();

    // ✅ Move bins FIRST, before any swap computation uses them
    _moveBins(currentState.activeTick, startingTick, lastTwa);

    // Now execute swap with up-to-date bin state
    // ... swap computation ...
    emit Swap(msg.sender, recipient, tokenAIn, exactOutput, amountIn, amountOut, currentState.activeTick);
}
```

---

## Detection Patterns

### Code Patterns to Search For

```
# TWAP windows that may be too short
grep -rn "TWAP_PERIOD\|twapPeriod\|secondsAgo\s*=\s*[0-9]" --include="*.sol" | grep -E "[0-9]+ (minutes|seconds)"

# Live reserve pricing for LP tokens (flash loan vulnerable)
grep -rn "getReserves\(\)" --include="*.sol" | grep -Ev "twap\|TWAP\|time_weighted"

# Single pool check that sets min/max price
grep -rn "minPrice\|maxPrice" --include="*.sol" | grep -v "require\|assert"

# Bin move after swap in concentrated liquidity
grep -rn "_moveBins\|moveBins" --include="*.sol"

# Fee-based IV oracle (manipulable via wash trades)
grep -rn "feeGrowthGlobal\|aggregatedFees\|feeGrowth" --include="*.sol" | grep -i "volatil\|iv\|ltv"
```

### Audit Checklist

- [ ] Is the TWAP observation window long enough to resist economically feasible attacks given pool liquidity?
- [ ] Are LP token prices derived from live `getReserves()` calls (flash-loan vulnerable)?
- [ ] Does the multi-pool oracle system fall back to a single pool's price for min/max?
- [ ] Is there a Chainlink cross-check to bound DEX-sourced prices?
- [ ] In concentrated liquidity AMMs, are price bins/ticks updated before swap computation?
- [ ] Can an attacker inflate TWAP-based implied volatility via wash trades in flashbots?
- [ ] Is the TWAP period sensitive to the liquidity level of the specific pool used?
- [ ] Does the protocol validate that the pool has sufficient TVL for the TWAP to be manipulation-resistant?

---

### Real-World Examples

- **Ouroboros 2024** — Short TWAP windows on low-liquidity ETH/TITANX and TITANX/DRAGONX pools — Pashov Audit Group 2024 — MEDIUM
- **Abracadabra Money (MagicLP)** — LP aggregator uses live pool reserves for price → flash loan manipulation — Code4rena 2024 — HIGH
- **f(x) v2** — Single low-TVL pool can bypass multi-pool anchor/deviation check → premature liquidations — OpenZeppelin 2024 — HIGH
- **Aloe Protocol** — Uniswap V3 fee growth manipulable as IV proxy → LTV decrease → forced liquidations — Sherlock 2023 — MEDIUM
- **Salty.IO** — Reserve ratio manipulation to create undercollateralized USDS loan — Code4rena 2024 — MEDIUM
- **Maverick** — Bin state updated post-swap creates price manipulation window — Code4rena 2022 — MEDIUM

---

### Keywords for Search

`uniswap twap manipulation`, `short twap window`, `low tvl oracle`, `lp token oracle manipulation`, `getReserves oracle`, `flash loan lp price`, `reserve ratio manipulation`, `twap period too short`, `concentrated liquidity oracle`, `bin movement after swap`, `maverick price manipulation`, `fee growth implied volatility`, `iv manipulation aloe`, `multi pool oracle bypass`, `spot price oracle`, `low liquidity twap attack`, `undercollateralized loan oracle`, `lp collateral manipulation`, `chainlink twap cross validation`, `abracadabra oracle`

### Related Vulnerabilities

- [DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md](DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md) — Flash loan oracle manipulation (broader)
- [DB/oracle/](DB/oracle/) — Oracle vulnerability patterns
- [DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md](DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md) — DEX aggregator call data exploitation
- [DB/amm/](DB/amm/) — AMM-specific vulnerabilities
