---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: withdrawal_unstaking_logic

# Attack Vector Details (Required)
attack_type: logical_error|economic_exploit|state_manipulation
affected_component: withdrawal_queue|share_calculation|fund_transfer|delay_mechanism

# Technical Primitives (Required)
primitives:
  - withdrawal_queue
  - unstaking
  - queued_withdrawal
  - share_to_asset_conversion
  - withdrawal_delay
  - slippage_protection
  - partial_failure_handling
  - eigenlayer_settlement
  - cooldown_period
  - epoch_management
  - pending_withdrawal_amount
  - completequeuedwithdrawal

# Impact Classification (Required)
severity: critical
impact: fund_loss|permanent_lockup|dos|accounting_error
exploitability: 0.7
financial_impact: critical

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - lrt
  - liquid_restaking
  - withdrawal
  - unstaking
  - fund_lockup

# Version Info
language: solidity|rust|move
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Withdrawal Queue Manipulation / Epoch Mismanagement
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Pending Withdrawal Amount Reset | `reports/eigenlayer_findings/_pendingwithdrawalamount-can-be-arbitrarily-reset.md` | HIGH | Halborn |
| New Withdrawal Requests During Settlement | `reports/eigenlayer_findings/h-1-creating-new-withdrawal-requests-in-conjunction-with-settleepochfromeigenlay.md` | HIGH | Sherlock |
| Strategy Cap 0 Doesn't Update Queue | `reports/eigenlayer_findings/h-2-setting-the-strategy-cap-to-0-does-not-update-the-total-shares-held-or-the-w.md` | HIGH | Sherlock |
| Canceled Withdrawal Impacts Future Unstaking | `reports/eigenlayer_findings/m-06-the-time-available-for-a-canceled-withdrawal-should-not-impact-future-unsta.md` | MEDIUM | Code4rena |

### Share/Amount Calculation Errors During Withdrawal
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Direct Loss of Principal on Full Withdrawal | `reports/eigenlayer_findings/eig-7-direct-loss-of-user-principal-funds-when-processing-a-full-withdrawal-of-p.md` | CRITICAL | Hexens |
| Withdrawal Impossible Due to Shares Appreciation | `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-va.md` | HIGH | Sherlock |
| Incorrect lidoLockedETH Blocks Redemption | `reports/eigenlayer_findings/incorrect-lidolockedeth-value-can-block-full-redeeming-of-puffeth-in-vault.md` | MEDIUM | Immunefi |
| ETH Withdrawers Don't Earn Yield | `reports/eigenlayer_findings/m-11-eth-withdrawers-do-not-earn-yield-while-waiting-for-a-withdrawal.md` | MEDIUM | Sherlock |
| Withdrawal Request Value Incorrect | `reports/eigenlayer_findings/m-14-value-of-ethernas-withdrawal-request-is-incorrect.md` | MEDIUM | Sherlock |
| Inconsistent Withdraw Request Valuation | `reports/eigenlayer_findings/m-6-the-_getvalueofwithdrawrequest-function-uses-different-methods-for-selecting.md` | MEDIUM | Sherlock |
| Inaccurate Available Shares Estimation | `reports/eigenlayer_findings/m-9-requestwithdrawal-doesnt-estimate-accurately-the-available-shares-for-withdr.md` | MEDIUM | Sherlock |

### Fund Lockup During Withdrawal
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Base Tokens Not Transferred After Restaking Expired | `reports/eigenlayer_findings/base-tokens-are-not-transferred-out-after-restaking-expired-withdrawals.md` | HIGH | Quantstamp |
| Withdrawals Locked Forever (Contract Recipient) | `reports/eigenlayer_findings/h-01-withdrawals-can-be-locked-forever-if-recipient-is-a-contract.md` | HIGH | Code4rena |
| Lack of Withdrawal Functionality in Strategies | `reports/eigenlayer_findings/h-03-lack-of-withdrawal-functionality-in-strategy-contracts.md` | HIGH | Pashov Audit Group |
| Users Cannot Unstake (Missing onERC721Received) | `reports/eigenlayer_findings/h-06-users-cannot-unstake-from-yiedlethstakingetherfisol-because-yieldaccountsol.md` | HIGH | Code4rena |
| Kelp Finalize Cooldown Blocked by Dust Request | `reports/eigenlayer_findings/h-13-kelp_finalizecooldown-cannot-claim-the-withdrawal-if-adversary-would-reques.md` | HIGH | Sherlock |
| Instant Withdrawals Loss for StakingProxy | `reports/eigenlayer_findings/instant-withdrawals-in-priority-pool-can-result-in-loss-of-funds-for-stakingprox.md` | HIGH | Cyfrin |
| Last Holder Can't Exit (Zero Supply) | `reports/eigenlayer_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md` | MEDIUM | Code4rena |
| Funds Stuck if One Request Fails | `reports/eigenlayer_findings/m-21-funds-stuck-if-one-of-the-withdrawal-requests-cannot-be-finalized.md` | MEDIUM | Sherlock |
| Users May Not Be Able to Withdraw | `reports/eigenlayer_findings/users-may-not-be-able-to-withdraw.md` | MEDIUM | Quantstamp |

### Slashing Interaction with Withdrawals
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Impossible to Slash Queued Withdrawals | `reports/eigenlayer_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| Slash During Withdrawal Breaks Accounting | `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` | HIGH | Immunefi |
| Partial Failure in Withdrawal Requests | `reports/eigenlayer_findings/insufficient-handling-of-partial-failures-in-withdrawal-requests.md` | HIGH | Immunefi |

### Withdrawal Delay Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lockup Period Decreased by Re-Staking | `reports/eigenlayer_findings/lockup-period-for-unstaking-can-be-decreased-by-staking-again-with-shorter-locku.md` | HIGH | Quantstamp |
| withdrawalDelayBlocks Not Initialized After M2 | `reports/eigenlayer_findings/withdrawaldelayblocks-cannot-be-initialised-after-m2-upgrade.md` | HIGH | SigmaPrime |
| Withdrawal Delay Bypass via L1 Operations | `reports/eigenlayer_findings/withdrawal-delay-can-be-bypassed-when-l1-operations-processed-more-than-once-per.md` | MEDIUM | Spearbit |

### Missing Slippage/Deadline Protection
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack of Slippage and Deadline on Withdraw/Deposit | `reports/eigenlayer_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md` | MEDIUM | Code4rena |
| Redeem Functions Blocked by Shared Cooldown | `reports/eigenlayer_findings/h-01-the-redeem-related-functions-are-likely-to-be-blocked.md` | HIGH | Code4rena |

### Reentrancy / Access Control in Withdrawals
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Direct Theft via Reentrancy During Unstaking | `reports/eigenlayer_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md` | CRITICAL | Hexens |
| Withdrawals Not Pausable | `reports/eigenlayer_findings/m-02-withdrawals-and-claims-are-meant-to-be-pausable-but-it-is-not-possible-in-p.md` | MEDIUM | Code4rena |
| MEV Exploits via Zero-Slippage Withdrawals | `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |

---

# Restaking Withdrawal & Unstaking Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Restaking Protocol Withdrawal Security Audits**

---

## Table of Contents

1. [Withdrawal Queue Manipulation](#1-withdrawal-queue-manipulation)
2. [Share/Amount Calculation Errors During Withdrawal](#2-shareamount-calculation-errors-during-withdrawal)
3. [Fund Lockup During Withdrawal](#3-fund-lockup-during-withdrawal)
4. [Slashing Interaction with Withdrawals](#4-slashing-interaction-with-withdrawals)
5. [Withdrawal Delay Bypass](#5-withdrawal-delay-bypass)
6. [Missing Slippage/Deadline Protection](#6-missing-slippagedeadline-protection)
7. [Partial Failure Handling](#7-partial-failure-handling)
8. [Reentrancy and Access Control in Withdrawal Flows](#8-reentrancy-and-access-control-in-withdrawal-flows)

---

## 1. Withdrawal Queue Manipulation

### Overview

Withdrawal queue state (epoch counters, pending amounts, queue ordering) can be manipulated or become inconsistent, leading to system deadlock or accounting errors. EigenLayer's 2-step withdrawal process (initiate → claim after delay) creates a window where queue state can diverge from reality.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-1-creating-new-withdrawal-requests-in-conjunction-with-settleepochfromeigenlay.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/_pendingwithdrawalamount-can-be-arbitrarily-reset.md` (Tagus V2 - Halborn)
> - `reports/eigenlayer_findings/h-2-setting-the-strategy-cap-to-0-does-not-update-the-total-shares-held-or-the-w.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **epoch/queue state transitions are not atomic** with EigenLayer's settlement process. When the settlement epoch is not incremented immediately upon initiation, or when queue state variables are permissionlessly modifiable, the internal withdrawal accounting diverges from EigenLayer's actual state.

**Frequency:** Common (4/34 reports)
**Validation:** Strong — 3+ independent auditors (Sherlock, Halborn, Code4rena)

#### Attack Scenario

1. Withdrawal epoch is initiated with EigenLayer (7-day delay starts)
2. Attacker creates new withdrawal requests during the delay period
3. New requests target the same (already-settling) epoch because the counter wasn't incremented
4. When settlement completes, the new requests reference an already-consumed epoch
5. System deadlock: LRT tokens burned but ETH unclaimable

### Vulnerable Pattern Examples

**Example 1: Epoch Not Incremented on Settlement Initiation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-1-creating-new-withdrawal-requests-in-conjunction-with-settleepochfromeigenlay.md`
```solidity
// ❌ VULNERABLE: settleEpochFromEigenLayer doesn't increment the epoch
function settleEpochFromEigenLayer(
    IDelegationManager.Withdrawal[] calldata withdrawals
) external {
    // Process the withdrawals...
    for (uint i = 0; i < withdrawals.length; i++) {
        delegationManager.completeQueuedWithdrawal(withdrawals[i], ...);
    }
    // BUG: currentEpoch is NOT incremented here
    // Users can still create requests for this epoch during 7-day delay
}
```

**Example 2: Permissionless Pending Amount Reset** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/_pendingwithdrawalamount-can-be-arbitrarily-reset.md`
```solidity
// ❌ VULNERABLE: Anyone can call claimCompletedWithdrawals and reset _pendingWithdrawalAmount
function claimCompletedWithdrawals() external {
    // No access control — anyone can call
    _pendingWithdrawalAmount = 0; // Resets regardless of actual state
    // getTotalDeposited() now returns incorrect value
}
```

**Example 3: Strategy Cap Change Doesn't Update Queue** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-2-setting-the-strategy-cap-to-0-does-not-update-the-total-shares-held-or-the-w.md`
```solidity
// ❌ VULNERABLE: Setting cap to 0 queues EigenLayer withdrawal but doesn't sync
function setOperatorStrategyCap(address operator, address strategy, uint256 cap) external onlyOwner {
    if (cap == 0) {
        // Queues withdrawal from EigenLayer
        _queueWithdrawalFromOperatorStrategy(operator, strategy);
        // BUG: assetRegistry.shares and withdrawalQueue NOT updated
        // Users see stale (inflated) share count
    }
}
```

**Example 4: Canceled Withdrawal Pollutes FIFO Queue** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-06-the-time-available-for-a-canceled-withdrawal-should-not-impact-future-unsta.md`
```solidity
// ❌ VULNERABLE: Canceled withdrawal's timestamp persists in queue
function requestWithdrawal(uint256 amount) external {
    uint256 availableAt = max(
        block.timestamp + unstakingDelay,
        queue[queue.length - 1].availableAt  // BUG: This may be a canceled entry
    );
    queue.push(WithdrawalRequest(amount, availableAt, msg.sender));
}
```

### Impact Analysis

#### Technical Impact
- System deadlock: withdrawal epochs become unprocessable (4/34 reports)
- Double-counted shares: users withdraw based on stale inflated share counts
- Queue corruption: canceled/stale entries pollute future withdrawals
- State desynchronization between LRT protocol and EigenLayer

#### Business Impact
- Permanent fund lockup for users (LRT tokens burned, ETH unclaimable)
- Protocol-level insolvency risk
- Loss of user trust and protocol reputation
- **Financial impact observed:** Up to entire protocol TVL at risk

#### Affected Scenarios
- Multi-epoch settlement in protocols with 7-day EigenLayer withdrawal delay
- Operator strategy changes (cap adjustments, strategy rotation)
- Permissionless withdrawal claim functions
- FIFO-ordered withdrawal queues with cancellation support

### Secure Implementation

**Fix 1: Atomic Epoch Increment**
```solidity
// ✅ SECURE: Increment epoch as soon as withdrawal is initiated
function initiateEpochSettlement() external {
    uint256 epoch = currentEpoch;
    currentEpoch++; // Immediately increment — new requests go to next epoch
    
    // Queue withdrawal with EigenLayer for current epoch
    _queueEigenLayerWithdrawal(epoch);
}
```

**Fix 2: Access-Controlled Queue State**
```solidity
// ✅ SECURE: Restrict who can modify pending withdrawal state
function claimCompletedWithdrawals() external onlyRestaker {
    require(msg.sender == registeredRestaker, "Not authorized");
    uint256 claimed = _processCompletedWithdrawals();
    _pendingWithdrawalAmount -= claimed; // Decrement by actual claimed amount
}
```

**Fix 3: Sync Queue on Strategy Changes**
```solidity
// ✅ SECURE: Update all dependent state when strategy changes
function setOperatorStrategyCap(address operator, address strategy, uint256 cap) external onlyOwner {
    if (cap == 0) {
        uint256 shares = _getOperatorShares(operator, strategy);
        _queueWithdrawalFromOperatorStrategy(operator, strategy);
        assetRegistry.decreaseShares(strategy, shares);
        withdrawalQueue.queueCurrentEpochSettlement(strategy, shares);
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `settleEpoch` or `completeQueuedWithdrawal` without epoch increment
- Pattern 2: Public/external functions that modify `_pendingWithdrawalAmount` or similar state
- Pattern 3: Strategy cap/config changes without corresponding queue updates
- Pattern 4: FIFO queues that reference previous entries' timestamps without filtering canceled entries
```

#### Audit Checklist
- [ ] Is the epoch counter incremented atomically with EigenLayer withdrawal initiation?
- [ ] Are queue state variables (pending amounts, shares) only modifiable by authorized contracts?
- [ ] Do strategy changes (cap, rotation) synchronize with the withdrawal queue?
- [ ] Are canceled/expired entries pruned from queue ordering state?
- [ ] Can new withdrawal requests be created for an epoch already being settled?

---

## 2. Share/Amount Calculation Errors During Withdrawal

### Overview

Incorrect amount/share calculations during the withdrawal process cause direct financial loss. This includes rounding losses on withdrawal amounts, stale share snapshots that don't account for yield accumulation, and inconsistent valuation methods across different asset types.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/eig-7-direct-loss-of-user-principal-funds-when-processing-a-full-withdrawal-of-p.md` (EigenLayer - Hexens)
> - `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-va.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/incorrect-lidolockedeth-value-can-block-full-redeeming-of-puffeth-in-vault.md` (Puffer Finance - Immunefi)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **share-to-asset conversions are performed at a fixed point in time** (request time) without accounting for value changes during the withdrawal delay. Additionally, rounding functions designed for deposit validation are incorrectly applied to withdrawal amounts, and different assets use inconsistent valuation methods.

**Frequency:** Common (7/34 reports)
**Validation:** Strong — 4+ independent auditors (Hexens, Sherlock, Immunefi, Code4rena)

#### Attack Scenario

1. User requests withdrawal, shares are recorded at current conversion rate
2. During the 7-day EigenLayer delay, yield accumulates or slashing occurs
3. Share-to-asset rate changes, but the recorded shares don't update
4. Settlement uses stale values, causing either overpayment or underpayment
5. In extreme cases, the total shares owed exceed available shares, permanently blocking settlement

### Vulnerable Pattern Examples

**Example 1: Rounding Function Applied to Withdrawal Amount** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/eig-7-direct-loss-of-user-principal-funds-when-processing-a-full-withdrawal-of-p.md`
```solidity
// ❌ VULNERABLE: _calculateRestakedBalanceGwei rounds down heavily (up to 1.5 ETH loss)
function _processFullWithdrawal(uint64 withdrawalAmountGwei, ...) internal {
    // BUG: Applies a rounding function designed for deposits to withdrawals
    withdrawalAmountGwei = _calculateRestakedBalanceGwei(withdrawalAmountGwei);
    // 30.74 ETH withdrawal → rounded to 29 ETH → 1.74 ETH lost permanently
    
    _sendETH(podOwner, withdrawalAmountGwei * GWEI_TO_WEI);
}
```

**Example 2: Stale Shares Cause Settlement Failure** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-va.md`
```solidity
// ❌ VULNERABLE: Shares recorded at request time, but value changes during delay
function requestWithdrawal(uint256 amount) external {
    uint256 shares = convertToShares(amount);
    sharesOwed[currentEpoch] += shares; // Fixed at current rate
}

function settleEpoch() external {
    // If shares appreciated (like ERC4626), actual shares < shares owed
    // With idle funds in deposit pool, total available < total owed
    // REVERTS: INCORRECT_NUMBER_OF_SHARES_QUEUED
    delegationManager.completeQueuedWithdrawal(withdrawal, ...);
}
```

**Example 3: stETH Request/Claim Amount Mismatch** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-lidolockedeth-value-can-block-full-redeeming-of-puffeth-in-vault.md`
```solidity
// ❌ VULNERABLE: lidoLockedETH mismatch accumulates over time
function initiateWithdrawal(uint256 amount) external {
    lidoLockedETH += amount; // Tracks requested amount
    lido.requestWithdrawals(amount);
}

function claimWithdrawal() external {
    uint256 received = address(this).balance - balanceBefore;
    lidoLockedETH -= received; // Actual received < requested (stETH rounding)
    // Residual: lidoLockedETH ratchets upward, inflating totalAssets()
}
```

**Example 4: Yield Token vs Underlying Asset Valuation Mismatch** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-6-the-_getvalueofwithdrawrequest-function-uses-different-methods-for-selecting.md`
```solidity
// ❌ VULNERABLE: Different vaults use inconsistent valuation for withdrawal queue
function _getValueOfWithdrawRequest(address vault) internal returns (uint256) {
    if (vault == sUSDe_vault) {
        // Prices at yield token rate (sUSDe → USDe conversion rate)
        return request.shares * sUSDe.convertToAssets(1e18);
    } else if (vault == stETH_vault) {
        // Prices at fixed 1:1 rate
        return request.amount;
    }
    // Inconsistent: sUSDe withdrawal price changes, stETH doesn't
}
```

### Impact Analysis

#### Technical Impact
- Direct loss of user principal: up to 1.5 ETH per withdrawal via rounding (1/34 reports)
- Permanent settlement failure: total shares owed exceed available (1/34 reports)
- Inflated `totalAssets()`: phantom locked amounts inflate share price (3/34 reports)
- Incorrect liquidation triggers: withdrawal queue valued inconsistently

#### Business Impact
- Protocol-level insolvency from accumulated accounting drift
- Users receive less than entitled during withdrawal
- Yield loss during withdrawal delay not compensated
- **Financial impact observed:** 1.5 ETH loss per withdrawal; protocol insolvency at scale

#### Affected Scenarios
- ERC4626-style strategies where shares appreciate over time
- stETH/rebasing token withdrawals (request ≠ received)
- Multi-asset protocols with different oracle/valuation methods per asset
- Penalized validators with reduced effective balance

### Secure Implementation

**Fix 1: Use Actual Amounts for Withdrawals**
```solidity
// ✅ SECURE: Don't apply rounding functions to withdrawal amounts
function _processFullWithdrawal(uint64 withdrawalAmountGwei, ...) internal {
    // Return actual withdrawal amount, not the rounded restaked balance
    uint64 amountToSend = withdrawalAmountGwei;
    uint64 restakedBalance = _calculateRestakedBalanceGwei(withdrawalAmountGwei);
    
    // Return excess immediately
    uint64 excess = amountToSend - restakedBalance;
    _sendETH(podOwner, amountToSend * GWEI_TO_WEI);
}
```

**Fix 2: Track Actual vs Requested Amounts**
```solidity
// ✅ SECURE: Subtract requested amount, not received amount
function claimWithdrawal(uint256 requestId) external {
    uint256 requestedAmount = withdrawalRequests[requestId].amount;
    lidoLockedETH -= requestedAmount; // Always decrement by what was requested
    
    uint256 received = address(this).balance - balanceBefore;
    // Any shortfall is a real loss, reflected in totalAssets accurately
}
```

**Fix 3: Adjust Shares for Appreciation**
```solidity
// ✅ SECURE: Account for share value changes between request and settlement
function settleEpoch(uint256 epoch) external {
    uint256 currentRate = strategy.sharesToUnderlying(1e18);
    uint256 requestRate = epochRequestRate[epoch];
    
    // Adjust shares owed based on rate change
    uint256 adjustedShares = sharesOwed[epoch] * requestRate / currentRate;
    delegationManager.completeQueuedWithdrawal(adjustedShares, ...);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `_calculateRestakedBalanceGwei()` applied to withdrawal amounts
- Pattern 2: `sharesOwed` fixed at request time without update mechanism
- Pattern 3: `lidoLockedETH -= msg.value` (received) instead of `lidoLockedETH -= requestedAmount`
- Pattern 4: Different `_getValueOfWithdrawRequest()` methods across vault types
- Pattern 5: No yield accrual during withdrawal delay period
```

#### Audit Checklist
- [ ] Are rounding/validation functions designed for deposits also applied to withdrawals?
- [ ] Do withdrawal amounts update when share-to-asset ratios change during the delay?
- [ ] Is `totalAssets()` accurate after partial claims (received < requested)?
- [ ] Are withdrawal queue entries valued consistently across all asset types?
- [ ] Do withdrawing users earn yield during the withdrawal delay?

---

## 3. Fund Lockup During Withdrawal

### Overview

Withdrawal funds become permanently locked due to missing functionality, interface incompatibilities, ETH transfer mechanism failures, zero-denominator edge cases, or all-or-nothing batch finalization patterns. This is the most common withdrawal vulnerability category (10/34 reports).

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-01-withdrawals-can-be-locked-forever-if-recipient-is-a-contract.md` (Renzo - Code4rena)
> - `reports/eigenlayer_findings/h-03-lack-of-withdrawal-functionality-in-strategy-contracts.md` (Nexus - Pashov)
> - `reports/eigenlayer_findings/h-06-users-cannot-unstake-from-yiedlethstakingetherfisol-because-yieldaccountsol.md` (BendDAO - Code4rena)
> - `reports/eigenlayer_findings/h-13-kelp_finalizecooldown-cannot-claim-the-withdrawal-if-adversary-would-reques.md` (Notional - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **withdrawal flows assume ideal execution conditions** — strategies always have withdrawal functions, ETH transfers always succeed, external protocols always return expected values, and batch operations are atomic. In practice, any single point of failure in the withdrawal chain permanently locks funds.

**Frequency:** Very Common (10/34 reports)
**Validation:** Strong — 6+ independent auditors

#### Attack Scenario (ETH Transfer Lockup)

1. User calls `withdraw()` which records their address as recipient
2. Later, `claim()` uses `payable(msg.sender).transfer(amount)` to send ETH
3. If msg.sender is a multisig/smart wallet with `receive()` requiring >2300 gas, transfer reverts
4. The 2-step design locked the address at `withdraw()` time — user can't change recipient
5. ETH is permanently locked in the WithdrawQueue contract

### Vulnerable Pattern Examples

**Example 1: transfer() Instead of call() for ETH** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-01-withdrawals-can-be-locked-forever-if-recipient-is-a-contract.md`
```solidity
// ❌ VULNERABLE: transfer() has 2300 gas limit — fails for smart wallets
function claim(uint256 withdrawRequestIndex) external {
    WithdrawRequest memory request = withdrawQueue[msg.sender][withdrawRequestIndex];
    require(block.timestamp >= request.claimTimestamp, "Not ready");
    
    // BUG: 2300 gas limit, multisigs/smart wallets will revert
    payable(msg.sender).transfer(request.amountToRedeem);
}
```

**Example 2: Missing Withdrawal Implementation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-03-lack-of-withdrawal-functionality-in-strategy-contracts.md`
```solidity
// ❌ VULNERABLE: Strategy has deposit but no withdraw
contract LidoStrategy is IStrategy {
    function deposit(uint256 amount) external {
        IERC20(stETH).transferFrom(msg.sender, address(this), amount);
        // Deposits to Lido
    }
    
    // BUG: No withdraw() function exists
    // Protocol can never retrieve deposited tokens or rewards
}
```

**Example 3: Missing ERC721 Receiver Interface** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-06-users-cannot-unstake-from-yiedlethstakingetherfisol-because-yieldaccountsol.md`
```solidity
// ❌ VULNERABLE: YieldAccount doesn't implement onERC721Received
contract YieldAccount is IYieldAccount, Initializable {
    // BUG: Missing ERC721Holder/onERC721Received
    // EtherFi's WithdrawRequestNFT uses _safeMint which requires this interface
    // All unstake attempts revert with "ERC721: transfer to non ERC721Receiver"
}
```

**Example 4: Hardcoded Withdrawal Request Index** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-13-kelp_finalizecooldown-cannot-claim-the-withdrawal-if-adversary-would-reques.md`
```solidity
// ❌ VULNERABLE: Always claims the 0th request — can be front-run
function _finalizeCooldown() internal {
    uint256[] memory requestIds = new uint256[](1);
    requestIds[0] = stETH.getWithdrawalRequests(address(this))[0]; // Always index 0
    // Adversary front-runs with dust requestWithdrawals, pushing real request to index 1
    stETH.claimWithdrawals(requestIds);
}
```

**Example 5: Last Holder Division by Zero** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`
```solidity
// ❌ VULNERABLE: Burns entire supply before processing the withdrawal
function initiate_unstake(uint256 amount) external {
    _burn(msg.sender, amount);
    // If last holder: totalSupply() now equals 0
}

function process_unstake() external {
    // BUG: Division by zero when all supply has been burned
    let ratio = bigdecimal::from_ratio_u128(unstake_amount, sx_init_amount); // 0 denominator!
}
```

**Example 6: All-or-Nothing Batch Finalization** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-21-funds-stuck-if-one-of-the-withdrawal-requests-cannot-be-finalized.md`
```solidity
// ❌ VULNERABLE: Single failure blocks all withdrawals
function finalizeWithdrawals() external {
    for (uint256 i = 0; i < requests.length; i++) {
        bool finalized = _checkFinalized(requests[i]);
        if (!finalized) revert WithdrawalNotFinalized(); // Blocks entire batch
        _processWithdrawal(requests[i]);
    }
}
```

### Impact Analysis

#### Technical Impact
- Permanent fund lockup: users cannot retrieve deposited ETH/tokens (10/34 reports)
- Missing strategy withdrawal creates irrecoverable assets
- Interface incompatibility permanently blocks unstaking
- Batch failures cascade to all pending withdrawals

#### Business Impact
- Complete loss of user funds in affected protocols
- Protocol forced to deploy upgrades to recover funds (if proxy-based)
- Severe reputation damage
- **Financial impact observed:** Entire protocol TVL at risk for missing withdrawal functions; per-user lockup for transfer failures

#### Affected Scenarios
- Smart wallet / multisig users calling withdrawal functions
- Integration with EtherFi, Lido, or other LSTs that use `_safeMint`
- Strategies deployed without withdrawal functions
- Batch withdrawal processing with heterogeneous underlying protocols
- Last-user-exits scenarios with zero total supply

### Secure Implementation

**Fix 1: Use call() for ETH Transfers**
```solidity
// ✅ SECURE: No gas limit, compatible with all recipients
function claim(uint256 withdrawRequestIndex) external {
    WithdrawRequest memory request = withdrawQueue[msg.sender][withdrawRequestIndex];
    require(block.timestamp >= request.claimTimestamp, "Not ready");
    
    (bool success, ) = payable(msg.sender).call{value: request.amountToRedeem}("");
    require(success, "ETH transfer failed");
}
```

**Fix 2: Track Withdrawal Request IDs**
```solidity
// ✅ SECURE: Track specific request IDs instead of hardcoding index
function _triggerCooldown(uint256 amount) internal {
    uint256 requestId = stETH.requestWithdrawals(amount);
    pendingRequestIds.push(requestId); // Store the actual ID
}

function _finalizeCooldown() internal {
    uint256 requestId = pendingRequestIds[pendingRequestIds.length - 1];
    stETH.claimWithdrawal(requestId); // Use stored ID, not index 0
}
```

**Fix 3: Independent Request Processing**
```solidity
// ✅ SECURE: Handle each withdrawal request independently
function finalizeWithdrawals() external {
    for (uint256 i = 0; i < requests.length; i++) {
        try this._processWithdrawal(requests[i]) {
            // Success
        } catch {
            // Mark as failed, allow retry
            requests[i].status = Status.FAILED;
            emit WithdrawalFailed(i);
        }
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `payable.transfer()` or `payable.send()` for ETH transfers
- Pattern 2: Strategy contracts with `deposit()` but no `withdraw()` function
- Pattern 3: `_safeMint` targets without `onERC721Received` implementation
- Pattern 4: Hardcoded array index `[0]` for withdrawal request claims
- Pattern 5: Division by `totalSupply` without zero-check
- Pattern 6: `if (!finalized) revert` inside batch processing loops
- Pattern 7: Single boolean flag for both request and claim operations
```

#### Audit Checklist
- [ ] Does every ETH transfer use `call{value:}` instead of `transfer()`?
- [ ] Does every deposit-taking strategy have a corresponding withdrawal function?
- [ ] Do all contracts receiving ERC721 tokens implement `onERC721Received`?
- [ ] Are withdrawal request IDs tracked instead of assumed by index?
- [ ] Is there a zero-supply guard before division operations?
- [ ] Can individual withdrawal requests be processed independently?
- [ ] Are request and claim operations gated by separate flags?

---

## 4. Slashing Interaction with Withdrawals

### Overview

Slashing events occurring during the 2-step withdrawal process create irrecoverable accounting errors. When EigenLayer slashes queued withdrawals, the LRT protocol's pending amount tracking, withdrawal roots, and share balances diverge from reality.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` (Puffer Finance - Immunefi)
> - `reports/eigenlayer_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` (EigenLayer - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **mid-withdrawal slashing invalidates the withdrawal root** used to claim. When `slashQueuedWithdrawal` is called between initiation and claim, the withdrawal root is set to `false`, making `claimWithdrawal` permanently revert. The protocol's pending share counters are never corrected.

**Frequency:** Moderate (3/34 reports)
**Validation:** Strong — 3 independent auditors (Immunefi, Code4rena)

### Vulnerable Pattern Examples

**Example 1: Withdrawal Root Invalidated by Slashing** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`
```solidity
// ❌ VULNERABLE: No handling of slashing between initiate and claim
function initiateWithdrawal(uint256 shares) external {
    eigenLayerPendingWithdrawalSharesAmount += shares;
    withdrawalRoot = delegationManager.queueWithdrawals(shares);
    withdrawalRootPending[withdrawalRoot] = true;
}

function claimWithdrawal(bytes32 root) external {
    require(withdrawalRootPending[root], "Not pending");
    // If slashQueuedWithdrawal was called, root is no longer valid in EigenLayer
    // This call reverts permanently
    delegationManager.completeQueuedWithdrawal(root, ...);
    
    // eigenLayerPendingWithdrawalSharesAmount is NEVER decremented
    // totalAssets() permanently inflated
}
```

**Example 2: Broken Loop Index in slashQueuedWithdrawal** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
```solidity
// ❌ VULNERABLE: ++i inside else block — loop skips when index should be skipped
function slashQueuedWithdrawal(
    address recipient,
    QueuedWithdrawal memory queuedWithdrawal,
    IERC20[] memory tokens,
    uint256[] memory indicesToSkip
) external onlyOwner {
    for (uint256 i = 0; i < tokens.length; ) {
        if (indicesToSkip[currentSkipIndex] == i) {
            currentSkipIndex++;
            // BUG: ++i is in the else block, so when we skip, i doesn't increment
            // Loop processes same index forever
        } else {
            tokens[i].safeTransfer(recipient, amounts[i]);
            unchecked { ++i; } // This should be outside the if/else
        }
    }
}
```

### Impact Analysis

#### Technical Impact
- Protocol insolvency: `totalAssets()` permanently inflated by phantom pending shares
- Unslashable queued withdrawals defeat the entire slashing mechanism
- Withdrawal roots become permanently invalid after mid-flight slashing

#### Business Impact
- Bank run risk: later withdrawers discover protocol is insolvent
- Security model undermined: adversaries include malicious strategies that can't be slashed
- **Financial impact observed:** Full protocol TVL at risk

### Secure Implementation

**Fix 1: Handle Slashed Withdrawals Gracefully**
```solidity
// ✅ SECURE: Try/catch with accounting correction
function claimWithdrawal(bytes32 root) external {
    require(withdrawalRootPending[root], "Not pending");
    
    try delegationManager.completeQueuedWithdrawal(root, ...) {
        eigenLayerPendingWithdrawalSharesAmount -= withdrawalShares[root];
    } catch {
        // Withdrawal was slashed — correct the accounting
        eigenLayerPendingWithdrawalSharesAmount -= withdrawalShares[root];
        withdrawalRootPending[root] = false;
        emit WithdrawalSlashed(root, withdrawalShares[root]);
    }
}
```

**Fix 2: Correct Loop Index Placement**
```solidity
// ✅ SECURE: Increment outside the if/else
for (uint256 i = 0; i < tokens.length; ) {
    if (indicesToSkip[currentSkipIndex] == i) {
        currentSkipIndex++;
    } else {
        tokens[i].safeTransfer(recipient, amounts[i]);
    }
    unchecked { ++i; } // Always increment
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: 2-step withdrawal without try/catch on the claim step
- Pattern 2: `eigenLayerPendingWithdrawalSharesAmount` with no correction path on failure
- Pattern 3: `unchecked { ++i; }` inside conditional branches of a loop
- Pattern 4: `withdrawalRootPending` state not updated when EigenLayer invalidates the root
```

#### Audit Checklist
- [ ] Does the claim function handle the case where EigenLayer has already slashed the withdrawal?
- [ ] Is the pending withdrawal counter decremented on both success AND failure?
- [ ] Does `totalAssets()` correctly exclude slashed withdrawal amounts?
- [ ] Are loop indices correctly incremented in all branches (including skip logic)?

---

## 5. Withdrawal Delay Bypass

### Overview

Withdrawal delay mechanisms that enforce a minimum lockup period before users can access funds can be bypassed or become uninitialized, undermining the security assumptions of the restaking protocol.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/lockup-period-for-unstaking-can-be-decreased-by-staking-again-with-shorter-locku.md` (Sapien - Quantstamp)
> - `reports/eigenlayer_findings/withdrawaldelayblocks-cannot-be-initialised-after-m2-upgrade.md` (EigenLayer - SigmaPrime)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **withdrawal delays are either recalculable, uninitialized after upgrades, or not updated on retry**. Weighted-average lockup recalculation allows dilution via large short-lockup stakes. Storage variables settable only in `initialize()` become stuck after proxy upgrades. L1 operation timestamps aren't refreshed on retry.

**Frequency:** Moderate (3/34 reports)
**Validation:** Moderate — 3 auditors (Quantstamp, SigmaPrime, Spearbit)

### Vulnerable Pattern Examples

**Example 1: Lockup Dilution via Re-Staking** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/lockup-period-for-unstaking-can-be-decreased-by-staking-again-with-shorter-locku.md`
```solidity
// ❌ VULNERABLE: Weighted average allows lockup dilution
function stake(uint256 amount, uint256 lockupDays) external {
    uint256 existingWeight = stakers[msg.sender].amount * stakers[msg.sender].lockupDays;
    uint256 newWeight = amount * lockupDays;
    uint256 totalAmount = stakers[msg.sender].amount + amount;
    
    // BUG: Attacker stakes 100x amount with 1-day lockup to dilute 365-day lockup
    stakers[msg.sender].lockupDays = (existingWeight + newWeight) / totalAmount;
    stakers[msg.sender].amount = totalAmount;
}
```

**Example 2: Delay Variable Not Initialized After Upgrade** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/withdrawaldelayblocks-cannot-be-initialised-after-m2-upgrade.md`
```solidity
// ❌ VULNERABLE: withdrawalDelayBlocks can only be set in initialize()
contract DelegationManager is Initializable {
    uint256 public withdrawalDelayBlocks;
    
    function initialize(uint256 _withdrawalDelayBlocks) external initializer {
        withdrawalDelayBlocks = _withdrawalDelayBlocks;
    }
    
    // After M2 upgrade: initialize() already called → can't set new delay
    // withdrawalDelayBlocks = 0 → no withdrawal delay enforced
}
```

### Secure Implementation

**Fix 1: Enforce Monotonic Lockup**
```solidity
// ✅ SECURE: New stakes cannot reduce existing lockup
function stake(uint256 amount, uint256 lockupDays) external {
    require(
        lockupDays >= stakers[msg.sender].lockupDays,
        "Cannot reduce lockup period"
    );
    stakers[msg.sender].amount += amount;
    stakers[msg.sender].lockupDays = lockupDays; // Only increases
}
```

**Fix 2: Post-Initialization Setter**
```solidity
// ✅ SECURE: Allow owner to set delay after upgrade
function setMinWithdrawalDelayBlocks(uint256 _delay) external onlyOwner {
    require(_delay <= MAX_WITHDRAWAL_DELAY_BLOCKS, "Exceeds max");
    withdrawalDelayBlocks = _delay;
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Can lockup periods be reduced by re-staking with a shorter duration?
- [ ] Are withdrawal delay variables settable via a post-initialization function?
- [ ] Are timestamps updated when L1 operations are retried?
- [ ] Does the delay calculation use the actual processing timestamp, not the original queue timestamp?

---

## 6. Missing Slippage/Deadline Protection

### Overview

Withdrawal and deposit functions that rely on oracle prices lack user-specified minimum output and deadline parameters, exposing users to value loss from oracle fluctuations, MEV sandwich attacks, and shared cooldown DoS.

**Frequency:** Moderate (2/34 reports, plus cross-references in other categories)
**Validation:** Moderate — 2 auditors (Code4rena)

### Vulnerable Pattern Examples

**Example 1: No Slippage on LRT Withdrawal** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`
```solidity
// ❌ VULNERABLE: No minimum output or deadline
function withdraw(uint256 ezETHAmount) external {
    uint256 ethAmount = calculateRedeemAmount(ezETHAmount); // Oracle-dependent
    // No minEthAmount parameter — user can't protect against adverse price movement
    // No deadline parameter — transaction can execute at any future time
    _processWithdrawal(msg.sender, ethAmount);
}
```

**Example 2: Shared Cooldown DoS on Redemption** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-01-the-redeem-related-functions-are-likely-to-be-blocked.md`
```solidity
// ❌ VULNERABLE: Shared cooldown timer across all users
// Any deposit by any Pirex user resets the GMX cooldown for ALL users
function redeemPxGlp(uint256 amount) external {
    // Reverts if within cooldown period
    require(block.timestamp >= lastActionTime + cooldownDuration, "Cooldown");
    // BUG: lastActionTime is reset by ANY user's deposit, not per-user
    // Attacker deposits every block for ~$9.6/day to permanently block all redemptions
}
```

### Secure Implementation

```solidity
// ✅ SECURE: User-specified slippage and deadline
function withdraw(
    uint256 ezETHAmount,
    uint256 minEthAmount,  // Slippage protection
    uint256 deadline        // Transaction expiry
) external {
    require(block.timestamp <= deadline, "Transaction expired");
    uint256 ethAmount = calculateRedeemAmount(ezETHAmount);
    require(ethAmount >= minEthAmount, "Slippage exceeded");
    _processWithdrawal(msg.sender, ethAmount);
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Do all deposit/withdrawal functions accept `minAmountOut` parameters?
- [ ] Do all functions accept `deadline` parameters?
- [ ] Are cooldown timers per-user rather than per-contract?
- [ ] Is there a mechanism to defend against MEV sandwiching on oracle-priced operations?

---

## 7. Partial Failure Handling

### Overview

Batch withdrawal operations that assume atomicity (all succeed or all fail) create vulnerability when any single request fails. One stuck or failed request blocks all subsequent withdrawals.

**Frequency:** Moderate (3/34 reports)
**Validation:** Strong — 3 independent auditors (Immunefi, Sherlock)

### Vulnerable Pattern Examples

**Example 1: Gas Griefing Causes Batch Cancellation** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-31-keeper-can-make-depositsorderswithdrawals-fail-and-receive-feerewards.md`
```solidity
// ❌ VULNERABLE: 63/64 gas rule allows targeted failure
function executeWithdrawal(bytes32 key) external {
    try this._executeWithdrawal(key) {
        // Success path
    } catch {
        // Catch path: cancels the entire withdrawal, keeper still gets fee
        _cancelWithdrawal(key);
        payExecutionFee(msg.sender); // Keeper gets paid for causing failure
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Per-request error handling with retry
function executeBatchWithdrawals(bytes32[] calldata keys) external {
    for (uint256 i = 0; i < keys.length; i++) {
        try this._executeWithdrawal(keys[i]) {
            emit WithdrawalCompleted(keys[i]);
        } catch {
            // Mark as failed, allow retry later — don't cancel
            failedWithdrawals[keys[i]] = true;
            emit WithdrawalFailed(keys[i]);
        }
    }
}
```

---

## 8. Reentrancy and Access Control in Withdrawal Flows

### Overview

Missing reentrancy protection and insufficient access control on withdrawal-related functions allow manipulation or theft during the unstaking process.

**Frequency:** Moderate (3/34 reports)
**Validation:** Moderate — 3 auditors (Hexens, Code4rena)

### Vulnerable Pattern Examples

**Example 1: Reentrancy During Unstaking** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md`
```solidity
// ❌ VULNERABLE: update() callable during swap callback
function update() external {
    uint256 surplus = HYPE.balanceOf(address(this)) - totalStaked;
    if (surplus > 0) {
        // Transfers surplus to SovereignPool
        HYPE.transfer(sovereignPool, surplus);
    }
}

// Attack: Attacker initiates swap → in swap callback, calls update()
// Surplus is "donated" to pool during swap, attacker uses it as swap payment
// Result: Attacker gets stHYPE for free
```

**Example 2: Missing Pause Modifier on Withdrawals** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-02-withdrawals-and-claims-are-meant-to-be-pausable-but-it-is-not-possible-in-p.md`
```solidity
// ❌ VULNERABLE: Inherits PausableUpgradeable but doesn't use it
contract WithdrawQueue is PausableUpgradeable {
    function withdraw(uint256 amount) external {
        // BUG: Missing `whenNotPaused` modifier
        _processWithdrawal(msg.sender, amount);
    }
    
    function claim(uint256 index) external {
        // BUG: Missing `whenNotPaused` modifier
        _processClaim(msg.sender, index);
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Reentrancy guard and pause modifier
contract WithdrawQueue is PausableUpgradeable, ReentrancyGuard {
    function withdraw(uint256 amount) external nonReentrant whenNotPaused {
        _processWithdrawal(msg.sender, amount);
    }
    
    function claim(uint256 index) external nonReentrant whenNotPaused {
        _processClaim(msg.sender, index);
    }
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Increment epoch counters atomically with EigenLayer withdrawal initiation
2. Use `call{value:}` for all ETH transfers — never `transfer()` or `send()`
3. Implement withdrawal functions for every strategy that accepts deposits
4. Add `nonReentrant` and `whenNotPaused` modifiers to all withdrawal functions
5. Track withdrawal request IDs explicitly — never assume array indices
6. Handle mid-flight slashing with try/catch and accounting correction
7. Add `minAmountOut` and `deadline` parameters to all user-facing functions
8. Process batch withdrawals independently with per-request error handling

#### Testing Requirements
- Unit tests for: withdrawal with zero total supply, slash during withdrawal delay, re-staking with shorter lockup
- Integration tests for: EigenLayer settlement with share appreciation, stETH claim with rounding, batch withdrawal with partial failures
- Fuzzing targets: share-to-asset conversion ratios, lockup period calculations, queue state transitions

### Keywords for Search

> These keywords enhance vector search retrieval:

`withdrawal`, `unstaking`, `withdraw queue`, `queued withdrawal`, `withdrawal delay`, `cooldown`, `fund lockup`, `permanently locked`, `settlement`, `epoch`, `eigenlayer withdrawal`, `completeQueuedWithdrawal`, `claimWithdrawal`, `pending withdrawal`, `share calculation`, `rounding error`, `partial failure`, `slashing during withdrawal`, `lockup bypass`, `slippage protection`, `MEV`, `sandwich`, `reentrancy`, `transfer vs call`, `payable transfer`, `onERC721Received`, `safeMint`, `zero supply`, `batch finalization`, `restaking`, `LRT`, `liquid restaking token`, `puffer`, `renzo`, `kelp`, `rio network`, `eigenpod`

### Related Vulnerabilities

- [EigenPod Beacon Chain Verification](EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md)
- [Restaking Slashing Mechanism](RESTAKING_SLASHING_VULNERABILITIES.md)
- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)
- [LRT Exchange Rate and Oracle](LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md)
- [Restaking Operator and Delegation](RESTAKING_OPERATOR_DELEGATION_VULNERABILITIES.md)
