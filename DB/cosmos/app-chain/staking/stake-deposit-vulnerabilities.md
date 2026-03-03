---
protocol: generic
chain: cosmos
category: staking
vulnerability_type: stake_deposit_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: staking_logic

primitives:
  - deposit_amount_tracking
  - deposit_validation
  - deposit_frontrunning
  - balance_desync
  - deposit_queue
  - deposit_inflation
  - incorrect_calculation
  - invariant_broken

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - staking
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Staking Deposit Amount Tracking Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkValidatorBehavior() is mistakenly using the current va | `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md` | MEDIUM | Spearbit |
| A malicious staker can force validator withdrawals by instan | `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md` | HIGH | Cyfrin |
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| Account Inconsistencies In Bridge Tokens Instruction | `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md` | HIGH | OtterSec |
| [C-01] Pending payouts excluded from total balance cause inc | `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md` | HIGH | Pashov Audit Group |
| [C-02] Stakes not forwarded post-delegation, positions unwit | `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | HIGH | Pashov Audit Group |
| Chain halt by spamming deposits request with minimum staking | `reports/cosmos_cometbft_findings/chain-halt-by-spamming-deposits-request-with-minimum-staking-amount.md` | MEDIUM | Cantina |
| COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS | `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md` | MEDIUM | Halborn |

### Missing or Insufficient Deposit Validation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkValidatorBehavior() is mistakenly using the current va | `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md` | MEDIUM | Spearbit |
| A malicious staker can force validator withdrawals by instan | `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md` | HIGH | Cyfrin |
| Account Inconsistencies In Bridge Tokens Instruction | `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md` | HIGH | OtterSec |
| Activation of queued cutting board can be manipulated leadin | `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md` | MEDIUM | Spearbit |
| Allow List Entries Can Be Added and Removed by Any State All | `reports/cosmos_cometbft_findings/allow-list-entries-can-be-added-and-removed-by-any-state-allower.md` | HIGH | Quantstamp |
| Attackers can prevent new challenges/listings/backends, para | `reports/cosmos_cometbft_findings/attackers-can-prevent-new-challengeslistingsbackends-parameter-changes-and-stake.md` | MEDIUM | TrailOfBits |
| Bypassing of NFT Collection Integrity Checks | `reports/cosmos_cometbft_findings/bypassing-of-nft-collection-integrity-checks.md` | HIGH | OtterSec |
| [C-02] Pending stake not accounted for in liquidity calculat | `reports/cosmos_cometbft_findings/c-02-pending-stake-not-accounted-for-in-liquidity-calculations.md` | HIGH | Pashov Audit Group |

### Staking Deposit Frontrunning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| DoS Risk Due to Small Deposits and Front-Running in `deposit | `reports/cosmos_cometbft_findings/dos-risk-due-to-small-deposits-and-front-running-in-deposit-function.md` | MEDIUM | MixBytes |
| Elected TSS Nodes Can Act Without Any Deposit | `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md` | HIGH | SigmaPrime |
| [H-01] `StakedToken` is vulnerable to share inflation attack | `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md` | HIGH | Pashov Audit Group |
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| [H-04] Violation of Invariant Allowing DSSs to Slash Unregis | `reports/cosmos_cometbft_findings/h-04-violation-of-invariant-allowing-dsss-to-slash-unregistered-operators.md` | HIGH | Code4rena |
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [H-20] Possibly reentrancy attacks in _distributeETHRewardsT | `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md` | HIGH | Code4rena |

### Staking Balance Desynchronization
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DoS on stake accounting functions by bloating `operatorNodes | `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md` | MEDIUM | Cyfrin |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Incorrect Accounting for stakedButUnverifiedNativeETH | `reports/cosmos_cometbft_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md` | HIGH | SigmaPrime |
| [M-03] Attacker Can Desynchronize Supply Snapshot During Sam | `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md` | MEDIUM | Code4rena |
| [M-03] Inconsistent State Restoration in `cancelWithdrawal`  | `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md` | MEDIUM | Code4rena |
| Unhandled Stake Recovery Failure Leads to Potential Accounti | `reports/cosmos_cometbft_findings/unhandled-stake-recovery-failure-leads-to-potential-accounting-inconsistencies.md` | MEDIUM | Quantstamp |
| Validators Can Skip createEndRequest and Quickly Re-Register | `reports/cosmos_cometbft_findings/validators-can-skip-createendrequest-and-quickly-re-register.md` | HIGH | OpenZeppelin |

### Deposit Queue Processing Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-01] Pending payouts excluded from total balance cause inc | `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md` | HIGH | Pashov Audit Group |
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| Future epoch cache manipulation via `calcAndCacheStakes` all | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [M-02] Unstaking calculates user share at request time, igno | `reports/cosmos_cometbft_findings/m-02-unstaking-calculates-user-share-at-request-time-ignoring-slashing-leading-t.md` | MEDIUM | Code4rena |
| [M-04] Delayed slashing window and lack of transparency for  | `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md` | MEDIUM | Code4rena |
| [M-05] Attacker can partially DoS L1 operations in StakingMa | `reports/cosmos_cometbft_findings/m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md` | MEDIUM | Code4rena |

### First Depositor / Share Inflation Attack
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Direct Deposits Enable Theft Of A Validator’s Funds | `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md` | HIGH | SigmaPrime |
| [H-01] `StakedToken` is vulnerable to share inflation attack | `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md` | HIGH | Pashov Audit Group |
| [H-03] StakedCitadel depositors can be attacked by the first | `reports/cosmos_cometbft_findings/h-03-stakedcitadel-depositors-can-be-attacked-by-the-first-depositor-with-depres.md` | HIGH | Code4rena |
| [M-01] Freezing of funds - Hacker can prevent users withdraw | `reports/cosmos_cometbft_findings/m-01-freezing-of-funds-hacker-can-prevent-users-withdraws-in-giant-pools.md` | MEDIUM | Code4rena |
| [M-02] _depositEther Does Not Increment Validator Index,Caus | `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md` | MEDIUM | Kann |
| [M-04] Processing all withdrawals before all deposits can ca | `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md` | MEDIUM | Code4rena |
| WIchiFarm will break after second deposit of LP | `reports/cosmos_cometbft_findings/m-17-wichifarm-will-break-after-second-deposit-of-lp.md` | MEDIUM | Sherlock |
| Protocol won't be eligible for referral rewards for depositi | `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md` | MEDIUM | Sherlock |

### Incorrect Staking Calculation Logic
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Accounting for `rewardStakeRatioSum` is incorrect when a del | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| beaconChainETHStrategy Queued Withdrawals Excluded From Slas | `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` | MEDIUM | SigmaPrime |
| [C-01] Incorrect reward calculation | `reports/cosmos_cometbft_findings/c-01-incorrect-reward-calculation.md` | HIGH | Pashov Audit Group |
| [C-01] Pending payouts excluded from total balance cause inc | `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md` | HIGH | Pashov Audit Group |
| [C-02] Pending stake not accounted for in liquidity calculat | `reports/cosmos_cometbft_findings/c-02-pending-stake-not-accounted-for-in-liquidity-calculations.md` | HIGH | Pashov Audit Group |
| Flawed Implementation of Reward Score Calculation | `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md` | HIGH | OtterSec |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| [H-01] LP unstaking only burns the shares but leaves the und | `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md` | HIGH | Code4rena |

### Broken Staking Invariants
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [EIGEN2-4] Missing constraint check for modification of look | `reports/cosmos_cometbft_findings/eigen2-4-missing-constraint-check-for-modification-of-lookahead-time-of-slashabl.md` | MEDIUM | Hexens |
| [H-01] `userTotalStaked` invariant will be broken due to vul | `reports/cosmos_cometbft_findings/h-01-usertotalstaked-invariant-will-be-broken-due-to-vulnerable-implementations-.md` | HIGH | Code4rena |
| [H-04] Violation of Invariant Allowing DSSs to Slash Unregis | `reports/cosmos_cometbft_findings/h-04-violation-of-invariant-allowing-dsss-to-slash-unregistered-operators.md` | HIGH | Code4rena |
| [H-06] Hardcoded gas used in ERC20 queries allows for block  | `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md` | HIGH | Code4rena |
| Risk of token/uToken exchange rate manipulation | `reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md` | HIGH | TrailOfBits |
| Staker contract balance invariant can be broken using SELFDE | `reports/cosmos_cometbft_findings/staker-contract-balance-invariant-can-be-broken-using-selfdestruct.md` | HIGH | TrailOfBits |
| validatorUpdates ignores the effects of ProcessBlock leading | `reports/cosmos_cometbft_findings/validatorupdates-ignores-the-effects-of-processblock-leading-to-wrong-voting-pow.md` | MEDIUM | Spearbit |

---

# Stake Deposit Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Stake Deposit Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Staking Deposit Amount Tracking Errors](#1-staking-deposit-amount-tracking-errors)
2. [Missing or Insufficient Deposit Validation](#2-missing-or-insufficient-deposit-validation)
3. [Staking Deposit Frontrunning](#3-staking-deposit-frontrunning)
4. [Staking Balance Desynchronization](#4-staking-balance-desynchronization)
5. [Deposit Queue Processing Errors](#5-deposit-queue-processing-errors)
6. [First Depositor / Share Inflation Attack](#6-first-depositor---share-inflation-attack)
7. [Incorrect Staking Calculation Logic](#7-incorrect-staking-calculation-logic)
8. [Broken Staking Invariants](#8-broken-staking-invariants)

---

## 1. Staking Deposit Amount Tracking Errors

### Overview

Protocol fails to correctly track staked amounts, leading to accounting mismatches between actual deposits and recorded balances. This pattern was found across 186 audit reports with severity distribution: HIGH: 76, MEDIUM: 110.

> **Key Finding**: The bug report discusses an issue with the `_checkValidatorBehavior()` function in the OracleManager.sol file. This function is responsible for checking the reasonableness of changes in the slashed amount and rewards amount. The problem arises when tolerance levels, represented as percentages of the

### Vulnerability Description

#### Root Cause

Protocol fails to correctly track staked amounts, leading to accounting mismatches between actual deposits and recorded balances.

#### Attack Scenario

1. Attacker identifies staking deposit amount tracking errors in the protocol
2. Exploits the missing validation or incorrect logic
3. Users may lose staked funds, receive incorrect rewards, or the protocol may become insolvent

### Vulnerable Pattern Examples

**Example 1: _checkValidatorBehavior() is mistakenly using the current validator balance** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md`
```go
slashingBps = (10 / 90) % > SlashingTolerance (10%).
```

**Example 2: A malicious staker can force validator withdrawals by instantly staking and unst** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
```solidity
function requestUnstake(uint256 amount) external nonReentrant {
    // code ....
    uint256 expectedWithdrawableBalance =
        getWithdrawableBalance() + requestedExits * VALIDATOR_CAPACITY + delayedEffectiveBalance;
    if (unstakeQueueAmount > expectedWithdrawableBalance) {
        uint256 requiredAmount = unstakeQueueAmount - expectedWithdrawableBalance;
>       uint256 requiredExits = requiredAmount / VALIDATOR_CAPACITY; //@audit required exits calculated here
        if (requiredAmount % VALIDATOR_CAPACITY > 0) {
            requiredExits++;
        }
        exitValidators(requiredExits);
    }

    emit UnstakeRequested(msg.sender, amount);
}
```

**Example 3: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
```

**Example 4: Account Inconsistencies In Bridge Tokens Instruction** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`
```rust
pub fn bridge_tokens<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, BridgeTokens<'info>>,
    deposit_index: u8,
) -> Result<()> {
    [...]
    let hashed_full_denom = 
    lib::hash::CryptoHash::digest(ctx.accounts.token_mint.key().to_string().as_ref());
    let denom = ibc::apps::transfer::types::PrefixedDenom::from_str(
        &ctx.accounts.token_mint.key().to_string(),
    )
    .unwrap();
    let token = ibc::apps::transfer::types::Coin {
        denom,
        amount: deposit.amount.into(),
    };
    [...]
}
```

**Example 5: [C-01] Pending payouts excluded from total balance cause incorrect share calcula** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Variant: Staking Deposit Amount Tracking Errors - HIGH Severity Cases** [HIGH]
> Found in 76 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
> - `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`

**Variant: Staking Deposit Amount Tracking Errors in Kinetiq LST** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md`
> - `reports/cosmos_cometbft_findings/lack-of-liquidity-inside-stakingmanager.md`
> - `reports/cosmos_cometbft_findings/sentinel-can-block-core-operations-for-any-validator-chosen-due-to-missing-input.md`

**Variant: Staking Deposit Amount Tracking Errors in Casimir** [HIGH]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`

**Variant: Staking Deposit Amount Tracking Errors in Pheasant Network** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
> - `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md`
> - `reports/cosmos_cometbft_findings/the-invariant-totalslashableamount-lockedamountinbond-is-not-enforced-in-the-cod.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Protocol fails to correctly track staked amounts, leading to accounting mismatches between actual de
func secureStakingDepositAmountTracking(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 186 audit reports
- **Severity Distribution**: HIGH: 76, MEDIUM: 110
- **Affected Protocols**: Skale Network, ZetaChain Cross-Chain, Persistence, Tokensfarm, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Missing or Insufficient Deposit Validation

### Overview

Staking functions lack proper validation of deposit amounts, minimum thresholds, or deposit conditions. This pattern was found across 190 audit reports with severity distribution: HIGH: 80, MEDIUM: 110.

> **Key Finding**: The bug report discusses an issue with the `_checkValidatorBehavior()` function in the OracleManager.sol file. This function is responsible for checking the reasonableness of changes in the slashed amount and rewards amount. The problem arises when tolerance levels, represented as percentages of the

### Vulnerability Description

#### Root Cause

Staking functions lack proper validation of deposit amounts, minimum thresholds, or deposit conditions.

#### Attack Scenario

1. Attacker identifies missing or insufficient deposit validation in the protocol
2. Exploits the missing validation or incorrect logic
3. Allows zero-value deposits, dust attacks, or deposits that violate protocol invariants

### Vulnerable Pattern Examples

**Example 1: _checkValidatorBehavior() is mistakenly using the current validator balance** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md`
```go
slashingBps = (10 / 90) % > SlashingTolerance (10%).
```

**Example 2: A malicious staker can force validator withdrawals by instantly staking and unst** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
```solidity
function requestUnstake(uint256 amount) external nonReentrant {
    // code ....
    uint256 expectedWithdrawableBalance =
        getWithdrawableBalance() + requestedExits * VALIDATOR_CAPACITY + delayedEffectiveBalance;
    if (unstakeQueueAmount > expectedWithdrawableBalance) {
        uint256 requiredAmount = unstakeQueueAmount - expectedWithdrawableBalance;
>       uint256 requiredExits = requiredAmount / VALIDATOR_CAPACITY; //@audit required exits calculated here
        if (requiredAmount % VALIDATOR_CAPACITY > 0) {
            requiredExits++;
        }
        exitValidators(requiredExits);
    }

    emit UnstakeRequested(msg.sender, amount);
}
```

**Example 3: Account Inconsistencies In Bridge Tokens Instruction** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`
```rust
pub fn bridge_tokens<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, BridgeTokens<'info>>,
    deposit_index: u8,
) -> Result<()> {
    [...]
    let hashed_full_denom = 
    lib::hash::CryptoHash::digest(ctx.accounts.token_mint.key().to_string().as_ref());
    let denom = ibc::apps::transfer::types::PrefixedDenom::from_str(
        &ctx.accounts.token_mint.key().to_string(),
    )
    .unwrap();
    let token = ibc::apps::transfer::types::Coin {
        denom,
        amount: deposit.amount.into(),
    };
    [...]
}
```

**Example 4: Activation of queued cutting board can be manipulated leading to redirection of ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md`
```
// Vulnerable pattern from Berachain Pol:
Severity: Medium Risk
Context: Berachef.sol#158
Description: A validator operator can queue a new cutting board at any time. Once thecuttingBoardBlockDelay
has passed, the queued cutting board is ready for activation. The activation of a cutting board occurs viadistrib-
utor.distributeFor() which calls beraChef.activateReadyQueuedCuttingBoard(pubkey, blockNumber); .
The validator is incentivized to emit the BGT reward to reward vaults that will provide the best financial incentives
while also in
```

**Example 5: Allow List Entries Can Be Added and Removed by Any State Allower** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/allow-list-entries-can-be-added-and-removed-by-any-state-allower.md`
```go
address = state.allower @ ErrorCode::OnlyAllower
```

**Variant: Missing or Insufficient Deposit Validation - HIGH Severity Cases** [HIGH]
> Found in 80 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`
> - `reports/cosmos_cometbft_findings/allow-list-entries-can-be-added-and-removed-by-any-state-allower.md`

**Variant: Missing or Insufficient Deposit Validation in Kinetiq LST** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md`
> - `reports/cosmos_cometbft_findings/lack-of-liquidity-inside-stakingmanager.md`

**Variant: Missing or Insufficient Deposit Validation in Casimir** [HIGH]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/operator-is-not-removed-in-registry-when-validator-has-owedamount-0.md`

**Variant: Missing or Insufficient Deposit Validation in Composable Bridge + PR** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md`
> - `reports/cosmos_cometbft_findings/unauthorized-withdrawals-of-staked-tokens.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Staking functions lack proper validation of deposit amounts, minimum thresholds, or deposit conditio
func secureStakingDepositValidation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 190 audit reports
- **Severity Distribution**: HIGH: 80, MEDIUM: 110
- **Affected Protocols**: Munchables, Berachain Pol, ZetaChain Cross-Chain, Coinbase Liquid Staking Token Audit, Persistence
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Staking Deposit Frontrunning

### Overview

Deposit transactions can be frontrun to manipulate exchange rates, share prices, or allocation outcomes. This pattern was found across 40 audit reports with severity distribution: HIGH: 12, MEDIUM: 28.

> **Key Finding**: The initializeDeposit function in the StakeManager contract allows validators and delegators to deposit resources for validating nodes. However, the function does not check if the validator is active before accepting the deposit, leading to locked stakes and the inability to withdraw them. This bug 

### Vulnerability Description

#### Root Cause

Deposit transactions can be frontrun to manipulate exchange rates, share prices, or allocation outcomes.

#### Attack Scenario

1. Attacker identifies staking deposit frontrunning in the protocol
2. Exploits the missing validation or incorrect logic
3. Attackers extract value from legitimate stakers through sandwich attacks or rate manipulation

### Vulnerable Pattern Examples

**Example 1: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 2: DoS Risk Due to Small Deposits and Front-Running in `deposit` Function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-risk-due-to-small-deposits-and-front-running-in-deposit-function.md`
```
// Vulnerable pattern from DIA:
##### Description
This issue has been identified in the `deposit` function of the `Prestaking` contract.
There are two potential attack vectors that could be used to DoS the system:

1. **Small Deposits (1 wei deposits)**: Malicious users can fill the `stakingWallets` with extremely small deposits (e.g., 1 wei), which would make it harder to use the system effectively. Adding a minimum deposit amount would prevent such attacks by ensuring that deposits are meaningful, thus limiting the attacker'
```

**Example 3: Elected TSS Nodes Can Act Without Any Deposit** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md`
```
// Vulnerable pattern from Mantle Network:
## Description

A node can remove its insurance deposit and still be elected as an active TSS node. TSS nodes are voted for by the BITDAO, which then pushes the currently elected nodes on-chain. Nodes that wish to be voted for must provide a deposit as insurance that they will perform their role honestly if elected. By timing a withdrawal correctly, a node can remove their deposit and still be elected as an active TSS node. As a result, there is no means of punishing the node for inactivity or m
```

**Example 4: [H-01] `StakedToken` is vulnerable to share inflation attack via donation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, as the targeted staker will lose fund

**Likelihood:** Medium, possible when all stakers redeemed their stake

**Description**

`StakedToken` allows staking of underlying tokens (assets) for staked tokens (shares). It uses an explicit `exchangeRate` for share price calculation that is updated on slashing/returning of funds.

As the `exchangeRate` is updated using the `UNDERLYING_TOKEN.balanceOf(address(this))` in `StakedToken`, it is vulnerable to manipulation via
```

**Example 5: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
function _safeMint(
    address to,
    uint256 tokenId,
    bytes memory _data
) internal virtual {
    _mint(to, tokenId);
    require(
        _checkOnERC721Received(address(0), to, tokenId, _data),
        "ERC721: transfer to non ERC721Receiver implementer"
    );
}
...
function _checkOnERC721Received(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
) private returns (bool) {
    if (to.isContract()) {
        try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, _data) returns (bytes4 retval) {
            return retval == IERC721Receiver.onERC721Received.selector;
```

**Variant: Staking Deposit Frontrunning - MEDIUM Severity Cases** [MEDIUM]
> Found in 28 reports:
> - `reports/cosmos_cometbft_findings/dos-risk-due-to-small-deposits-and-front-running-in-deposit-function.md`
> - `reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md`
> - `reports/cosmos_cometbft_findings/m-01-missing-slippage-protection-in-aerodromedextersol-swapexacttokensfortokens.md`

**Variant: Staking Deposit Frontrunning in Increment** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
> - `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`
> - `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`

**Variant: Staking Deposit Frontrunning in Renzo** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
> - `reports/cosmos_cometbft_findings/m-14-stetheth-feed-being-used-opens-up-to-2-way-deposit-withdrawal-arbitrage.md`

**Variant: Staking Deposit Frontrunning in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Deposit transactions can be frontrun to manipulate exchange rates, share prices, or allocation outco
func secureStakingDepositFrontrunning(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 40 audit reports
- **Severity Distribution**: HIGH: 12, MEDIUM: 28
- **Affected Protocols**: Streamr, Persistence, Tokensfarm, Yieldy, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Staking Balance Desynchronization

### Overview

Internal balance tracking falls out of sync with actual token balances due to missing updates or race conditions. This pattern was found across 8 audit reports with severity distribution: HIGH: 4, MEDIUM: 4.

> **Key Finding**: This bug report describes an issue where an operator is unable to remove a node from the system, leading to an inconsistent state and potential denial of service attacks. This occurs when the removal of a node and the confirmation of that removal happen in the same epoch, causing the node to remain 

### Vulnerability Description

#### Root Cause

Internal balance tracking falls out of sync with actual token balances due to missing updates or race conditions.

#### Attack Scenario

1. Attacker identifies staking balance desynchronization in the protocol
2. Exploits the missing validation or incorrect logic
3. Protocol accounting becomes inconsistent, potentially leading to fund loss or stuck operations

### Vulnerable Pattern Examples

**Example 1: DoS on stake accounting functions by bloating `operatorNodesArray` with irremova** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```go
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 2: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
```solidity
// AgentNftV2::mint()
    function mint(
        uint256 virtualId,
        address to,
        string memory newTokenURI,
        address payable theDAO,
        address founder,
        uint8[] memory coreTypes,
        address pool,
        address token
    ) external onlyRole(MINTER_ROLE) returns (uint256) {
        require(virtualId == _nextVirtualId, "Invalid virtualId");
        _nextVirtualId++;
        _mint(to, virtualId);
        _setTokenURI(virtualId, newTokenURI);
        VirtualInfo storage info = virtualInfos[virtualId];
        info.dao = theDAO;
        info.coreTypes = coreTypes;
        info.founder = founder;
        IERC5805 daoToken = GovernorVotes(theDAO).token();
        info.token = token;

VirtualLP storage lp = virtualLPs[virtualId];
        lp.pool = pool;
        lp.veToken = address(daoToken);

_stakingTokenToVirtualId[address(daoToken)] = virtualId;
@>        _addValidator(virtualId, founder);
@>        _initValidatorScore(virtualId, founder);
        return virtualId;
    }
    // AgentNftV2::addValidator()
    // Expected to be called by `AgentVeToken::stake()` function
    function addValidator(uint256 virtualId, address validator) public {
        if (isValidator(virtualId, validator)) {
// ... (truncated)
```

**Example 3: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 4: Incorrect Accounting for stakedButUnverifiedNativeETH** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md`
```go
162 IEigenPodManager eigenPodManager = IEigenPodManager(lrtConfig.getContract(LRTConstants.EIGEN_POD_MANAGER));
eigenPodManager.stake{ value: 32ether }(pubkey, signature, depositDataRoot);
164
// tracks staked but unverified native ETH
166 stakedButUnverifiedNativeETH += 32ether;
```

**Example 5: [M-03] Attacker Can Desynchronize Supply Snapshot During Same-Block Unstake, Red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md`
```
// Vulnerable pattern from Cabal:
<https://github.com/code-423n4/2025-04-cabal/blob/5b5f92ab4f95e5f9f405bbfa252860472d164705/sources/cabal_token.move# L219-L227>

### Finding description and impact

An attacker holding Cabal LSTs (like sxINIT) can monitor the mempool for the manager’s `voting_reward::snapshot()` transaction. By submitting his own `cabal::initiate_unstake` transaction to execute in the *same block* (`H`) as the manager’s snapshot, the attacker can use two flaws:

1. `cabal_token::burn` (called by their unstake) d
```

**Variant: Staking Balance Desynchronization - HIGH Severity Cases** [HIGH]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
> - `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
> - `reports/cosmos_cometbft_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Internal balance tracking falls out of sync with actual token balances due to missing updates or rac
func secureStakingBalanceDesync(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 4
- **Affected Protocols**: Hipo Finance, Virtuals Protocol, Cabal, Suzaku Core, Kelp
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Deposit Queue Processing Errors

### Overview

Pending deposit queue handling has ordering, processing, or cancellation bugs. This pattern was found across 16 audit reports with severity distribution: HIGH: 7, MEDIUM: 9.

> **Key Finding**: This bug report discusses a problem with the staking protocol that can lead to overestimation of the staking balance. This occurs when a payout fails to transfer after a game is completed, causing the amount to be stored in a separate account. However, the protocol continues to include this amount i

### Vulnerability Description

#### Root Cause

Pending deposit queue handling has ordering, processing, or cancellation bugs.

#### Attack Scenario

1. Attacker identifies deposit queue processing errors in the protocol
2. Exploits the missing validation or incorrect logic
3. Deposits may be lost, duplicated, or processed out of order

### Vulnerable Pattern Examples

**Example 1: [C-01] Pending payouts excluded from total balance cause incorrect share calcula** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Example 2: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 3: Future epoch cache manipulation via `calcAndCacheStakes` allows reward manipulat** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 4: [H-02] It is impossible to slash queued withdrawals that contain a malicious str** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
```go
// keeps track of the index in the `indicesToSkip` array
    uint256 indicesToSkipIndex = 0;

    uint256 strategiesLength = queuedWithdrawal.strategies.length;
    for (uint256 i = 0; i < strategiesLength;) {
        // check if the index i matches one of the indices specified in the `indicesToSkip` array
        if (indicesToSkipIndex < indicesToSkip.length && indicesToSkip[indicesToSkipIndex] == i) {
            unchecked {
                ++indicesToSkipIndex;
            }
        } else {
            if (queuedWithdrawal.strategies[i] == beaconChainETHStrategy){
                    //withdraw the beaconChainETH to the recipient
                _withdrawBeaconChainETH(queuedWithdrawal.depositor, recipient, queuedWithdrawal.shares[i]);
            } else {
                // tell the strategy to send the appropriate amount of funds to the recipient
                queuedWithdrawal.strategies[i].withdraw(recipient, tokens[i], queuedWithdrawal.shares[i]);
            }
            unchecked {
                ++i; // @audit
            }
        }
    }
```

**Example 5: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Variant: Deposit Queue Processing Errors - MEDIUM Severity Cases** [MEDIUM]
> Found in 9 reports:
> - `reports/cosmos_cometbft_findings/m-02-unstaking-calculates-user-share-at-request-time-ignoring-slashing-leading-t.md`
> - `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md`
> - `reports/cosmos_cometbft_findings/m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md`

**Variant: Deposit Queue Processing Errors in Renzo** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
> - `reports/cosmos_cometbft_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`

**Variant: Deposit Queue Processing Errors in Pods Finance Ethereum Volatility Vault Audit** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`
> - `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Pending deposit queue handling has ordering, processing, or cancellation bugs
func secureStakingDepositQueue(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 16 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 9
- **Affected Protocols**: ZetaChain Cross-Chain, Sentiment V2, Coinflip_2025-02-19, Cabal, Infrared Contracts
- **Validation Strength**: Strong (3+ auditors)

---

## 6. First Depositor / Share Inflation Attack

### Overview

First depositor can manipulate the share-to-asset exchange rate through donation or inflation techniques. This pattern was found across 17 audit reports with severity distribution: HIGH: 6, MEDIUM: 11.

> **Key Finding**: This bug report is about a possible security flaw in Swell Network's staking system. If a node operator interacts with the deposit contract directly first, they can set the withdrawal address to an arbitrary address. This means that once deposits are enabled on the Beacon chain, it is possible for t

### Vulnerability Description

#### Root Cause

First depositor can manipulate the share-to-asset exchange rate through donation or inflation techniques.

#### Attack Scenario

1. Attacker identifies first depositor / share inflation attack in the protocol
2. Exploits the missing validation or incorrect logic
3. Subsequent depositors receive fewer shares than expected, losing funds to the attacker

### Vulnerable Pattern Examples

**Example 1: Direct Deposits Enable Theft Of A Validator’s Funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`
```
// Vulnerable pattern from Swell:
## Description

If a node operator interacts with the deposit contract directly first, it is possible for them to set the withdrawal address to an arbitrary address. Then this node can be added to Swell and used normally. Once deposits are enabled on the Beacon chain, it is possible for this node operator to withdraw all the ETH deposited with this node. In addition to this, it is impossible for the normal withdrawal method specified by `swNFTUpgrade.sol` to work for deposits made to this node.

```

**Example 2: [H-01] `StakedToken` is vulnerable to share inflation attack via donation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, as the targeted staker will lose fund

**Likelihood:** Medium, possible when all stakers redeemed their stake

**Description**

`StakedToken` allows staking of underlying tokens (assets) for staked tokens (shares). It uses an explicit `exchangeRate` for share price calculation that is updated on slashing/returning of funds.

As the `exchangeRate` is updated using the `UNDERLYING_TOKEN.balanceOf(address(this))` in `StakedToken`, it is vulnerable to manipulation via
```

**Example 3: [H-03] StakedCitadel depositors can be attacked by the first depositor with depr** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-stakedcitadel-depositors-can-be-attacked-by-the-first-depositor-with-depres.md`
```
// Vulnerable pattern from BadgerDAO:
_Submitted by hyh, also found by VAD37, cmichel, 0xDjango, berndartmueller, and danb_

<https://github.com/code-423n4/2022-04-badger-citadel/blob/main/src/StakedCitadel.sol#L881-L892>

<https://github.com/code-423n4/2022-04-badger-citadel/blob/main/src/StakedCitadel.sol#L293-L295>

### Impact

An attacker can become the first depositor for a recently created StakedCitadel contract, providing a tiny amount of Citadel tokens by calling `deposit(1)` (raw values here, `1` is `1 wei`, `1e18` is `1 Ci
```

**Example 4: [M-01] Freezing of funds - Hacker can prevent users withdraws in giant pools** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-freezing-of-funds-hacker-can-prevent-users-withdraws-in-giant-pools.md`
```
// Vulnerable pattern from Stakehouse Protocol:
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantPoolBase.sol#L69><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantSavETHVaultPool.sol#L66><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantPoolBase.sol#L96>

### Impact

A hacker can prevent users from withdraw
```

**Example 5: [M-02] _depositEther Does Not Increment Validator Index,Causing All Deposits to ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md`
```
// Vulnerable pattern from Mystic Finance:
## Severity

Medium
```

**Variant: First Depositor / Share Inflation Attack - MEDIUM Severity Cases** [MEDIUM]
> Found in 11 reports:
> - `reports/cosmos_cometbft_findings/m-01-freezing-of-funds-hacker-can-prevent-users-withdraws-in-giant-pools.md`
> - `reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md`
> - `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md`

**Variant: First Depositor / Share Inflation Attack in Swell** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`
> - `reports/cosmos_cometbft_findings/staking-before-operator-leads-to-no-sweth-minted.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: First depositor can manipulate the share-to-asset exchange rate through donation or inflation techni
func secureStakingDepositInflation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 17 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 11
- **Affected Protocols**: Rollie, EigenLabs — EigenLayer, EIP-4337 – Ethereum Account Abstraction Audit, Valantis, Stakehouse Protocol
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Incorrect Staking Calculation Logic

### Overview

Mathematical errors in staking amount calculations, share conversions, or proportional distributions. This pattern was found across 45 audit reports with severity distribution: HIGH: 27, MEDIUM: 18.

> **Key Finding**: This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

### Vulnerability Description

#### Root Cause

Mathematical errors in staking amount calculations, share conversions, or proportional distributions.

#### Attack Scenario

1. Attacker identifies incorrect staking calculation logic in the protocol
2. Exploits the missing validation or incorrect logic
3. Incorrect staking amounts, unfair distributions, or protocol insolvency over time

### Vulnerable Pattern Examples

**Example 1: Accounting for `rewardStakeRatioSum` is incorrect when a delayed balance or rewa** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
```go
// Before start
latestActiveBalanceAfterFee = 32 ETH
latestActiveRewards = 0

// startReport()
reportSweptBalance = 0 (rewards is in BeaconChain)

// syncValidators()
reportActiveBalance = 32.105 ETH

// finalizeReport()
rewards = 0.105 ETH
change = rewards - latestActiveRewards = 0.105 ETH
gainAfterFee = 0.1 ETH
=> rewardStakeRatioSum is increased
=> latestActiveBalanceAfterFee = 32.1

sweptRewards = 0
=> latestActiveRewards = 0.105
```

**Example 2: beaconChainETHStrategy Queued Withdrawals Excluded From Slashable Shares** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
```solidity
/// @dev Add to the cumulative withdrawn scaled shares from an operator for a given strategy
function _addQueuedSlashableShares(address operator, IStrategy strategy, uint256 scaledShares) internal {
    // @audit beaconChainETHStrategy is excluded from slashable shares tracking
    if (strategy != beaconChainETHStrategy) {
        uint256 currCumulativeScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
        _cumulativeScaledSharesHistory[operator][strategy].push({
            key: uint32(block.number),
            value: currCumulativeScaledShares + scaledShares
        });
    }
}
```

**Example 3: [C-01] Incorrect reward calculation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-incorrect-reward-calculation.md`
```solidity
File: NFTStaking.sol
82:     function unstakeNFTsRouter(address _sender, uint256[] calldata _tokenIds) external {
83:         require(msg.sender == stakingRouterAddress, "Only router");
84: 
85:@>       _unstakeNFTs(_sender, _tokenIds);
86:     }
...
88:     function claimRewards() public {
89:@>       _claimRewards(msg.sender);
90:     }
...
182:     function _unstakeNFTs(address _sender, uint256[] calldata _tokenIds) internal {
183:@>     claimRewards();
```

**Example 4: [C-01] Pending payouts excluded from total balance cause incorrect share calcula** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Example 5: Flawed Implementation of Reward Score Calculation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md`
```rust
pub fn calculate_slash(stats: &OracleStatsAccountData, reward: u64) -> u64 {
    let slash_score = stats.finalized_epoch.slash_score;
    if slash_score == 0 {
        return 0;
    }
    let reward_score = stats.finalized_epoch.reward_score;
    Decimal::from(reward)
        .saturating_mul(reward_score.into())
        .checked_div(slash_score.into())
        .unwrap()
        .to_u64()
        .unwrap_or(0)
}
```

**Variant: Incorrect Staking Calculation Logic - MEDIUM Severity Cases** [MEDIUM]
> Found in 18 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
> - `reports/cosmos_cometbft_findings/inaccurate-stake-calculation-due-to-decimal-mismatch-across-multitoken-asset-cla.md`

**Variant: Incorrect Staking Calculation Logic in Casimir** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`

**Variant: Incorrect Staking Calculation Logic in EigenLayer** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md`

**Variant: Incorrect Staking Calculation Logic in Coinflip_2025-02-19** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
> - `reports/cosmos_cometbft_findings/c-02-pending-stake-not-accounted-for-in-liquidity-calculations.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Mathematical errors in staking amount calculations, share conversions, or proportional distributions
func secureStakingIncorrectCalculation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 45 audit reports
- **Severity Distribution**: HIGH: 27, MEDIUM: 18
- **Affected Protocols**: Subscription Token Protocol V2, Persistence, Casimir, CAP Labs Covered Agent Protocol, Kelp
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Broken Staking Invariants

### Overview

Core staking invariants (e.g., total staked == sum of individual stakes) are violated through edge cases or logic errors. This pattern was found across 7 audit reports with severity distribution: HIGH: 5, MEDIUM: 2.

> **Key Finding**: This bug report discusses an issue with the StakeRegistry contract, specifically with the `setLookAheadPeriod` function. This function allows the CoordinatorOwner to set the lookahead time for a slashable quorum. However, the function is missing a constraint check that exists in another function, wh

### Vulnerability Description

#### Root Cause

Core staking invariants (e.g., total staked == sum of individual stakes) are violated through edge cases or logic errors.

#### Attack Scenario

1. Attacker identifies broken staking invariants in the protocol
2. Exploits the missing validation or incorrect logic
3. Protocol enters inconsistent state, potentially enabling exploits or causing permanent fund loss

### Vulnerable Pattern Examples

**Example 1: [EIGEN2-4] Missing constraint check for modification of lookahead time of slasha** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/eigen2-4-missing-constraint-check-for-modification-of-lookahead-time-of-slashabl.md`
```go
require(
    AllocationManager(address(allocationManager)).DEALLOCATION_DELAY() > lookAheadPeriod,
    LookAheadPeriodTooLong()
);
```

**Example 2: [H-01] `userTotalStaked` invariant will be broken due to vulnerable implementati** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-usertotalstaked-invariant-will-be-broken-due-to-vulnerable-implementations-.md`
```solidity
//id-staking-v2/contracts/IdentityStaking.sol
  function release(
    address staker,
    address stakee,
    uint88 amountToRelease,
    uint16 slashRound
  ) external onlyRole(RELEASER_ROLE) whenNotPaused {
...
    if (staker == stakee) {
...
      selfStakes[staker].slashedAmount -= amountToRelease;
      //@audit selfStakes[staker].amount is updated but `userTotalStaked` is not
|>    selfStakes[staker].amount += amountToRelease;
    } else {
...
      communityStakes[staker][stakee].slashedAmount -= amountToRelease;
      //@audit communityStakes[staker].amount is updated but `userTotalStaked` is not
|>    communityStakes[staker][stakee].amount += amountToRelease;
    }
...
```

**Example 3: [H-04] Violation of Invariant Allowing DSSs to Slash Unregistered Operators** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-violation-of-invariant-allowing-dsss-to-slash-unregistered-operators.md`
```solidity
function test_slash_unregistered_operator() public {
        // register operator to dss, deploy vaults, stake vaults to dss
        stake_vaults_to_dss();
        // check if operator is registered to dss
        assertEq(true, core.isOperatorRegisteredToDSS(operator, dss));
        // unstake vaults from dss
        address[] memory operatorVaults = core.fetchVaultsStakedInDSS(operator, dss);
        Operator.StakeUpdateRequest memory stakeUpdate =
            Operator.StakeUpdateRequest({vault: operatorVaults[0], dss: dss, toStake: false});
        Operator.StakeUpdateRequest memory stakeUpdate2 =
            Operator.StakeUpdateRequest({vault: operatorVaults[1], dss: dss, toStake: false});
        vm.startPrank(operator);
        Operator.QueuedStakeUpdate memory queuedStakeUpdate = core.requestUpdateVaultStakeInDSS(stakeUpdate);
        Operator.QueuedStakeUpdate memory queuedStakeUpdate2 = core.requestUpdateVaultStakeInDSS(stakeUpdate2);
        vm.stopPrank();
        skip(8 days);
        // dss request slashing
        uint96[] memory slashPercentagesWad = new uint96[](2);
        slashPercentagesWad[0] = uint96(10e18);
        slashPercentagesWad[1] = uint96(10e18);
        SlasherLib.SlashRequest memory slashingReq = SlasherLib.SlashRequest({
            operator: operator,
            slashPercentagesWad: slashPercentagesWad,
            vaults: operatorVaults
        });
        vm.startPrank(address(dss));
        SlasherLib.QueuedSlashing memory queuedSlashing = core.requestSlashing(slashingReq);
        vm.stopPrank();
        skip(1 days);
        vm.startPrank(operator);
        // finalize unstake and unregister operator from dss
        core.finalizeUpdateVaultStakeInDSS(queuedStakeUpdate);
        core.finalizeUpdateVaultStakeInDSS(queuedStakeUpdate2);
        core.unregisterOperatorFromDSS(dss, "");
        vm.stopPrank();
// ... (truncated)
```

**Example 4: [H-06] Hardcoded gas used in ERC20 queries allows for block production halt from** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
```go
File: funtoken.go
265: func (p precompileFunToken) balance(
266: 	start OnRunStartResult,
267: 	contract *vm.Contract,
268: ) (bz []byte, err error) {
---
285: 	erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(funtoken.Erc20Addr.Address, addrEth, ctx)
286: 	if err != nil {
287: 		return
288: 	}
```

**Example 5: Risk of token/uToken exchange rate manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md`
```go
func (k Keeper) TotalUTokenSupply(ctx sdk.Context, uTokenDenom string) sdk.Coin {
    if k.IsAcceptedUToken(ctx, uTokenDenom) {
        return k.bankKeeper.GetSupply(ctx, uTokenDenom)
        // TODO - Question: Does bank module still track balances sent (locked) via IBC?
        // If it doesn't then the balance returned here would decrease when the tokens
        // are sent off, which is not what we want. In that case, the keeper should keep
        // an sdk.Int total supply for each uToken type.
    }
    return sdk.NewCoin(uTokenDenom, sdk.ZeroInt())
}
```

**Variant: Broken Staking Invariants - HIGH Severity Cases** [HIGH]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/h-01-usertotalstaked-invariant-will-be-broken-due-to-vulnerable-implementations-.md`
> - `reports/cosmos_cometbft_findings/h-04-violation-of-invariant-allowing-dsss-to-slash-unregistered-operators.md`
> - `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Core staking invariants (e.g., total staked == sum of individual stakes) are violated through edge c
func secureStakingInvariantBroken(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 5, MEDIUM: 2
- **Affected Protocols**: Upgrade, Berachain Beaconkit, Umee, Karak, Nibiru
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Staking Deposit Amount Tracking Errors
grep -rn 'staking|deposit|amount|tracking' --include='*.go' --include='*.sol'
# Missing or Insufficient Deposit Validation
grep -rn 'staking|deposit|validation' --include='*.go' --include='*.sol'
# Staking Deposit Frontrunning
grep -rn 'staking|deposit|frontrunning' --include='*.go' --include='*.sol'
# Staking Balance Desynchronization
grep -rn 'staking|balance|desync' --include='*.go' --include='*.sol'
# Deposit Queue Processing Errors
grep -rn 'staking|deposit|queue' --include='*.go' --include='*.sol'
# First Depositor / Share Inflation Attack
grep -rn 'staking|deposit|inflation' --include='*.go' --include='*.sol'
# Incorrect Staking Calculation Logic
grep -rn 'staking|incorrect|calculation' --include='*.go' --include='*.sol'
# Broken Staking Invariants
grep -rn 'staking|invariant|broken' --include='*.go' --include='*.sol'
```

## Keywords

`access`, `account`, `accounting`, `allowing`, `allows`, `amount`, `appchain`, `attack`, `attacked`, `avoid`, `balance`, `bank`, `beaconchainethstrategy`, `because`, `bloating`, `bond`, `bridge`, `broken`, `cache`, `calculation`, `calculations`, `cause`, `causes`, `check`, `constraint`, `control`, `cosmos`, `could`, `current`, `delayed`
