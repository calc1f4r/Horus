---
protocol: generic
chain: cosmos
category: rewards
vulnerability_type: reward_theft_manipulation

attack_type: logical_error|economic_exploit|dos
affected_component: rewards_logic

primitives:
  - flashloan_theft
  - frontrunning
  - orphaned_capture
  - dilution
  - gauge_exploit
  - vault_interaction
  - escrow_assignment
  - commission_error

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - rewards
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Reward Flashloan Theft
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Flashloan `TEL` tokens to stake and exit in the same block c | `reports/cosmos_cometbft_findings/h-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md` | HIGH | Sherlock |
| [M-04] Launched tokens are vulnerable to flashloan attacks f | `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md` | MEDIUM | Code4rena |
| Flashloan `TEL` tokens to stake and exit in the same block c | `reports/cosmos_cometbft_findings/m-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md` | MEDIUM | Sherlock |
| ZivoeYDL::distributeYield yield distribution is flash-loan m | `reports/cosmos_cometbft_findings/m-11-zivoeydldistributeyield-yield-distribution-is-flash-loan-manipulatable.md` | MEDIUM | Sherlock |

### Reward Frontrunning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] User can earn rewards by frontrunning the new rewards | `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md` | MEDIUM | Code4rena |
| Adversary can grief kicker by frontrunning kickAuction call  | `reports/cosmos_cometbft_findings/m-10-adversary-can-grief-kicker-by-frontrunning-kickauction-call-with-a-large-am.md` | MEDIUM | Sherlock |
| [M-11] `ValidatorWithdrawalVault.distributeRewards` can be c | `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md` | MEDIUM | Code4rena |
| [M-12] `ValidatorWithdrawalVault.settleFunds` doesn't check  | `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md` | MEDIUM | Code4rena |
| A part of ETH rewards can be stolen by sandwiching `claimDel | `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md` | MEDIUM | Sherlock |
| TSS Nodes Reporting Slashing Are Vulnerable To Front Running | `reports/cosmos_cometbft_findings/tss-nodes-reporting-slashing-are-vulnerable-to-front-running.md` | MEDIUM | SigmaPrime |
| Users could avoid loss by frontrunning to request unstake | `reports/cosmos_cometbft_findings/users-could-avoid-loss-by-frontrunning-to-request-unstake.md` | MEDIUM | Cyfrin |

### Reward Orphaned Capture
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-02] Orphaned rewards captured by first staker | `reports/cosmos_cometbft_findings/m-02-orphaned-rewards-captured-by-first-staker.md` | MEDIUM | Pashov Audit Group |
| [M-10] Unsafe casting from `uint256` to `uint128` in Rewards | `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md` | MEDIUM | Code4rena |

### Reward Dilution
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| [M-07] Desynchronization of Cabal’s internal accounting with | `reports/cosmos_cometbft_findings/m-07-desynchronization-of-cabals-internal-accounting-with-actual-staked-init-amo.md` | MEDIUM | Code4rena |
| New staking between reward epochs will dilute rewards for ex | `reports/cosmos_cometbft_findings/m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md` | MEDIUM | Sherlock |
| Timestamp boundary condition causes reward dilution for acti | `reports/cosmos_cometbft_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md` | HIGH | Cyfrin |

### Reward Gauge Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Users staking via the `SurplusGuildMinter` can be imm | `reports/cosmos_cometbft_findings/h-04-users-staking-via-the-surplusguildminter-can-be-immediately-slashed-when-st.md` | HIGH | Code4rena |
| Attackers will steal rewards from legitimate pools by making | `reports/cosmos_cometbft_findings/h-2-attackers-will-steal-rewards-from-legitimate-pools-by-making-duplicate-pools.md` | HIGH | Sherlock |
| [M-02] VE3DRewardPool.sol is incompatible with Bal/veBal | `reports/cosmos_cometbft_findings/m-02-ve3drewardpoolsol-is-incompatible-with-balvebal.md` | MEDIUM | Code4rena |
| [M-09] Users can deflate other markets Guild holders rewards | `reports/cosmos_cometbft_findings/m-09-users-can-deflate-other-markets-guild-holders-rewards-by-staking-less-price.md` | MEDIUM | Code4rena |
| [M-13] LendingTerm `debtCeiling` function uses `creditMinter | `reports/cosmos_cometbft_findings/m-13-lendingterm-debtceiling-function-uses-creditminterbuffer-incorrectly.md` | MEDIUM | Code4rena |
| [M-17] Strategy in StakerVault.sol can steal more rewards ev | `reports/cosmos_cometbft_findings/m-17-strategy-in-stakervaultsol-can-steal-more-rewards-even-though-its-designed-.md` | MEDIUM | Code4rena |
| [M-17] The gauge status wasn't checked before reducing the u | `reports/cosmos_cometbft_findings/m-17-the-gauge-status-wasnt-checked-before-reducing-the-users-gauge-weight.md` | MEDIUM | Code4rena |
| [M-19] Over 90% of the Guild staked in a gauge can be unstak | `reports/cosmos_cometbft_findings/m-19-over-90-of-the-guild-staked-in-a-gauge-can-be-unstaked-despite-the-gauge-ut.md` | MEDIUM | Code4rena |

### Reward Vault Interaction
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] Vault creator can prevent users from claiming staking | `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md` | MEDIUM | Code4rena |
| [M-02] A snapshot may face a permanent DoS if both a slashin | `reports/cosmos_cometbft_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md` | MEDIUM | Code4rena |
| [M-04] Processing all withdrawals before all deposits can ca | `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md` | MEDIUM | Code4rena |
| [M-06] `_getRewardsAmountPerVault` might be using an outdate | `reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md` | MEDIUM | Pashov Audit Group |
| [M-11] `ValidatorWithdrawalVault.distributeRewards` can be c | `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md` | MEDIUM | Code4rena |
| [M-12] `ValidatorWithdrawalVault.settleFunds` doesn't check  | `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md` | MEDIUM | Code4rena |
| [M-16] dETH / ETH / LPTokenETH can become depegged due to ET | `reports/cosmos_cometbft_findings/m-16-deth-eth-lptokeneth-can-become-depegged-due-to-eth-20-reward-slashing.md` | MEDIUM | Code4rena |
| [M-17] Strategy in StakerVault.sol can steal more rewards ev | `reports/cosmos_cometbft_findings/m-17-strategy-in-stakervaultsol-can-steal-more-rewards-even-though-its-designed-.md` | MEDIUM | Code4rena |

### Reward Escrow Assignment
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Assignment Of Incorrect Reward Escrow | `reports/cosmos_cometbft_findings/assignment-of-incorrect-reward-escrow.md` | HIGH | OtterSec |
| Front-Running redeem Can Prevent Indexers From Receiving Rew | `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md` | HIGH | OpenZeppelin |
| [H-04] Staking rewards can be drained | `reports/cosmos_cometbft_findings/h-04-staking-rewards-can-be-drained.md` | HIGH | Code4rena |
| [M-01] Vault creator can prevent users from claiming staking | `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md` | MEDIUM | Code4rena |
| [M-27] Faulty Escrow config will lock up reward tokens in St | `reports/cosmos_cometbft_findings/m-27-faulty-escrow-config-will-lock-up-reward-tokens-in-staking-contract.md` | MEDIUM | Code4rena |

### Reward Commission Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-08] Recreated pools receive a wrong AVAX amount due to mi | `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md` | MEDIUM | Code4rena |
| [M-18] Node runners can lose all their stake rewards due to  | `reports/cosmos_cometbft_findings/m-18-node-runners-can-lose-all-their-stake-rewards-due-to-how-the-dao-commission.md` | MEDIUM | Code4rena |
| Stakers lose their commission if they unstake as they cannot | `reports/cosmos_cometbft_findings/m-8-stakers-lose-their-commission-if-they-unstake-as-they-cannot-claim-their-pen.md` | MEDIUM | Sherlock |

---

# Reward Theft Manipulation - Comprehensive Database

**A Complete Pattern-Matching Guide for Reward Theft Manipulation in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Reward Flashloan Theft](#1-reward-flashloan-theft)
2. [Reward Frontrunning](#2-reward-frontrunning)
3. [Reward Orphaned Capture](#3-reward-orphaned-capture)
4. [Reward Dilution](#4-reward-dilution)
5. [Reward Gauge Exploit](#5-reward-gauge-exploit)
6. [Reward Vault Interaction](#6-reward-vault-interaction)
7. [Reward Escrow Assignment](#7-reward-escrow-assignment)
8. [Reward Commission Error](#8-reward-commission-error)

---

## 1. Reward Flashloan Theft

### Overview

Implementation flaw in reward flashloan theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: This bug report is about an issue found in the Telcoin Staking Module. It was found by WATCHPUG and is known as Issue H-1. It is related to a vulnerability in the Checkpoints#getAtBlock() function. This vulnerability allows a malicious user to fake their stake and gain high rewards with minimal mate

### Vulnerability Description

#### Root Cause

Implementation flaw in reward flashloan theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward flashloan theft in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Flashloan `TEL` tokens to stake and exit in the same block can fake a huge amoun** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md`
```
// Vulnerable pattern from Telcoin:
Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/83
```

**Example 2: [M-04] Launched tokens are vulnerable to flashloan attacks forcing premature gra** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
```solidity
//contracts/fun/Bonding.sol
    function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
        Token memory info = tokenInfo[srcTokenAddress];
        require(info.tradingOnUniswap, "Token is not graduated yet");

        FERC20 token = FERC20(srcTokenAddress);
        IERC20 agentToken = IERC20(info.agentToken);
        address pairAddress = factory.getPair(srcTokenAddress, router.assetToken());
        for (uint i = 0; i < accounts.length; i++) {
            address acc = accounts[i];
            uint256 balance = token.balanceOf(acc);
            if (balance > 0) {
                token.burnFrom(acc, balance);
|>              agentToken.transferFrom(pairAddress, acc, balance);//@audit no time restrictions, unwrapToken allows atomic agentToken conversion upon graduation
            }
        }
    }
```

**Example 3: Flashloan `TEL` tokens to stake and exit in the same block can fake a huge amoun** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-flashloan-tel-tokens-to-stake-and-exit-in-the-same-block-can-fake-a-huge-amo.md`
```
// Vulnerable pattern from Telcoin:
Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/83
```

**Example 4: ZivoeYDL::distributeYield yield distribution is flash-loan manipulatable** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-11-zivoeydldistributeyield-yield-distribution-is-flash-loan-manipulatable.md`
```go
// Distribute protocol earnings.
...
            else if (_recipient == IZivoeGlobals_YDL(GBL).stZVE()) {
                uint256 splitBIPS = (
>>                  IERC20(IZivoeGlobals_YDL(GBL).stZVE()).totalSupply() * BIPS
                ) / (
                    IERC20(IZivoeGlobals_YDL(GBL).stZVE()).totalSupply() + 
                    IERC20(IZivoeGlobals_YDL(GBL).vestZVE()).totalSupply()
                );
...
        // Distribute residual earnings.
...
                else if (_recipient == IZivoeGlobals_YDL(GBL).stZVE()) {
                    uint256 splitBIPS = (
>>                      IERC20(IZivoeGlobals_YDL(GBL).stZVE()).totalSupply() * BIPS
                    ) / (
                        IERC20(IZivoeGlobals_YDL(GBL).stZVE()).totalSupply() + 
                        IERC20(IZivoeGlobals_YDL(GBL).vestZVE()).totalSupply()
                    );
...
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward flashloan theft logic allows exploitation through missing validation, 
func secureRewardFlashloanTheft(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Zivoe, Virtuals Protocol, Telcoin
- **Validation Strength**: Moderate (2 auditors)

---

## 2. Reward Frontrunning

### Overview

Implementation flaw in reward frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: MEDIUM: 7.

> **Key Finding**: The report discusses a bug in the LiquidProxy.sol contract, which is part of the Ron staking contract. The bug allows users to earn rewards without actually staking their tokens for a long period of time. This is done by frontrunning the new rewards arrival and immediately withdrawing them. The repo

### Vulnerability Description

#### Root Cause

Implementation flaw in reward frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward frontrunning in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-01] User can earn rewards by frontrunning the new rewards accumulation in Ron** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
```go
User -> delegate -> RonStaking -> Wait atleast a day -> New Rewards
```

**Example 2: Adversary can grief kicker by frontrunning kickAuction call with a large amount ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-adversary-can-grief-kicker-by-frontrunning-kickauction-call-with-a-large-am.md`
```go
Therefore the lower the MOMP, the lower the NP. Lower NP will mean that kicker will be rewarded less and punished more compared to a higher NP. Quoted from the white paper, The MOMP, or “most optimistic matching price,” is the price at which a loan of average size would match with the most favorable lenders on the book. Technically, it is the highest price for which
the amount of deposit above it exceeds the average loan debt of the pool. In `_kick` function, MOMP is calculated as this. Notice how total pool debt is divided by number of loans to find the average loan debt size.
```

**Example 3: [M-11] `ValidatorWithdrawalVault.distributeRewards` can be called to make operat** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`
```
// Vulnerable pattern from Stader Labs:
An attacker can call `distributeRewards` right before `settleFunds` to make `operatorShare < penaltyAmount`. As a result, the validator will face loses.

### Proof of Concept

`ValidatorWithdrawalVault.distributeRewards` can be called by anyone. It's purpose is to distribute validators rewards among the stakers protocol and the operator. After the call, the balance of `ValidatorWithdrawalVault` becomes 0.

`ValidatorWithdrawalVault.settle` is called when a validator is withdrawn from beacon chai
```

**Example 4: A part of ETH rewards can be stolen by sandwiching `claimDelayedWithdrawals()`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-a-part-of-eth-rewards-can-be-stolen-by-sandwiching-claimdelayedwithdrawals.md`
```go
receive() external payable {
    (bool success,) = address(rewardDistributor()).call{value: msg.value}('');
    require(success);
}
```

**Example 5: TSS Nodes Reporting Slashing Are Vulnerable To Front Running** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/tss-nodes-reporting-slashing-are-vulnerable-to-front-running.md`
```
// Vulnerable pattern from Mantle Network:
## Description

Reporting nodes can be front run and miss out on rewards. TSS nodes are responsible for broadcasting off-chain node slashing decisions on-chain; however, it is possible for any other user to read this transaction information while it is in the Ethereum mempool and front-run the report. This will result in the reporting node not receiving the reward they are entitled to for sending the transaction.

This happens because the information needed to report a node slashing does not con
```

**Variant: Reward Frontrunning in Stader Labs** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`
> - `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward frontrunning logic allows exploitation through missing validation, inc
func secureRewardFrontrunning(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 7 audit reports
- **Severity Distribution**: MEDIUM: 7
- **Affected Protocols**: Casimir, Stader Labs, Ajna, Mantle Network, Liquid Ron
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Reward Orphaned Capture

### Overview

Implementation flaw in reward orphaned capture logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The report describes a bug in a contract called `sdeusd.move`. This bug occurs when rewards are distributed while there are no `sdeUSD` holders. The bug allows the first subsequent staker to capture all orphaned rewards at a 1:1 conversion rate, which means they get all the rewards without having to

### Vulnerability Description

#### Root Cause

Implementation flaw in reward orphaned capture logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward orphaned capture in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-02] Orphaned rewards captured by first staker** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-orphaned-rewards-captured-by-first-staker.md`
```go
// transfer_in_rewards() - No check for active stakers
public fun transfer_in_rewards(...) {
    // Missing: assert!(total_supply(management) > 0, ENoActiveStakers);
    update_vesting_amount(management, amount, clock);
}

// convert_to_shares() - 1:1 ratio when no existing stakers
if (total_supply == 0 || total_assets == 0) {
    assets  // First staker gets 1:1 regardless of unvested rewards
}
```

**Example 2: [M-10] Unsafe casting from `uint256` to `uint128` in RewardsManager** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md`
```go
can cause an overflow which, in turn, can lead to unforeseen consequences such as:

*   The inability to calculate new rewards, as `nextExchangeRate > exchangeRate_` will always be true after the overflow.
*   Reduced rewards because `toBucket.lpsAtStakeTime` will be reduced.
*   Reduced rewards because `toBucket.rateAtStakeTime` will be reduced.
*   In case `bucketState.rateAtStakeTime` overflows first but does not go beyond the limits in the new epoch, it will result in increased rewards being accrued.

### Proof of Concept

In `RewardsManager.stake()` and `RewardsManager.moveStakedLiquidity()`, the functions downcast `uint256` to `uint128` without checking whether it is bigger than `uint128` or not.

In `stake()` & `moveStakedLiquidity()` when `getLP >= type(uint128).max`:
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward orphaned capture logic allows exploitation through missing validation,
func secureRewardOrphanedCapture(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Ajna Protocol, Elixir_2025-08-17
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Reward Dilution

### Overview

Implementation flaw in reward dilution logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: The `Staking.unstakeRequest()` function is causing issues with the mETH/ETH rate being fixed and not reflecting any losses or rewards that may occur while waiting for `Staking.claimUnstakeRequest()` to be executed. This can result in unequal distribution of losses and rewards among users who submit 

### Vulnerability Description

#### Root Cause

Implementation flaw in reward dilution logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward dilution in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Fixed exchange rate at unstaking fails to socialize slashing and distorts reward** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeD
```

**Example 2: [M-07] Desynchronization of Cabal’s internal accounting with actual staked INIT ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-07-desynchronization-of-cabals-internal-accounting-with-actual-staked-init-amo.md`
```go
fun compound_xinit_pool_rewards(m_store: &mut ModuleStore, pool_index: u64) {
    let coin_metadata = coin::metadata(@initia_std, string::utf8(b"uinit"));
    let reward_fa = pool_router::withdraw_rewards(coin_metadata);
    let reward_amount = fungible_asset::amount(&reward_fa);

    if (reward_amount > 0) {
        // calculate fee amount
        let fee_ratio = bigdecimal::from_ratio_u64(m_store.xinit_stake_reward_fee_bps, BPS_BASE);
        let fee_amount = bigdecimal::mul_by_u64_truncate(fee_ratio, reward_amount);
        let fee_fa = fungible_asset::extract(&mut reward_fa, fee_amount);
        let rewards_remaining = reward_amount - fee_amount;
        primary_fungible_store::deposit(package::get_commission_fee_store_address(), fee_fa);

        m_store.stake_reward_amounts[pool_index] = m_store.stake_reward_amounts[pool_index] + rewards_remaining;
        pool_router::add_stake(reward_fa);

        // mint xINIT to pool
        m_store.staked_amounts[pool_index] = m_store.staked_amounts[pool_index] + rewards_remaining;
        coin::mint_to(&m_store.x_init_caps.mint_cap, package::get_assets_store_address(), rewards_remaining);
    } else {
        fungible_asset::destroy_zero(reward_fa);
    }
}
```

**Example 3: New staking between reward epochs will dilute rewards for existing stakers. Anyo** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-new-staking-between-reward-epochs-will-dilute-rewards-for-existing-stakers-a.md`
```
// Vulnerable pattern from Covalent:
Source: https://github.com/sherlock-audit/2023-11-covalent-judging/issues/47
```

**Example 4: Timestamp boundary condition causes reward dilution for active operators** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md`
```solidity
function _wasActiveAt(uint48 enabledTime, uint48 disabledTime, uint48 timestamp) private pure returns (bool) {
    return enabledTime != 0 && enabledTime <= timestamp && (disabledTime == 0 || disabledTime >= timestamp); //@audit disabledTime >= timestamp means an operator is active at a timestamp when he was disabled
 }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward dilution logic allows exploitation through missing validation, incorre
func secureRewardDilution(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Mantle Network, Cabal, Covalent, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Reward Gauge Exploit

### Overview

Implementation flaw in reward gauge exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 2, MEDIUM: 7.

> **Key Finding**: Bug report summary:

Users can stake into a gauge directly or indirectly. When a user stakes into a new gauge, their lastGaugeLossApplied mapping is set to the current timestamp. However, if a user stakes into a gauge that has previously experienced a loss, they are immediately considered slashed an

### Vulnerability Description

#### Root Cause

Implementation flaw in reward gauge exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward gauge exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Users staking via the `SurplusGuildMinter` can be immediately slashed whe** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-users-staking-via-the-surplusguildminter-can-be-immediately-slashed-when-st.md`
```go
247:        uint256 _lastGaugeLoss = lastGaugeLoss[gauge];
248:        uint256 _lastGaugeLossApplied = lastGaugeLossApplied[gauge][user];
249:        if (getUserGaugeWeight[user][gauge] == 0) {
250:            lastGaugeLossApplied[gauge][user] = block.timestamp;
251:        } else {
252:            require(
253:                _lastGaugeLossApplied >= _lastGaugeLoss,
254:                "GuildToken: pending loss"
255:            );
256:        }
```

**Example 2: Attackers will steal rewards from legitimate pools by making duplicate pools for** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-attackers-will-steal-rewards-from-legitimate-pools-by-making-duplicate-pools.md`
```
// Vulnerable pattern from Super DCA Liquidity Network:
Source: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/662
```

**Example 3: [M-02] VE3DRewardPool.sol is incompatible with Bal/veBal** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-ve3drewardpoolsol-is-incompatible-with-balvebal.md`
```
// Vulnerable pattern from veToken Finance:
_Submitted by 0x52_

`getReward` will become completely unusable if bal is added as an support asset.

### Proof of Concept

veBal is not staked bal, it is staked 80-20 bal/eth LP. Rewards from gauges are paid in bal NOT 80-20 bal/eth LP. All rewards to this address will be received as bal. If the contract tries to deposit bal directly it will fail, causing getReward to always revert if bal is a supported asset (as all documentation conveys that it will be).

### Recommended Mitigation Steps

Ex
```

**Example 4: [M-17] Strategy in StakerVault.sol can steal more rewards even though it's desig** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-17-strategy-in-stakervaultsol-can-steal-more-rewards-even-though-its-designed-.md`
```
// Vulnerable pattern from Backd:
_Submitted by hansfriese_

<https://github.com/code-423n4/2022-05-backd/tree/main/protocol/contracts/StakerVault.sol#L95>

<https://github.com/code-423n4/2022-05-backd/tree/main/protocol/contracts/tokenomics/LpGauge.sol#L52-L63>

### Impact

Strategy in StakerVault.sol can steal more rewards even though it's designed strategies shouldn't get rewards.

Also there will be a problem with a rewarding system in LpGauge.sol so that some normal users wouldn't get rewards properly.

### Proof of Concept
```

**Example 5: [M-26] If `HERMES` gauge rewards are not queued for distribution every week, the** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-26-if-hermes-gauge-rewards-are-not-queued-for-distribution-every-week-they-are.md`
```
// Vulnerable pattern from Maia DAO Ecosystem:
In order to queue weekly `HERMES` rewards for distribution, `FlywheelGaugeRewards::queueRewardsForCycle` must be called during the next cycle (week). If a cycle has passed and no one calls `queueRewardsForCycle` to queue rewards, cycle gauge rewards are lost as the internal accounting does not take into consideration time passing, only the last processed cycle.

### Issue details

The minter kicks off a new epoch via calling `BaseV2Minter::updatePeriod`. The execution flow goes to `FlywheelGauge
```

**Variant: Reward Gauge Exploit - MEDIUM Severity Cases** [MEDIUM]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/m-02-ve3drewardpoolsol-is-incompatible-with-balvebal.md`
> - `reports/cosmos_cometbft_findings/m-09-users-can-deflate-other-markets-guild-holders-rewards-by-staking-less-price.md`
> - `reports/cosmos_cometbft_findings/m-13-lendingterm-debtceiling-function-uses-creditminterbuffer-incorrectly.md`

**Variant: Reward Gauge Exploit in Ethereum Credit Guild** [HIGH]
> Protocol-specific variant found in 5 reports:
> - `reports/cosmos_cometbft_findings/h-04-users-staking-via-the-surplusguildminter-can-be-immediately-slashed-when-st.md`
> - `reports/cosmos_cometbft_findings/m-09-users-can-deflate-other-markets-guild-holders-rewards-by-staking-less-price.md`
> - `reports/cosmos_cometbft_findings/m-13-lendingterm-debtceiling-function-uses-creditminterbuffer-incorrectly.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward gauge exploit logic allows exploitation through missing validation, in
func secureRewardGaugeExploit(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 9 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 7
- **Affected Protocols**: Maia DAO Ecosystem, veToken Finance, Super DCA Liquidity Network, Ethereum Credit Guild, Backd
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Reward Vault Interaction

### Overview

Implementation flaw in reward vault interaction logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 19 audit reports with severity distribution: HIGH: 5, MEDIUM: 14.

> **Key Finding**: This bug report describes a vulnerability in the MultiRewardStaking smart contract, which can be exploited by a vault creator to prevent users from claiming rewards from the staking contract. The vault creator can present a high APY and low fee percentage to draw in stakers, and when the staking con

### Vulnerability Description

#### Root Cause

Implementation flaw in reward vault interaction logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward vault interaction in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-01] Vault creator can prevent users from claiming staking rewards** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md`
```solidity
// SPDX-License-Identifier: GPL-3.0
// Docgen-SOLC: 0.8.15

pragma solidity ^0.8.15;

import { Test } from "forge-std/Test.sol";
import { MockERC20 } from "./utils/mocks/MockERC20.sol";
import { IMultiRewardEscrow } from "../src/interfaces/IMultiRewardEscrow.sol";
import { MultiRewardStaking, IERC20 } from "../src/utils/MultiRewardStaking.sol";
import { MultiRewardEscrow } from "../src/utils/MultiRewardEscrow.sol";

contract NoRewards is Test {
  MockERC20 stakingToken;
  MockERC20 rewardToken1;
  MockERC20 rewardToken2;
  IERC20 iRewardToken1;
  IERC20 iRewardToken2;
  MultiRewardStaking staking;
  MultiRewardEscrow escrow;

  address alice = address(0xABCD);
  address bob = address(0xDCBA);

  ///////////// ZERO ADDRESS //////////
  address feeRecipient = address(0x0);
  

  function setUp() public {
    vm.label(alice, "alice");
    vm.label(bob, "bob");

    stakingToken = new MockERC20("Staking Token", "STKN", 18);

    rewardToken1 = new MockERC20("RewardsToken1", "RTKN1", 18);
    rewardToken2 = new MockERC20("RewardsToken2", "RTKN2", 18);
// ... (truncated)
```

**Example 2: [M-02] A snapshot may face a permanent DoS if both a slashing event occurs in th** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md`
```solidity
function validateSnapshotProofs(
            address nodeOwner,
            BeaconProofs.BalanceProof[] calldata balanceProofs,
            BeaconProofs.BalanceContainer calldata balanceContainer
        )
            external
            nonReentrant
            nodeExists(nodeOwner)
            whenFunctionNotPaused(Constants.PAUSE_NATIVEVAULT_VALIDATE_SNAPSHOT)
        {
            NativeVaultLib.Storage storage self = _state();
            NativeVaultLib.NativeNode storage node = self.ownerToNode[nodeOwner];
            NativeVaultLib.Snapshot memory snapshot = node.currentSnapshot;

            if (node.currentSnapshotTimestamp == 0) revert NoActiveSnapshot();

            BeaconProofs.validateBalanceContainer(snapshot.parentBeaconBlockRoot, balanceContainer);

            for (uint256 i = 0; i < balanceProofs.length; i++) {
                NativeVaultLib.ValidatorDetails memory validatorDetails =
                    node.validatorPubkeyHashToDetails[balanceProofs[i].pubkeyHash];

                if (validatorDetails.status != NativeVaultLib.ValidatorStatus.ACTIVE) revert InactiveValidator();
                if (validatorDetails.lastBalanceUpdateTimestamp >= node.currentSnapshotTimestamp) {
                    revert ValidatorAlreadyProved();
                }

    153         int256 balanceDeltaWei = self.validateSnapshotProof(
                    nodeOwner, validatorDetails, balanceContainer.containerRoot, balanceProofs[i]
                );

                snapshot.remainingProofs--;
    158         snapshot.balanceDeltaWei += balanceDeltaWei;
            }

    161     _updateSnapshot(node, snapshot, nodeOwner);
        }
```

**Example 3: [M-04] Processing all withdrawals before all deposits can cause some deposit to ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md`
```go
> 1. Alice stake 10 HYPE (and receive 10 kHYPE)
> 2. Bob stake 1 HYPE (and receive 1 kHYPE)
> 3. Carol stake 1 HYPE (and receive 1 kHYPE)
> 4. Alice queue withdrawal for 10 kHYPE (which result in 9 HYPE to be withdrawn after fees)
> 5. Bob queue withdrawal for 1 kHYPE (which result in 0.9 HYPE to be withdrawn)
>
> L1 Operation logics:
> 1. Alice's withdrawal is processed first: undelegation fails (as nothing has been delegated yet), withdrawal 9 HYPE from "staking" to "spot" succeed (reduce the staking balance available to delegate)
> 2. Bob's withdrawal is processed second: undelegation fails (same reason), withdrawal of 0.9 HYPE from "staking" to "spot" succeed, now equal to 9.9 HYPE being unstaked.
> 3. Alice's deposit is processed, which tries to delegate 9 HYPE, but as they are already in the withdrawal process, this fails as there isn't enough "staking" balance to delegate.
> 4. Bob's deposit is processed for 1 HYPE and successfully pass, making the delegated balance equal to 1 HYPE.
> 5. Carol's deposit is processed for 1 HYPE and successfully pass, making the delegated balance equal to 2 HYPE.
>
> So, at the end of the whole process we will have this state:
>
> L1 Spot: 0 HYPE (still in unstaking queue for 7 days)
> L1 "Unstaking Queue": 9.9 HYPE
> L1 Staking: 0.1 HYPE
> L1 Delegated: 2 HYPE
>
```

**Example 4: [M-06] `_getRewardsAmountPerVault` might be using an outdated vault power** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md`
```go
// https://github.com/symbioticfi/core/blob/main/src/contracts/vault/Vault.sol#L237
            if (slashedAmount > 0) {
                uint256 activeSlashed = slashedAmount.mulDiv(activeStake_, slashableStake);
                uint256 nextWithdrawalsSlashed = slashedAmount - activeSlashed;

                _activeStake.push(Time.timestamp(), activeStake_ - activeSlashed);
                withdrawals[captureEpoch + 1] = nextWithdrawals - nextWithdrawalsSlashed;
            }
```

**Example 5: [M-11] `ValidatorWithdrawalVault.distributeRewards` can be called to make operat** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`
```
// Vulnerable pattern from Stader Labs:
An attacker can call `distributeRewards` right before `settleFunds` to make `operatorShare < penaltyAmount`. As a result, the validator will face loses.

### Proof of Concept

`ValidatorWithdrawalVault.distributeRewards` can be called by anyone. It's purpose is to distribute validators rewards among the stakers protocol and the operator. After the call, the balance of `ValidatorWithdrawalVault` becomes 0.

`ValidatorWithdrawalVault.settle` is called when a validator is withdrawn from beacon chai
```

**Variant: Reward Vault Interaction - HIGH Severity Cases** [HIGH]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/missing-_grantrole-for-keeper_role-will-prevent-calling-of-critical-keeper-funct.md`
> - `reports/cosmos_cometbft_findings/penalty-system-delays-the-rewards-instead-of-reducing-them.md`
> - `reports/cosmos_cometbft_findings/the-exponential-decay-logic-slashes-stakers-principal-amount.md`

**Variant: Reward Vault Interaction in Popcorn** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md`
> - `reports/cosmos_cometbft_findings/m-27-faulty-escrow-config-will-lock-up-reward-tokens-in-staking-contract.md`

**Variant: Reward Vault Interaction in Stader Labs** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md`
> - `reports/cosmos_cometbft_findings/m-12-validatorwithdrawalvaultsettlefunds-doesnt-check-amount-that-user-has-insid.md`

**Variant: Reward Vault Interaction in Stakehouse Protocol** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-16-deth-eth-lptokeneth-can-become-depegged-due-to-eth-20-reward-slashing.md`
> - `reports/cosmos_cometbft_findings/m-21-eip1559-rewards-received-by-syndicate-during-the-period-when-it-has-no-regi.md`
> - `reports/cosmos_cometbft_findings/m-28-funds-are-not-claimed-from-syndicate-for-valid-bls-keys-of-first-key-is-inv.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward vault interaction logic allows exploitation through missing validation
func secureRewardVaultInteraction(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 19 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 14
- **Affected Protocols**: Lido, Stakehouse Protocol, Olympusdao, Part 2, Popcorn
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Reward Escrow Assignment

### Overview

Implementation flaw in reward escrow assignment logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: The vulnerability in the maybe_execute_stake_rewards function in OracleHeartbeat arises from incorrect utilization of the remaining_accounts.oracle_switch_reward_escrow account for distributing rewards. This results in the oracle's WSOL reward escrow failing to set up properly and no funds being tra

### Vulnerability Description

#### Root Cause

Implementation flaw in reward escrow assignment logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward escrow assignment in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: Assignment Of Incorrect Reward Escrow** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/assignment-of-incorrect-reward-escrow.md`
```rust
pub fn maybe_execute_stake_rewards(
    [...]
) -> Result<()> {
    [...]
    if let Some(oracle_wsol_reward_escrow) = &remaining_accounts.oracle_switch_reward_escrow {
        let res = NativeEscrow::spl_transfer(
            &ctx.accounts.token_program,
            &ctx.accounts.queue_escrow.to_account_info(),
            &oracle_wsol_reward_escrow.to_account_info(),
            &ctx.accounts.program_state.to_account_info(),
            &[&[STATE_SEED, &[state.bump]]],
            std::cmp::min(
                reward.saturating_sub(slash),
                oracle_wsol_reward_escrow.amount,
            ),
        );
        [...]
    }
}
```

**Example 2: Front-Running redeem Can Prevent Indexers From Receiving Rewards for Allocations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md`
```
// Vulnerable pattern from The Graph Timeline Aggregation Audit:
The [`redeem`](https://github.com/semiotic-ai/timeline-aggregation-protocol-contracts/blob/d8795c747d44da90f7717b3db9a08698e64a9b2f/src/Escrow.sol#L366) function in `Escrow.sol` enables Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone who knows the contents of a valid `signedRAV` and `allocationIDProof` can call `redeem` regardless of whether the proof and signed RAV belong to them. This is because `redeem` only che
```

**Example 3: [H-04] Staking rewards can be drained** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-staking-rewards-can-be-drained.md`
```
// Vulnerable pattern from Popcorn:
If ERC777 tokens are used for rewards, the entire balance of rewards in the staking contract can get drained by an attacker.

### Proof of Concept

ERC777 allow users to register a hook to notify them when tokens are transferred to them.

This hook can be used to reenter the contract and drain the rewards.

The issue is in the `claimRewards` in `MultiRewardStaking`.
The function does not follow the checks-effects-interactions pattern and therefore can be reentered when transferring tokens in the
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward escrow assignment logic allows exploitation through missing validation
func secureRewardEscrowAssignment(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 2
- **Affected Protocols**: The Graph Timeline Aggregation Audit, Switchboard On-chain, Popcorn
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Reward Commission Error

### Overview

Implementation flaw in reward commission error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: MEDIUM: 3.

> **Key Finding**: This bug report is related to the Gogopool protocol, which is a staking platform for Avalanche tokens (AVAX). The bug is related to the `MinipoolManager.sol` contract and the `recreateMinipool` function. This function is used to recreate minipools after a successful validation period. The bug is tha

### Vulnerability Description

#### Root Cause

Implementation flaw in reward commission error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reward commission error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reward operations

### Vulnerable Pattern Examples

**Example 1: [M-08] Recreated pools receive a wrong AVAX amount due to miscalculated compound** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-recreated-pools-receive-a-wrong-avax-amount-due-to-miscalculated-compounded.md`
```go
Minipool memory mp = getMinipool(minipoolIndex);
// Compound the avax plus rewards
// NOTE Assumes a 1:1 nodeOp:liqStaker funds ratio
uint256 compoundedAvaxNodeOpAmt = mp.avaxNodeOpAmt + mp.avaxNodeOpRewardAmt;
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxNodeOpAmt")), compoundedAvaxNodeOpAmt);
setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".avaxLiquidStakerAmt")), compoundedAvaxNodeOpAmt);
```

**Example 2: [M-18] Node runners can lose all their stake rewards due to how the DAO commissi** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-18-node-runners-can-lose-all-their-stake-rewards-due-to-how-the-dao-commission.md`
```solidity
function _updateDAORevenueCommission(uint256 _commissionPercentage) internal {
        require(_commissionPercentage <= MODULO, "Invalid commission");

        emit DAOCommissionUpdated(daoCommissionPercentage, _commissionPercentage);

        daoCommissionPercentage = _commissionPercentage;
    }
```

**Example 3: Stakers lose their commission if they unstake as they cannot claim their pending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-stakers-lose-their-commission-if-they-unstake-as-they-cannot-claim-their-pen.md`
```
// Vulnerable pattern from MorphL2:
Source: https://github.com/sherlock-audit/2024-08-morphl2-judging/issues/168
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reward commission error logic allows exploitation through missing validation,
func secureRewardCommissionError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: MEDIUM: 3
- **Affected Protocols**: GoGoPool, MorphL2, Stakehouse Protocol
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Reward Flashloan Theft
grep -rn 'reward|flashloan|theft' --include='*.go' --include='*.sol'
# Reward Frontrunning
grep -rn 'reward|frontrunning' --include='*.go' --include='*.sol'
# Reward Orphaned Capture
grep -rn 'reward|orphaned|capture' --include='*.go' --include='*.sol'
# Reward Dilution
grep -rn 'reward|dilution' --include='*.go' --include='*.sol'
# Reward Gauge Exploit
grep -rn 'reward|gauge|exploit' --include='*.go' --include='*.sol'
# Reward Vault Interaction
grep -rn 'reward|vault|interaction' --include='*.go' --include='*.sol'
# Reward Escrow Assignment
grep -rn 'reward|escrow|assignment' --include='*.go' --include='*.sol'
# Reward Commission Error
grep -rn 'reward|commission|error' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `accumulation`, `actual`, `actually`, `adversary`, `after`, `allocations`, `allowing`, `amount`, `amounts`, `anymore`, `anyone`, `appchain`, `assignment`, `attackers`, `attacks`, `avax`, `before`, `between`, `block`, `both`, `call`, `called`, `cannot`, `capture`, `captured`, `casting`, `cause`, `claim`, `claiming`
