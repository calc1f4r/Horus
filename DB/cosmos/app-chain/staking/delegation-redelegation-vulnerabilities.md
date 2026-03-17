---
protocol: generic
chain: cosmos
category: staking
vulnerability_type: delegation_redelegation_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: staking_logic

primitives:
  - self_manipulation
  - dos_revert
  - state_inconsistency
  - to_inactive
  - frontrunning
  - reward_manipulation
  - redelegation_error
  - unbonding_exploit

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

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | staking_logic | delegation_redelegation_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - UnstakeEntry
  - _initValidatorScore
  - balanceOf
  - closeRebalanceRequests
  - deposit
  - dos_revert
  - frontrunning
  - redelegation_error
  - reward_manipulation
  - safeTransferFrom
  - self_manipulation
  - service
  - state_inconsistency
  - their
  - to_inactive
  - unbonding_exploit
  - users
  - withdraw
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Delegation Self Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| In `Operator._transfer()`, `onDelegate()` should be called a | `reports/cosmos_cometbft_findings/in-operator_transfer-ondelegate-should-be-called-after-updating-the-token-balanc.md` | MEDIUM | Cyfrin |
| Lack of Liquid Staking Accounting | `reports/cosmos_cometbft_findings/lack-of-liquid-staking-accounting.md` | MEDIUM | OtterSec |
| Validator cannot set new address if more than 300 unstakes i | `reports/cosmos_cometbft_findings/m-1-validator-cannot-set-new-address-if-more-than-300-unstakes-in-its-array.md` | MEDIUM | Sherlock |
| `unbond_public` logic causes issues for some delegators prev | `reports/cosmos_cometbft_findings/m-2-unbond_public-logic-causes-issues-for-some-delegators-preventing-partial-wit.md` | MEDIUM | Sherlock |
| Adversary can abuse delegating to lower quorum | `reports/cosmos_cometbft_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md` | MEDIUM | Sherlock |
| Mismanagement Of Delegator Funds | `reports/cosmos_cometbft_findings/mismanagement-of-delegator-funds.md` | HIGH | OtterSec |
| The delegator resetting self-delegation causes multiple issu | `reports/cosmos_cometbft_findings/the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md` | HIGH | Cyfrin |

### Delegation Dos Revert
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-02] Stakes not forwarded post-delegation, positions unwit | `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | HIGH | Pashov Audit Group |
| Delegated Boost Persists Even If veRAAC Is Withdrawn/Reduced | `reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md` | MEDIUM | Codehawks |
| Delegators can redelegate stakes to jailed delegatee | `reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md` | MEDIUM | TrailOfBits |
| DPoS is vulnerable to signiﬁcant centralization risk | `reports/cosmos_cometbft_findings/dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md` | HIGH | TrailOfBits |
| Freezing of Validator Bond Delegations | `reports/cosmos_cometbft_findings/freezing-of-validator-bond-delegations.md` | MEDIUM | OtterSec |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H02] Delegators can prevent service providers from deregist | `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md` | HIGH | OpenZeppelin |
| [H11] A service provider can prevent their delegators from u | `reports/cosmos_cometbft_findings/h11-a-service-provider-can-prevent-their-delegators-from-undelegating-their-stak.md` | HIGH | OpenZeppelin |

### Delegation State Inconsistency
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incomplete Zero-Height Genesis Preparation in Allora Network | `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md` | MEDIUM | Sherlock |
| Mismanagement Of Delegator Funds | `reports/cosmos_cometbft_findings/mismanagement-of-delegator-funds.md` | HIGH | OtterSec |

### Delegation To Inactive
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Delegators can redelegate stakes to jailed delegatee | `reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md` | MEDIUM | TrailOfBits |
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| [H-01] Adversary can make honest parties unable to retrieve  | `reports/cosmos_cometbft_findings/h-01-adversary-can-make-honest-parties-unable-to-retrieve-their-assertion-stakes.md` | HIGH | Code4rena |
| [M-04] New stakes delegated even when validator is inactive | `reports/cosmos_cometbft_findings/m-04-new-stakes-delegated-even-when-validator-is-inactive.md` | MEDIUM | Pashov Audit Group |
| Potential Stake Lock and Inconsistency Due to Validator Stat | `reports/cosmos_cometbft_findings/potential-stake-lock-and-inconsistency-due-to-validator-state-transitions.md` | MEDIUM | OpenZeppelin |
| [PRST-4] Unbonding of validators does not give priority to i | `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md` | MEDIUM | Hexens |
| Slashing process could be reverted | `reports/cosmos_cometbft_findings/slashing-process-could-be-reverted.md` | MEDIUM | OpenZeppelin |

### Delegation Frontrunning
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-01] User can earn rewards by frontrunning the new rewards | `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md` | MEDIUM | Code4rena |

### Delegation Reward Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-05] `ValidatorRegistry::validatorScore/getPastValidatorSc | `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md` | HIGH | Code4rena |
| LACK OF UPPER LIMIT CHECKS ALLOWS BLOCKING WITHDRAWALS | `reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md` | MEDIUM | Halborn |
| Locked-In Licenses Can Be Transferred | `reports/cosmos_cometbft_findings/locked-in-licenses-can-be-transferred.md` | HIGH | OpenZeppelin |
| [M-01] User can earn rewards by frontrunning the new rewards | `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md` | MEDIUM | Code4rena |
| [M-04] Processing all withdrawals before all deposits can ca | `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md` | MEDIUM | Code4rena |
| [M-06] LP Redelegation Uses Inaccurate Internal Tracker Amou | `reports/cosmos_cometbft_findings/m-06-lp-redelegation-uses-inaccurate-internal-tracker-amount-leading-to-potentia.md` | MEDIUM | Code4rena |
| [M-14] `VotesUpgradeable::delegate` bypasses the `addValidat | `reports/cosmos_cometbft_findings/m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md` | MEDIUM | Code4rena |

### Delegation Redelegation Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| INADEQUATE TRACKING OF PENDING REDELEGATIONS | `reports/cosmos_cometbft_findings/inadequate-tracking-of-pending-redelegations.md` | MEDIUM | Halborn |
| [M-01] Incorrect Balance Check in Validator Redelegation Pro | `reports/cosmos_cometbft_findings/m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md` | MEDIUM | Code4rena |
| [M-06] LP Redelegation Uses Inaccurate Internal Tracker Amou | `reports/cosmos_cometbft_findings/m-06-lp-redelegation-uses-inaccurate-internal-tracker-amount-leading-to-potentia.md` | MEDIUM | Code4rena |
| Misleading Error Messages and Comments in msgClaimRewards an | `reports/cosmos_cometbft_findings/misleading-error-messages-and-comments-in-msgclaimrewards-and-performmsgclaimrew.md` | MEDIUM | Halborn |

### Delegation Unbonding Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Key typo may allow store corruption | `reports/cosmos_cometbft_findings/key-typo-may-allow-store-corruption.md` | HIGH | Halborn |
| [M-08] Unbonding validator random selection can be predicted | `reports/cosmos_cometbft_findings/m-08-unbonding-validator-random-selection-can-be-predicted.md` | MEDIUM | Code4rena |
| Changes of the `UnbondingTime` are not accounted for | `reports/cosmos_cometbft_findings/m-12-changes-of-the-unbondingtime-are-not-accounted-for.md` | MEDIUM | Sherlock |

---

# Delegation Redelegation Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Delegation Redelegation Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Delegation Self Manipulation](#1-delegation-self-manipulation)
2. [Delegation Dos Revert](#2-delegation-dos-revert)
3. [Delegation State Inconsistency](#3-delegation-state-inconsistency)
4. [Delegation To Inactive](#4-delegation-to-inactive)
5. [Delegation Frontrunning](#5-delegation-frontrunning)
6. [Delegation Reward Manipulation](#6-delegation-reward-manipulation)
7. [Delegation Redelegation Error](#7-delegation-redelegation-error)
8. [Delegation Unbonding Exploit](#8-delegation-unbonding-exploit)

---

## 1. Delegation Self Manipulation

### Overview

Implementation flaw in delegation self manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 2, MEDIUM: 5.

> **Key Finding**: A bug was discovered in the `_transfer()` function of the Operator contract in the Streamr Network Contracts repository. The bug allowed the operator owner to transfer their shares to other delegators, in anticipation of slashing, to avoid slashing. This is because the `onDelegate()` function was ca



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | staking_logic | delegation_redelegation_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `staking_logic`
- High-signal code keywords: `UnstakeEntry`, `_initValidatorScore`, `balanceOf`, `closeRebalanceRequests`, `deposit`, `dos_revert`, `frontrunning`, `redelegation_error`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `in.function -> only.function -> where.function`
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

Implementation flaw in delegation self manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation self manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: In `Operator._transfer()`, `onDelegate()` should be called after updating the to** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/in-operator_transfer-ondelegate-should-be-called-after-updating-the-token-balanc.md`
```go
File: contracts\OperatorTokenomics\Operator.sol
324:         // transfer creates a new delegator: check if the delegation policy allows this "delegation"
325:         if (balanceOf(to) == 0) {
326:             if (address(delegationPolicy) != address(0)) {
327:                 moduleCall(address(delegationPolicy), abi.encodeWithSelector(delegationPolicy.onDelegate.selector, to)); //@audit
should be called after _transfer()
328:             }
329:         }
330:
331:         super._transfer(from, to, amount);
332:
```

**Example 2: Lack of Liquid Staking Accounting** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-liquid-staking-accounting.md`
```
// Vulnerable pattern from Cosmos LSM:
## Validator Issues in Liquid Staking

CreateValidator lacks the liquid staking-related bookkeeping present in Delegate. In Delegate, specific checks and updates are performed when the delegation is initiated by a liquid staking provider, converting the staked tokens into an equivalent number of shares in the validator and safely updating the global liquid stake and validator liquid shares. However, no such checks or updates are performed for liquid staking when self-delegating the initial stake
```

**Example 3: Validator cannot set new address if more than 300 unstakes in it's array** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-validator-cannot-set-new-address-if-more-than-300-unstakes-in-its-array.md`
```
// Vulnerable pattern from Covalent:
Source: https://github.com/sherlock-audit/2023-11-covalent-judging/issues/25
```

**Example 4: `unbond_public` logic causes issues for some delegators preventing partial withd** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-unbond_public-logic-causes-issues-for-some-delegators-preventing-partial-wit.md`
```go
// Check if the delegator will fall below 10,000 bonded credits.
lt r16 10_000_000_000u64 into r17;

// If the validator is forcing the delegator to unbond OR the delegator will fall below 10,000 bonded credits.
or r11 r17 into r18;

// Determine the amount to unbond: requested amount if >= 10,000 credits, otherwise the full bonded amount.
ternary r18 r5.microcredits r2 into r19;
```

**Example 5: Adversary can abuse delegating to lower quorum** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md`
```
// Vulnerable pattern from FrankenDAO:
Source: https://github.com/sherlock-audit/2022-11-frankendao-judging/issues/24
```

**Variant: Delegation Self Manipulation - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/mismanagement-of-delegator-funds.md`
> - `reports/cosmos_cometbft_findings/the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation self manipulation logic allows exploitation through missing valida
func secureDelegationSelfManipulation(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 5
- **Affected Protocols**: Streamr, Templedao, ALEO, Cosmos LSM, Covalent
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Delegation Dos Revert

### Overview

Implementation flaw in delegation dos revert logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 27 audit reports with severity distribution: HIGH: 9, MEDIUM: 18.

> **Key Finding**: The bug report describes a problem in the 'BobStaking' smart contract where users who delegate governance are unable to withdraw their staked tokens. This is because when a user delegates governance, their tokens are moved to a 'DelegationSurrogate' contract. However, later calls to stake more token

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation dos revert logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation dos revert in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: [C-02] Stakes not forwarded post-delegation, positions unwithdrawable** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
```go
IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
stakers[receiver].amountStaked += _amount;
```

**Example 2: Delegated Boost Persists Even If veRAAC Is Withdrawn/Reduced** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md`
```solidity
This sets `UserBoost` with `amount` and an `expiry`, effectively guaranteeing that “X” units of veRAAC are delegated for that duration.
2. **No Ongoing Balance Check**\
   Once set, the **BoostController** never re‑checks whether the user still has that many veRAAC tokens locked in veRAACToken. The contract only checks the user’s balance at the moment of delegation (via `if (userBalance < amount) revert InsufficientVeBalance()`).
3. **User Reduces or Withdraws veRAAC**\
   Right after delegating, the user calls:
```

**Example 3: Delegators can redelegate stakes to jailed delegatee** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md`
```
// Vulnerable pattern from Elixir Protocol:
## Denial of Service Vulnerability

**Difficulty:** High

**Type:** Denial of Service
```

**Example 4: DPoS is vulnerable to signiﬁcant centralization risk** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md`
```
// Vulnerable pattern from Upgrade:
## Diﬃculty: N/A
```

**Example 5: Freezing of Validator Bond Delegations** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/freezing-of-validator-bond-delegations.md`
```
// Vulnerable pattern from Cosmos LSM:
## Vulnerability Details

The vulnerability arises from the interaction between tokenized shares, validator bond shares, and the delegation mechanisms in the staking module. Specifically, it exploits a flaw that allows a malicious user to repeatedly manipulate the `ValidatorBondShares` balance of a validator, potentially freezing other delegators’ validator bond delegations. 

While `TokenizeShares` does not permit `validatorbond`, tokens can still be transferred to a delegator with a `validator
```

**Variant: Delegation Dos Revert - MEDIUM Severity Cases** [MEDIUM]
> Found in 18 reports:
> - `reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md`
> - `reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md`
> - `reports/cosmos_cometbft_findings/freezing-of-validator-bond-delegations.md`

**Variant: Delegation Dos Revert in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
> - `reports/cosmos_cometbft_findings/h11-a-service-provider-can-prevent-their-delegators-from-undelegating-their-stak.md`

**Variant: Delegation Dos Revert in Cabal** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md`
> - `reports/cosmos_cometbft_findings/m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md`

**Variant: Delegation Dos Revert in ALEO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-1-delegated-state-is-not-removed-after-it-reaches-zero-potentially-leading-to-.md`
> - `reports/cosmos_cometbft_findings/m-2-unbond_public-logic-causes-issues-for-some-delegators-preventing-partial-wit.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation dos revert logic allows exploitation through missing validation, i
func secureDelegationDosRevert(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 27 audit reports
- **Severity Distribution**: HIGH: 9, MEDIUM: 18
- **Affected Protocols**: Upgrade, KelpDAO, Templedao, Tortugal TIP, Core Contracts
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Delegation State Inconsistency

### Overview

Implementation flaw in delegation state inconsistency logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: Issue M-10 is a bug in the Allora Network's implementation of prepForZeroHeightGenesis, which is used to export the state of the network at a specific height. The current implementation is missing several key steps that are present in the reference implementation, potentially leading to inconsistent

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation state inconsistency logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation state inconsistency in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: Incomplete Zero-Height Genesis Preparation in Allora Network** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md`
```
// Vulnerable pattern from Allora:
Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/43
```

**Example 2: Mismanagement Of Delegator Funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/mismanagement-of-delegator-funds.md`
```go
func (k Keeper) UnstakeEntry(ctx sdk.Context, validator, chainID, creator, unstakeDescription string) error {
    [...]
    err = k.dualstakingKeeper.UnbondFull(ctx, existingEntry.GetAddress(), validator, existingEntry.GetAddress(), existingEntry.GetChain(), existingEntry.Stake, true)
    if err != nil {
        return utils.LavaFormatWarning("can't unbond self delegation", err,
            utils.Attribute{Key: "address", Value: existingEntry.Address},
            utils.Attribute{Key: "spec", Value: chainID},
        )
    }
    [...]
    return k.epochStorageKeeper.AppendUnstakeEntry(ctx, existingEntry, unstakeHoldBlocks)
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation state inconsistency logic allows exploitation through missing vali
func secureDelegationStateInconsistency(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Lava, Allora
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Delegation To Inactive

### Overview

Implementation flaw in delegation to inactive logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 2, MEDIUM: 5.

> **Key Finding**: This report discusses a bug in the Elixir Protocol that could lead to a denial of service. The issue is caused by a helper method that does not prevent users from delegating to a validator that has been jailed. This means that honest users could accidentally lose access to their stake. The bug occur

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation to inactive logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation to inactive in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: Delegators can redelegate stakes to jailed delegatee** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md`
```
// Vulnerable pattern from Elixir Protocol:
## Denial of Service Vulnerability

**Difficulty:** High

**Type:** Denial of Service
```

**Example 2: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 3: [H-01] Adversary can make honest parties unable to retrieve their assertion stak** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-adversary-can-make-honest-parties-unable-to-retrieve-their-assertion-stakes.md`
```go
A -- B -- C -- D(latest confirmed) -- E
```

**Example 4: [M-04] New stakes delegated even when validator is inactive** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-new-stakes-delegated-even-when-validator-is-inactive.md`
```go
if (amount > 0) {
            address delegateTo = validatorManager.getDelegation(address(this));
            require(delegateTo != address(0), "No delegation set");

            // Send tokens to delegation
            l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);

            emit Delegate(delegateTo, amount);
        }
```

**Example 5: [PRST-4] Unbonding of validators does not give priority to inactive validators** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
```
// Vulnerable pattern from Persistence:
**Severity:** Medium

**Path:** x/liquidstake/keeper/liquidstake.go:LiquidUnstake#L344-L459

**Description:**

When a user wants to withdraw their `stkXPRT` for `xprt`, they will call `LiquidUnstake`. In the function, the module will back out delegations for each validator according to their weight for a total of the unbonding amount. The module takes the whole set of validators and does not check their active status.

By not giving priority to unbonding inactive validators first, it will furthe
```

**Variant: Delegation To Inactive - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
> - `reports/cosmos_cometbft_findings/h-01-adversary-can-make-honest-parties-unable-to-retrieve-their-assertion-stakes.md`

**Variant: Delegation To Inactive in FCHAIN Validator and Staking Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
> - `reports/cosmos_cometbft_findings/potential-stake-lock-and-inconsistency-due-to-validator-state-transitions.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation to inactive logic allows exploitation through missing validation, 
func secureDelegationToInactive(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 5
- **Affected Protocols**: Persistence, Arbitrum Foundation, Elixir Protocol, Kinetiq_2025-02-26, Forta Protocol Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Delegation Frontrunning

### Overview

Implementation flaw in delegation frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The report discusses a bug in the LiquidProxy.sol contract, which is part of the Ron staking contract. The bug allows users to earn rewards without actually staking their tokens for a long period of time. This is done by frontrunning the new rewards arrival and immediately withdrawing them. The repo

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation frontrunning logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation frontrunning in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: [M-01] User can earn rewards by frontrunning the new rewards accumulation in Ron** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
```go
User -> delegate -> RonStaking -> Wait atleast a day -> New Rewards
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation frontrunning logic allows exploitation through missing validation,
func secureDelegationFrontrunning(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Liquid Ron
- **Validation Strength**: Single auditor

---

## 6. Delegation Reward Manipulation

### Overview

Implementation flaw in delegation reward manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 17 audit reports with severity distribution: HIGH: 4, MEDIUM: 13.

> **Key Finding**: The `MsgSetBeforeSendHook` in the `tokenfactory` module allows the creator of a token to set a custom logic for determining whether a transfer should succeed. However, a malicious token creator can set an invalid address as the hook, causing transfers to fail and potentially leading to a denial of s

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation reward manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation reward manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 2: [H-05] `ValidatorRegistry::validatorScore/getPastValidatorScore` allows validato** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
```solidity
function _initValidatorScore(
    uint256 virtualId,
    address validator
) internal {
    _baseValidatorScore[validator][virtualId] = _getMaxScore(virtualId);
}
```

**Example 3: LACK OF UPPER LIMIT CHECKS ALLOWS BLOCKING WITHDRAWALS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md`
```rust
fn change_unlock_period_of_delegator_deposit(&mut self, value: U64) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value.0 != protocol_settings.unlock_period_of_delegator_deposit.0,
        "The value is not changed."
    );
    protocol_settings.unlock_period_of_delegator_deposit = value;
    self.protocol_settings.set(&protocol_settings);
}
```

**Example 4: Locked-In Licenses Can Be Transferred** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/locked-in-licenses-can-be-transferred.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
Possession of an [`FNode`](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/FNodes.sol) license is a [requirement to become a validator](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L194-L196) on FCHAIN. Validators must [lock](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L209) their ERC-721-compliant `FN
```

**Example 5: [M-01] User can earn rewards by frontrunning the new rewards accumulation in Ron** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
```go
User -> delegate -> RonStaking -> Wait atleast a day -> New Rewards
```

**Variant: Delegation Reward Manipulation - MEDIUM Severity Cases** [MEDIUM]
> Found in 13 reports:
> - `reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md`
> - `reports/cosmos_cometbft_findings/m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
> - `reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md`

**Variant: Delegation Reward Manipulation in Virtuals Protocol** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-05-validatorregistryvalidatorscoregetpastvalidatorscore-allows-validator-to-ea.md`
> - `reports/cosmos_cometbft_findings/m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md`

**Variant: Delegation Reward Manipulation in Covalent** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-5-no-cooldown-in-recoverunstaking-opens-up-several-possible-attacks-by-abusing.md`
> - `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation reward manipulation logic allows exploitation through missing vali
func secureDelegationRewardManipulation(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 4, MEDIUM: 13
- **Affected Protocols**: KelpDAO, Virtuals Protocol, ZetaChain Cross-Chain, Cosmos Module, 0x v3 Staking
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Delegation Redelegation Error

### Overview

Implementation flaw in delegation redelegation error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 1, MEDIUM: 4.

> **Key Finding**: The `MsgSetBeforeSendHook` in the `tokenfactory` module allows the creator of a token to set a custom logic for determining whether a transfer should succeed. However, a malicious token creator can set an invalid address as the hook, causing transfers to fail and potentially leading to a denial of s

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation redelegation error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation redelegation error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 2: INADEQUATE TRACKING OF PENDING REDELEGATIONS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/inadequate-tracking-of-pending-redelegations.md`
```go
if let Some(delegation) = delegated_amount {
 // Terra core returns zero if there is another active redelegation
 // That means we cannot start a new redelegation, so we only remove a validator from
 // the registry.
 // We'll do a redelegation manually later by sending RedelegateProxy to the hub
 if delegation.can_redelegate.amount < delegation.amount.amount {
  return StdResult::Ok(Response::new());
 }

 let (_, delegations) =
  calculate_delegations(delegation.amount.amount, validators.as_slice())?;
```

**Example 3: [M-01] Incorrect Balance Check in Validator Redelegation Process May Block Legit** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md`
```solidity
function closeRebalanceRequests(
    address stakingManager,
    address[] calldata validators
) external whenNotPaused nonReentrant onlyRole(MANAGER_ROLE) {
    // ...
    uint256 totalAmount = 0;
    for (uint256 i = 0; i < validators.length; ) {
        // ...
        totalAmount += request.amount;
        // ...
    }
    // Trigger redelegation through StakingManager if there's an amount to delegate
    if (totalAmount > 0) {
        IStakingManager(stakingManager).processValidatorRedelegation(totalAmount);
    }
}
```

**Example 4: [M-06] LP Redelegation Uses Inaccurate Internal Tracker Amount, Leading to Poten** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-lp-redelegation-uses-inaccurate-internal-tracker-amount-leading-to-potentia.md`
```go
fun redelegate_lp(pool: &StakePool, new_validator_address: String) {
        let denom = coin::metadata_to_denom(pool.metadata);
        let coin = Coin { denom, amount: pool.amount }; // <<< Uses pool.amount

        let msg = MsgBeginRedelegate {
            // ... other fields ...
            amount: vector[coin] // <<< Amount specified in the message
        };
        cosmos::stargate(&object::generate_signer_for_extending(&pool.ref), marshal(&msg));
    }
```

**Example 5: Misleading Error Messages and Comments in msgClaimRewards and performMsgClaimRew** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/misleading-error-messages-and-comments-in-msgclaimrewards-and-performmsgclaimrew.md`
```go
func performMsgClaimRewards(f *masterchefkeeper.Keeper, ctx sdk.Context, contractAddr sdk.AccAddress, msgClaimRewards *types.MsgClaimRewards) (*wasmbindingstypes.RequestResponse, error) {
	if msgClaimRewards == nil {
		return nil, wasmvmtypes.InvalidRequest{Err: "Invalid claim rewards parameter"}
	}

	msgServer := masterchefkeeper.NewMsgServerImpl(*f)
	_, err := sdk.AccAddressFromBech32(msgClaimRewards.Sender)
	if err != nil {
		return nil, errorsmod.Wrap(err, "invalid address")
	}

	msgMsgClaimRewards := &types.MsgClaimRewards{
		Sender:  msgClaimRewards.Sender,
		PoolIds: msgClaimRewards.PoolIds,
	}

	if err := msgMsgClaimRewards.ValidateBasic(); err != nil {
		return nil, errorsmod.Wrap(err, "failed validating msgMsgDelegate")
	}

	_, err = msgServer.ClaimRewards(sdk.WrapSDKContext(ctx), msgMsgClaimRewards) // Discard the response because it's empty
	if err != nil {
		return nil, errorsmod.Wrap(err, "elys redelegation msg")
	}

	resp := &wasmbindingstypes.RequestResponse{
		Code:   paramtypes.RES_OK,
		Result: "Redelegation succeed!",
	}

	return resp, nil
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation redelegation error logic allows exploitation through missing valid
func secureDelegationRedelegationError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 4
- **Affected Protocols**: Protocol, Cabal, MANTRA, Kinetiq, Cosmos Module
- **Validation Strength**: Moderate (2 auditors)

---

## 8. Delegation Unbonding Exploit

### Overview

Implementation flaw in delegation unbonding exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report describes an issue with two keys having the same value. These keys are used to retrieve data from the Cosmos store, and since they have the same value, they can corrupt each other when used in different parts of the codebase. This issue can be fixed by changing one of the keys to a u

### Vulnerability Description

#### Root Cause

Implementation flaw in delegation unbonding exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies delegation unbonding exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to delegation operations

### Vulnerable Pattern Examples

**Example 1: Key typo may allow store corruption** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/key-typo-may-allow-store-corruption.md`
```go
var (
	// Keys for store prefixes
	// Last* values are constant during a block.
	LastValidatorPowerKey = []byte{0x11} // prefix for each key to a validator index, for bonded validators
	LastTotalPowerKey     = []byte{0x12} // prefix for the total power

	ValidatorsKey             = []byte{0x21} // prefix for each key to a validator
	ValidatorsByConsAddrKey   = []byte{0x22} // prefix for each key to a validator index, by pubkey
	ValidatorsByPowerIndexKey = []byte{0x23} // prefix for each key to a validator index, sorted by power

	DelegationKey                    = []byte{0x31} // key for a delegation
	UnbondingDelegationKey           = []byte{0x32} // key for an unbonding-delegation
	UnbondingDelegationByValIndexKey = []byte{0x33} // prefix for each key for an unbonding-delegation, by validator operator
	RedelegationKey                  = []byte{0x34} // key for a redelegation
	RedelegationByValSrcIndexKey     = []byte{0x35} // prefix for each key for an redelegation, by source validator operator
	RedelegationByValDstIndexKey     = []byte{0x36} // prefix for each key for an redelegation, by destination validator operator
	PeriodDelegationKey              = []byte{0x37} // key for a period delegation

	UnbondingIDKey    = []byte{0x37} // key for the counter for the incrementing id for UnbondingOperations
	UnbondingIndexKey = []byte{0x38} // prefix for an index for looking up unbonding operations by their IDs
	UnbondingTypeKey  = []byte{0x39} // prefix for an index containing the type of unbonding operations

	UnbondingQueueKey    = []byte{0x41} // prefix for the timestamps in unbonding queue
	RedelegationQueueKey = []byte{0x42} // prefix for the timestamps in redelegations queue
	ValidatorQueueKey    = []byte{0x43} // prefix for the timestamps in validator queue

	HistoricalInfoKey   = []byte{0x50} // prefix for the historical info
	ValidatorUpdatesKey = []byte{0x61} // prefix for the end block validator updates key

	ParamsKey = []byte{0x51} // prefix for parameters for module x/staking

	DelegationByValIndexKey = []byte{0x71} // key for delegations by a validator
)
```

**Example 2: [M-08] Unbonding validator random selection can be predicted** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-unbonding-validator-random-selection-can-be-predicted.md`
```go
let mut iteration_index = 0;

while claimed.u128() > 0 {
    let mut rng = XorShiftRng::seed_from_u64(block_height + iteration_index);
    let random_index = rng.gen_range(0, deletable_delegations.len());
    // ...
}
```

**Example 3: Changes of the `UnbondingTime` are not accounted for** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-12-changes-of-the-unbondingtime-are-not-accounted-for.md`
```rust
pub fn on_validator_unstake(deps: DepsMut, msg: Reply) -> Result<Response, ContractError> {
    let attributes = &msg.result.unwrap().events[0].attributes;
    let mut fund = Coin::default();
    let mut payout_at = Timestamp::default();
    for attr in attributes {
        if attr.key == "amount" {
            fund = Coin::from_str(&attr.value).unwrap();
        } else if attr.key == "completion_time" {
            let completion_time = DateTime::parse_from_rfc3339(&attr.value).unwrap();
            let seconds = completion_time.timestamp() as u64;
            let nanos = completion_time.timestamp_subsec_nanos() as u64;
            payout_at = Timestamp::from_seconds(seconds);
            payout_at = payout_at.plus_nanos(nanos);
        }
    }
    UNSTAKING_QUEUE.push_back(deps.storage, &UnstakingTokens { fund, payout_at })?;

    Ok(Response::default())
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in delegation unbonding exploit logic allows exploitation through missing valida
func secureDelegationUnbondingExploit(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Cosmos SDK, Andromeda – Validator Staking ADO and Vesting ADO, Anchor
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Delegation Self Manipulation
grep -rn 'delegation|self|manipulation' --include='*.go' --include='*.sol'
# Delegation Dos Revert
grep -rn 'delegation|dos|revert' --include='*.go' --include='*.sol'
# Delegation State Inconsistency
grep -rn 'delegation|state|inconsistency' --include='*.go' --include='*.sol'
# Delegation To Inactive
grep -rn 'delegation|to|inactive' --include='*.go' --include='*.sol'
# Delegation Frontrunning
grep -rn 'delegation|frontrunning' --include='*.go' --include='*.sol'
# Delegation Reward Manipulation
grep -rn 'delegation|reward|manipulation' --include='*.go' --include='*.sol'
# Delegation Redelegation Error
grep -rn 'delegation|redelegation|error' --include='*.go' --include='*.sol'
# Delegation Unbonding Exploit
grep -rn 'delegation|unbonding|exploit' --include='*.go' --include='*.sol'
```

## Keywords

`accounted`, `accounting`, `accumulation`, `actually`, `address`, `adversary`, `after`, `allora`, `allow`, `allows`, `amount`, `appchain`, `array`, `assertion`, `balance`, `balances`, `block`, `blocking`, `boost`, `called`, `cannot`, `changes`, `check`, `checks`, `corruption`, `cosmos`, `decreased`, `delegated`, `delegatee`, `delegating`

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

`UnstakeEntry`, `_initValidatorScore`, `appchain`, `balanceOf`, `closeRebalanceRequests`, `cosmos`, `defi`, `delegation_redelegation_vulnerabilities`, `deposit`, `dos_revert`, `frontrunning`, `redelegation_error`, `reward_manipulation`, `safeTransferFrom`, `self_manipulation`, `service`, `staking`, `state_inconsistency`, `their`, `to_inactive`, `unbonding_exploit`, `users`, `withdraw`
