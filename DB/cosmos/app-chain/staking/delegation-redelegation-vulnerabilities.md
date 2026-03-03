---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: delegation_redelegation_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - self_delegation_manipulation
  - delegation_dos
  - undelegation_bypass
  - redelegation_tracking
  - delegation_reward_theft
  - delegation_state_inconsistency
  - delegation_to_inactive
  - delegation_frontrunning

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - delegation
  - redelegate
  - undelegate
  - self_delegation
  - delegator
  - delegate
  - bonding
  - unbonding
  
language: go
version: all
---

## References
- [denial-of-slashing.md](../../../../reports/cosmos_cometbft_findings/denial-of-slashing.md)
- [dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md](../../../../reports/cosmos_cometbft_findings/dpos-is-vulnerable-to-signiﬁcant-centralization-risk.md)
- [h-2-the-expired-judgment-does-not-include-the-current-block.md](../../../../reports/cosmos_cometbft_findings/h-2-the-expired-judgment-does-not-include-the-current-block.md)
- [h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md](../../../../reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md)
- [h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md](../../../../reports/cosmos_cometbft_findings/h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md)
- [h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md](../../../../reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md)
- [h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md](../../../../reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md)
- [linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md](../../../../reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md)
- [mismanagement-of-delegator-funds.md](../../../../reports/cosmos_cometbft_findings/mismanagement-of-delegator-funds.md)
- [rounding-errors-after-slashing-addressed.md](../../../../reports/cosmos_cometbft_findings/rounding-errors-after-slashing-addressed.md)
- [h11-a-service-provider-can-prevent-their-delegators-from-undelegating-their-stak.md](../../../../reports/cosmos_cometbft_findings/h11-a-service-provider-can-prevent-their-delegators-from-undelegating-their-stak.md)
- [the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md](../../../../reports/cosmos_cometbft_findings/the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md)
- [delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md](../../../../reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md)
- [delegators-can-redelegate-stakes-to-jailed-delegatee.md](../../../../reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md)
- [iterations-over-slashes-addressed.md](../../../../reports/cosmos_cometbft_findings/iterations-over-slashes-addressed.md)
- [m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md](../../../../reports/cosmos_cometbft_findings/m-01-incorrect-balance-check-in-validator-redelegation-process-may-block-legitim.md)
- [m-03-unable-to-check-state-if-proposalid-0.md](../../../../reports/cosmos_cometbft_findings/m-03-unable-to-check-state-if-proposalid-0.md)
- [m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md](../../../../reports/cosmos_cometbft_findings/m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md)
- [m-1-delegated-state-is-not-removed-after-it-reaches-zero-potentially-leading-to-.md](../../../../reports/cosmos_cometbft_findings/m-1-delegated-state-is-not-removed-after-it-reaches-zero-potentially-leading-to-.md)
- [m-6-delegate-can-keep-can-keep-delegatee-trapped-indefinitely.md](../../../../reports/cosmos_cometbft_findings/m-6-delegate-can-keep-can-keep-delegatee-trapped-indefinitely.md)

## Vulnerability Title

**Delegation and Redelegation Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 35 audit reports (12 HIGH, 23 MEDIUM severity) across 25 protocols by 12 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Delegation Dos

**Frequency**: 21/35 reports | **Severity**: MEDIUM | **Validation**: Strong (8 auditors)
**Protocols affected**: Allora, Elixir Protocol, MilkyWay, Upgrade, Cabal

The reported bug states that there is an issue with the Delegated Boost feature in the BoostController contract. This feature allows users to delegate their veRAAC tokens to another address for a set amount of time. However, the bug allows users to exploit the system by delegating a large amount and

**Example 1.1** [MEDIUM] — Core Contracts
Source: `delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md`
```solidity
// ❌ VULNERABLE: Delegation Dos
This sets `UserBoost` with `amount` and an `expiry`, effectively guaranteeing that “X” units of veRAAC are delegated for that duration.
2. **No Ongoing Balance Check**\
   Once set, the **BoostController** never re‑checks whether the user still has that many veRAAC tokens locked in veRAACToken. The contract only checks the user’s balance at the moment of delegation (via `if (userBalance < amount) revert InsufficientVeBalance()`).
3. **User Reduces or Withdraws veRAAC**\
   Right after delegating, the user calls:
```

**Example 1.2** [HIGH] — Ethos EVM
Source: `denial-of-slashing.md`
```solidity
// ❌ VULNERABLE: Delegation Dos
function verifyDoubleSigning(
    address operator,
    DoubleSigningEvidence memory e
) external {
    [...]
    for (uint256 i = 0; i < delegatedValidators.length; i++) {
        [...]
        if (EthosAVSUtils.compareStrings(delegatedValidators[i].validatorPubkey,
                                          e.validatorPubkey) &&
            isDelegationSlashable(delegatedValidators[i].endTimestamp))
        {
            timestampValid = true;
            stake = EthosAVSUtils.maxUint96(stake, delegatedValidators[i].stake);
        }
    }
    [...]
}
```

#### Pattern 2: Self Delegation Manipulation

**Frequency**: 9/35 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Streamr, Covalent, FrankenDAO, Templedao, Cosmos LSM

This bug report is about a vulnerability in the Audius Protocol in which a service provider can maliciously or unintentionally prevent their delegators from undelegating their stake. This is done by the service provider decreasing their stake by an amount that is equal to or less than the minimum am

**Example 2.1** [MEDIUM] — Streamr
Source: `in-operator_transfer-ondelegate-should-be-called-after-updating-the-token-balanc.md`
```solidity
// ❌ VULNERABLE: Self Delegation Manipulation
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

**Example 2.2** [MEDIUM] — Andromeda – Validator Staking ADO and Vesting ADO
Source: `m-15-batch-creation-will-break-if-vestings-are-opened-to-recipients.md`
```solidity
// ❌ VULNERABLE: Self Delegation Manipulation
As per my communication with the team, the only change that will occur is that the restriction for the `owner` in the claiming and delegation functions will be replaced with a restriction for the `recipient`. For the following reason, it will be impossible to create vestings with a direct delegation. 

When a vesting gets created, it can only be done by the owner due to the following [check](https://github.com/sherlock-audit/2024-05-andromeda-ado/blob/bbbf73e5d1e4092ab42ce1f827e33759308d3786/andromeda-core/contracts/finance/andromeda-vesting/src/contract.rs#L126-L129)
```

#### Pattern 3: Redelegation Tracking

**Frequency**: 2/35 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Cabal, Protocol

The report describes a bug in the `krp-staking-contracts/basset_sei_validators_registry` contract. When the `remove_validator` function is executed and the redelegation is not possible, the validator is removed from storage but there is no proper tracking of pending redelegations. This can cause pro

**Example 3.1** [MEDIUM] — Protocol
Source: `inadequate-tracking-of-pending-redelegations.md`
```solidity
// ❌ VULNERABLE: Redelegation Tracking
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

**Example 3.2** [MEDIUM] — Cabal
Source: `m-06-lp-redelegation-uses-inaccurate-internal-tracker-amount-leading-to-potentia.md`
```solidity
// ❌ VULNERABLE: Redelegation Tracking
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

#### Pattern 4: Delegation To Inactive

**Frequency**: 2/35 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Kinetiq_2025-02-26, Persistence

The `StakingManager` contract in the HYPE staking system has a bug that could potentially harm stakers. When users stake their HYPE tokens, the funds are distributed to a validator through a function called `_distributeStake()`. However, this function does not check if the validator is still active 

**Example 4.1** [MEDIUM] — Kinetiq_2025-02-26
Source: `m-04-new-stakes-delegated-even-when-validator-is-inactive.md`
```solidity
// ❌ VULNERABLE: Delegation To Inactive
if (amount > 0) {
            address delegateTo = validatorManager.getDelegation(address(this));
            require(delegateTo != address(0), "No delegation set");

            // Send tokens to delegation
            l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);

            emit Delegate(delegateTo, amount);
        }
```

#### Pattern 5: Delegation State Inconsistency

**Frequency**: 1/35 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Allora

Issue M-10 is a bug in the Allora Network's implementation of prepForZeroHeightGenesis, which is used to export the state of the network at a specific height. The current implementation is missing several key steps that are present in the reference implementation, potentially leading to inconsistent


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 12 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 35
- HIGH severity: 12 (34%)
- MEDIUM severity: 23 (65%)
- Unique protocols affected: 25
- Independent audit firms: 12
- Patterns with 3+ auditor validation (Strong): 2

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> `delegation`, `redelegate`, `undelegate`, `self-delegation`, `delegator`, `delegate`, `bonding`, `unbonding`, `redelegation-tracking`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
