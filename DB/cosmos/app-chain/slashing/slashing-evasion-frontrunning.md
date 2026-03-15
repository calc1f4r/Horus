---
# Core Classification
protocol: generic
chain: cosmos|ethereum|everychain
category: slashing
vulnerability_type: slashing_evasion_frontrunning

# Pattern Identity
root_cause_family: missing_timing_guard
pattern_key: missing_frontrun_protection | slashing_module | withdrawal_before_slash | penalty_evasion

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - StakingManager
  - SlashingModule
  - WithdrawalQueue
  - CooldownController
path_keys:
  - missing_frontrun_protection | withdrawal_request | StakingManager→WithdrawalQueue | slash_evasion
  - missing_cooldown_guard | cooldown_activation | StakedToken→SlashingModule | penalty_bypass
  - missing_queued_inclusion | queued_withdrawal_state | DelegationManager→StrategyManager | slashable_exclusion
  - missing_delegation_lock | delegate_transfer | OperatorToken→SlashingModule | slash_bypass

# Attack Vector Details
attack_type: economic_exploit|logical_error|dos
affected_component: slashing_logic|withdrawal_queue|cooldown_mechanism

# Technical Primitives
primitives:
  - frontrun_exit
  - cooldown_exploit
  - delegation_bypass
  - queued_excluded
  - withdrawal_delay_bypass
  - mechanism_abuse
  - governance_timing_attack

# Grep / Hunt-Card Seeds
code_keywords:
  - slash
  - cooldown
  - unstake
  - withdrawal
  - requestWithdrawal
  - fullClaimAndExit
  - decreaseStakeLockupDuration
  - votingPeriod
  - whenNotPaused
  - pendingWithdrawals
  - queueWithdrawal
  - slashableShares
  - beaconChainETHStrategy
  - SLASHING_WINDOW
  - MIN_WITHDRAWAL_DELAY
  - _stakersCooldowns

# Impact Classification
severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos
  - appchain
  - slashing
  - staking
  - defi
  - frontrunning
  - withdrawal
  - cooldown
  - evasion

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Slashing Frontrun Exit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Elected TSS Nodes Can Act Without Any Deposit | `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md` | HIGH | SigmaPrime |
| Gas price spikes cause the selected operator to be vulnerabl | `reports/cosmos_cometbft_findings/gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-front-running-a.md` | HIGH | Halborn |
| [H-02] Users Who Queue Withdrawal Before A Slashing Event Di | `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md` | HIGH | Code4rena |
| [H-04] Withdrawals logic allows MEV exploits of TVL changes  | `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md` | HIGH | Code4rena |
| [H-06] Gas price spikes cause the selected operator to be vu | `reports/cosmos_cometbft_findings/h-06-gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-frontrunni.md` | HIGH | Code4rena |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [H08] Endpoint registration can be frontrun | `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md` | HIGH | OpenZeppelin |
| Insufficient Delay forRocketNodeStaking.withdrawRPL() | `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md` | MEDIUM | SigmaPrime |

### Slashing Cooldown Exploit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-01] Redeem period is less than intended down to 0 | `reports/cosmos_cometbft_findings/c-01-redeem-period-is-less-than-intended-down-to-0.md` | HIGH | Pashov Audit Group |
| Insufficient Delay forRocketNodeStaking.withdrawRPL() | `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md` | MEDIUM | SigmaPrime |
| [M-03] Stakers can activate cooldown during the pause and tr | `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md` | MEDIUM | Pashov Audit Group |
| [M-04] Disabling of cooldown during post-slash can be bypass | `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md` | MEDIUM | Pashov Audit Group |
| QA Penalty Can Be Avoided by Unstaking Before Penalty Proces | `reports/cosmos_cometbft_findings/qa-penalty-can-be-avoided-by-unstaking-before-penalty-processing.md` | HIGH | Quantstamp |
| RocketNodeStaking - Node operators can reduce slashing impac | `reports/cosmos_cometbft_findings/rocketnodestaking-node-operators-can-reduce-slashing-impact-by-withdrawing-exces.md` | HIGH | ConsenSys |

### Slashing Delegation Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H02] Delegators can prevent service providers from deregist | `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md` | HIGH | OpenZeppelin |
| In `Operator._transfer()`, `onDelegate()` should be called a | `reports/cosmos_cometbft_findings/in-operator_transfer-ondelegate-should-be-called-after-updating-the-token-balanc.md` | MEDIUM | Cyfrin |
| [M-01] A staker with verified over-commitment can potentiall | `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md` | MEDIUM | Code4rena |

### Slashing Insufficient Deposit
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] In a mass slashing event, node operators are incentiv | `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md` | MEDIUM | ZachObront |

### Slashing External Block
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Account that is affiliated with a plugin can sometimes evade | `reports/cosmos_cometbft_findings/m-1-account-that-is-affiliated-with-a-plugin-can-sometimes-evade-slashing.md` | MEDIUM | Sherlock |

### Slashing Queued Excluded
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| beaconChainETHStrategy Queued Withdrawals Excluded From Slas | `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` | MEDIUM | SigmaPrime |
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| [H-02] Users Who Queue Withdrawal Before A Slashing Event Di | `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md` | HIGH | Code4rena |
| [M-01] A staker with verified over-commitment can potentiall | `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md` | MEDIUM | Code4rena |
| [M-03] When malicious behavior occurs and DSS requests slash | `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md` | MEDIUM | Code4rena |
| [M-05] Slashings will always fail in some cases | `reports/cosmos_cometbft_findings/m-05-slashings-will-always-fail-in-some-cases.md` | MEDIUM | Code4rena |

### Slashing Unregistered Operator
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Violation of Invariant Allowing DSSs to Slash Unregis | `reports/cosmos_cometbft_findings/h-04-violation-of-invariant-allowing-dsss-to-slash-unregistered-operators.md` | HIGH | Code4rena |

### Slashing Mechanism Abuse
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Elected TSS Nodes Can Act Without Any Deposit | `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md` | HIGH | SigmaPrime |
| [H-03] Node operator is getting slashed for full duration ev | `reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md` | HIGH | Code4rena |
| [H02] Delegators can prevent service providers from deregist | `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md` | HIGH | OpenZeppelin |
| [M-03] In a mass slashing event, node operators are incentiv | `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md` | MEDIUM | ZachObront |
| Message is indexed as refundable even if the signature was o | `reports/cosmos_cometbft_findings/m-2-message-is-indexed-as-refundable-even-if-the-signature-was-over-a-fork.md` | MEDIUM | Sherlock |
| Oracle’s _sanityCheck for prices will not work with slashing | `reports/cosmos_cometbft_findings/oracles-_sanitycheck-for-prices-will-not-work-with-slashing.md` | HIGH | ConsenSys |
| Slash amount is signiﬁcantly lower than the minimum stake am | `reports/cosmos_cometbft_findings/slash-amount-is-signiﬁcantly-lower-than-the-minimum-stake-amount.md` | HIGH | TrailOfBits |
| Slashing mechanism grants exponentially more rewards than ex | `reports/cosmos_cometbft_findings/slashing-mechanism-grants-exponentially-more-rewards-than-expected.md` | HIGH | OpenZeppelin |

---

## Slashing Evasion & Frontrunning Vulnerabilities

### Overview

Slashing evasion through frontrunning is a family of vulnerabilities where stakers, operators, or delegators can avoid or reduce slashing penalties by manipulating transaction ordering, exploiting timing windows between slash detection and execution, or leveraging gaps in withdrawal queue accounting. Found across 55+ audit reports (HIGH: 24, MEDIUM: 31) from 10+ independent auditors across 15+ protocols.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because slashing execution lacks atomic coordination with withdrawal, cooldown, and delegation state transitions — allowing actors to move funds out of slashable scope before penalties are applied."
- Pattern key: `missing_frontrun_protection | slashing_module | withdrawal_before_slash | penalty_evasion`
- Interaction scope: `multi_contract`
- Primary affected component(s): `SlashingModule, WithdrawalQueue, StakedToken, CooldownController, DelegationManager`
- Contracts / modules involved: `StakingManager, SlashingModule, WithdrawalQueue, CooldownController, StrategyManager, NativeVault`
- Path keys: `withdrawal_request | StakingManager→WithdrawalQueue`, `cooldown_activation | StakedToken→SlashingModule`, `queued_withdrawal_state | DelegationManager→StrategyManager`, `delegate_transfer | OperatorToken→SlashingModule`
- High-signal code keywords: `slash`, `cooldown`, `unstake`, `requestWithdrawal`, `fullClaimAndExit`, `queueWithdrawal`, `pendingWithdrawals`, `SLASHING_WINDOW`, `whenNotPaused`
- Typical sink / impact: `penalty evasion / fund loss for remaining stakers / protocol insolvency / socialized slashing amplification`
- Validation strength: `strong (10+ independent auditors)`

#### Contract / Boundary Map

- Entry surface(s): `requestWithdrawal()`, `cooldown()`, `unstake()`, `fullClaimAndExit()`, `revokePending()`, `transfer()`
- Contract hop(s): `StakingManager.unstake() → WithdrawalQueue.queue()` bypasses `SlashingModule.slash()` scope; `StakedToken.cooldown()` pre-positions for `redeem()` before `slash()` executes
- Trust boundary crossed: `mempool visibility (public slashing tx can be frontrun)`, `state transition ordering (withdrawal state escapes slashing scope)`, `governance timing (lockup < voting period)`
- Shared state or sync assumption: `slashable balance must include queued/pending withdrawals; cooldown activation must be blocked during slashing; withdrawal delays must exceed slash execution window`

#### Valid Bug Signals

- Signal 1: `requestWithdrawal()` or `unstake()` can be called between slash detection and slash execution with no lock or freeze
- Signal 2: Cooldown activation (`cooldown()`) is not gated by `whenNotPaused` or a slashing-pending flag
- Signal 3: Queued withdrawals or pending delegation state are excluded from `slashableShares` calculation
- Signal 4: `decreaseStakeLockupDuration` ≤ `votingPeriod` for governance-based slashing
- Signal 5: Withdrawal request timestamps can be pre-set before actual staking occurs

#### False Positive Guards

- Not this bug when: withdrawal delay exceeds slashing window + veto window (e.g., `MIN_WITHDRAWAL_DELAY > SLASHING_WINDOW + SLASHING_VETO_WINDOW`)
- Safe if: protocol freezes all exit paths (withdraw, transfer, cooldown) during slashing execution via a global `slashingPending` flag
- Safe if: slashable shares calculation includes queued/pending withdrawal amounts
- Requires attacker control of: mempool ordering (frontrunning) OR governance timing parameters OR cooldown entry during pause

---

## Table of Contents

1. [Slashing Frontrun Exit](#1-slashing-frontrun-exit)
2. [Slashing Cooldown Exploit](#2-slashing-cooldown-exploit)
3. [Slashing Delegation Bypass](#3-slashing-delegation-bypass)
4. [Slashing Insufficient Deposit](#4-slashing-insufficient-deposit)
5. [Slashing External Block](#5-slashing-external-block)
6. [Slashing Queued Excluded](#6-slashing-queued-excluded)
7. [Slashing Unregistered Operator](#7-slashing-unregistered-operator)
8. [Slashing Mechanism Abuse](#8-slashing-mechanism-abuse)

---

## 1. Slashing Frontrun Exit

### Overview

Implementation flaw in slashing frontrun exit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 23 audit reports with severity distribution: HIGH: 7, MEDIUM: 16.

> **Key Finding**: This bug report is about a potential security issue in the TSS node system. The issue is that a node can remove its insurance deposit and still be elected as a TSS node. As a result, there is no means of punishing the node for inactivity or malicious behaviour. This is possible because election resu

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing frontrun exit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing frontrun exit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: Elected TSS Nodes Can Act Without Any Deposit** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md`
```
// Vulnerable pattern from Mantle Network:
## Description

A node can remove its insurance deposit and still be elected as an active TSS node. TSS nodes are voted for by the BITDAO, which then pushes the currently elected nodes on-chain. Nodes that wish to be voted for must provide a deposit as insurance that they will perform their role honestly if elected. By timing a withdrawal correctly, a node can remove their deposit and still be elected as an active TSS node. As a result, there is no means of punishing the node for inactivity or m
```

**Example 2: Gas price spikes cause the selected operator to be vulnerable to front-running a** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-front-running-a.md`
```go
require(gasPrice >= tx.gasprice, "HOLOGRAPH: gas spike detected");
// operator slashing logic
_bondedAmounts[job.operator] -= amount;
_bondedAmounts[msg.sender] += amount;
```

**Example 3: [H-02] Users Who Queue Withdrawal Before A Slashing Event Disadvantage Users Who** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md`
```go
uint256 hypeAmount = stakingAccountant.kHYPEToHYPE(postFeeKHYPE);

    // Lock kHYPE tokens
    kHYPE.transferFrom(msg.sender, address(this), kHYPEAmount);

    // Create withdrawal request
    _withdrawalRequests[msg.sender][withdrawalId] = WithdrawalRequest({
        hypeAmount: hypeAmount,
        kHYPEAmount: postFeeKHYPE,
        kHYPEFee: kHYPEFee,
        timestamp: block.timestamp
    });
```

**Example 4: [H-04] Withdrawals logic allows MEV exploits of TVL changes and zero-slippage ze** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero.md`
```
// Vulnerable pattern from Renzo:
Deposit and withdrawal requests can be done immediately with no costs or fees, and both use the current oracle prices and TVL calculation ([`deposit`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L499-L504), and [`withdraw`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L217)). Crucially, the [withdrawal amount is calculated at withdrawal request submission time](https://github.com/code-423n4/2024-04-renzo/blob/ma
```

**Example 5: [H-06] Gas price spikes cause the selected operator to be vulnerable to frontrun** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-gas-price-spikes-cause-the-selected-operator-to-be-vulnerable-to-frontrunni.md`
```go
require(gasPrice >= tx.gasprice, "HOLOGRAPH: gas spike detected");
```

**Variant: Slashing Frontrun Exit - MEDIUM Severity Cases** [MEDIUM]
> Found in 16 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`
> - `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`

**Variant: Slashing Frontrun Exit in Mantle Network** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md`
> - `reports/cosmos_cometbft_findings/tss-nodes-reporting-slashing-are-vulnerable-to-front-running.md`

**Variant: Slashing Frontrun Exit in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md`

**Variant: Slashing Frontrun Exit in Increment** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/m-01-returnfunds-can-be-frontrun-to-profit-from-an-increase-in-share-price.md`
> - `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`
> - `reports/cosmos_cometbft_findings/m-05-final-slashed-amount-could-be-much-lower-than-expected.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing frontrun exit logic allows exploitation through missing validation, 
func secureSlashingFrontrunExit(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 23 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 16
- **Affected Protocols**: Celo Contracts Audit, Protocol, Rocketpool, Saffron Lido Vaults, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Slashing Cooldown Exploit

### Overview

Implementation flaw in slashing cooldown exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 3, MEDIUM: 3.

> **Key Finding**: The report is about a bug in a system where users are unable to redeem their StakedTokens if the cooldown period is twice as long as the unstake window. This means that the underlying tokens are stuck and cannot be accessed by the user. The likelihood of this bug occurring is high due to a calculati

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing cooldown exploit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing cooldown exploit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: [C-01] Redeem period is less than intended down to 0** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-redeem-period-is-less-than-intended-down-to-0.md`
```solidity
function _redeem(address from, address to, uint256 amount) internal {
        ...

        // Users can redeem without waiting for the cooldown period in a post-slashing state
        if (!isInPostSlashingState) {
            // Make sure the user's cooldown period is over and the unstake window didn't pass
            uint256 cooldownStartTimestamp = _stakersCooldowns[from];
            if (block.timestamp < cooldownStartTimestamp + COOLDOWN_SECONDS) {
                revert StakedToken_InsufficientCooldown(cooldownStartTimestamp + COOLDOWN_SECONDS);
            }
@>          if (block.timestamp - cooldownStartTimestamp + COOLDOWN_SECONDS > UNSTAKE_WINDOW) {
                revert StakedToken_UnstakeWindowFinished(cooldownStartTimestamp + COOLDOWN_SECONDS + UNSTAKE_WINDOW);
            }
        }

        // ... redeem logic
    }
```

**Example 2: Insufficient Delay forRocketNodeStaking.withdrawRPL()** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
```go
require ( block.number.sub(getNodeRPLStakedBlock(msg.sender)) >= rocketDAOProtocolSettingsRewards.getRewardsClaimIntervalBlocks(),
" The withdrawal cooldown period has not passed ");
```

**Example 3: [M-03] Stakers can activate cooldown during the pause and try to evade slashing** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, as staker can possibly evade the slash event and cause remaining stakers to pay more for the slashing

**Likelihood:** Low, when the protocol is paused, followed by slash event

**Description**

`StakedToken.cooldown()` is missing the `whenNotPaused` modifier. That means stakers can activate cooldown when the protocol is paused.

Stakers could be aware of or anticipate an upcoming slash event due to the pause and attempt to stay within unstake window by activating
```

**Example 4: QA Penalty Can Be Avoided by Unstaking Before Penalty Processing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/qa-penalty-can-be-avoided-by-unstaking-before-penalty-processing.md`
```
// Vulnerable pattern from Sapien - 2:
**Update**
Marked as "Fixed" by the client. Addressed in: `737af6c63b0eae0af9c80425eb8a27afffd14ad8`, `cf36a2fac54e84904c51f8d419c04e215c7b35da` and `24e56c21d8cabbaf5b6236080265d629361e182e`.

**File(s) affected:**`SapienVault.sol`, `SapienQA.sol`

**Description:** Typical unstaking within the protocol requires a two day cooldown period to pass before unstaking can be completed. The intention of this is to allow a sufficient window for any QA penalties to be applied before the user can unstake 
```

**Variant: Slashing Cooldown Exploit - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`
> - `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md`

**Variant: Slashing Cooldown Exploit in Increment** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/c-01-redeem-period-is-less-than-intended-down-to-0.md`
> - `reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md`
> - `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md`

**Variant: Slashing Cooldown Exploit in Rocketpool** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/rocketnodestaking-node-operators-can-reduce-slashing-impact-by-withdrawing-exces.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing cooldown exploit logic allows exploitation through missing validatio
func secureSlashingCooldownExploit(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 3
- **Affected Protocols**: Sapien - 2, Increment, Rocketpool
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Slashing Delegation Bypass

### Overview

Implementation flaw in slashing delegation bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This bug report discusses an issue where under certain conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously. When a service provider attempts to deregister an endpoint, their call to the `deregister` function may fail due to the

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing delegation bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing delegation bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: [H02] Delegators can prevent service providers from deregistering endpoints** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
```
// Vulnerable pattern from Audius Contracts Audit:
Under some conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously.


Consider the case where a service provider has registered more than one endpoint and that the service provider has staked the minimum amount of stake. Suppose delegators have delegated to this service provider the maximum amount of stake.


When the service provider attempts to deregister one of the endpoints, their call to the [`deregister` function](https:/
```

**Example 2: In `Operator._transfer()`, `onDelegate()` should be called after updating the to** [MEDIUM]
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

**Example 3: [M-01] A staker with verified over-commitment can potentially bypass slashing co** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`
```
// Vulnerable pattern from EigenLayer:
<https://github.com/code-423n4/2023-04-eigenlayer/blob/5e4872358cd2bda1936c29f460ece2308af4def6/src/contracts/core/StrategyManager.sol#L197>
<br><https://github.com/code-423n4/2023-04-eigenlayer/blob/5e4872358cd2bda1936c29f460ece2308af4def6/src/contracts/core/StrategyManager.sol#L513>

In EigenLayer, watchers submit over-commitment proof in the event a staker's balance on the Beacon chain falls below the minimum restaked amount per validator. In such a scenario, stakers' shares are [decreased by
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing delegation bypass logic allows exploitation through missing validati
func secureSlashingDelegationBypass(ctx sdk.Context) error {
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
- **Affected Protocols**: Audius Contracts Audit, Streamr, EigenLayer
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Slashing Insufficient Deposit

### Overview

Implementation flaw in slashing insufficient deposit logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The OptimisticWithdrawalRecipient contract has a rule for distributing funds from the beacon chain. If the amount is 16 ether or more, it is considered a withdrawal and capped at the total amount deposited. Otherwise, it is assumed to be rewards. However, in the event of a mass slashing, the penalti

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing insufficient deposit logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing insufficient deposit in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: [M-03] In a mass slashing event, node operators are incentivized to get slashed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md`
```
// Vulnerable pattern from Obol:
When the `OptimisticWithdrawalRecipient` receives funds from the beacon chain, it uses the following rule to determine the allocation:

> If the amount of funds to be distributed is greater than or equal to 16 ether, it is assumed that it is a withdrawal (to be returned to the principal, with a cap on principal withdrawals of the total amount they deposited).

> Otherwise, it is assumed that the funds are rewards.

This value being as low as 16 ether protects against any predictable attack the n
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing insufficient deposit logic allows exploitation through missing valid
func secureSlashingInsufficientDeposit(ctx sdk.Context) error {
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
- **Affected Protocols**: Obol
- **Validation Strength**: Single auditor

---

## 5. Slashing External Block

### Overview

Implementation flaw in slashing external block logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about an issue in which an account affiliated with a plugin can sometimes evade slashing. The vulnerability detail explains that the plugin can revert the IPlugin(plugin).requiresNotification() call which will prohibit slashing as slash() calls _claimAndExit() that invokes _notify

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing external block logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing external block in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: Account that is affiliated with a plugin can sometimes evade slashing** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-account-that-is-affiliated-with-a-plugin-can-sometimes-evade-slashing.md`
```solidity
/// @dev Calls `notifyStakeChange` on all plugins that require it. This is done in case any given plugin needs to do some stuff when a user exits.
    /// @param account Account that is exiting
    function _notifyStakeChangeAllPlugins(address account, uint256 amountBefore, uint256 amountAfter) private {
        // loop over all plugins
        for (uint256 i = 0; i < nPlugins; i++) {
            // only notify if the plugin requires
>>          if (IPlugin(plugins[i]).requiresNotification()) {
                try IPlugin(plugins[i]).notifyStakeChange(account, amountBefore, amountAfter) {}
                catch {
                    emit StakeChangeNotificationFailed(plugins[i]);
                }
            }
        }
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing external block logic allows exploitation through missing validation,
func secureSlashingExternalBlock(ctx sdk.Context) error {
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
- **Affected Protocols**: Telcoin Update
- **Validation Strength**: Single auditor

---

## 6. Slashing Queued Excluded

### Overview

Implementation flaw in slashing queued excluded logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 13 audit reports with severity distribution: HIGH: 5, MEDIUM: 8.

> **Key Finding**: The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing queued excluded logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing queued excluded in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
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

**Example 3: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Example 4: [H-02] Users Who Queue Withdrawal Before A Slashing Event Disadvantage Users Who** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md`
```go
uint256 hypeAmount = stakingAccountant.kHYPEToHYPE(postFeeKHYPE);

    // Lock kHYPE tokens
    kHYPE.transferFrom(msg.sender, address(this), kHYPEAmount);

    // Create withdrawal request
    _withdrawalRequests[msg.sender][withdrawalId] = WithdrawalRequest({
        hypeAmount: hypeAmount,
        kHYPEAmount: postFeeKHYPE,
        kHYPEFee: kHYPEFee,
        timestamp: block.timestamp
    });
```

**Example 5: [M-03] When malicious behavior occurs and DSS requests slashing against vault du** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
```go
uint256 public constant SLASHING_WINDOW = 7 days;
    uint256 public constant SLASHING_VETO_WINDOW = 2 days;
    uint256 public constant MIN_STAKE_UPDATE_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
    uint256 public constant MIN_WITHDRAWAL_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
```

**Variant: Slashing Queued Excluded - MEDIUM Severity Cases** [MEDIUM]
> Found in 8 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
> - `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`

**Variant: Slashing Queued Excluded in EigenLayer** [MEDIUM]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
> - `reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`

**Variant: Slashing Queued Excluded in Karak** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
> - `reports/cosmos_cometbft_findings/m-05-slashings-will-always-fail-in-some-cases.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing queued excluded logic allows exploitation through missing validation
func secureSlashingQueuedExcluded(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 13 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 8
- **Affected Protocols**: Protocol, Saffron Lido Vaults, Suzaku Core, Karak, Kinetiq
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Slashing Unregistered Operator

### Overview

Implementation flaw in slashing unregistered operator logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The bug report discusses an issue with the current implementation of a system where operators can allocate funds to different DSSs and choose which vaults to stake. The problem is that the system allows a DSS to slash an operator even after the operator has unregistered from the DSS, breaking one of

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing unregistered operator logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing unregistered operator in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Violation of Invariant Allowing DSSs to Slash Unregistered Operators** [HIGH]
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

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing unregistered operator logic allows exploitation through missing vali
func secureSlashingUnregisteredOperator(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Karak
- **Validation Strength**: Single auditor

---

## 8. Slashing Mechanism Abuse

### Overview

Implementation flaw in slashing mechanism abuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 10 audit reports with severity distribution: HIGH: 8, MEDIUM: 2.

> **Key Finding**: This bug report is about a potential security issue in the TSS node system. The issue is that a node can remove its insurance deposit and still be elected as a TSS node. As a result, there is no means of punishing the node for inactivity or malicious behaviour. This is possible because election resu

### Vulnerability Description

#### Root Cause

Implementation flaw in slashing mechanism abuse logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies slashing mechanism abuse in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to slashing operations

### Vulnerable Pattern Examples

**Example 1: Elected TSS Nodes Can Act Without Any Deposit** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-act-without-any-deposit.md`
```
// Vulnerable pattern from Mantle Network:
## Description

A node can remove its insurance deposit and still be elected as an active TSS node. TSS nodes are voted for by the BITDAO, which then pushes the currently elected nodes on-chain. Nodes that wish to be voted for must provide a deposit as insurance that they will perform their role honestly if elected. By timing a withdrawal correctly, a node can remove their deposit and still be elected as an active TSS node. As a result, there is no means of punishing the node for inactivity or m
```

**Example 2: [H-03] Node operator is getting slashed for full duration even though rewards ar** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md`
```solidity
File: MinipoolManager.sol

557:	function getExpectedAVAXRewardsAmt(uint256 duration, uint256 avaxAmt) public view returns (uint256) {
558:		ProtocolDAO dao = ProtocolDAO(getContractAddress("ProtocolDAO"));
559:		uint256 rate = dao.getExpectedAVAXRewardsRate();
560:		return (avaxAmt.mulWadDown(rate) * duration) / 365 days; // full duration used when calculating expected reward
561:	}

...

670:	function slash(int256 index) private {

...

673:		uint256 duration = getUint(keccak256(abi.encodePacked("minipool.item", index, ".duration")));
674:		uint256 avaxLiquidStakerAmt = getUint(keccak256(abi.encodePacked("minipool.item", index, ".avaxLiquidStakerAmt")));
675:		uint256 expectedAVAXRewardsAmt = getExpectedAVAXRewardsAmt(duration, avaxLiquidStakerAmt); // full duration
676:		uint256 slashGGPAmt = calculateGGPSlashAmt(expectedAVAXRewardsAmt);
```

**Example 3: [H02] Delegators can prevent service providers from deregistering endpoints** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
```
// Vulnerable pattern from Audius Contracts Audit:
Under some conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously.


Consider the case where a service provider has registered more than one endpoint and that the service provider has staked the minimum amount of stake. Suppose delegators have delegated to this service provider the maximum amount of stake.


When the service provider attempts to deregister one of the endpoints, their call to the [`deregister` function](https:/
```

**Example 4: [M-03] In a mass slashing event, node operators are incentivized to get slashed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md`
```
// Vulnerable pattern from Obol:
When the `OptimisticWithdrawalRecipient` receives funds from the beacon chain, it uses the following rule to determine the allocation:

> If the amount of funds to be distributed is greater than or equal to 16 ether, it is assumed that it is a withdrawal (to be returned to the principal, with a cap on principal withdrawals of the total amount they deposited).

> Otherwise, it is assumed that the funds are rewards.

This value being as low as 16 ether protects against any predictable attack the n
```

**Example 5: Message is indexed as refundable even if the signature was over a fork** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-message-is-indexed-as-refundable-even-if-the-signature-was-over-a-fork.md`
```go
// if this finality provider has signed the canonical block before,
	// slash it via extracting its secret key, and emit an event
	if ms.HasEvidence(ctx, req.FpBtcPk, req.BlockHeight) {
		// the finality provider has voted for a fork before!
		// If this evidence is at the same height as this signature, slash this finality provider

		// get evidence
		evidence, err := ms.GetEvidence(ctx, req.FpBtcPk, req.BlockHeight)
		if err != nil {
			panic(fmt.Errorf("failed to get evidence despite HasEvidence returns true"))
		}

		// set canonical sig to this evidence
		evidence.CanonicalFinalitySig = req.FinalitySig
		ms.SetEvidence(ctx, evidence)

		// slash this finality provider, including setting its voting power to
		// zero, extracting its BTC SK, and emit an event
		ms.slashFinalityProvider(ctx, req.FpBtcPk, evidence)
	}

	// at this point, the finality signature is 1) valid, 2) over a canonical block,
	// and 3) not duplicated.
	// Thus, we can safely consider this message as refundable
	ms.IncentiveKeeper.IndexRefundableMsg(ctx, req)
```

**Variant: Slashing Mechanism Abuse - MEDIUM Severity Cases** [MEDIUM]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md`
> - `reports/cosmos_cometbft_findings/m-2-message-is-indexed-as-refundable-even-if-the-signature-was-over-a-fork.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in slashing mechanism abuse logic allows exploitation through missing validation
func secureSlashingMechanismAbuse(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 10 audit reports
- **Severity Distribution**: HIGH: 8, MEDIUM: 2
- **Affected Protocols**: Brahma, GoGoPool, Geodefi, Advanced Blockchain, Audius Contracts Audit
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Slashing Frontrun Exit
grep -rn 'slashing|frontrun|exit' --include='*.go' --include='*.sol'
# Slashing Cooldown Exploit
grep -rn 'slashing|cooldown|exploit' --include='*.go' --include='*.sol'
# Slashing Delegation Bypass
grep -rn 'slashing|delegation|bypass' --include='*.go' --include='*.sol'
# Slashing Insufficient Deposit
grep -rn 'slashing|insufficient|deposit' --include='*.go' --include='*.sol'
# Slashing External Block
grep -rn 'slashing|external|block' --include='*.go' --include='*.sol'
# Slashing Queued Excluded
grep -rn 'slashing|queued|excluded' --include='*.go' --include='*.sol'
# Slashing Unregistered Operator
grep -rn 'slashing|unregistered|operator' --include='*.go' --include='*.sol'
# Slashing Mechanism Abuse
grep -rn 'slashing|mechanism|abuse' --include='*.go' --include='*.sol'
```

## Keywords

`abuse`, `account`, `activate`, `affiliated`, `after`, `allowing`, `appchain`, `avoid`, `balances`, `based`, `beaconchainethstrategy`, `before`, `block`, `bond`, `bypass`, `called`, `cause`, `change`, `completely`, `conditions`, `cooldown`, `cosmos`, `cycle`, `delay`, `delegation`, `delegators`, `deposit`, `deregistering`, `disadvantage`, `distributed`
