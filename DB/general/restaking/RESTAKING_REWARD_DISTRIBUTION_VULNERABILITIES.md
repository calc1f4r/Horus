---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: reward_distribution

# Attack Vector Details (Required)
attack_type: front_running|logical_error|reentrancy|access_control
affected_component: reward_distributor|staking_rewards|claim_function|accounting

# Technical Primitives (Required)
primitives:
  - reward_distribution
  - front_running
  - sandwich_attack
  - reward_theft
  - permissionless_claim
  - msg_sender_confusion
  - time_weighted
  - reward_accounting
  - reentrancy
  - execution_layer_rewards
  - staking_rewards

# Impact Classification (Required)
severity: high|medium
impact: fund_loss|reward_theft|dos|locked_rewards
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - rewards
  - staking
  - front-running
  - sandwich
  - reentrancy
  - accounting

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Front-Running / Sandwich Attacks on Reward Distribution
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Front-Running Reward Distribution (CAP Labs) | `reports/eigenlayer_findings/reward-distribution-enables-front-running-attacks-and-reward-siphoning.md` | HIGH | Trail of Bits |
| Sandwiching claimDelayedWithdrawals() | `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md` | MEDIUM | Sherlock |
| Front-Running rewardValidators() | `reports/eigenlayer_findings/m-02-front-running-rewardvalidators-to-dilute-steal-rewards.md` | MEDIUM | Sherlock |
| No cooldown in recoverUnstaking() | `reports/eigenlayer_findings/m-03-no-cooldown-in-recoverunstaking-enables-reward-siphoning.md` | MEDIUM | Sherlock |
| Sandwich AutoPxGmx.compound | `reports/eigenlayer_findings/m-sandwich-attack-on-autopxgmx-compound.md` | MEDIUM | Code4rena |

### Reward Accounting Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Direct Loss from msg.sender Confusion | `reports/eigenlayer_findings/critical-direct-loss-of-rewards-on-restaking-msg-sender-confusion.md` | CRITICAL | Shieldify |
| Delayed Rewards Bypass Accounting | `reports/eigenlayer_findings/delayed-rewards-can-be-claimed-without-updating-internal-accounting.md` | HIGH | Cyfrin |
| rewardStakeRatioSum Double Counting | `reports/eigenlayer_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-delayed-balance-or-rewards-a.md` | HIGH | Cyfrin |
| RewardsManager Stale Bucket Snapshots | `reports/eigenlayer_findings/h-rewardsmanager-doesnt-delete-old-bucket-snapshot-on-unstaking.md` | HIGH | Sherlock |

### Rewards Lost / Unclaimable
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Execution Layer Rewards Lost | `reports/eigenlayer_findings/m-16-execution-layer-rewards-are-lost.md` | MEDIUM | Sherlock |
| Low Gas Limit Prevents Reward Receipt | `reports/eigenlayer_findings/m-05-low-gas-limit-prevents-reward-receipt.md` | MEDIUM | Sherlock |
| Missing claimAllRewards Implementation | `reports/eigenlayer_findings/inability-to-claim-protocol-rewards-missing-implementation.md` | HIGH | Cantina |
| EigenPod Balance > 16 ETH Blocks Rewards | `reports/eigenlayer_findings/h-reward-calculation-blocked-if-eigenpod-balance-exceeds-16-eth.md` | HIGH | MixBytes |
| Rewards Re-Staked on Exit Instead of Withdrawn | `reports/eigenlayer_findings/m-user-rewards-restaked-on-exit-instead-of-withdrawn.md` | MEDIUM | Cyfrin |
| Referral Rewards Lost (Self-Referral) | `reports/eigenlayer_findings/m-referral-rewards-lost-self-referral.md` | MEDIUM | Sherlock |

### Reentrancy-Based Reward Theft  
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Reentrancy in VaultRewarderLib | `reports/eigenlayer_findings/h-steal-reward-tokens-via-reentrancy-in-vaultrewarderlib.md` | HIGH | Sherlock |
| Withdraw Stake Before Claim = Permanent Loss | `reports/eigenlayer_findings/h-withdrawing-stake-before-claiming-rewards-permanent-loss.md` | HIGH | Pashov |

### Access Control on Reward Claims
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Access Control for claimRewards | `reports/eigenlayer_findings/m-missing-access-control-for-claiming-rewards.md` | MEDIUM | Halborn |

---

# Restaking Reward Distribution Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Reward Distribution Security in Restaking Protocols**

---

## Table of Contents

1. [Sandwich / Front-Running Reward Claims](#1-sandwich--front-running-reward-claims)
2. [msg.sender Confusion in Reward Re-Staking](#2-msgsender-confusion-in-reward-re-staking)
3. [Reward Accounting Double-Counting](#3-reward-accounting-double-counting)
4. [Stale Snapshot Data After Unstaking](#4-stale-snapshot-data-after-unstaking)
5. [Rewards Lost — Missing Implementations](#5-rewards-lost--missing-implementations)
6. [Reentrancy-Based Reward Theft](#6-reentrancy-based-reward-theft)
7. [Reward Dilution via Just-In-Time Staking](#7-reward-dilution-via-just-in-time-staking)

---

## 1. Sandwich / Front-Running Reward Claims

### Overview

Permissionless reward claim functions that instantly increase TVL enable sandwich attacks: deposit before claim, claim (TVL increases), withdraw at higher exchange rate. This captures rewards that belong to long-term stakers.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/reward-distribution-enables-front-running-attacks-and-reward-siphoning.md` (CAP Labs - Trail of Bits)
> - `reports/eigenlayer_findings/m-sandwich-attack-on-autopxgmx-compound.md` (Redacted Cartel - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **reward claim functions are permissionless and instantly increase the contract's TVL/balance**, allowing attackers to atomically deposit before + withdraw after, capturing a proportional share of rewards without long-term staking.

**Frequency:** Common (5/19 reports)
**Validation:** Strong — 3 independent auditors (Sherlock, Trail of Bits, Code4rena)

### Vulnerable Pattern Examples

**Example 1: Sandwich claimDelayedWithdrawals** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md`
```solidity
// ❌ VULNERABLE: Permissionless claim instantly increases TVL
// Attack sequence:
// 1. Deposit 40 ETH, receive ~40e18 LRT tokens
reETH.coordinator.depositETH{value: 40 ether}();

// 2. Call permissionless claim — TVL increases by 7.2 ETH instantly
delayedWithdrawalRouter.claimDelayedWithdrawals(
    address(operatorDelegator), 1
);

// 3. Withdraw all — captures proportional share of 7.2 ETH rewards
reETH.coordinator.requestWithdrawal(
    ETH_ADDRESS, reETH.token.balanceOf(attacker)
);
// Result: ~3.59 ETH profit from zero staking duration
```

**Example 2: AMM Compound Function Sandwich** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-sandwich-attack-on-autopxgmx-compound.md`
```solidity
// ❌ VULNERABLE: Caller controls swap parameters
SWAP_ROUTER.exactInputSingle(ISwapRouter.ExactInputSingleParams({
    tokenIn: gmx,
    tokenOut: pxGmx,
    fee: params.fee,            // Caller controls — routes to illiquid pool
    recipient: address(this),
    amountIn: gmxAmountIn,
    amountOutMinimum: 1,        // Accepts maximum slippage!
    sqrtPriceLimitX96: 0
}));
```

### Impact Analysis

- **Financial impact observed:** ~50% of rewards stolen per attack (3.59 ETH on 7.2 ETH rewards)
- Repeatable every time rewards accumulate
- Long-term stakers continuously diluted

### Secure Implementation

```solidity
// ✅ SECURE: Time-weighted reward distribution
function claimRewards() external {
    uint256 rewardsAmount = _claimFromEigenLayer();
    
    // Option 1: Add to pending rewards, distribute over time
    pendingRewards += rewardsAmount;
    rewardsDistributionEndTime = block.timestamp + DISTRIBUTION_PERIOD;
    
    // Option 2: Snapshot-based — only distribute to depositors before claim
    rewardsPerShareSnapshot = rewardsAmount * 1e18 / totalSharesAtLastSnapshot;
}

// ✅ SECURE: Use oracle for compound swap parameters
function compound() external {
    uint256 amountOutMin = oracle.getPrice(gmx, pxGmx) * gmxAmountIn * 
                           (10000 - MAX_SLIPPAGE_BPS) / 10000;
    SWAP_ROUTER.exactInputSingle(ISwapRouter.ExactInputSingleParams({
        fee: poolFee,           // Protocol-controlled
        amountOutMinimum: amountOutMin,  // Oracle-derived
        // ...
    }));
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Are reward claim functions permissionless?
- [ ] Does claiming instantly increase TVL/balance?
- [ ] Can deposits + withdrawals be performed atomically around claims?
- [ ] Do swap parameters come from caller input without validation?

---

## 2. msg.sender Confusion in Reward Re-Staking

### Overview

Using `this.stake(reward)` (external call) instead of an internal call changes `msg.sender` from the user to the contract itself, causing rewards to be staked to the contract's account instead of the user's.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/critical-direct-loss-of-rewards-on-restaking-msg-sender-confusion.md` (Yeet Cup - Shieldify)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`this.stake(reward)` makes an external call, changing `msg.sender` from the user to `address(this)`** in the context of the `stake()` function. The reward amount is credited to the contract, not the user.

**Frequency:** Rare (1/19 reports) but CRITICAL severity
**Validation:** Moderate — Shieldify security

### Vulnerable Pattern Examples

**Example 1: External Call Changes msg.sender** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/critical-direct-loss-of-rewards-on-restaking-msg-sender-confusion.md`
```solidity
// ❌ VULNERABLE: this.stake() makes msg.sender = address(this)
function reStake() external {
    _updateRewards(msg.sender);
    uint reward = earned[msg.sender];
    require(reward > 0, "No rewards to claim");
    earned[msg.sender] = 0;
    
    this.stake(reward); // EXTERNAL CALL! msg.sender becomes address(this)
    // User's earned balance zeroed, but stake goes to the contract itself
}

function stake(uint256 _amount) external {
    // msg.sender is now address(this), not the original user!
    balanceOf[msg.sender] += _amount; // Credits contract, not user
    totalSupply += _amount;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Use internal state modification
function reStake() external {
    _updateRewards(msg.sender);
    uint reward = earned[msg.sender];
    require(reward > 0, "No rewards to claim");
    earned[msg.sender] = 0;
    
    // Direct state modification — no external call
    balanceOf[msg.sender] += reward;
    totalSupply += reward;
    emit Staked(msg.sender, reward);
}
```

---

## 3. Reward Accounting Double-Counting

### Overview

When reward tracking variables are not properly synchronized with external systems (e.g., EigenLayer's DelayedWithdrawalRouter), rewards get counted multiple times across reporting cycles, inflating withdrawal entitlements.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-delayed-balance-or-rewards-a.md` (Casimir - Cyfrin)
> - `reports/eigenlayer_findings/delayed-rewards-can-be-claimed-without-updating-internal-accounting.md` (Casimir - Cyfrin)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **delayed effective balance and delayed rewards are assumed to be claimed between reporting cycles**. If unclaimed, the next report's `reportSweptBalance` counts them again, causing `rewardStakeRatioSum` to increase infinitely each cycle.

**Frequency:** Common (3/19 reports — multiple Casimir findings)
**Validation:** Strong — Cyfrin (2 independent findings from same audit)

### Vulnerable Pattern Examples

**Example 1: Unclaimed Rewards Re-Counted** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-delayed-balance-or-rewards-a.md`
```solidity
// ❌ VULNERABLE: Rewards counted again if not claimed between reports
function completeReport(uint256 reportSweptBalance, ...) external {
    // reportSweptBalance includes EigenPod's full balance
    // If previous rewards weren't claimed, they're still in EigenPod
    // → counted AGAIN in this report's swept balance
    
    uint256 rewards = reportSweptBalance - previousDeposits;
    rewardStakeRatioSum += rewards * 1e18 / activatedDeposits;
    // rewardStakeRatioSum grows indefinitely → users withdraw > deposited
}
```

**Example 2: Direct External Claim Bypasses Accounting** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/delayed-rewards-can-be-claimed-without-updating-internal-accounting.md`
```solidity
// ❌ VULNERABLE: EigenLayer function callable by anyone with CasimirManager as recipient
// Anyone can call: DelayedWithdrawalRouter.claimDelayedWithdrawals(CasimirManager, n)
// This bypasses CasimirManager.claimRewards() which updates:
//   delayedRewards -= claimedAmount;
//   reservedFeeBalance += fees;
// Result: delayedRewards stays inflated, fees never collected
```

### Secure Implementation

```solidity
// ✅ SECURE: Track claimed vs unclaimed in receive() 
receive() external payable {
    if (msg.sender == address(eigenWithdrawals)) {
        // Track exact amount received regardless of claim path
        totalClaimedFromEigenLayer += msg.value;
        delayedRewards -= msg.value;
        uint256 fee = msg.value * feeRate / 1e18;
        reservedFeeBalance += fee;
    }
}

// ✅ SECURE: Use checkpoints, not running sums
function completeReport(uint256 reportSweptBalance) external {
    uint256 previouslyAccounted = lastAccountedSweptBalance;
    uint256 newRewards = reportSweptBalance - previouslyAccounted;
    lastAccountedSweptBalance = reportSweptBalance; // Checkpoint!
    rewardStakeRatioSum += newRewards * 1e18 / activatedDeposits;
}
```

---

## 4. Stale Snapshot Data After Unstaking

### Overview

When Solidity `delete` is used on a struct containing nested mappings, the mappings are not cleared. Re-staking with the same tokenId reuses stale snapshot data, inflating reward calculations.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-rewardsmanager-doesnt-delete-old-bucket-snapshot-on-unstaking.md` (Ajna - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`delete stakes[tokenId_]` doesn't clear the `mapping(uint256 => BucketState) snapshot` nested inside the struct** (Solidity limitation). When the tokenId is restaked, old snapshot values are reused, inflating interest calculations.

**Frequency:** Moderate (2/19 reports)
**Validation:** Moderate — Sherlock (hyh)

### Vulnerable Pattern Examples

**Example 1: Nested Mapping Survives Delete** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-rewardsmanager-doesnt-delete-old-bucket-snapshot-on-unstaking.md`
```solidity
// ❌ VULNERABLE: delete doesn't clear nested mappings
struct StakeInfo {
    address ajnaPool;
    uint96  lastInteractionBurnEpoch;
    address owner;
    uint96  stakingEpoch;
    mapping(uint256 => BucketState) snapshot; // NOT reset by delete!
}

function unstake(uint256 tokenId_) external override {
    if (msg.sender != stakes[tokenId_].owner) revert NotOwnerOfDeposit();
    _claimRewards(tokenId_, IPool(ajnaPool).currentBurnEpoch());
    delete stakes[tokenId_]; // snapshot mapping persists!
}

// Re-staking same tokenId → old snapshot values used for interest calc
function stake(uint256 tokenId_) external override {
    stakes[tokenId_].owner = msg.sender;
    // snapshot[bucketId] still has old values → inflated rewards
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Clear snapshot entries explicitly
function unstake(uint256 tokenId_) external override {
    StakeInfo storage info = stakes[tokenId_];
    
    // Clear each bucket snapshot entry
    uint256[] memory buckets = stakedBuckets[tokenId_];
    for (uint i = 0; i < buckets.length; i++) {
        delete info.snapshot[buckets[i]];
    }
    delete stakedBuckets[tokenId_];
    delete stakes[tokenId_];
}
```

---

## 5. Rewards Lost — Missing Implementations

### Overview

Multiple patterns cause rewards to become permanently unclaimable: missing claim implementations, insufficient gas limits for forwarding, threshold-based reverts, and self-referral addresses.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-16-execution-layer-rewards-are-lost.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/m-05-low-gas-limit-prevents-reward-receipt.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/inability-to-claim-protocol-rewards-missing-implementation.md` (Level Money - Cantina)
> - `reports/eigenlayer_findings/h-reward-calculation-blocked-if-eigenpod-balance-exceeds-16-eth.md` (KelpDAO - MixBytes)

### Vulnerability Description

#### Root Cause (Pattern A — EL Rewards)

Execution layer rewards are credited via balance increases, not ETH transfers. Contracts relying solely on `receive()` never see these rewards.

#### Root Cause (Pattern B — Gas Limit)

Hardcoded gas limits (e.g., `10_000`) are insufficient for multi-hop reward forwarding chains (OperatorDelegator → RewardDistributor → treasury/pool).

#### Root Cause (Pattern C — Missing Implementation)

No function exists to call external protocol reward claim functions (e.g., Aave's `claimAllRewards`, EigenLayer's `RewardsCoordinator`).

**Frequency:** Very Common (6/19 reports)
**Validation:** Strong — 4 independent auditors

### Vulnerable Pattern Examples

**Example 1: Hardcoded Gas Limit Blocks Forwarding** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-05-low-gas-limit-prevents-reward-receipt.md`
```solidity
// ❌ VULNERABLE: 10,000 gas insufficient for multi-hop forwarding
function transferETH(address recipient, uint256 amount) internal {
    (bool success,) = recipient.call{value: amount, gas: 10_000}('');
    if (!success) { revert ETH_TRANSFER_FAILED(); }
    // RewardDistributor.receive() → splits to treasury + pool
    // Each split requires ~8000 gas → total > 10,000 → REVERT
}
```

**Example 2: Self-Referral Loses Rewards** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-referral-rewards-lost-self-referral.md`
```solidity
// ❌ VULNERABLE: address(this) used as referral = self-referral = no rewards
function _ethTOeEth(uint256 _amount) internal returns (uint256) {
    return IeETHLiquidityPool(eETHLiquidityPool).deposit{value: _amount}(
        address(this)  // Depositor and referral are the same → invalid referral
    );
}
```

**Example 3: Missing Claim Implementation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/inability-to-claim-protocol-rewards-missing-implementation.md`
```solidity
// ❌ VULNERABLE: No function to call Aave or EigenLayer reward claims
// Missing:
// - RewardsController.claimAllRewards(assets, address(this))
// - RewardsCoordinator.processClaim(claim, address(this))
// - RewardsController.allowClaimOnBehalf(claimer)
// Result: AAVE, ARB, OP, ZKSYNC rewards permanently locked
```

### Secure Implementation

```solidity
// ✅ SECURE: Remove hardcoded gas limit for protocol addresses
function transferETH(address recipient, uint256 amount) internal {
    (bool success,) = recipient.call{value: amount}('');
    if (!success) { revert ETH_TRANSFER_FAILED(); }
}

// ✅ SECURE: Add reward claim functions
function claimExternalRewards(address rewardsController, address[] calldata assets) external onlyAdmin {
    IRewardsController(rewardsController).claimAllRewards(assets, address(this));
}

// ✅ SECURE: Use owner for referral
function _ethTOeEth(uint256 _amount) internal returns (uint256) {
    return IeETHLiquidityPool(eETHLiquidityPool).deposit{value: _amount}(owner());
}

// ✅ SECURE: Add manual balance sweep for EL rewards
function distributeRemainingBalance() external {
    uint256 value = address(this).balance;
    uint256 treasuryShare = value * treasuryBPS / MAX_BPS;
    _sendETH(treasury, treasuryShare);
    _sendETH(operatorRewardPool, value - treasuryShare);
}
```

---

## 6. Reentrancy-Based Reward Theft

### Overview

Reward claim functions that transfer tokens before finalizing state allow reentrancy attacks via token callbacks, enabling multiple claims of the same rewards.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-steal-reward-tokens-via-reentrancy-in-vaultrewarderlib.md` (Notional - Sherlock)
> - `reports/eigenlayer_findings/h-withdrawing-stake-before-claiming-rewards-permanent-loss.md` (LizardStaking - Pashov)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **reward tokens are transferred before the debt tracker is fully updated, and the claim function lacks a reentrancy guard**. Tokens with transfer hooks (ERC-777, fee-on-transfer callbacks) allow re-entering `claimAccountRewards` mid-execution.

**Frequency:** Moderate (3/19 reports)
**Validation:** Strong — 2 independent auditors (Sherlock, Pashov)

### Vulnerable Pattern Examples

**Example 1: Re-Entering Claim via Token Callback** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-steal-reward-tokens-via-reentrancy-in-vaultrewarderlib.md`
```solidity
// ❌ VULNERABLE: Transfer before state finalization
function _claimRewardToken(address rewardToken, address account, 
                           uint256 vaultSharesBefore, uint256 vaultSharesAfter,
                           uint256 rewardsPerVaultShare) internal returns (uint256 rewardToClaim) {
    rewardToClaim = _getRewardsToClaim(rewardToken, account, vaultSharesBefore, 
                                       vaultSharesAfter, rewardsPerVaultShare);
    
    VaultStorage.getAccountRewardDebt()[rewardToken][account] = (
        (vaultSharesAfter * rewardsPerVaultShare) / INTERNAL_TOKEN_PRECISION
    );
    
    if (0 < rewardToClaim) {
        // Token transfer with callback potential — attacker re-enters here
        try IEIP20NonStandard(rewardToken).transfer(account, rewardToClaim) {
            // Attacker re-enters claimAccountRewards during transfer
            // Debt was set for vaultSharesAfter (10), but re-entry reads it
            // New claim: (10 * 2.0) - 20 = 0... Wait, issues with 
            // vaultSharesBefore on re-entry = vaultSharesAfter from first
        }
    }
}

// Attack: 
// Bob has 100 shares, redeems 90 → first claim: 100 reward tokens
// During transfer callback → re-enter claim → debt=20, shares=10
// Second claim: (10 * 20.0) - 20 = 180 tokens
// Total stolen: 280 tokens
```

**Example 2: Withdraw Deletes Reward Data** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-withdrawing-stake-before-claiming-rewards-permanent-loss.md`
```solidity
// ❌ VULNERABLE: withdrawStake deletes data needed for reward calculation
function withdrawStake(uint256 stakeId) external {
    delete userStakes[msg.sender][stakeId]; // Deletes reward tracking data!
    // If claimReward() was not called first → rewards permanently lost
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Add reentrancy guard + checks-effects-interactions
function _claimRewardToken(...) internal nonReentrant returns (uint256 rewardToClaim) {
    rewardToClaim = _getRewardsToClaim(...);
    
    // Update debt BEFORE transfer
    VaultStorage.getAccountRewardDebt()[rewardToken][account] = 
        (vaultSharesAfter * rewardsPerVaultShare) / PRECISION;
    
    if (rewardToClaim > 0) {
        IERC20(rewardToken).safeTransfer(account, rewardToClaim);
    }
}

// ✅ SECURE: Auto-claim rewards on withdrawal
function withdrawStake(uint256 stakeId) external {
    _claimReward(msg.sender, stakeId); // Claim first!
    delete userStakes[msg.sender][stakeId];
}
```

---

## 7. Reward Dilution via Just-In-Time Staking

### Overview

Staking protocols that distribute rewards proportionally to current stake without time-weighting allow attackers to stake large amounts moments before reward distribution, capture a disproportionate share, then immediately unstake.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/m-02-front-running-rewardvalidators-to-dilute-steal-rewards.md` (Covalent - Sherlock)
> - `reports/eigenlayer_findings/m-03-no-cooldown-in-recoverunstaking-enables-reward-siphoning.md` (Covalent - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`rewardValidators()` distributes rewards proportionally to all current stakes without any time-weighting**, and there is no cooldown on staking/unstaking that would prevent atomic manipulation.

**Frequency:** Common (4/19 reports)
**Validation:** Strong — Multiple independent finders (Sherlock)

### Vulnerable Pattern Examples

**Example 1: Front-Run rewardValidators** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-02-front-running-rewardvalidators-to-dilute-steal-rewards.md`
```solidity
// ❌ VULNERABLE: No time-weighting on reward distribution
function rewardValidators(uint128 validatorId, uint128 amount) external {
    // Rewards distributed proportionally to current shares
    Validator storage v = _validators[validatorId];
    v.exchangeRate += amount * DIVIDER / v.totalShares;
    // New staker with 50% of shares gets 50% of rewards
    // regardless of staking duration
}

// Attack:
// Alice has 50,000 CQT staked with validator
// Bob front-runs rewardValidators() with 50,000 CQT stake
// rewardValidators(1000 CQT) → Bob gets 500 CQT 
// Bob unstakes immediately with 50,500 CQT
```

**Example 2: recoverUnstaking Has No Cooldown** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/m-03-no-cooldown-in-recoverunstaking-enables-reward-siphoning.md`
```solidity
// ❌ VULNERABLE: No cooldown allows instant re-stake after unstake
function recoverUnstaking(uint128 validatorId, uint128 unstakingId) external {
    // No cooldown check — can be called immediately
    Unstaking storage unstaking = _validators[validatorId].unstakings[unstakingId];
    // Transfers unstaked amount back as active stake
    // Attacker: unstake → listen for rewards → recoverUnstaking → capture share → unstake again
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Time-weighted reward distribution
function rewardValidators(uint128 validatorId, uint128 amount) external {
    // Use checkpoint-based shares — new stakes enter "pending" pool
    Validator storage v = _validators[validatorId];
    
    // Only distribute to shares that were active before this block
    uint256 eligibleShares = v.totalShares - v.pendingShares;
    v.exchangeRate += amount * DIVIDER / eligibleShares;
    
    // Move pending shares to active after reward distribution
    v.totalShares = v.totalShares; // Already counted
    v.pendingShares = 0;
}

// ✅ SECURE: Add cooldown to recoverUnstaking
function recoverUnstaking(uint128 validatorId, uint128 unstakingId) external {
    Unstaking storage unstaking = _validators[validatorId].unstakings[unstakingId];
    require(
        block.timestamp >= unstaking.timestamp + RECOVERY_COOLDOWN,
        "Cooldown not elapsed"
    );
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Never make reward claim functions permissionless if they instantly change TVL
2. Use time-weighted reward distribution (checkpoints or pending share pools)
3. Never use `this.functionName()` for internal state modifications 
4. Track external reward claims in `receive()` with source filtering
5. Use checkpoints instead of running sums for reward accounting
6. Clear nested mappings explicitly on unstake (Solidity `delete` doesn't)
7. Add reentrancy guards on all reward claim/transfer functions
8. Auto-claim pending rewards before allowing stake withdrawal
9. Remove hardcoded gas limits for protocol-controlled addresses
10. Implement claim functions for all external reward sources

#### Testing Requirements
- Sandwich test: deposit → claim → withdraw in same transaction
- Reentrancy test: mock token with transfer callback that re-enters claim
- Accounting test: verify reward tracking across multiple reporting cycles with unclaimed rewards
- Time-weighting test: verify new stakers don't capture existing rewards

### Keywords for Search

> These keywords enhance vector search retrieval:

`reward`, `rewards`, `distribution`, `claim`, `claimRewards`, `claimDelayedWithdrawals`, `rewardValidators`, `sandwich`, `front-running`, `MEV`, `time-weighted`, `reward dilution`, `just-in-time staking`, `msg.sender confusion`, `this.stake`, `reStake`, `double counting`, `rewardStakeRatioSum`, `snapshot`, `nested mapping`, `delete struct`, `reentrancy`, `token callback`, `execution layer rewards`, `gas limit`, `self-referral`, `permissionless claim`, `restaking`, `eigenlayer`, `Casimir`, `Rio Network`, `Covalent`, `Ajna`, `Redacted Cartel`

### Related Vulnerabilities

- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)
- [Restaking Slashing Mechanisms](RESTAKING_SLASHING_VULNERABILITIES.md)
