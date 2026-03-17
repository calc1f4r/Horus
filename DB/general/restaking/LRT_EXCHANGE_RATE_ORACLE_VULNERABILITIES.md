---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: exchange_rate_oracle

# Attack Vector Details (Required)
attack_type: oracle_manipulation|front_running|economic_exploit|logical_error
affected_component: price_oracle|exchange_rate|rate_provider|lrt_pricing

# Technical Primitives (Required)
primitives:
  - exchange_rate
  - price_oracle
  - lst_oracle
  - rate_provider
  - front_running
  - sandwich
  - mev
  - oracle_manipulation
  - stale_price
  - circuit_breaker
  - slippage
  - arbitrage
  - upgradeable_proxy

# Impact Classification (Required)
severity: high
impact: fund_loss|arbitrage|oracle_manipulation|price_manipulation
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - oracle
  - exchange_rate
  - lrt
  - lst
  - front-running
  - mev
  - price-manipulation

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | price_oracle | exchange_rate_oracle

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - arbitrage
  - balanceOf
  - block.timestamp
  - borrow
  - circuit_breaker
  - claimWithdrawal
  - deposit
  - depositAsset
  - exchange_rate
  - free
  - front_running
  - gaming
  - getAssetPrice
  - getCollateralValue
  - getMintRate
  - getPriceInEth
  - getRate
  - getTokenBalanceFromStrategy
  - lst_oracle
  - mev
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Oracle Manipulation via Upgradeable LST Proxies
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| No Checks on LST Price Oracles (Kelp) | `reports/eigenlayer_findings/no-checks-on-lst-price-oracles.md` | MEDIUM | SigmaPrime |
| Compromised LST Admin Can Manipulate Price (Tokemak) | `reports/eigenlayer_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md` | MEDIUM | Sherlock |

### Exchange Rate Frontrunning / Sandwich
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Withdrawals Logic Allows MEV Exploits of TVL Changes | `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero-.md` | HIGH | Code4rena |
| Stealing Funds When Rates Change (Vector Reserve) | `reports/eigenlayer_findings/stealing-funds-when-rates-change.md` | MEDIUM | Quantstamp |
| Operator Undelegation Manipulates Exchange Rate | `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md` | HIGH | Sherlock |

### Stale / Incorrect Rate Providers
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Exchange Rate to Balancer Pools | `reports/eigenlayer_findings/m-12-incorrect-exchange-rate-provided-to-balancer-pools.md` | MEDIUM | Code4rena |
| Withdrawal Oracle Overprices LSTs During Exit | `reports/eigenlayer_findings/m-6-withdrawals-ongoing-for-oeth-apxeth-weeth-and-almost-any-lst-are-overpriced-b.md` | MEDIUM | Sherlock |
| EigenPod Balance Blocks Reward Calculation | `reports/eigenlayer_findings/h-reward-calculation-blocked-if-eigenpod-balance-exceeds-16-eth.md` | HIGH | MixBytes |

### Exchange Rate Calculation Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Transfer Before Calculation Inflates Rate | `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md` | HIGH | Code4rena |
| Incorrect Queued Withdrawal Deflates Rate | `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md` | HIGH | Code4rena |
| Share Appreciation Blocks Settlement | `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-val.md` | HIGH | Sherlock |

---

# LRT Exchange Rate & Oracle Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Exchange Rate and Oracle Security in Liquid Restaking Token (LRT) Protocols**

---

## Table of Contents

1. [LST Oracle Manipulation via Upgradeable Proxies](#1-lst-oracle-manipulation-via-upgradeable-proxies)
2. [Exchange Rate Sandwich / Frontrunning](#2-exchange-rate-sandwich--frontrunning)
3. [Stale or Divergent Rate Providers](#3-stale-or-divergent-rate-providers)
4. [Exchange Rate Calculation Errors](#4-exchange-rate-calculation-errors)
5. [Withdrawal Pricing During Beacon Chain Exits](#5-withdrawal-pricing-during-beacon-chain-exits)
6. [Share Value Appreciation Blocking Settlement](#6-share-value-appreciation-blocking-settlement)

---

## 1. LST Oracle Manipulation via Upgradeable Proxies

### Overview

LRT protocols query LST exchange rates (e.g., `swETH.swETHToETHRate()`) directly. When the LST contract is an upgradeable proxy, the proxy admin can manipulate the rate function by upgrading the implementation, causing the LRT to misprice deposits and withdrawals.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/no-checks-on-lst-price-oracles.md` (Kelp - SigmaPrime)
> - `reports/eigenlayer_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md` (Tokemak - Sherlock)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | price_oracle | exchange_rate_oracle`
- Interaction scope: `single_contract`
- Primary affected component(s): `price_oracle|exchange_rate|rate_provider|lrt_pricing`
- High-signal code keywords: `arbitrage`, `balanceOf`, `block.timestamp`, `borrow`, `circuit_breaker`, `claimWithdrawal`, `deposit`, `depositAsset`
- Typical sink / impact: `fund_loss|arbitrage|oracle_manipulation|price_manipulation`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `before.function -> is.function -> uses.function`
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

### Vulnerability Description

#### Root Cause

This vulnerability exists because **LST rate functions are trusted as gospel with no bounds checking, rate-of-change limits, or circuit breakers**. Since many LSTs use TransparentUpgradeableProxy, the proxy admin can upgrade the implementation to return arbitrary rates.

**Frequency:** Moderate (3/31 reports across different protocols)
**Validation:** Strong — 2 independent auditors (SigmaPrime, Sherlock)

### Vulnerable Pattern Examples

**Example 1: Unbounded LST Rate Query** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`
```solidity
// ❌ VULNERABLE: Fully trusts upgradeable proxy rate — no bounds or circuit breaker
function getPriceInEth(address token) external view returns (uint256 price) {
    price = swEth.swETHToETHRate();
    // swETH is TransparentUpgradeableProxy
    // Admin can upgrade to: function swETHToETHRate() returns (uint256) { return 1e36; }
    // 1000x inflation → drain vault on withdrawal
}
```

**Example 2: No Rate-of-Change Guard** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/no-checks-on-lst-price-oracles.md`
```solidity
// ❌ VULNERABLE: No sanity bounds on queried rate
function getAssetPrice(address asset) public view returns (uint256) {
    if (asset == SWETH) {
        return ISwETH(swETHAddress).getRate(); // Could return ANY value
    }
    if (asset == RETH) {
        return IRocketTokenRETH(rETHAddress).getExchangeRate(); // Could return ANY value
    }
    // No min/max bounds, no rate-of-change check, no staleness check
}
```

### Impact Analysis

- LST admin (or compromised key) sets rate to extreme value
- LRT prices all assets using this rate → deposits/withdrawals at manipulated price
- **Financial impact:** Entire LRT TVL drainable in single transaction
- **Protocols at risk:** Kelp (swETH, rETH, cbETH), Tokemak (swETH, rETH)

### Secure Implementation

```solidity
// ✅ SECURE: Rate-of-change circuit breaker + bounds
function getAssetPrice(address asset) public view returns (uint256 rate) {
    rate = ISwETH(asset).getRate();
    
    // Bounds check — LST rates should be close to 1:1
    require(rate >= MIN_LST_RATE && rate <= MAX_LST_RATE, "Rate out of bounds");
    // e.g., MIN = 0.9e18, MAX = 1.3e18
    
    // Rate-of-change check — max ±5% per day
    uint256 lastRate = lastKnownRates[asset];
    uint256 maxDelta = lastRate * MAX_RATE_CHANGE_BPS / 10000;
    require(
        rate >= lastRate - maxDelta && rate <= lastRate + maxDelta,
        "Rate change too large"
    );
    
    lastKnownRates[asset] = rate;
    lastRateUpdateTime[asset] = block.timestamp;
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Are any LST price sources upgradeable proxies?
- [ ] Are there bounds/circuit-breakers on queried exchange rates?
- [ ] Is there a rate-of-change limit that triggers a pause?
- [ ] Can a single compromised admin manipulate all LRT pricing?

---

## 2. Exchange Rate Sandwich / Frontrunning

### Overview

LRT deposits and withdrawals that use internal exchange rates with no fees, no slippage, and instant settlement enable risk-free arbitrage: deposit before a rate increase, withdraw after — capturing the TVL change without exposure.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero-.md` (Renzo - Code4rena)
> - `reports/eigenlayer_findings/stealing-funds-when-rates-change.md` (Vector Reserve - Quantstamp)
> - `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **deposits and withdrawals use the current exchange rate with zero fees and zero slippage**, effectively creating a zero-cost DEX. Any TVL change (rewards, slashing, operator actions) creates a risk-free arbitrage window.

**Frequency:** Common (5/31 reports)
**Validation:** Strong — 3 independent auditors (Code4rena, Quantstamp, Sherlock)

### Vulnerable Pattern Examples

**Example 1: Zero-Fee DEX via LRT Deposit/Withdraw** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero-.md`
```solidity
// ❌ VULNERABLE: No fees or slippage on deposit/withdraw = free DEX
function deposit(address token, uint256 amount) external {
    uint256 shares = amount * totalSupply / totalAssets; // Current rate, no fee
    _mint(msg.sender, shares);
}

function requestWithdrawal(address token, uint256 shares) external {
    uint256 amount = shares * totalAssets / totalSupply; // Current rate, no fee
    // Amount calculated at REQUEST time, not claim time → free option on TVL change
}

// Attack scenarios:
// 1. Sandwich oracle updates: deposit before TVL increase → withdraw after
// 2. LST manipulation: deposit stETH at old rate → withdraw ETH at new rate
// 3. Risk-free arb: deposit before rewards → withdraw after claim
```

**Example 2: Rate Change Sandwich** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/stealing-funds-when-rates-change.md`
```solidity
// ❌ VULNERABLE: vETHPerRestakedLST update can be sandwiched
// Rate: 1:1 → update to 1:1.15
// Attack:
// 1. Deposit 300 LST at rate 1:1 → get 300 vETH
// 2. Rate updates to 1:1.15
// 3. Withdraw 300 vETH at rate 1:1.15 → get 345 LST
// Profit: 45 LST (15% of deposit)

function updateRate(uint256 newRate) external onlyAdmin {
    vETHPerRestakedLST = newRate; // No protection against sandwiching
}
```

### Impact Analysis

- **Financial impact observed:** 15% or more of deposit amount stolen per attack
- Repeatable every time TVL changes (rewards, slashing, rate updates)
- All LRT protocols without deposit/withdrawal fees or delays are vulnerable

### Secure Implementation

```solidity
// ✅ SECURE: Deposit/withdrawal fees + time-delayed pricing
function deposit(address token, uint256 amount) external {
    uint256 shares = amount * totalSupply / totalAssets;
    uint256 fee = shares * DEPOSIT_FEE_BPS / 10000; // e.g., 0.1%
    _mint(msg.sender, shares - fee);
    _mint(feeRecipient, fee);
}

function requestWithdrawal(uint256 shares) external {
    // Use min(requestTimeAmount, claimTimeAmount) to prevent free options
    withdrawalRequests[id] = WithdrawalRequest({
        shares: shares,
        requestTimeRate: totalAssets * 1e18 / totalSupply,
        timestamp: block.timestamp
    });
}

function claimWithdrawal(uint256 id) external {
    WithdrawalRequest memory req = withdrawalRequests[id];
    uint256 claimTimeAmount = req.shares * totalAssets / totalSupply;
    uint256 requestTimeAmount = req.shares * req.requestTimeRate / 1e18;
    // Use the LESSER amount to prevent gaming
    uint256 amount = claimTimeAmount < requestTimeAmount ? claimTimeAmount : requestTimeAmount;
}
```

---

## 3. Stale or Divergent Rate Providers

### Overview

Rate providers that return stale values (using `lastPrice` instead of live price) or that diverge from the actual exchange mechanism create arbitrage windows between DeFi pools and the LRT protocol.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-12-incorrect-exchange-rate-provided-to-balancer-pools.md` (Renzo - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`getRate()` (used by Balancer pools) returns `lastPrice` from the previous rate update, while `getMintRate()` (used internally) returns the current rate**. This creates a persistent divergence enabling cross-venue arbitrage.

**Frequency:** Moderate (2/31 reports)
**Validation:** Moderate — Code4rena finders

### Vulnerable Pattern Examples

**Example 1: getRate() vs getMintRate() Divergence** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-12-incorrect-exchange-rate-provided-to-balancer-pools.md`
```solidity
// ❌ VULNERABLE: Two different rate functions return different values
function getRate() external view returns (uint256) {
    return lastPrice; // Set by previous updatePrice() call — STALE
}

function getMintRate() public view returns (uint256) {
    uint256 oracleRate = oracle.getEzETHPrice();
    uint256 internalRate = totalAssets * 1e18 / totalSupply;
    return oracleRate > internalRate ? oracleRate : internalRate; // LIVE
}

// Balancer pool uses getRate() (stale), deposit contract uses getMintRate() (live)
// If ezETH price ↑: getRate < getMintRate → buy cheap in Balancer, mint expensive via deposit
// If ezETH price ↓: getRate > getMintRate → mint cheap via deposit, sell expensive in Balancer
```

### Secure Implementation

```solidity
// ✅ SECURE: Single source of truth for all rate queries
function getRate() external view returns (uint256) {
    return getMintRate(); // Same rate everywhere — no arbitrage window
}
```

---

## 4. Exchange Rate Calculation Errors

### Overview

Errors in the TVL aggregation that feeds the exchange rate — wrong address keys, wrong loop indices, transfer-before-calculation — create systematic mispricing of LRT tokens.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md` (Kelp DAO - Code4rena)
> - `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md` (Renzo - Code4rena)

### Vulnerability Description

#### Root Cause (Pattern A — Transfer-Before-Calculation)

Tokens transferred to the contract before share calculation inflates `totalAssets` (which reads `balanceOf`), causing the depositor to receive fewer shares than expected.

#### Root Cause (Pattern B — Queued Withdrawal Omission)

Wrong address key in queued withdrawal lookup (`queuedShares[address(this)]` instead of `queuedShares[address(token)]`) removes queued withdrawals from TVL, deflating it and over-minting LRT.

**Frequency:** Common (4/31 reports)
**Validation:** Strong — Code4rena with multiple independent finders

### Vulnerable Pattern Examples

**Example 1: Deposit Inflates Own Price** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md`
```solidity
// ❌ VULNERABLE: Transfer BEFORE share calculation
function depositAsset(address asset, uint256 depositAmount) external {
    // Step 1: Transfer — inflates balanceOf(this)
    IERC20(asset).transferFrom(msg.sender, address(this), depositAmount);
    
    // Step 2: Mint — reads inflated balanceOf(this) in price calculation
    uint256 rsethAmount = _mintRsETH(asset, depositAmount);
    // totalETHInPool was 10, deposit is 30
    // After transfer: totalETHInPool = 40
    // rsETHPrice = 40 / 10 = 4.0 (should be 10/10 = 1.0)
    // rsethAmount = 30 / 4.0 = 7.5 (should be 30 / 1.0 = 30)
    // User loses 75% of deposit value!
}
```

**Example 2: Wrong Key Zeros Queued Withdrawals** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md`
```solidity
// ❌ VULNERABLE: address(this) instead of address(token) — always 0
function getTokenBalanceFromStrategy(IERC20 token) external view returns (uint256) {
    return queuedShares[address(this)] == 0  // BUG: should be address(token)
        ? tokenStrategyMapping[token].userUnderlyingView(address(this))
        : tokenStrategyMapping[token].userUnderlyingView(address(this)) +
            tokenStrategyMapping[token].sharesToUnderlyingView(
                queuedShares[address(token)]
            );
    // queuedShares[address(this)] is always 0 → queued amounts ignored
    // TVL deflated → more ezETH minted per deposit
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Calculate BEFORE transfer
function depositAsset(address asset, uint256 depositAmount) external {
    uint256 rsethAmount = _mintRsETH(asset, depositAmount); // Pre-transfer TVL
    IERC20(asset).transferFrom(msg.sender, address(this), depositAmount);
    rsETH.mint(msg.sender, rsethAmount);
}

// ✅ SECURE: Use correct key
function getTokenBalanceFromStrategy(IERC20 token) external view returns (uint256) {
    return queuedShares[address(token)] == 0  // FIXED: address(token)
        ? tokenStrategyMapping[token].userUnderlyingView(address(this))
        : /* ... include queued shares ... */;
}
```

---

## 5. Withdrawal Pricing During Beacon Chain Exits

### Overview

After initiating a withdrawal from an LST to native ETH, the oracle continues pricing the position as a yield-bearing LST (not bare ETH), creating overvaluation during the exit queue period.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-6-withdrawals-ongoing-for-oeth-apxeth-weeth-and-almost-any-lst-are-overpriced-b.md` (Notional - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **after `initiateWithdraw` burns LSTs and enters the beacon chain exit queue, the oracle still prices the position using `TRADING_MODULE.getOraclePrice(YIELD_TOKEN, asset)`** which returns the pre-exit yield-bearing price. The actual backing is now bare ETH (or worse, queued ETH with delay risk).

**Frequency:** Moderate (2/31 reports)
**Validation:** Moderate — Sherlock finders

### Vulnerable Pattern Examples

**Example 1: LST Price Used After Exit Initiation** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-6-withdrawals-ongoing-for-oeth-apxeth-weeth-and-almost-any-lst-are-overpriced-b.md`
```solidity
// ❌ VULNERABLE: Oracle prices position as yield-bearing LST during exit queue
function getCollateralValue() public view returns (uint256) {
    // After initiateWithdraw: LSTs burned, waiting for beacon chain exit
    // But oracle still returns yield-bearing LST price!
    (int256 rate, ) = TRADING_MODULE.getOraclePrice(YIELD_TOKEN, BORROW_TOKEN);
    return totalAssets * uint256(rate) / 1e18;
    // totalAssets is actually queued ETH, not LSTs
    // Overvaluation allows users to borrow more than backing supports
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Track asset state transitions
function getCollateralValue() public view returns (uint256) {
    uint256 activeValue = activeLSTBalance * getLSTPrice();
    uint256 exitQueueValue = exitQueueBalance * 1e18; // Price as ETH, not LST!
    return activeValue + exitQueueValue;
}
```

---

## 6. Share Value Appreciation Blocking Settlement

### Overview

When withdrawal requests record the EigenLayer share count needed at request time, and shares appreciate in value before settlement (ERC4626-like), the idle deposit pool funds convert to fewer shares than originally recorded, making the withdrawal impossible to settle.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-val.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **withdrawal requests record absolute share counts, but EigenLayer strategy shares can appreciate in value over time** (like ERC4626). When idle funds in the deposit pool are converted to shares to fulfill the withdrawal, the conversion returns fewer shares than originally recorded, leaving a permanent deficit.

**Frequency:** Rare (1/31 reports) but permanent DoS
**Validation:** Moderate — Sherlock finders

### Vulnerable Pattern Examples

**Example 1: Share Appreciation Creates Settlement Gap** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-val.md`
```solidity
// ❌ VULNERABLE: Records share count at request time, not value
function requestWithdrawal(uint256 amount) external {
    uint256 sharesNeeded = strategy.underlyingToSharesView(amount);
    // At request: 100 cbETH = 100 EL shares
    pendingWithdrawals.push(PendingWithdrawal({
        shares: sharesNeeded, // Records 100 shares
        // ...
    }));
}

function settleEpochFromDepositPool() external {
    // Time passes, shares appreciate 10%: 100 cbETH = 90.9 EL shares now
    uint256 sharesAvailable = strategy.deposit(idlePoolBalance);
    // 100 cbETH yields 90.9 shares, need 100 → short 9.1 shares
    
    if (sharesAvailable < pendingWithdrawals.totalShares) {
        // Settlement stuck forever — can't produce enough shares
        revert InsufficientShares();
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Record withdrawal in underlying value, not shares
function requestWithdrawal(uint256 amount) external {
    pendingWithdrawals.push(PendingWithdrawal({
        underlyingAmount: amount, // Record VALUE, not shares
        timestamp: block.timestamp
    }));
}

function settleEpoch() external {
    uint256 totalUnderlying = pendingWithdrawals.totalUnderlyingAmount;
    // Use current conversion — always produces correct output
    uint256 sharesNeeded = strategy.underlyingToSharesView(totalUnderlying);
    strategy.withdraw(sharesNeeded);
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Add rate-of-change circuit breakers for all LST oracle sources
2. Implement bounds checking on exchange rates (min/max LST rate)
3. Add deposit/withdrawal fees to eliminate zero-cost arbitrage
4. Use `min(requestTimeAmount, claimTimeAmount)` for withdrawal pricing
5. Provide a single rate function for all consumers (no getRate vs getMintRate divergence)
6. Calculate shares before token transfer, not after (CEI pattern)
7. Track withdrawal state transitions — price as ETH during exit queue, not as LST
8. Record withdrawals in underlying value, not share count
9. Verify all address keys match intended mapping (token vs contract)
10. Consider time delays on deposits after large TVL changes

#### Testing Requirements
- Sandwich test: deposit→rate-change→withdraw in same block
- Oracle manipulation: mock upgradeable LST with rate changes
- Rate divergence: verify getRate == getMintRate across all conditions
- Share appreciation: test settlement after strategy yield accrual
- Circuit breaker test: verify rate-of-change limits trigger correctly

### Keywords for Search

> These keywords enhance vector search retrieval:

`exchange rate`, `oracle`, `price oracle`, `LST oracle`, `rate provider`, `getRate`, `getMintRate`, `swETHToETHRate`, `getExchangeRate`, `getRSETHPrice`, `upgradeable proxy`, `circuit breaker`, `rate-of-change`, `bounds checking`, `sandwich attack`, `frontrunning`, `MEV`, `arbitrage`, `zero-fee DEX`, `stale price`, `lastPrice`, `withdrawal pricing`, `exit queue`, `share appreciation`, `settlement gap`, `transfer before calculation`, `CEI violation`, `queuedShares`, `TVL deflation`, `TVL inflation`, `restaking`, `eigenlayer`, `LRT`, `Renzo`, `Kelp`, `Tokemak`, `Napier`, `Vector Reserve`, `Rio Network`, `Notional`

### Related Vulnerabilities

- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)
- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [Restaking Reward Distribution](RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md)

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

`arbitrage`, `balanceOf`, `block.timestamp`, `borrow`, `circuit_breaker`, `claimWithdrawal`, `defi`, `deposit`, `depositAsset`, `eigenlayer`, `exchange_rate`, `exchange_rate_oracle`, `free`, `front-running`, `front_running`, `gaming`, `getAssetPrice`, `getCollateralValue`, `getMintRate`, `getPriceInEth`, `getRate`, `getTokenBalanceFromStrategy`, `lrt`, `lst`, `lst_oracle`, `mev`, `oracle`, `oracle_manipulation`, `price-manipulation`, `price_oracle`, `rate_provider`, `restaking`, `sandwich`, `slippage`, `stale_price`, `upgradeable_proxy`
