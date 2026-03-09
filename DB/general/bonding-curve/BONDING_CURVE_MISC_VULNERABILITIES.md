---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bonding_curve
vulnerability_type: miscellaneous

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error|oracle_manipulation|flash_loan
affected_component: oracle|twap|stablecoin|rebalance|wash_trading|flash_loan|batch_operations|configuration

# Technical Primitives (Required)
primitives:
  - bonding_curve
  - oracle
  - twap
  - stablecoin
  - rebalance
  - wash_trading
  - flash_loan
  - batch_operations
  - selfdestruct
  - downcast
  - supply_invariant
  - collateral_depeg
  - rate_limiting
  - kerosene
  - self_liquidation
  - curve_metapool

# Impact Classification (Required)
severity: critical
impact: fund_loss|manipulation|dos|value_leak
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - defi
  - bonding_curve
  - oracle
  - flash_loan
  - stablecoin
  - rebalance
  - wash_trading
  - miscellaneous

# Version Info
language: solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Oracle & TWAP Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| USSD - Oracle USD vs DAI Denomination | `reports/bonding_curve_findings/h-11-oracle-price-should-be-denominated-in-dai-instead-of-usd.md` | HIGH | Sherlock |
| Ubiquity - Stale TWAP Oracle | `reports/bonding_curve_findings/m-1-libubiquitypoolmintdollarredeemdollar-reliance-on-outdated-twap-oracle-may-b.md` | MEDIUM | Sherlock |

### Flash Loan Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DYAD - Flash Loan Protection Bypass via Self-Liquidation | `reports/bonding_curve_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md` | HIGH | Code4rena |

### Rebalancing & Reward Exploits
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Arrakis V2 - Rebalance Rate Limiting Missing | `reports/bonding_curve_findings/m-2-lack-of-rebalance-rate-limiting-allow-operators-to-drain-vaults.md` | MEDIUM | Sherlock |
| Primex - Wash Trading to Steal Rewards | `reports/bonding_curve_findings/wash-trades-to-steal-keeper-and-spot-trading-rewards.md` | MEDIUM | Sherlock |

### Batch Operation & Configuration Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Dria - Batch Purchase Failure | `reports/bonding_curve_findings/buyeragent-batch-purchase-failure-due-to-asset-transfer-or-approval-revocation.md` | MEDIUM | Code4rena |
| GTE - Supply Downcast Breaks Invariant | `reports/bonding_curve_findings/m-30-bonding-curve-invariant-can-be-broken-due-to-unsafely-down-casting-supply-to.md` | MEDIUM | Code4rena |

---

# Bonding Curve Miscellaneous Vulnerabilities

**Patterns for Oracle Misuse, Flash Loan Bypasses, Stablecoin Peg Issues, Rebalancing Exploits, Wash Trading, and Configuration Errors in Bonding Curve Protocols**

---

## Table of Contents

1. [Oracle Price Denomination Mismatch (USD vs DAI)](#1-oracle-price-denomination-mismatch-usd-vs-dai)
2. [Stale TWAP Oracle Due to Unpoked Metapool](#2-stale-twap-oracle-due-to-unpoked-metapool)
3. [Flash Loan Protection Bypass via Self-Liquidation](#3-flash-loan-protection-bypass-via-self-liquidation)
4. [Rebalance Rate Limiting Missing — Vault Drainage](#4-rebalance-rate-limiting-missing--vault-drainage)
5. [Wash Trading to Steal Keeper/Spot Trading Rewards](#5-wash-trading-to-steal-keeperspot-trading-rewards)
6. [Batch Operation Fails Atomically on Single Asset](#6-batch-operation-fails-atomically-on-single-asset)
7. [Unsafe Downcast Breaks Supply Invariant](#7-unsafe-downcast-breaks-supply-invariant)
8. [Collateral Depeg Cascading to Bonding Curve](#8-collateral-depeg-cascading-to-bonding-curve)
9. [Asymmetric Base/Quote Treatment in Virtual Bonding Curve](#9-asymmetric-basequote-treatment-in-virtual-bonding-curve)
10. [Protocol Fees Stuck After Graduation](#10-protocol-fees-stuck-after-graduation)
11. [Token Supply Not Correctly Burned on Graduation](#11-token-supply-not-correctly-burned-on-graduation)
12. [Graduation Stuck Due to Third-Party Contract Interference](#12-graduation-stuck-due-to-third-party-contract-interference)

---

## 1. Oracle Price Denomination Mismatch (USD vs DAI)

### Overview

A stablecoin bonding curve pegged to DAI uses all oracle price feeds denominated in USD instead of DAI. When DAI depegs upward (e.g., DAI > $1.01), the system moves *away* from the peg instead of toward it, because it believes the stablecoin is worth more USD than it actually is worth in DAI.

> 📖 Reference: `reports/bonding_curve_findings/h-11-oracle-price-should-be-denominated-in-dai-instead-of-usd.md`

### Vulnerability Description

#### Root Cause
All oracles (WETH, WBTC, DAI, USDC) return USD price, but the stablecoin targets DAI peg. `getOwnValuation()` divides by the DAI/USD rate, which is imprecise and inverted during depegs.

### Vulnerable Pattern Examples

**Example 1: USD Oracle for DAI-Pegged Stablecoin** [HIGH]
```solidity
// ❌ VULNERABLE: All oracle feeds return USD prices, protocol is pegged to DAI
contract StableOracleWETH {
    function getPriceUSD() external view returns (uint256) {
        // Returns WETH/USD — not WETH/DAI!
        return chainlinkFeed.latestAnswer() * 1e10;
    }
}

function getOwnValuation() internal view returns (uint256) {
    // Uses USD-denominated pool price as if it's DAI
    uint256 usdPrice = pool.getPrice();
    // When DAI = $1.05: system thinks stablecoin is above peg, sells to push down
    // Actually: stablecoin is correctly priced in DAI but USD oracle is wrong
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Use DAI-denominated oracles
contract StableOracleWETH {
    function getPriceDAI() external view returns (uint256) {
        uint256 wethUsd = chainlinkFeed.latestAnswer();
        uint256 daiUsd = daiOracle.latestAnswer();
        return (wethUsd * 1e18) / daiUsd;  // WETH/DAI price
    }
}
```

### Detection Patterns
```
- Stablecoin pegged to DAI/USDC but oracle feeds in USD
- getOwnValuation() using pool price without DAI adjustment
- Rebalancing logic that drives price in wrong direction during collateral depeg
```

---

## 2. Stale TWAP Oracle Due to Unpoked Metapool

### Overview

When a TWAP oracle reads cumulative balances from a Curve metapool, but the metapool's internal `_update()` is never triggered, the TWAP values remain stale. Minting/burning decisions based on stale TWAP can be exploited.

> 📖 Reference: `reports/bonding_curve_findings/m-1-libubiquitypoolmintdollarredeemdollar-reliance-on-outdated-twap-oracle-may-b.md`

### Vulnerable Pattern Examples

**Example 1: TWAP Reads Stale Cumulative Balances** [MEDIUM]
```solidity
// ❌ VULNERABLE: Reads stale cumulative balances from metapool
function update() internal {
    // LibTWAPOracle.sol — called during mintDollar/redeemDollar
    uint256[2] memory balances = IMetaPool(ts.pool).get_balances();
    // But the metapool's cumulative balance wasn't updated since last interaction!
    // If no one trades on the pool, TWAP is stale for hours/days
    ts.priceCumulativeLast = [balances[0] * timeElapsed, balances[1] * timeElapsed];
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Poke the metapool before reading TWAP
function update() internal {
    // Force metapool to update cumulative balances
    IMetaPool(ts.pool).remove_liquidity(0, [uint256(0), uint256(0)]);
    
    // Now read fresh cumulative balances
    uint256[2] memory balances = IMetaPool(ts.pool).get_balances();
    ts.priceCumulativeLast = [balances[0] * timeElapsed, balances[1] * timeElapsed];
}
```

### Detection Patterns
```
- TWAP oracle reading from a Curve/Uniswap pool without poking it first
- consult() or update() that trusts cumulative values without freshness guarantee
- Mint/burn gated by TWAP that may be stale
```

---

## 3. Flash Loan Protection Bypass via Self-Liquidation

### Overview

Flash loan protection using `idToBlockOfLastDeposit` blocks same-block withdrawals after deposits. But if `liquidate()` uses `vault.move()` which doesn't update the deposit tracker for the recipient, a self-liquidation can bypass the protection entirely.

> 📖 Reference: `reports/bonding_curve_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md`

### Vulnerability Description

#### Root Cause
`deposit()` sets `idToBlockOfLastDeposit[id] = block.number`. `withdraw()` checks this. But `liquidate → vault.move(id, to, amount)` doesn't update `idToBlockOfLastDeposit[to]`, so the recipient account (controlled by attacker) can withdraw immediately.

#### Attack Scenario
1. Flash-borrow collateral
2. `deposit(accountA, collateral)` — sets `idToBlockOfLastDeposit[A] = block.number`
3. Manipulate price (e.g., kerosene price) to make accountA liquidatable
4. `liquidate(accountA, accountB)` — calls `vault.move(A, B, collateral)`
5. `withdraw(accountB, collateral)` — passes because `idToBlockOfLastDeposit[B]` was never set
6. Repay flash loan with profit

### Vulnerable Pattern Examples

**Example 1: Move Doesn't Update Deposit Tracker** [HIGH]
```solidity
// ❌ VULNERABLE: vault.move() doesn't update idToBlockOfLastDeposit for recipient
function deposit(uint256 id, uint256 amount) external {
    idToBlockOfLastDeposit[id] = block.number;
    // ... transfer collateral in ...
}

function withdraw(uint256 id, uint256 amount) external {
    if (idToBlockOfLastDeposit[id] == block.number) revert DepositedInSameBlock();
    // ... transfer collateral out ...
}

function liquidate(uint256 id, uint256 to) external {
    vault.move(id, to, collateral);  // No idToBlockOfLastDeposit update for 'to'!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Update deposit tracker in move()
function move(uint256 from, uint256 to, uint256 amount) external {
    idToBlockOfLastDeposit[to] = block.number;  // Block same-block withdrawal
    // ... transfer logic ...
}
```

### Detection Patterns
```
- idToBlockOfLastDeposit or similar flash loan guard
- move/transfer functions that don't update the flash loan tracker
- Self-liquidation enabling same-block deposit-withdraw cycle
```

---

## 4. Rebalance Rate Limiting Missing — Vault Drainage

### Overview

When `rebalance()` enforces slippage per call (~1%) but has no rate limit, a malicious operator can call it hundreds of times in one transaction, compounding the slippage loss to drain an arbitrarily large share of vault funds.

> 📖 Reference: `reports/bonding_curve_findings/m-2-lack-of-rebalance-rate-limiting-allow-operators-to-drain-vaults.md`

### Vulnerable Pattern Examples

**Example 1: Per-Call Slippage Without Frequency Limit** [MEDIUM]
```solidity
// ❌ VULNERABLE: ~1% slippage per call, but unlimited calls per transaction
function rebalance(RebalanceParams calldata params) external onlyOperator {
    // Validates slippage per individual call
    _checkMinReturn(params);  // ~1% tolerance
    // No cooldown, no per-period cap, no cumulative loss tracking
    
    pool.swap(params.amount, params.direction);
}

// Attacker: call rebalance() 100x in one tx = 100% drained
```

### Secure Implementation

```solidity
// ✅ SECURE: Rate limit + cumulative loss tracking
uint256 public lastRebalanceTimestamp;
uint256 public cumulativeLoss;

function rebalance(RebalanceParams calldata params) external onlyOperator {
    require(block.timestamp >= lastRebalanceTimestamp + REBALANCE_COOLDOWN, "Cooldown");
    
    uint256 valueBefore = totalUnderlyingWithFees();
    pool.swap(params.amount, params.direction);
    uint256 valueAfter = totalUnderlyingWithFees();
    
    uint256 loss = valueBefore > valueAfter ? valueBefore - valueAfter : 0;
    cumulativeLoss += loss;
    require(cumulativeLoss <= MAX_CUMULATIVE_LOSS, "Cumulative loss exceeded");
    
    lastRebalanceTimestamp = block.timestamp;
}
```

### Detection Patterns
```
- rebalance/reweight functions without cooldown or frequency limit
- Per-call slippage tolerance without cumulative cap
- Operator-callable functions with no rate limiting
```

---

## 5. Wash Trading to Steal Keeper/Spot Trading Rewards

### Overview

When a DEX rewards traders based on position activity without distinguishing wash trades, an attacker can open and close positions in the same transaction to accumulate trading volume, then claim disproportionate rewards from the treasury.

> 📖 Reference: `reports/bonding_curve_findings/wash-trades-to-steal-keeper-and-spot-trading-rewards.md`

### Vulnerability Description

#### Root Cause
`closePositionByCondition()` accepts `CLOSE_BY_TRADER` as a close reason. Activity tracking increments on open and doesn't decrement on close. Rewards are distributed proportionally to `traderActivity / totalActivity`.

### Vulnerable Pattern Examples

**Example 1: Open+Close Same Block Earns Rewards** [MEDIUM]
```solidity
// ❌ VULNERABLE: Activity not rescinded on close
function openPosition(...) external {
    periodInfo.traderActivity[msg.sender] += positionSize;
    periodInfo.totalActivity += positionSize;
}

function closePositionByCondition(
    uint256 positionId, 
    CloseReason reason  // CLOSE_BY_TRADER allowed!
) external {
    // Activity NOT decremented!
    // Even though position existed for 0 blocks
}

function claimReward() external {
    uint256 reward = (periodInfo.totalReward * periodInfo.traderActivity[trader]) / periodInfo.totalActivity;
    // Wash trader gets proportional share of ALL rewards
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Minimum position duration + restrict close reasons
function closePositionByCondition(uint256 positionId, CloseReason reason) external {
    require(reason != CloseReason.CLOSE_BY_TRADER, "Use closePosition() instead");
}

function claimReward() external {
    // Only count activity from positions held for minimum duration
    uint256 qualifiedActivity = getQualifiedActivity(trader, MIN_HOLD_BLOCKS);
    uint256 reward = (periodInfo.totalReward * qualifiedActivity) / periodInfo.totalActivity;
}
```

---

## 6. Batch Operation Fails Atomically on Single Asset

### Overview

When a batch purchase function iterates over multiple assets and any single asset transfer fails (ownership changed, approval revoked), the entire batch reverts, preventing all legitimate purchases from succeeding.

> 📖 Reference: `reports/bonding_curve_findings/buyeragent-batch-purchase-failure-due-to-asset-transfer-or-approval-revocation.md`

### Vulnerable Pattern Examples

**Example 1: All-or-Nothing Batch Purchase** [MEDIUM]
```solidity
// ❌ VULNERABLE: Single failure reverts the entire batch
function purchase(address[] calldata assets) external {
    for (uint256 i = 0; i < assets.length; i++) {
        Swan(swan).purchase(assets[i]);  // Reverts if ANY asset has issues
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Try/catch per asset, skip failures
function purchase(address[] calldata assets) external {
    for (uint256 i = 0; i < assets.length; i++) {
        try Swan(swan).purchase(assets[i]) {
            emit PurchaseSucceeded(assets[i]);
        } catch {
            emit PurchaseFailed(assets[i]);
        }
    }
}
```

### Detection Patterns
```
- Batch functions iterating external calls without try/catch
- Purchase/claim loops that revert atomically
- Multi-asset operations with no per-item error handling
```

---

## 7. Unsafe Downcast Breaks Supply Invariant

### Overview

When bonding curve supply is stored as `uint256` but downcast to `uint128` for invariant calculations, values above `type(uint128).max` silently wrap to zero or a small number, completely breaking the price formula.

### Vulnerable Pattern Examples

**Example: Silent Uint128 Downcast** [MEDIUM]
```solidity
// ❌ VULNERABLE: Supply > 2^128 overflows silently
function getPrice() public view returns (uint256) {
    uint128 supply = uint128(totalSupply);  // Silent overflow if > 2^128!
    return (supply * supply) / PRECISION;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Use SafeCast or explicit check
function getPrice() public view returns (uint256) {
    require(totalSupply <= type(uint128).max, "Supply overflow");
    uint128 supply = uint128(totalSupply);
    return (supply * supply) / PRECISION;
}
```

### Detection Patterns
```
- uint128(totalSupply) or uint128(reserves) without overflow check
- Bonding curve formulas using narrower types than storage
- SafeCast not used for downcast operations
```

---

## 8. Collateral Depeg Cascading to Bonding Curve

### Overview

When a bonding curve's reserve asset (e.g., DAI, USDC) depegs but the curve doesn't adjust its pricing model, the curve continues to price tokens as if the reserve maintains its peg—creating arbitrage opportunities that drain reserves.

### Vulnerable Pattern Examples

**Example: Fixed Reserve Ratio During Depeg** [MEDIUM]
```solidity
// ❌ VULNERABLE: Assumes 1 DAI = $1 always
function getAmountOut(uint256 ethIn) public view returns (uint256 tokensOut) {
    uint256 daiReserve = daiBalance;  // Valued at $1.00 even if DAI = $0.90
    tokensOut = (ethIn * totalSupply) / (daiReserve * ethPrice);
}
```

### Detection Patterns
```
- Bonding curve with stablecoin reserves and no depeg handling
- Fixed price assumptions for reserve assets
- No circuit breaker for significant reserve value deviation
```

---

## 9. Asymmetric Base/Quote Treatment in Virtual Bonding Curve

### Overview

When a virtual bonding curve applies different formulas or fee treatments to base vs quote tokens, buy and sell prices diverge from the expected curve, enabling risk-free arbitrage between the two directions.

### Vulnerable Pattern Examples

**Example: Different Fee Application for Buy vs Sell** [MEDIUM]
```solidity
// ❌ VULNERABLE: Fee applied to base on buy, but to quote on sell
function buy(uint256 quoteIn) external returns (uint256 baseOut) {
    baseOut = getBaseOut(quoteIn);
    baseOut -= fee(baseOut);  // Fee on OUTPUT
}

function sell(uint256 baseIn) external returns (uint256 quoteOut) {
    quoteOut = getQuoteOut(baseIn);
    quoteOut -= fee(quoteOut);  // Fee also on OUTPUT — but base vs quote different!
}
```

### Detection Patterns
```
- Different fee application between buy and sell paths
- Virtual reserves updated asymmetrically for buys vs sells
- Curve formula not symmetric: buy(sell(x)) != x (minus fees)
```

---

## 10. Protocol Fees Stuck After Graduation

### Overview

When protocol fees are accumulated in the bonding curve contract but the fee claim function is only callable before graduation, all accumulated fees become permanently stuck after the token graduates to a DEX.

### Vulnerable Pattern Examples

**Example: Fee Claim Requires Non-Graduated State** [MEDIUM]
```solidity
// ❌ VULNERABLE: Fees locked after graduation
function claimFees() external onlyProtocol {
    require(!graduated, "Cannot claim after graduation");  // Stuck!
    payable(treasury).transfer(accumulatedFees);
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Allow fee claims regardless of graduation status
function claimFees() external onlyProtocol {
    uint256 fees = accumulatedFees;
    accumulatedFees = 0;
    payable(treasury).transfer(fees);
}
```

---

## 11. Token Supply Not Correctly Burned on Graduation

### Overview

When graduation transfers tokens from the bonding curve to a DEX pool, unsold tokens should be burned. If the burn doesn't account for tokens already in transit or held by the graduation contract, the supply is inflated.

### Vulnerable Pattern Examples

**Example: Missing Burn of Unsold Tokens** [MEDIUM]
```solidity
// ❌ VULNERABLE: Unsold tokens not burned during graduation
function graduate() external {
    // Add liquidity to DEX
    router.addLiquidity(token, weth, tokenAmount, ethAmount, ...);
    // Forgot to burn: totalSupply - soldTokens - liquidityTokens
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Burn all unsold tokens during graduation
function graduate() external {
    router.addLiquidity(token, weth, tokenForLiquidity, ethAmount, ...);
    
    uint256 unsoldTokens = token.balanceOf(address(this));
    if (unsoldTokens > 0) {
        token.burn(unsoldTokens);
    }
}
```

---

## 12. Graduation Stuck Due to Third-Party Contract Interference

### Overview

When graduation relies on successful interaction with a third-party contract (DEX router, pair factory), and that contract can be front-run, paused, or has unexpected behavior, the graduation permanently fails.

### Vulnerable Pattern Examples

**Example: Hard Dependency on External Contract** [MEDIUM]
```solidity
// ❌ VULNERABLE: If Uniswap router call fails, graduation is permanently stuck
function graduate() external {
    // No fallback if this reverts (router paused, pair already exists, etc.)
    router.addLiquidityETH{value: ethBalance}(
        token, tokenAmount, 0, 0, address(this), block.timestamp
    );
    graduated = true;  // Never reached if above reverts
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Fallback mechanism for graduation
function graduate() external {
    try router.addLiquidityETH{value: ethBalance}(
        token, tokenAmount, 0, 0, address(this), block.timestamp
    ) {
        graduated = true;
    } catch {
        // Allow retry or alternative graduation path
        emit GraduationFailed();
    }
}

function rescueGraduation() external onlyAdmin {
    // Alternative graduation path (e.g., different DEX, direct pair creation)
}
```

---

## Prevention Guidelines

### Development Best Practices
1. **Denominate oracle prices** in the actual peg target, not a proxy (USD ≠ DAI)
2. **Poke underlying pools** before reading TWAP values
3. **Update flash loan trackers** in all transfer/move functions, not just deposit
4. **Rate-limit rebalancing** with cumulative loss caps, not just per-call slippage
5. **Minimum hold duration** for reward-eligible trading activity
6. **Try/catch in batch operations** — don't let one failure revert all
7. **Use SafeCast** for all narrowing type conversions
8. **Build graduation fallbacks** — don't hard-depend on single DEX contracts
9. **Allow fee claims post-graduation** — don't gate claims on active-curve state
10. **Burn unsold tokens** during graduation to prevent supply inflation

### Testing Requirements
- Test oracle behavior during stablecoin depegs
- Test TWAP freshness across multiple blocks without pool activity
- Test self-liquidation flash loan attack path
- Test rebalance() called 100+ times in one transaction
- Test batch operations with failing individual items
- Test graduation with pre-existing DEX pairs

### Keywords for Search

`oracle denomination`, `DAI`, `USD`, `TWAP`, `stale oracle`, `metapool`, `update`, `flash loan protection`, `idToBlockOfLastDeposit`, `self-liquidation`, `vault.move`, `rebalance`, `rate limit`, `slippage`, `wash trading`, `traderActivity`, `batch purchase`, `try catch`, `unsafe downcast`, `uint128`, `SafeCast`, `depeg`, `collateral`, `protocol fees`, `graduation`, `burn`, `unsold tokens`, `addLiquidityETH`
