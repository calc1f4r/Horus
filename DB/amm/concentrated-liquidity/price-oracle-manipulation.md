---
title: "Price Oracle Manipulation in Concentrated Liquidity AMMs"
protocol: generic
category: amm/concentrated-liquidity
vulnerability_class: "Price Oracle Vulnerabilities"
vulnerability_type: price_oracle_manipulation
attack_type: oracle_manipulation|flash_loan|sandwich_attack
affected_component: price_oracle|twap_oracle|slot0_price_feed
severity: high
impact: fund_loss|unfair_liquidation|incorrect_valuation
chain: "Multi-chain"
affected_protocols:
  - "Uniswap V3/V4"
  - "PancakeSwap V3"
  - "Maverick"
  - "Panoptic"
  - "Aloe"
  - "Tokemak"
tags:
  - "slot0-manipulation"
  - "twap-bypass"
  - "oracle-attack"
  - "price-manipulation"
  - "sqrtPriceX96"
  - "observation-cardinality"
  - "tick-calculation"
last_updated: "2025-01-15"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | unknown | unknown

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _calculatePriceFromLiquidity
  - _gasSwapIn
  - _getOracleData
  - _getReferencePoolPriceX96
  - beforeSwap
  - consult
  - deployNewPool
  - getPriceInEth
  - getPriceUnsafe
  - getTWAPPrice
  - liquidate
  - observe
  - reallocate
  - rebalance
  - repay
  - safeObserve
  - setPositionTicks
  - swap
  - totalSupply
  - validateAndGetPrice
---

# Price Oracle Manipulation in Concentrated Liquidity AMMs

## Overview

Concentrated liquidity AMMs like Uniswap V3 provide on-chain price data through two primary mechanisms: spot prices via `slot0` and time-weighted average prices (TWAP) via the observation oracle. Both mechanisms have distinct vulnerability patterns that protocols integrating these AMMs frequently mishandle.

**Root Cause Statement:**
> "This vulnerability exists because protocols use spot prices from `slot0` or improperly configured TWAP oracles to derive critical values for swaps, liquidations, collateral calculations, and position management, allowing MEV bots and attackers to manipulate prices via flash loans and sandwich attacks leading to loss of funds, unfair liquidations, and incorrect valuations."

**Observed Frequency:** 68+ reports analyzed covering slot0 manipulation, TWAP bypasses, oracle cardinality attacks, and tick calculation errors.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | unknown | unknown`
- Interaction scope: `single_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `_calculatePriceFromLiquidity`, `_gasSwapIn`, `_getOracleData`, `_getReferencePoolPriceX96`, `beforeSwap`, `consult`, `deployNewPool`, `getPriceInEth`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `DualPriceOracle.function -> SecureOracle.function`
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

#### Code Patterns to Look For

```solidity
(uint160 sqrtPriceX96,,,,,,) = pool.slot0();
uint256 price = FullMath.mulDiv(uint256(sqrtPriceX96) * sqrtPriceX96, 1e18, 1 << 192);

(int56[] memory ticks,) = pool.observe(secondsAgos); // secondsAgos too short or cardinality attacker-controlled
factory.deployPool(token0, token1, fee, initialSqrtPriceX96); // initial spot price becomes trusted state
oracle.getPriceUnsafe(pool); // price feeds liquidations, collateral, or swaps
```

#### False Positive Detail

- Direct `slot0` reads are not automatically exploitable when used only for UI quotes or bounded hints; prioritize reads that determine collateral value, liquidation eligibility, swap limits, mint/burn amounts, or accounting.
- TWAP usage is still suspect when the window is short, observation cardinality can be cheaply changed, negative ticks are rounded the wrong way, or decimal normalization differs by token.
- Flash-loan manipulation requires sufficient pool price impact or thin liquidity on the trusted pool; deep liquidity plus independent sanity bounds lowers severity.

## Vulnerable Pattern Examples

### Pattern 1: Direct slot0 Usage for Price-Sensitive Operations (HIGH - 12+ reports)

Using `slot0.sqrtPriceX96` directly for swap calculations, liquidity allocations, or collateral valuations exposes protocols to single-block price manipulation.

**Reference**: [h-01-usage-of-slot0-to-get-sqrtpricelimitx96-is-extremely-prone-to-manipulation.md](../../../reports/constant_liquidity_amm/h-01-usage-of-slot0-to-get-sqrtpricelimitx96-is-extremely-prone-to-manipulation.md) (Shieldify - Steakhut, HIGH)

```solidity
// VULNERABLE: Direct slot0 usage in price calculation
function _calculatePriceFromLiquidity(address _pool) internal view returns (uint256) {
    IUniswapV3Pool pool = IUniswapV3Pool(_pool);
    (uint160 sqrtPriceX96,,,,,,) = pool.slot0();  // @audit easily manipulated
    
    uint256 _sqrtPriceX96_1 = uint256(sqrtPriceX96) * (uint256(sqrtPriceX96)) * (1e18) >> (96 * 2);
    return _sqrtPriceX96_1;
}
```

**Reference**: [h-02-use-of-slot0-to-get-sqrtpricelimitx96-can-lead-to-price-manipulation.md](../../../reports/constant_liquidity_amm/h-02-use-of-slot0-to-get-sqrtpricelimitx96-can-lead-to-price-manipulation.md) (Code4rena - Maia DAO, HIGH)

```solidity
// VULNERABLE: slot0 used to calculate swap limits
function _gasSwapIn() internal {
    (uint160 sqrtPriceX96,,,,,,) = IUniswapV3Pool(poolAddress).slot0();
    
    // Calculate Price limit depending on pre-set price impact
    uint160 exactSqrtPriceImpact = (sqrtPriceX96 * (priceImpactPercentage / 2)) / GLOBAL_DIVISIONER;
    uint160 sqrtPriceLimitX96 = zeroForOneOnInflow ? sqrtPriceX96 - exactSqrtPriceImpact : sqrtPriceX96 + exactSqrtPriceImpact;
    
    // Attacker manipulates sqrtPriceX96 → user swaps at unfavorable price
    IUniswapV3Pool(poolAddress).swap(
        address(this),
        zeroForOneOnInflow,
        int256(_amount),
        sqrtPriceLimitX96,  // @audit derived from manipulated price
        abi.encode(SwapCallbackData({tokenIn: gasTokenGlobalAddress}))
    );
}
```

---

### Pattern 2: slot0-Based Reallocation/Rebalancing (HIGH - 9+ reports)

Using spot prices to trigger position reallocation or rebalancing allows attackers to force unfavorable reallocations.

**Reference**: [h-01-reallocation-depends-on-the-slot0-price-which-can-be-manipulated.md](../../../reports/constant_liquidity_amm/h-01-reallocation-depends-on-the-slot0-price-which-can-be-manipulated.md) (Code4rena - Predy, HIGH)

```solidity
// VULNERABLE: Permissionless reallocation based on spot price
function reallocate(
    DataType.PairStatus storage _assetStatusUnderlying,
    SqrtPerpAssetStatus storage _sqrtAssetStatus
) internal returns (bool, bool, int256 deltaPositionBase, int256 deltaPositionQuote) {
    // Uses slot0 for current price - can be manipulated
    (uint160 currentSqrtPrice, int24 currentTick,,,,,) = IUniswapV3Pool(_sqrtAssetStatus.uniswapPool).slot0();
    
    // Determines if rebalance is needed based on manipulable tick
    if (currentTick < _sqrtAssetStatus.tickLower) {
        isOutOfRange = true;
        tick = _sqrtAssetStatus.tickLower;
    } else if (currentTick < _sqrtAssetStatus.tickUpper) {
        isOutOfRange = false;
    } else {
        isOutOfRange = true;
        tick = _sqrtAssetStatus.tickUpper;
    }
    
    // Attacker manipulates price → forces unfavorable reallocation → drains fees
}
```

---

### Pattern 3: slot0 Tick for Position Tick Setting (HIGH)

Using the tick from slot0 rather than deriving tick from sqrtPriceX96 causes asymmetric positions at tick boundaries.

**Reference**: [h-2-strategy-main-ticks-are-set-according-to-the-tick-in-slot0-leading-to-incorr.md](../../../reports/constant_liquidity_amm/h-2-strategy-main-ticks-are-set-according-to-the-tick-in-slot0-leading-to-incorr.md) (Sherlock - Yieldoor, HIGH)

```solidity
// VULNERABLE: Using slot0 tick directly
function rebalance() external {
    (uint160 sqrtPriceX96, int24 tick,,,,,) = pool.slot0();
    
    // Problem: When price is exactly at tick boundary, tick value is off by 1
    // sqrtPriceX96 might equal getSqrtRatioAtTick(tick + 1), not tick
    // This causes asymmetric position allocation
    
    int24 tickLower = tick - tickSpacing;
    int24 tickUpper = tick + tickSpacing;
    // Position is NOT symmetric around actual price
}
```

---

### Pattern 4: TWAP Observation Cardinality Manipulation (HIGH)

Exploiting uninitialized observations in the Uniswap V3 observation array to corrupt TWAP calculations.

**Reference**: [h-2-oraclesol-manipulation-via-increasing-uniswap-v3-pool-observationcardinality.md](../../../reports/constant_liquidity_amm/h-2-oraclesol-manipulation-via-increasing-uniswap-v3-pool-observationcardinality.md) (Sherlock - Aloe, HIGH)

```solidity
// VULNERABLE: Not checking if observations are initialized
function observe(uint32 ago, uint256 seed) internal view returns (...) {
    // Attacker increases observationCardinality
    // New slots have timestamp = 1, other values = 0
    
    // Oracle reads uninitialized observation as valid data
    // Corrupted tickCumulatives used in TWAP calculation
    
    // Example: Array [12, 20, 25, 30, 1, 1, 1]
    // If seed points to uninitialized slot with timestamp 1,
    // wrong interpolation occurs
}

// SECURE: Check initialized field
function observe(uint32 ago, uint256 seed) internal view returns (...) {
    Observation memory obs = observations[index];
    require(obs.initialized, "Uninitialized observation");
    // Continue with valid observation
}
```

---

### Pattern 5: Negative Tick Delta Rounding Error (HIGH - 19+ reports)

Failing to round down for negative tick deltas when calculating TWAP causes incorrect price.

**Reference**: [h-05-_getreferencepoolpricex96-will-show-incorrect-price-for-negative-tick-delta.md](../../../reports/constant_liquidity_amm/h-05-_getreferencepoolpricex96-will-show-incorrect-price-for-negative-tick-delta.md) (Code4rena - Revert Lend, HIGH)

**Reference**: [m-03-incorrect-price-for-negative-ticks-due-to-lack-of-rounding-down.md](../../../reports/constant_liquidity_amm/m-03-incorrect-price-for-negative-ticks-due-to-lack-of-rounding-down.md) (Code4rena - Predy, MEDIUM)

```solidity
// VULNERABLE: No rounding for negative tick deltas
function _getReferencePoolPriceX96(IUniswapV3Pool pool, uint32 twapSeconds) internal view returns (uint256) {
    uint32[] memory secondsAgos = new uint32[](2);
    secondsAgos[0] = 0;
    secondsAgos[1] = twapSeconds;
    (int56[] memory tickCumulatives,) = pool.observe(secondsAgos);
    
    // @audit Missing rounding for negative deltas!
    int24 tick = int24((tickCumulatives[0] - tickCumulatives[1]) / int56(uint56(twapSeconds)));
    sqrtPriceX96 = TickMath.getSqrtRatioAtTick(tick);
}

// SECURE: Round down for negative deltas (Uniswap OracleLibrary pattern)
function consult(address pool, uint32 secondsAgo) internal view returns (int24 arithmeticMeanTick) {
    int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
    
    arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(secondsAgo)));
    // Always round to negative infinity
    if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(uint56(secondsAgo)) != 0)) {
        arithmeticMeanTick--;
    }
}
```

---

### Pattern 6: Insufficient TWAP Duration (MEDIUM)

Using TWAP windows that are too short (< 30 minutes) makes manipulation economically viable.

**Reference**: [m-10-taporacle-twap-duration-for-uniswap-oracle-should-be-at-least-30-mins.md](../../../reports/constant_liquidity_amm/m-10-taporacle-twap-duration-for-uniswap-oracle-should-be-at-least-30-mins.md) (Pashov - TapiocaDAO, MEDIUM)

```solidity
// VULNERABLE: 10-minute TWAP window
const args = [
    'TAP/USDC',
    // ... other args ...
    600,  // @audit 10 minutes is too short - should be 1800+ (30 mins)
    10,   // observation length
    // ...
];

// Attack feasibility increases with:
// 1. Low liquidity in pool
// 2. Short TWAP window
// 3. Multi-block MEV (validator controlling consecutive blocks)
```

**Reference**: [m-06-uniswap-oracle-prices-can-be-manipulated.md](../../../reports/constant_liquidity_amm/m-06-uniswap-oracle-prices-can-be-manipulated.md) (Pashov - Ouroboros, MEDIUM)

```solidity
// VULNERABLE: 36-second short TWAP, 5-minute long TWAP
uint32 shortTwapSeconds = 36 seconds;  // @audit Way too short
uint32 longTwapSeconds = 5 minutes;    // @audit Still manipulable

// Low liquidity ($4.7M) + short TWAP = feasible manipulation
// Multi-pool oracle (ETH/TITANX + TITANX/DRAGONX) amplifies manipulation
```

---

### Pattern 7: Reserve-Based Oracle Pricing (HIGH)

Using pool reserves directly for LP token pricing instead of manipulation-resistant sources.

**Reference**: [h-15-maverick-oracle-can-be-manipulated.md](../../../reports/constant_liquidity_amm/h-15-maverick-oracle-can-be-manipulated.md) (Sherlock - Tokemak, HIGH)

```solidity
// VULNERABLE: Using manipulable reserves for pricing
function getPriceInEth(address boostedPosition) external view returns (uint256) {
    // Reserves change with swaps - can be manipulated with flash loans
    (uint256 reserveTokenA, uint256 reserveTokenB) = boostedPosition.getReserves();
    uint256 boostedPositionTotalSupply = boostedPosition.totalSupply();
    
    // External prices are correct, but reserves are manipulated
    uint256 priceInEthTokenA = rootPriceOracle.getPriceInEth(address(pool.tokenA()));
    uint256 priceInEthTokenB = rootPriceOracle.getPriceInEth(address(pool.tokenB()));
    
    // Attack: Flash loan → swap to change reserves → inflate/deflate LP price
    return (reserveTokenA * priceInEthTokenA + reserveTokenB * priceInEthTokenB) / boostedPositionTotalSupply;
}
```

---

### Pattern 8: Decimal Mismatch in sqrtPriceX96 Calculation (HIGH)

Hardcoding decimal divisors instead of dynamically calculating based on token decimals.

**Reference**: [h-06-discrepency-in-the-uniswap-v3-position-price-calculation-because-of-decimal.md](../../../reports/constant_liquidity_amm/h-06-discrepency-in-the-uniswap-v3-position-price-calculation-because-of-decimal.md) (Code4rena - ParaSpace, HIGH)

```solidity
// VULNERABLE: Hardcoded 1e9 divisor ignores decimal differences
function _getOracleData(...) internal view returns (...) {
    if (token1Decimal == token0Decimal) {
        sqrtPriceX96 = uint160(
            (SqrtLib.sqrt(((token0Price * (10**18)) / (token1Price))) * 2**96) / 1E9
        );
    } else if (token1Decimal > token0Decimal) {
        // @audit 1E9 should be 10**(9 + token1Decimal - token0Decimal)
        sqrtPriceX96 = uint160(
            (SqrtLib.sqrt((token0Price * (10**(18 + token1Decimal - token0Decimal))) / (token1Price)) * 2**96) / 1E9
        );
    }
    // When token1Decimal > token0Decimal, price is MASSIVELY inflated
}
```

---

### Pattern 9: Spot Price in Factory/Deployment (MEDIUM)

Using spot prices during pool deployment for initial liquidity calculations.

**Reference**: [m-01-panopticfactory-uses-spot-price-when-deploying-new-pools-resulting-in-liqui.md](../../../reports/constant_liquidity_amm/m-01-panopticfactory-uses-spot-price-when-deploying-new-pools-resulting-in-liqui.md) (Code4rena - Panoptic, MEDIUM)

```solidity
// VULNERABLE: Spot price for deployment liquidity calculation
function deployNewPool(...) external {
    (uint160 currentSqrtPriceX96, , , , , , ) = v3Pool.slot0();  // @audit manipulable
    
    uint128 fullRangeLiquidity;
    if (token0 == WETH) {
        fullRangeLiquidity = uint128(
            Math.mulDiv96RoundingUp(FULL_RANGE_LIQUIDITY_AMOUNT_WETH, currentSqrtPriceX96)
        );
    }
    // Attacker manipulates price → deployer deposits unfavorable token ratios
}
```

---

### Pattern 10: Hook/Callback Price Manipulation (HIGH)

Using current prices in swap hooks/callbacks for fee distribution or other calculations.

**Reference**: [h-17-uniswapimplementationbeforeswap-is-vulnerable-to-price-manipulation-attack.md](../../../reports/constant_liquidity_amm/h-17-uniswapimplementationbeforeswap-is-vulnerable-to-price-manipulation-attack.md) (Sherlock - Flayer, HIGH)

```solidity
// VULNERABLE: Hook uses current price for fee swap
function beforeSwap(...) public override returns (...) {
    if (trigger && pendingPoolFees.amount1 != 0) {
        // Current price is used - can be manipulated in same tx
        (uint160 sqrtPriceX96,,,) = poolManager.getSlot0(poolId);
        
        // Attack:
        // 1. Sell tokens to decrease price
        // 2. Trigger swap that uses discounted price for fee conversion
        // 3. Buy tokens back
        // Result: Attacker gets more value from fee conversion
        
        (, ethIn, tokenOut, ) = SwapMath.computeSwapStep({
            sqrtPriceCurrentX96: sqrtPriceX96,  // @audit manipulated
            // ...
        });
    }
}
```

---

## Secure Implementation Examples

### Secure Pattern 1: TWAP Oracle with Proper Configuration

```solidity
// SECURE: Use TWAP with adequate duration and validation
contract SecureOracle {
    uint32 public constant MIN_TWAP_SECONDS = 1800; // 30 minutes minimum
    
    function getTWAPPrice(address pool, uint32 twapSeconds) public view returns (uint256) {
        require(twapSeconds >= MIN_TWAP_SECONDS, "TWAP too short");
        
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = twapSeconds;
        secondsAgos[1] = 0;
        
        (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
        
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        int24 arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(twapSeconds)));
        
        // Critical: Round to negative infinity for negative deltas
        if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(uint56(twapSeconds)) != 0)) {
            arithmeticMeanTick--;
        }
        
        return TickMath.getSqrtRatioAtTick(arithmeticMeanTick);
    }
}
```

### Secure Pattern 2: Dual Price Validation

```solidity
// SECURE: Compare spot vs TWAP with deviation check
contract DualPriceOracle {
    uint256 public constant MAX_DEVIATION_BPS = 500; // 5% max
    
    function validateAndGetPrice(address pool) external view returns (uint160 sqrtPriceX96) {
        // Get spot price
        (uint160 spotSqrtPriceX96,,,,,,) = IUniswapV3Pool(pool).slot0();
        
        // Get TWAP price
        uint160 twapSqrtPriceX96 = getTWAPPrice(pool, 1800);
        
        // Calculate deviation
        uint256 deviation;
        if (spotSqrtPriceX96 > twapSqrtPriceX96) {
            deviation = ((spotSqrtPriceX96 - twapSqrtPriceX96) * 10000) / twapSqrtPriceX96;
        } else {
            deviation = ((twapSqrtPriceX96 - spotSqrtPriceX96) * 10000) / twapSqrtPriceX96;
        }
        
        require(deviation <= MAX_DEVIATION_BPS, "Price deviation too high");
        
        // Use more conservative (lower for collateral) price
        return spotSqrtPriceX96 < twapSqrtPriceX96 ? spotSqrtPriceX96 : twapSqrtPriceX96;
    }
}
```

### Secure Pattern 3: sqrtPrice-Based Tick Derivation

```solidity
// SECURE: Derive tick from sqrtPriceX96 for accurate positioning
function setPositionTicks() internal view returns (int24 tickLower, int24 tickUpper) {
    (uint160 sqrtPriceX96, int24 slotTick,,,,,) = pool.slot0();
    
    // Don't use slotTick directly - derive from sqrtPriceX96
    int24 actualTick = TickMath.getTickAtSqrtRatio(sqrtPriceX96);
    
    // Round to tick spacing
    int24 tickSpacing = pool.tickSpacing();
    int24 roundedTick = (actualTick / tickSpacing) * tickSpacing;
    
    tickLower = roundedTick - (tickSpacing * 2);
    tickUpper = roundedTick + (tickSpacing * 2);
}
```

### Secure Pattern 4: Initialized Observation Check

```solidity
// SECURE: Validate observation is initialized before use
function safeObserve(
    IUniswapV3Pool pool,
    uint32 ago
) internal view returns (int56 tickCumulative, uint160 secondsPerLiquidityCumulativeX128) {
    uint32[] memory secondsAgos = new uint32[](1);
    secondsAgos[0] = ago;
    
    // Use pool's observe which handles initialization checks
    (int56[] memory tickCumulatives, uint160[] memory secondsPerLiquidityCumulativeX128s) = 
        pool.observe(secondsAgos);
    
    // Additional: verify the observation index is within initialized range
    (, , uint16 observationIndex, uint16 observationCardinality,,,) = pool.slot0();
    require(observationCardinality > 0, "No observations");
    
    return (tickCumulatives[0], secondsPerLiquidityCumulativeX128s[0]);
}
```

---

## Impact Analysis

### Technical Impact

| Impact Type | Severity | Description |
|-------------|----------|-------------|
| Price Manipulation | HIGH | Attackers control sqrtPriceX96 via flash loans/large swaps |
| State Corruption | HIGH | Incorrect prices propagate through collateral/liquidation logic |
| Oracle Poisoning | HIGH | Corrupted TWAP calculations from uninitialized observations |
| Calculation Errors | MEDIUM | Wrong tick rounding causes ~0.01% price deviation per tick |

### Financial Impact

1. **Unfair Liquidations** (8/68 reports) - Manipulated prices liquidate healthy positions
2. **Value Extraction** (12/68 reports) - Attackers extract value via sandwich attacks on protocol swaps
3. **Incorrect Collateral Valuation** (6/68 reports) - Over/undervalued LP positions in lending
4. **Fee Theft** (4/68 reports) - Discounted fee conversions via price manipulation

### Attack Scenarios

1. **Sandwich Attack on Protocol Swaps**
   - Attacker sees protocol swap in mempool
   - Front-run: manipulate slot0.sqrtPriceX96
   - Protocol executes swap at unfavorable price
   - Back-run: restore price and profit

2. **Flash Loan Reallocation Attack**
   - Flash loan large amount
   - Swap to move price out of position range
   - Trigger permissionless reallocation
   - Reverse swap, repay flash loan
   - Position now has suboptimal allocation

3. **Multi-Block TWAP Manipulation**
   - Validator controls 2-3 consecutive blocks
   - Manipulate price for duration of blocks
   - Sufficient to skew short TWAP windows
   - Execute profitable trades based on manipulated oracle

---

## Detection Patterns

### Static Analysis

```yaml
# Semgrep rule for slot0 usage detection
rules:
  - id: slot0-price-usage
    patterns:
      - pattern: |
          $POOL.slot0()
      - pattern-not-inside: |
          require($TWAP_CHECK, ...)
    message: "Direct slot0 usage without TWAP validation - potential manipulation"
    severity: WARNING
```

### Manual Audit Checklist

- [ ] Is `slot0.sqrtPriceX96` used for price-sensitive operations?
- [ ] Is TWAP duration at least 30 minutes?
- [ ] Are negative tick deltas rounded down (toward negative infinity)?
- [ ] Are observation initialization checks performed?
- [ ] Is there spot vs TWAP deviation validation?
- [ ] Are token decimals handled correctly in price calculations?
- [ ] Are reallocation/rebalance functions permissioned or rate-limited?
- [ ] Is price validated before critical operations (liquidations, swaps)?

---

## Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|--------------|----------|------------|------|
| Steakhut | slot0 for price calculation | HIGH | Shieldify | 2024 |
| Maia DAO | slot0 for swap limits | HIGH | Code4rena | 2023 |
| Predy | slot0 for reallocation trigger | HIGH | Code4rena | 2024 |
| Aloe | Observation cardinality manipulation | HIGH | Sherlock | 2023 |
| Revert Lend | Missing negative tick rounding | HIGH | Code4rena | 2024 |
| Tokemak | Reserve-based LP pricing | HIGH | Sherlock | 2023 |
| ParaSpace | Decimal mismatch in sqrtPrice | HIGH | Code4rena | 2022 |
| Panoptic | Spot price in factory | MEDIUM | Code4rena | 2024 |
| TapiocaDAO | 10-min TWAP too short | MEDIUM | Pashov | 2024 |
| Yieldoor | slot0 tick vs sqrtPrice tick | HIGH | Sherlock | 2025 |
| Flayer | Hook price manipulation | HIGH | Sherlock | 2024 |
| GammaSwap | Spot price for collateral | MEDIUM | Pashov | 2024 |
| Ouroboros | Short TWAP + low liquidity | MEDIUM | Pashov | 2024 |

---

## Keywords for Search

**Primary Terms:** slot0, sqrtPriceX96, price manipulation, oracle manipulation, TWAP bypass

**Oracle Terms:** observationCardinality, tickCumulatives, getPriceUnsafe, observe, observation array

**Attack Vectors:** sandwich attack, flash loan manipulation, MEV, frontrunning, multi-block attack

**Impacts:** unfair liquidation, collateral manipulation, value extraction, oracle poisoning

**Related APIs:** slot0(), observe(), getSqrtRatioAtTick(), getTickAtSqrtRatio(), OracleLibrary

**Code Patterns:** missing TWAP validation, hardcoded decimals, no initialization check, missing rounding

**Protocol Examples:** uniswap_v3, uniswap_v4, maia_dao, aloe, predy, panoptic, tokemak, revert_lend, steakhut, paraspace

---

## Related Vulnerabilities

- [Tick Range Position Vulnerabilities](./tick-range-position-vulnerabilities.md) - Tick boundary issues
- [Slippage Sandwich Frontrun](./slippage-sandwich-frontrun.md) - MEV attack patterns
- [Fee Collection Distribution](./fee-collection-distribution.md) - Fee manipulation via price

---

## References

1. [Uniswap V3 OracleLibrary](https://github.com/Uniswap/v3-periphery/blob/main/contracts/libraries/OracleLibrary.sol)
2. [Uniswap TWAP Oracle Study](https://blog.uniswap.org/uniswap-v3-oracles)
3. [Euler TWAP Parameters](https://docs.euler.finance/euler-protocol/eulers-default-parameters#twap-length)
4. [Rari Fuse VUSD Hack Analysis](https://cmichel.io/replaying-ethereum-hacks-rari-fuse-vusd-price-manipulation/)

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

`_calculatePriceFromLiquidity`, `_gasSwapIn`, `_getOracleData`, `_getReferencePoolPriceX96`, `beforeSwap`, `consult`, `deployNewPool`, `getPriceInEth`, `getPriceUnsafe`, `getTWAPPrice`, `liquidate`, `observation-cardinality`, `observe`, `oracle-attack`, `price-manipulation`, `reallocate`, `rebalance`, `repay`, `safeObserve`, `setPositionTicks`, `slot0-manipulation`, `sqrtPriceX96`, `swap`, `tick-calculation`, `totalSupply`, `twap-bypass`, `validateAndGetPrice`
