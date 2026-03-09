---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: share_accounting

# Attack Vector Details (Required)
attack_type: donation_attack|accounting_error|state_manipulation|reentrancy
affected_component: share_calculation|tvl_calculation|vault_accounting|supply_tracking

# Technical Primitives (Required)
primitives:
  - share_inflation
  - first_depositor
  - donation_attack
  - tvl_calculation
  - queued_withdrawal
  - strategy_allocation
  - exchange_rate
  - rounding
  - supply_desynchronization
  - shares_not_burned
  - double_counting
  - erc4626

# Impact Classification (Required)
severity: high
impact: fund_loss|inflation|dos|incorrect_pricing
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - lrt
  - share
  - accounting
  - tvl
  - vault
  - erc4626
  - donation
  - inflation

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### First Depositor / Vault Inflation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| rsETH Price Manipulation by First Staker | `reports/eigenlayer_findings/h-03-the-price-of-rseth-could-be-manipulated-by-the-first-staker.md` | HIGH | Code4rena |
| Rounding Error + Exchange Rate Manipulation (Napier) | `reports/eigenlayer_findings/h-4-victims-fund-can-be-stolen-due-to-rounding-error-and-exchange-rate-manipulati.md` | HIGH | Sherlock |
| Donation Attack on InceptionVault | `reports/eigenlayer_findings/vaults-are-vulnerable-to-a-donation-attack.md` | HIGH | Halborn |
| Downscale All Shares by 18 Decimals (RestakeFi) | `reports/eigenlayer_findings/attacker-can-downscale-all-protocol-shares-by-18-decimals.md` | HIGH | OpenZeppelin |
| Unexpected Assets Increase rsETH Price | `reports/eigenlayer_findings/unexpected-amount-of-supported-assets-could-increase-rseth-price.md` | MEDIUM | SigmaPrime |

### TVL Calculation Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Queued Withdrawal Deflates TVL (Renzo) | `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md` | HIGH | Code4rena |
| Wrong Loop Index in Withdraw Queue Balance | `reports/eigenlayer_findings/h-08-incorrect-withdraw-queue-balance-in-tvl-calculation.md` | HIGH | Code4rena |
| Static Strategy Allocation Tracking (Elytra) | `reports/eigenlayer_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md` | HIGH | Pashov |

### Transfer-Before-Calculation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Protocol Mints Less rsETH Than Intended | `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md` | HIGH | Code4rena |

### Share Accounting Desynchronization
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Shares Not Burned After Redemption (RestakeFi) | `reports/eigenlayer_findings/shares-not-burned-after-redemption-of-underlying-assets.md` | HIGH | OpenZeppelin |
| Setting Strategy Cap to 0 Doesn't Update Shares | `reports/eigenlayer_findings/h-2-setting-strategy-cap-to-0-does-not-update-total-shares-held-or-withdrawal-que.md` | HIGH | Sherlock |
| Incorrect stakedButUnverifiedNativeETH | `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md` | HIGH | SigmaPrime |
| Desynchronized Supply Snapshots (Cabal) | `reports/eigenlayer_findings/m-07-desynchronization-of-cabals-internal-accounting-with-actual-staked-init-amou.md` | MEDIUM | Code4rena |
| Supply Inflation via Unaccounted merge() | `reports/eigenlayer_findings/the-lockers-supply-can-be-arbitrarily-inflated-by-an-attacker-due-to-unaccounted.md` | HIGH | Immunefi |

### Slashing-Induced Accounting Breakage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Slash During Withdrawal Breaks Accounting | `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` | HIGH | Immunefi |
| Over-Slashing Withdrawable Shares | `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md` | HIGH | SigmaPrime |
| Double Slashing AVS + Beacon Chain | `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md` | HIGH | SigmaPrime |

### Reentrancy Accounting Corruption
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| redeemNative() Reentrancy Freezes Funds | `reports/eigenlayer_findings/h-redeemnative-reentrancy-enables-permanent-fund-freeze.md` | HIGH | MixBytes |

### Rounding / Conversion Precision
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Depositing Reverts Due to Share Round-Down | `reports/eigenlayer_findings/m-1-depositing-to-eigenlayer-can-revert-due-to-round-downs-in-converting-shares-a.md` | MEDIUM | Sherlock |

---

# LRT Share Accounting Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Share Accounting Security in Liquid Restaking Token (LRT) Protocols**

---

## Table of Contents

1. [First Depositor / Donation Attacks](#1-first-depositor--donation-attacks)
2. [TVL Calculation Errors](#2-tvl-calculation-errors)
3. [Transfer-Before-Calculation (CEI Violations)](#3-transfer-before-calculation-cei-violations)
4. [Share Accounting Desynchronization](#4-share-accounting-desynchronization)
5. [Slashing-Induced Accounting Breakage](#5-slashing-induced-accounting-breakage)
6. [Supply Inflation via Unaccounted Operations](#6-supply-inflation-via-unaccounted-operations)
7. [Rounding and Precision Failures](#7-rounding-and-precision-failures)

---

## 1. First Depositor / Donation Attacks

### Overview

First depositors can inflate the share price by depositing a minimal amount, then donating a large amount to the contract. Subsequent depositors' amounts round down to 0 shares, and the attacker absorbs all deposited funds.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-03-the-price-of-rseth-could-be-manipulated-by-the-first-staker.md` (Kelp DAO - Code4rena)
> - `reports/eigenlayer_findings/h-4-victims-fund-can-be-stolen-due-to-rounding-error-and-exchange-rate-manipulati.md` (Napier - Sherlock)
> - `reports/eigenlayer_findings/vaults-are-vulnerable-to-a-donation-attack.md` (Tagus v2 - Halborn)
> - `reports/eigenlayer_findings/attacker-can-downscale-all-protocol-shares-by-18-decimals.md` (RestakeFi - OpenZeppelin)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **share pricing uses `totalAssets / totalShares` where `totalAssets` includes direct token balances (`balanceOf`)**, which are manipulable via direct transfers. The first depositor mints 1 share, donates to inflate `totalAssets`, and subsequent deposits produce 0 shares due to integer division.

**Frequency:** Very Common (5/27 reports across 5 different protocols)
**Validation:** Strong — 4 independent auditors (Code4rena, Sherlock, Halborn, OpenZeppelin)

### Vulnerable Pattern Examples

**Example 1: rsETH Price Inflation via Donation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-03-the-price-of-rseth-could-be-manipulated-by-the-first-staker.md`
```solidity
// ❌ VULNERABLE: Price uses balanceOf which includes donations
function getRSETHPrice() external view returns (uint256 rsETHPrice) {
    uint256 rsEthSupply = rsETH.totalSupply();
    if (rsEthSupply == 0) return 1 ether;
    return totalETHInPool / rsEthSupply; // totalETHInPool uses balanceOf!
}

function getRsETHAmountToMint(address asset, uint256 amount) public view returns (uint256) {
    return (amount * lrtOracle.getAssetPrice(asset)) / lrtOracle.getRSETHPrice();
    // After donation: getRSETHPrice() returns enormous value
    // Small deposits → 0 rsETH (integer division rounds down)
}
```

**Example 2: 18-Decimal Downscaling** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/attacker-can-downscale-all-protocol-shares-by-18-decimals.md`
```solidity
// ❌ VULNERABLE: First depositor gets 1 share, then inflates price
// Step 1: Deposit 1 token → receive 1 share
// share_price = controller_total_underlying * 1e18 / protocol_token_total_shares
// share_price = 1 * 1e18 / 1 = 1e18

// Step 2: Transfer 10e18 tokens directly to controller
// share_price = (10e18 + 1) * 1e18 / 1 ≈ 10e36

// Step 3: Bob deposits 10e18 tokens
// bob_shares = 10e18 * 1e18 / 10e36 = 0 (rounded down)
// Bob's funds absorbed by attacker's 1 share
```

**Example 3: Napier stETH Partial Theft** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-4-victims-fund-can-be-stolen-due-to-rounding-error-and-exchange-rate-manipulati.md`
```solidity
// ❌ VULNERABLE: ZeroShares check insufficient against inflation
function prefundedDeposit() external nonReentrant returns (uint256, uint256) {
    uint256 assets = IWETH9(WETH).balanceOf(address(this)) - bufferEthCache;
    uint256 shares = previewDeposit(assets);
    if (shares == 0) revert ZeroShares(); // Only reverts on 0, not on partial theft!
    // Attacker donates 5 stETH, victim deposits 10 ETH → gets 1 share
    // Attacker redeems → gets ~7.5 ETH (steals ~2.5 ETH)
}
```

### Impact Analysis

- **Financial impact observed:** Up to 100% of victim's deposit stolen (0 shares), or partial theft (~25-50%)
- Affects ANY vault/LRT protocol using `balanceOf`-based pricing without inflation protection
- **Protocol frequency:** Kelp (2 findings), Napier (1), Tagus (1), RestakeFi (1)

### Secure Implementation

```solidity
// ✅ SECURE: Virtual offset (ERC4626 defense)
function totalAssets() public view returns (uint256) {
    return _totalAssets + VIRTUAL_OFFSET; // e.g., 1e6
}
function totalSupply() public view returns (uint256) {
    return _totalSupply + VIRTUAL_SHARES; // e.g., 1e6
}

// ✅ SECURE: Initial mint on deployment
constructor() {
    // Mint dead shares to prevent inflation
    _mint(address(0xdead), INITIAL_DEPOSIT);
}

// ✅ SECURE: Track deposits explicitly, not via balanceOf
function totalETHInPool() public view returns (uint256) {
    return _depositedETH; // NOT balanceOf(address(this))
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Does the share price formula use `balanceOf` or any externally-manipulable value?
- [ ] Is there protection against first depositor attacks (virtual shares/dead shares)?
- [ ] Can tokens be sent directly to the contract to inflate `totalAssets`?
- [ ] Does `previewDeposit` round down to values that cause loss?

---

## 2. TVL Calculation Errors

### Overview

TVL (Total Value Locked) calculations in LRT protocols aggregate balances across multiple sources (deposit pools, EigenLayer strategies, withdrawal queues). Incorrect aggregation — wrong addresses, wrong indices, missing components — leads to TVL inflation or deflation that corrupts share pricing.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md` (Renzo - Code4rena)
> - `reports/eigenlayer_findings/h-08-incorrect-withdraw-queue-balance-in-tvl-calculation.md` (Renzo - Code4rena)
> - `reports/eigenlayer_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md` (Elytra - Pashov)

### Vulnerability Description

#### Root Cause (Pattern A — Wrong Address Key)

`getTokenBalanceFromStrategy()` uses `queuedShares[address(this)]` instead of `queuedShares[address(token)]`, always returning 0 for queued withdrawal amounts.

#### Root Cause (Pattern B — Wrong Loop Index)

Nested loop uses `collateralTokens[i]` (outer operator delegator index) instead of `collateralTokens[j]` (inner token index), causing the same token to be counted multiple times.

#### Root Cause (Pattern C — Static Tracking)

`assetsAllocatedToStrategies[asset]` is a static variable incremented on deposit and decremented on withdrawal, but **doesn't track yield growth, P&L, or slashing losses** in the strategy.

**Frequency:** Very Common (5/27 reports, 3 patterns)
**Validation:** Strong — 3 independent auditors (Code4rena ×2, Pashov)

### Vulnerable Pattern Examples

**Example 1: Wrong Address Key Zeros Queued Balances** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md`
```solidity
// ❌ VULNERABLE: Wrong key — always returns 0 for queued withdrawals
function getTokenBalanceFromStrategy(IERC20 token) external view returns (uint256) {
    return
        queuedShares[address(this)] == 0  // BUG: should be address(token)
            ? tokenStrategyMapping[token].userUnderlyingView(address(this))
            : tokenStrategyMapping[token].userUnderlyingView(address(this)) +
                tokenStrategyMapping[token].sharesToUnderlyingView(
                    queuedShares[address(token)]
                );
}
// Result: TVL deflated by all queued withdrawal amounts
// → more ezETH minted per deposit → existing holders diluted
```

**Example 2: Wrong Loop Index — Same Token Counted Repeatedly** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-08-incorrect-withdraw-queue-balance-in-tvl-calculation.md`
```solidity
// ❌ VULNERABLE: collateralTokens[i] should be collateralTokens[j]
for (uint256 i = 0; i < odLength; ) {
    for (uint256 j = 0; j < tokenLength; ) {
        totalWithdrawalQueueValue += renzoOracle.lookupTokenValue(
            collateralTokens[i],  // BUG: i is OD index, should be j (token index)
            collateralTokens[j].balanceOf(withdrawQueue)
        );
        unchecked { ++j; }
    }
    unchecked { ++i; }
}
// If odLength > tokenLength → array-out-of-bounds revert
// If odLength == tokenLength → first token price used for all tokens
```

**Example 3: Static vs Dynamic Strategy Values** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
// ❌ VULNERABLE: Static tracking ignores yield, slashing, P&L
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset]; // STALE!
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);
    return poolBalance + strategyAllocated + unstakingVaultBalance;
    // strategyAllocated may be 100 ETH but actual strategy value is 120 ETH
    // → depositors get more shares than deserved (20 ETH unaccounted yield)
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Query actual strategy balances dynamically
function getTotalAssetTVL(address asset) public view returns (uint256) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyBalance = strategy.userUnderlyingView(address(this)); // Live query!
    uint256 queuedBalance = strategy.sharesToUnderlyingView(queuedShares[asset]);
    return poolBalance + strategyBalance + queuedBalance;
}

// ✅ SECURE: Use correct indices in nested loops
for (uint256 i = 0; i < odLength; ) {
    for (uint256 j = 0; j < tokenLength; ) {
        totalWithdrawalQueueValue += renzoOracle.lookupTokenValue(
            collateralTokens[j],  // FIXED: j for token index
            collateralTokens[j].balanceOf(withdrawQueue)
        );
    }
}
```

---

## 3. Transfer-Before-Calculation (CEI Violations)

### Overview

Depositing tokens via `transferFrom` into the contract *before* calculating the share mint amount inflates `totalAssets` (which uses `balanceOf`), causing the depositor to receive fewer shares than intended.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md` (Kelp DAO - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **tokens are transferred to the contract before the share calculation, and the share formula reads `balanceOf(address(this))` which already includes the deposited amount**, effectively double-counting the deposit in the denominator.

**Frequency:** Moderate (2/27 reports)
**Validation:** Strong — Code4rena (11 finders)

### Vulnerable Pattern Examples

**Example 1: Transfer Before Mint Calculation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md`
```solidity
// ❌ VULNERABLE: Transfer inflates totalAssets BEFORE share calculation
function depositAsset(address asset, uint256 depositAmount) external {
    // Transfer first — balanceOf(this) now includes depositAmount!
    IERC20(asset).transferFrom(msg.sender, address(this), depositAmount);
    
    // Calculate mint — getRSETHPrice() reads inflated balanceOf
    uint256 rsethAmount = _mintRsETH(asset, depositAmount);
    // Expected: 30 rsETH for 30 ETH deposit (with 10 ETH existing)
    // Actual: 30 * 1 / (40/10) = 7.5 rsETH (deposit counted in both num+denom)
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Calculate shares BEFORE transfer
function depositAsset(address asset, uint256 depositAmount) external {
    // Calculate first — using pre-transfer balance
    uint256 rsethAmount = _mintRsETH(asset, depositAmount);
    
    // Transfer AFTER calculation
    IERC20(asset).transferFrom(msg.sender, address(this), depositAmount);
    
    // Mint shares
    rsETH.mint(msg.sender, rsethAmount);
}
```

---

## 4. Share Accounting Desynchronization

### Overview

Internal share counters become desynchronized from actual state: shares not burned after redemption, caps set to 0 without updating totals, phantom ETH from staking/verification mismatches, supply inflated by uncounted operations.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/shares-not-burned-after-redemption-of-underlying-assets.md` (RestakeFi - OpenZeppelin)
> - `reports/eigenlayer_findings/h-2-setting-strategy-cap-to-0-does-not-update-total-shares-held-or-withdrawal-que.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md` (Kelp - SigmaPrime)

### Vulnerability Description

#### Root Cause (Pattern A — Shares Not Burned)

Request removed from array before `req.shares` is read for burning, so `req.shares = 0` at time of burn → shares never decreased.

#### Root Cause (Pattern B — Operator Removal Without Share Update)

Setting operator strategy cap to 0 queues EigenLayer withdrawal but doesn't update `assetRegistry` total shares or the withdrawal queue, creating double-counting.

#### Root Cause (Pattern C — Phantom ETH)

`stakedButUnverifiedNativeETH += 32 ether` on stake, but decremented by actual `effectiveBalance` which can be < 32 ETH (if slashed before verification), leaving phantom ETH.

**Frequency:** Very Common (6/27 reports)
**Validation:** Strong — 4 independent auditors

### Vulnerable Pattern Examples

**Example 1: Shares Read as 0 After Request Removal** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/shares-not-burned-after-redemption-of-underlying-assets.md`
```solidity
// ❌ VULNERABLE: Request removed BEFORE shares are read
function fulfillWithdrawal(uint256 requestId) external {
    WithdrawalRequest memory req = withdrawalRequests[requestId];
    
    // Remove from list FIRST — this zeros req.shares in the array
    _removeRequest(requestId);
    
    // Now req.shares is 0 → burn(0) → shares never actually burned
    token.burn(msg.sender, req.shares); // req.shares == 0!
    
    // Result: totalShares only increases, never decreases
    // All share-to-balance conversions permanently corrupted
}
```

**Example 2: Phantom ETH from Stake/Verify Mismatch** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md`
```solidity
// ❌ VULNERABLE: 32 ETH in, less than 32 ETH out
function stake(bytes32 pubkey) external {
    stakedButUnverifiedNativeETH += 32 ether; // Always 32 ETH
}

function verifyWithdrawalCredentials(ValidatorProof calldata proof) external {
    uint256 verified = proof.effectiveBalance; // May be < 32 ETH (slashing)
    stakedButUnverifiedNativeETH -= verified;  // e.g., 31 ETH
    // Phantom: 32 - 31 = 1 ETH still counted in TVL but doesn't exist
}
```

**Example 3: Strategy Cap 0 Without Share Update** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-2-setting-strategy-cap-to-0-does-not-update-total-shares-held-or-withdrawal-que.md`
```solidity
// ❌ VULNERABLE: Queues withdrawal from EL but doesn't update LRT shares
function setOperatorStrategyShareCaps(uint8 operatorId, StrategyShareCap[] caps) external {
    for (uint i = 0; i < caps.length; i++) {
        if (caps[i].cap == 0) {
            // Queues withdrawal from EigenLayer
            delegationManager.queueWithdrawals(withdrawalParams);
            // BUG: assetRegistry shares not updated!
            // BUG: withdrawalQueue not notified!
            // Users can still withdraw these shares → double-counting
        }
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Read shares BEFORE removing request
function fulfillWithdrawal(uint256 requestId) external {
    WithdrawalRequest memory req = withdrawalRequests[requestId];
    uint256 sharesToBurn = req.shares; // Copy BEFORE removal
    _removeRequest(requestId);
    token.burn(msg.sender, sharesToBurn); // Non-zero burn
}

// ✅ SECURE: Use consistent tracking for stake/verify
function stake(bytes32 pubkey) external {
    stakedButUnverifiedNativeETH += 32 ether;
}
function verifyWithdrawalCredentials(ValidatorProof proof) external {
    stakedButUnverifiedNativeETH -= 32 ether; // Always 32, not effectiveBalance
    verifiedNativeETH += proof.effectiveBalance; // Track actual separately
}
```

---

## 5. Slashing-Induced Accounting Breakage

### Overview

Slashing events that occur during active withdrawals permanently corrupt accounting variables, as withdrawal completion paths assume no slashing occurred between initiation and claim.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` (Puffer - Immunefi)
> - `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md` (EigenLayer - SigmaPrime)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`slashQueuedWithdrawal()` sets the withdrawal's `pending` flag to false, making `completeQueuedWithdrawal()` revert permanently**. The bookkeeping variable (`eigenLayerPendingWithdrawalSharesAmount`) is never decremented, inflating `totalAssets()` forever.

**Frequency:** Common (4/27 reports)
**Validation:** Strong — 2 independent auditors (Immunefi, SigmaPrime)

### Vulnerable Pattern Examples

**Example 1: Slash During Withdrawal = Permanent Inflation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`
```solidity
// ❌ VULNERABLE: Slashed withdrawal can never complete
// Timeline:
// 1. Puffer initiates withdrawal from EigenLayer
// 2. EigenLayer slashes the operator while withdrawal is pending
// 3. slashQueuedWithdrawal() sets: withdrawalRootPending[root] = false

// 4. Puffer tries to complete:
function claimWithdrawalFromEigenLayer(Withdrawal memory withdrawal) external {
    eigenLayerStrategyManager.completeQueuedWithdrawal(withdrawal, ...);
    // REVERTS: withdrawal no longer pending!
    
    // This line NEVER executes:
    $.eigenLayerPendingWithdrawalSharesAmount -= withdrawal.shares[0];
    // eigenLayerPendingWithdrawalSharesAmount stays inflated FOREVER
    // totalAssets() permanently overstated → protocol insolvency
}
```

**Example 2: Double AVS + Beacon Slashing** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`
```solidity
// ❌ VULNERABLE: bcsf doesn't account for maxMagnitude
// 32 ETH → operator slashed 50% by AVS (maxMagnitude = 0.5)
// → 16 ETH effective → beacon chain slashes 16 ETH
// → withdrawable = 16 * bcsf → bcsf computed without maxMagnitude
// → 8 ETH withdrawable instead of 16 (double-slashed)
uint64 newBCSF = uint64(
    prevBCSF.mulDiv(newRestakedBalanceWei, prevRestakedBalanceWei)
    // prevRestakedBalanceWei not scaled by dsf → bcsf too aggressive
);
```

### Secure Implementation

```solidity
// ✅ SECURE: Handle slashed withdrawal cleanup
function handleSlashedWithdrawal(Withdrawal memory withdrawal) external {
    // If withdrawal was slashed, clean up accounting manually:
    $.eigenLayerPendingWithdrawalSharesAmount -= withdrawal.shares[0];
    emit SlashedWithdrawalHandled(withdrawal.shares[0]);
}

// ✅ SECURE: Scale prevRestakedBalance by deposit scaling factor
uint64 newBCSF = uint64(
    prevBCSF.mulDiv(newRestakedBalanceWei, prevRestakedBalanceWei * dsf / WAD)
);
```

---

## 6. Supply Inflation via Unaccounted Operations

### Overview

Operations that modify supply counters without corresponding value changes (e.g., `merge()` adding to `supply` when just combining locks, or `compound()` adding to `staked_amounts` without real stakes) inflate supply indefinitely.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/the-lockers-supply-can-be-arbitrarily-inflated-by-an-attacker-due-to-unaccounted.md` (ZeroLend - Immunefi)
> - `reports/eigenlayer_findings/m-07-desynchronization-of-cabals-internal-accounting-with-actual-staked-init-amou.md` (Cabal - Code4rena)

### Vulnerability Description

#### Root Cause

`BaseLocker.merge()` calls `_depositFor()` with `MERGE_TYPE`, which unconditionally adds to `supply` even though no new tokens are locked — it just combines two existing locks. Repeated merge cycles inflate `supply` to any value.

**Frequency:** Moderate (2/27 reports)
**Validation:** Moderate — 2 independent auditors (Immunefi, Code4rena)

### Vulnerable Pattern Examples

**Example 1: merge() Inflates Supply Without New Value** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/the-lockers-supply-can-be-arbitrarily-inflated-by-an-attacker-due-to-unaccounted.md`
```solidity
// ❌ VULNERABLE: _depositFor always increases supply, even for merges
function merge(uint256 _from, uint256 _to) external {
    LockedBalance memory locked0 = locked[_from]; // 100 tokens
    LockedBalance memory locked1 = locked[_to];   // 200 tokens
    
    // Transfers locked0 into locked1
    _depositFor(_to, locked0.amount, locked1.end, locked1, MERGE_TYPE);
}

function _depositFor(uint256 _tokenId, uint256 _value, ...) internal {
    supply = supplyBefore + _value; // ALWAYS adds to supply!
    // For MERGE_TYPE: _value = 100 → supply += 100
    // But no new tokens were locked! Just rearranged existing locks
    // Repeated: supply → ∞, reward distribution → 0 per token
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Don't increase supply for merges
function _depositFor(uint256 _tokenId, uint256 _value, ..., DepositType _type) internal {
    if (_type != MERGE_TYPE) {
        supply = supplyBefore + _value; // Only for actual deposits
    }
    // ...
}
```

---

## 7. Rounding and Precision Failures

### Overview

Share-to-asset and asset-to-share conversions that both round down can cause strict equality checks to fail due to 1-wei discrepancies, permanently blocking deposits.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-1-depositing-to-eigenlayer-can-revert-due-to-round-downs-in-converting-shares-a.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`underlyingToSharesView` rounds down and `sharesToUnderlyingView` also rounds down**, creating 1-wei discrepancies. A strict equality check (`sharesReceived != sharesAllocated`) reverts on these expected rounding differences.

**Frequency:** Moderate (2/27 reports)
**Validation:** Moderate — Sherlock finders

### Vulnerable Pattern Examples

**Example 1: 1-Wei Discrepancy Blocks Deposits** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-1-depositing-to-eigenlayer-can-revert-due-to-round-downs-in-converting-shares-a.md`
```solidity
// ❌ VULNERABLE: Strict equality fails on rounding
function depositIntoStrategy(uint256 amount) internal {
    uint256 sharesAllocated = strategy.underlyingToSharesView(amount);
    uint256 sharesReceived = strategy.deposit(amount);
    
    // Both round down independently → 1 wei difference
    if (sharesReceived != sharesAllocated) {
        revert INCORRECT_NUMBER_OF_SHARES_RECEIVED();
        // 107636363636363636363 != 107636363636363636364
        // Deposits permanently blocked for certain amounts
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Allow rounding tolerance
function depositIntoStrategy(uint256 amount) internal {
    uint256 sharesAllocated = strategy.underlyingToSharesView(amount);
    uint256 sharesReceived = strategy.deposit(amount);
    
    // Allow 1-wei rounding difference
    uint256 diff = sharesReceived > sharesAllocated ? 
        sharesReceived - sharesAllocated : sharesAllocated - sharesReceived;
    if (diff > 1) {
        revert INCORRECT_NUMBER_OF_SHARES_RECEIVED();
    }
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Use virtual shares/dead shares to prevent first-depositor inflation attacks
2. Track deposits explicitly — never use `balanceOf` for share pricing
3. Calculate shares BEFORE transferring tokens (checks-effects-interactions)
4. Query actual strategy balances dynamically, not via static counters
5. Read shares before removing withdrawal requests from arrays
6. Use consistent increment/decrement amounts for tracking variables
7. Update ALL affected accounting variables when changing operator caps
8. Handle slashed withdrawals with explicit cleanup functions
9. Don't increase supply counters for merge/compound operations
10. Allow rounding tolerance instead of strict equality on share comparisons

#### Testing Requirements
- Donation attack test: first deposit → donate → second deposit → verify shares correct
- TVL consistency test: sum of all individual balances == reported totalAssets
- Ordering test: transfer-before-calculation vs calculation-before-transfer
- Rounding test: multiple deposit amounts including edge values near rounding boundaries
- Slashing integration test: initiate withdrawal → slash → attempt completion

### Keywords for Search

> These keywords enhance vector search retrieval:

`share accounting`, `share inflation`, `first depositor`, `donation attack`, `vault inflation`, `ERC4626`, `totalAssets`, `totalSupply`, `balanceOf manipulation`, `TVL calculation`, `queued withdrawal`, `queuedShares`, `strategy allocation`, `static tracking`, `transfer before calculation`, `CEI violation`, `shares not burned`, `phantom ETH`, `stakedButUnverifiedNativeETH`, `supply desynchronization`, `double counting`, `slashing accounting`, `eigenLayerPendingWithdrawalSharesAmount`, `over-slashing`, `merge supply inflation`, `rounding`, `precision`, `share conversion`, `round down`, `restaking`, `eigenlayer`, `LRT`, `Renzo`, `Kelp`, `Napier`, `RestakeFi`, `Elytra`, `Puffer`, `Rio Network`

### Related Vulnerabilities

- [LRT Exchange Rate & Oracle Vulnerabilities](LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md)
- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [Restaking Slashing Mechanisms](RESTAKING_SLASHING_VULNERABILITIES.md)
- [Restaking Reward Distribution](RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md)
