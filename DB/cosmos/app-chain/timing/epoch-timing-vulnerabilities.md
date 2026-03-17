---
protocol: generic
chain: cosmos
category: timing
vulnerability_type: epoch_timing_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: timing_logic

primitives:
  - epoch_transition
  - epoch_snapshot
  - cooldown_bypass
  - timestamp_boundary
  - unbonding_change
  - epoch_duration_break
  - expiration_bypass
  - block_time
  - race_condition

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - timing
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | timing_logic | epoch_timing_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AddBTCDelegationInclusionProof
  - BTCUndelegate
  - Indexers
  - _initializeValidatorStakeUpdate
  - _wasActiveAt
  - block.timestamp
  - block_time
  - calcAndCacheStakes
  - cooldown_bypass
  - epoch_duration_break
  - epoch_snapshot
  - epoch_transition
  - expiration_bypass
  - handlers
  - msg.sender
  - race_condition
  - that
  - timestamp_boundary
  - unbonding_change
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Timing Epoch Snapshot
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Future epoch cache manipulation via `calcAndCacheStakes` all | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| Historical reward loss due to `NodeId` reuse in `AvalancheL1 | `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md` | MEDIUM | Cyfrin |
| Immediate stake cache updates enable reward distribution wit | `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md` | HIGH | Cyfrin |
| Rewards distribution DoS due to uncached secondary asset cla | `reports/cosmos_cometbft_findings/rewards-distribution-dos-due-to-uncached-secondary-asset-classes.md` | MEDIUM | Cyfrin |

### Timing Cooldown Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Getting Max Staking Rewards Possible While Bypassing the Loc | `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md` | MEDIUM | Quantstamp |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [M-04] Disabling of cooldown during post-slash can be bypass | `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md` | MEDIUM | Pashov Audit Group |
| Lockup of vestings or completion time can be bypassed due to | `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md` | MEDIUM | Sherlock |
| OperationalStaking::_unstake Delegators can bypass 28 days u | `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md` | MEDIUM | Sherlock |
| Missing Balance Deduction in Unstaking Functions Allows Cont | `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md` | HIGH | Quantstamp |
| Missing Expiration Check when Adding to Existing Stake Allow | `reports/cosmos_cometbft_findings/missing-expiration-check-when-adding-to-existing-stake-allows-timelock-bypass.md` | MEDIUM | Quantstamp |

### Timing Timestamp Boundary
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| The EXPIRED judgment does not include the current block | `reports/cosmos_cometbft_findings/h-2-the-expired-judgment-does-not-include-the-current-block.md` | HIGH | Sherlock |
| Timestamp boundary condition causes reward dilution for acti | `reports/cosmos_cometbft_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md` | HIGH | Cyfrin |

### Timing Unbonding Change
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Changes of the `UnbondingTime` are not accounted for | `reports/cosmos_cometbft_findings/m-12-changes-of-the-unbondingtime-are-not-accounted-for.md` | MEDIUM | Sherlock |

### Timing Epoch Duration Break
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Changing the epoch duration will completely break the vault  | `reports/cosmos_cometbft_findings/m-5-changing-the-epoch-duration-will-completely-break-the-vault-and-the-slashers.md` | MEDIUM | Sherlock |

### Timing Expiration Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| If the Covenant signature does not pass , EXPIRED events it  | `reports/cosmos_cometbft_findings/h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md` | HIGH | Sherlock |
| Missing Expiration Check when Adding to Existing Stake Allow | `reports/cosmos_cometbft_findings/missing-expiration-check-when-adding-to-existing-stake-allows-timelock-bypass.md` | MEDIUM | Quantstamp |

### Timing Block Time
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DoS Can Close a Channel by Abusing Different Gas Limits Betw | `reports/cosmos_cometbft_findings/dos-can-close-a-channel-by-abusing-different-gas-limits-between-chains.md` | HIGH | Quantstamp |
| [M-04] Preventing balance updates by adding a new validator  | `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md` | MEDIUM | Pashov Audit Group |
| Btcstaking module allows `stakingTx` to be coinbase transact | `reports/cosmos_cometbft_findings/m-1-btcstaking-module-allows-stakingtx-to-be-coinbase-transaction-which-is-unsla.md` | MEDIUM | Sherlock |

### Timing Race Condition
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| BlobSidecars data availability race condition | `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md` | MEDIUM | Spearbit |
| Due Diligence into Farm managers | `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md` | HIGH | OtterSec |
| [EIGEN2-4] Missing constraint check for modification of look | `reports/cosmos_cometbft_findings/eigen2-4-missing-constraint-check-for-modification-of-lookahead-time-of-slashabl.md` | MEDIUM | Hexens |
| Exchange rate not updated properly | `reports/cosmos_cometbft_findings/exchange-rate-not-updated-properly.md` | MEDIUM | Halborn |
| Failure to enforce minimum oracle stake requirement | `reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md` | HIGH | TrailOfBits |
| Front-Running redeem Can Prevent Indexers From Receiving Rew | `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md` | HIGH | OpenZeppelin |
| [H-01] Permissionless `sendCurrentOperatorsKeys()` | `reports/cosmos_cometbft_findings/h-01-permissionless-sendcurrentoperatorskeys.md` | HIGH | Pashov Audit Group |
| [H-02] Edge from dishonest challenge edge tree can inherit t | `reports/cosmos_cometbft_findings/h-02-edge-from-dishonest-challenge-edge-tree-can-inherit-timer-from-honest-tree-.md` | HIGH | Code4rena |

---

# Epoch Timing Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Epoch Timing Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Timing Epoch Snapshot](#1-timing-epoch-snapshot)
2. [Timing Cooldown Bypass](#2-timing-cooldown-bypass)
3. [Timing Timestamp Boundary](#3-timing-timestamp-boundary)
4. [Timing Unbonding Change](#4-timing-unbonding-change)
5. [Timing Epoch Duration Break](#5-timing-epoch-duration-break)
6. [Timing Expiration Bypass](#6-timing-expiration-bypass)
7. [Timing Block Time](#7-timing-block-time)
8. [Timing Race Condition](#8-timing-race-condition)

---

## 1. Timing Epoch Snapshot

### Overview

Implementation flaw in timing epoch snapshot logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: The `AvalancheL1Middleware::calcAndCacheStakes` function in the Suzaku network has a bug where it does not check if the epoch provided is in the future. This allows attackers to manipulate reward calculations by locking in current stake values for future epochs. This can lead to inflated reward shar



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | timing_logic | epoch_timing_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `timing_logic`
- High-signal code keywords: `AddBTCDelegationInclusionProof`, `BTCUndelegate`, `Indexers`, `_initializeValidatorStakeUpdate`, `_wasActiveAt`, `block.timestamp`, `block_time`, `calcAndCacheStakes`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `allows.function -> did.function -> is.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in timing epoch snapshot logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing epoch snapshot in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: Future epoch cache manipulation via `calcAndCacheStakes` allows reward manipulat** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md`
```solidity
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No validation of epoch timing
    // ... rest of function caches values for any epoch, including future ones
}
```

**Example 2: Historical reward loss due to `NodeId` reuse in `AvalancheL1Middleware`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/historical-reward-loss-due-to-nodeid-reuse-in-avalanchel1middleware.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** The `AvalancheL1Middleware` contract is vulnerable to misattributing stake to a former operator (Operator A) if a new, colluding or coordinated operator (Operator B) intentionally re-registers a node using the *exact same `bytes32 nodeId`* that Operator A previously used. This scenario assumes Operator B is aware of Operator A's historical `nodeId` and that the underlying P-Chain NodeID (`P_X`, derived from the shared `bytes32 nodeId`) has become available for re-registration on
```

**Example 3: Immediate stake cache updates enable reward distribution without P-Chain confirm** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md`
```solidity
// In initializeValidatorStakeUpdate():
function _initializeValidatorStakeUpdate(address operator, bytes32 validationID, uint256 newStake) internal {
    uint48 currentEpoch = getCurrentEpoch();

    nodeStakeCache[currentEpoch + 1][validationID] = newStake;
    nodePendingUpdate[validationID] = true;

    // @audit P-Chain operation initiated but NOT confirmed
    balancerValidatorManager.initializeValidatorWeightUpdate(validationID, scaledWeight);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing epoch snapshot logic allows exploitation through missing validation, i
func secureTimingEpochSnapshot(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: Suzaku Core
- **Validation Strength**: Single auditor

---

## 2. Timing Cooldown Bypass

### Overview

Implementation flaw in timing cooldown bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 2, MEDIUM: 5.

> **Key Finding**: The client has marked a bug as "Fixed" and provided an explanation for the fix. The bug was related to the staking contract, which determines the multiplier a user gets based on staking amount and lockup period. However, the contract did not check if the lockup period had actually elapsed before all

### Vulnerability Description

#### Root Cause

Implementation flaw in timing cooldown bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing cooldown bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: Getting Max Staking Rewards Possible While Bypassing the Lockup Periods** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `b175349`.

![Image 42: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `228ae219c5478f375bed56376ffba8538ea2f09e`. The client provided the following explanation:

> The vulnerability was fixed by adding lock period validation checks across unstaking functions.

![
```

**Example 2: [H06] AUD lending market could affect the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
```
// Vulnerable pattern from Audius Contracts Audit:
In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would on
```

**Example 3: [M-04] Disabling of cooldown during post-slash can be bypassed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** Medium, as staker can bypass disabling of cooldown

**Likelihood:** Medium, during the post slash period

**Description**

When `StakedToken` is in the post-slashing state, the cooldown function is disabled, preventing the staker from activating it by setting `_stakersCooldowns[msg.sender] = block.timestamp`.

However, the staker can possibly bypass the disabling of the cooldown function by transferring to another account that has a valid cooldown timestamp.

That is be
```

**Example 4: Lockup of vestings or completion time can be bypassed due to missing check for s** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md`
```rust
pub struct Batch {
    /// The amount of tokens in the batch
    pub amount: Uint128,
    /// The amount of tokens that have been claimed.
    pub amount_claimed: Uint128,
    /// When the lockup ends.
    pub lockup_end: u64,
    /// How often releases occur.
    pub release_unit: u64,
    /// Specifies how much is to be released after each `release_unit`. If
    /// it is a percentage, it would be the percentage of the original amount.
    pub release_amount: WithdrawalType,
    /// The time at which the last claim took place in seconds.
    pub last_claimed_release_time: u64,
}
```

**Example 5: OperationalStaking::_unstake Delegators can bypass 28 days unstaking cooldown wh** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`
```
// Vulnerable pattern from Covalent:
Source: https://github.com/sherlock-audit/2023-11-covalent-judging/issues/78
```

**Variant: Timing Cooldown Bypass - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`

**Variant: Timing Cooldown Bypass in Sapien** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
> - `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing cooldown bypass logic allows exploitation through missing validation, 
func secureTimingCooldownBypass(ctx sdk.Context) error {
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
- **Affected Protocols**: Sapien - 2, Increment, Andromeda – Validator Staking ADO and Vesting ADO, Audius Contracts Audit, Covalent
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Timing Timestamp Boundary

### Overview

Implementation flaw in timing timestamp boundary logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: Issue H-2: The EXPIRED judgment does not include the current block, causing a potential panic and double reduction in TotalBondedSat for delegators. This is due to a bug in the GetStatus function, which does not include the current block in its judgment. The bug can be triggered by executing BTCUnde

### Vulnerability Description

#### Root Cause

Implementation flaw in timing timestamp boundary logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing timestamp boundary in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: The EXPIRED judgment does not include the current block** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-the-expired-judgment-does-not-include-the-current-block.md`
```go
func (ms msgServer) BTCUndelegate(goCtx context.Context, req *types.MsgBTCUndelegate) (*types.MsgBTCUndelegateResponse, error) {
	defer telemetry.ModuleMeasureSince(types.ModuleName, time.Now(), types.MetricsKeyBTCUndelegate)

	ctx := sdk.UnwrapSDKContext(goCtx)
	// basic stateless checks
	if err := req.ValidateBasic(); err != nil {
		return nil, status.Errorf(codes.InvalidArgument, "%v", err)
	}

	btcDel, bsParams, err := ms.getBTCDelWithParams(ctx, req.StakingTxHash)

	if err != nil {
		return nil, err
	}

	// ensure the BTC delegation with the given staking tx hash is active
	btcTip := ms.btclcKeeper.GetTipInfo(ctx)

->	btcDelStatus := btcDel.GetStatus(
		btcTip.Height,
		bsParams.CovenantQuorum,
	)

->	if btcDelStatus == types.BTCDelegationStatus_UNBONDED || btcDelStatus == types.BTCDelegationStatus_EXPIRED {
		return nil, types.ErrInvalidBTCUndelegateReq.Wrap("cannot unbond an unbonded BTC delegation")
	}
    ......
}
```

**Example 2: Timestamp boundary condition causes reward dilution for active operators** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md`
```solidity
function _wasActiveAt(uint48 enabledTime, uint48 disabledTime, uint48 timestamp) private pure returns (bool) {
    return enabledTime != 0 && enabledTime <= timestamp && (disabledTime == 0 || disabledTime >= timestamp); //@audit disabledTime >= timestamp means an operator is active at a timestamp when he was disabled
 }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing timestamp boundary logic allows exploitation through missing validatio
func secureTimingTimestampBoundary(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: Suzaku Core, Babylon chain launch (phase-2)
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Timing Unbonding Change

### Overview

Implementation flaw in timing unbonding change logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The `andromeda-validator-staking` contract allows the owner to stake and unstake tokens. However, if the `UnbondingTime` parameter is reduced while unstakings are already queued, it can result in a denial-of-service (DoS) situation where newer entries cannot be withdrawn until older entries expire. 

### Vulnerability Description

#### Root Cause

Implementation flaw in timing unbonding change logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing unbonding change in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: Changes of the `UnbondingTime` are not accounted for** [MEDIUM]
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
// Addresses: Implementation flaw in timing unbonding change logic allows exploitation through missing validation,
func secureTimingUnbondingChange(ctx sdk.Context) error {
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
- **Affected Protocols**: Andromeda – Validator Staking ADO and Vesting ADO
- **Validation Strength**: Single auditor

---

## 5. Timing Epoch Duration Break

### Overview

Implementation flaw in timing epoch duration break logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue with the vault and slashers in the Symbiotic Relay protocol. The epoch duration cannot be updated in these contracts, causing problems with staking and slashing mechanisms. This can lead to slashing being impossible or failing for a significant period of time. The 

### Vulnerability Description

#### Root Cause

Implementation flaw in timing epoch duration break logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing epoch duration break in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: Changing the epoch duration will completely break the vault and the slashers** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-changing-the-epoch-duration-will-completely-break-the-vault-and-the-slashers.md`
```
// Vulnerable pattern from Symbiotic Relay:
Source: https://github.com/sherlock-audit/2025-06-symbiotic-relay-judging/issues/410 

This issue has been acknowledged by the team but won't be fixed at this time.
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing epoch duration break logic allows exploitation through missing validat
func secureTimingEpochDurationBreak(ctx sdk.Context) error {
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
- **Affected Protocols**: Symbiotic Relay
- **Validation Strength**: Single auditor

---

## 6. Timing Expiration Bypass

### Overview

Implementation flaw in timing expiration bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: The bug report describes an issue where if the Covenant signature does not pass, EXPIRED events, it will still be executed. This causes a decrease in the `fp.TotalBondedSat` and can potentially lead to a negative balance in the system. The bug was found by LZ\_security and the root cause is that the

### Vulnerability Description

#### Root Cause

Implementation flaw in timing expiration bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing expiration bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: If the Covenant signature does not pass , EXPIRED events it will still be execut** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md`
```go
func (ms msgServer) AddBTCDelegationInclusionProof(
	goCtx context.Context,
	req *types.MsgAddBTCDelegationInclusionProof,
) (*types.MsgAddBTCDelegationInclusionProofResponse, error) {
    ......
	activeEvent := types.NewEventPowerDistUpdateWithBTCDel(
		&types.EventBTCDelegationStateUpdate{
			StakingTxHash: stakingTxHash.String(),
			NewState:      types.BTCDelegationStatus_ACTIVE,
		},
	)

	ms.addPowerDistUpdateEvent(ctx, timeInfo.TipHeight, activeEvent)

	// record event that the BTC delegation will become unbonded at EndHeight-w
	expiredEvent := types.NewEventPowerDistUpdateWithBTCDel(&types.EventBTCDelegationStateUpdate{
		StakingTxHash: req.StakingTxHash,
		NewState:      types.BTCDelegationStatus_EXPIRED,
	})

	// NOTE: we should have verified that EndHeight > btcTip.Height + min_unbonding_time
	ms.addPowerDistUpdateEvent(ctx, btcDel.EndHeight-params.UnbondingTimeBlocks, expiredEvent)
......
}
```

**Example 2: Missing Expiration Check when Adding to Existing Stake Allows Timelock Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-expiration-check-when-adding-to-existing-stake-allows-timelock-bypass.md`
```
// Vulnerable pattern from Sapien - 2:
**Update**
Marked as "Fixed" by the client. Addressed in: `ffda07756c53963c20a254c11c97f6809d08cfaf`.

**File(s) affected:**`SapienVault.sol`

**Description:** The `stake()` and `increaseAmount()` functions allow users to add tokens to stakes without validation that the initial stake's lockup period has not ended. This can allow for some stakes where the new `weightedStartTime + effectiveLockUpPeriod < block.timestamp` meaning the stake is immediately unlocked. This allows users to benefit from 
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing expiration bypass logic allows exploitation through missing validation
func secureTimingExpirationBypass(ctx sdk.Context) error {
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
- **Affected Protocols**: Sapien - 2, Babylon chain launch (phase-2)
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Timing Block Time

### Overview

Implementation flaw in timing block time logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: The client has acknowledged an important issue with the cross-chain protocol. The problem occurs when a packet times out instead of being executed, which can lead to a denial of service attack. This is because different chains have different gas limits, causing one chain to run out of gas while proc

### Vulnerability Description

#### Root Cause

Implementation flaw in timing block time logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing block time in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: DoS Can Close a Channel by Abusing Different Gas Limits Between Chains** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-can-close-a-channel-by-abusing-different-gas-limits-between-chains.md`
```
// Vulnerable pattern from Datachain - IBC:
**Update**
Marked as "Acknowledged" by the client. Addressed in: `af68fc1feac5a4964538a1f295425810895479dd`. The client provided the following explanation:

> This is indeed an important issue for the cross-chain protocol. However, it is difficut to address this within the TAO layer defined in the IBC, as the TAO layer does not support validation based on additional counterparty chain information. Therefore, we believe it is appropriate to resolve this issue in the App layer (i.e., the module co
```

**Example 2: [M-04] Preventing balance updates by adding a new validator in the current block** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md`
```go
if (validatorDetails.lastBalanceUpdateTimestamp >= node.currentSnapshotTimestamp) {
                revert ValidatorAlreadyProved();
            }
```

**Example 3: Btcstaking module allows `stakingTx` to be coinbase transaction which is unslash** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-btcstaking-module-allows-stakingtx-to-be-coinbase-transaction-which-is-unsla.md`
```
// Vulnerable pattern from Babylon chain launch (phase-2):
Source: https://github.com/sherlock-audit/2024-12-babylon-judging/issues/6
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing block time logic allows exploitation through missing validation, incor
func secureTimingBlockTime(ctx sdk.Context) error {
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
- **Affected Protocols**: Datachain - IBC, Karak-June, Babylon chain launch (phase-2)
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Timing Race Condition

### Overview

Implementation flaw in timing race condition logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 15 audit reports with severity distribution: HIGH: 6, MEDIUM: 9.

> **Key Finding**: This bug report describes a race condition that occurs when processing a block in the CometBFT system. Two event handlers, handleBeaconBlockFinalization() and handleFinalSidecarsReceived(), run in parallel and can cause a non-deterministic outcome when accessing the AvailabilityStore. This can lead 

### Vulnerability Description

#### Root Cause

Implementation flaw in timing race condition logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies timing race condition in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to timing operations

### Vulnerable Pattern Examples

**Example 1: BlobSidecars data availability race condition** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md`
```
// Vulnerable pattern from Berachain Beaconkit:
## Medium Risk Severity Report

**Context:** `beacon/blockchain/process.go#L74-L78`
```

**Example 2: Due Diligence into Farm managers** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md`
```go
// Unstake NFT twice
let gemworks_farm_authority_bump = 
    *ctx.bumps.get("gemworks_farm_authority").unwrap();
let gemworks_farm_treasury_bump = 
    *ctx.bumps.get("gemworks_farm_treasury").unwrap();
let gemworks_farmer_bump = 
    *ctx.bumps.get("gemworks_farmer").unwrap();

let unstake_ctx = CpiContext::new_with_signer(
    ctx.accounts.gemfarm_program.to_account_info().clone(),
    Unstake {
        ...
    },
    farmer_authority_signer_seeds,
);

unstake(unstake_ctx, ...)?;
  
let unstake_again_ctx = CpiContext::new_with_signer(
    ctx.accounts.gemfarm_program.to_account_info().clone(),
    Unstake {
        ...
    },
    farmer_authority_signer_seeds,
);

unstake(unstake_again_ctx, ...)?;
```

**Example 3: [EIGEN2-4] Missing constraint check for modification of lookahead time of slasha** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/eigen2-4-missing-constraint-check-for-modification-of-lookahead-time-of-slashabl.md`
```go
require(
    AllocationManager(address(allocationManager)).DEALLOCATION_DELAY() > lookAheadPeriod,
    LookAheadPeriodTooLong()
);
```

**Example 4: Exchange rate not updated properly** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/exchange-rate-not-updated-properly.md`
```
// Vulnerable pattern from Kakeru Contracts:
##### Description

The `execute_bond` function of the **basset\_inj\_hub** contract allows delegating to the validators a certain amount of staking, as well as to calculate the amount of binj/stinj tokens to be minted in exchange.

At some point in the function, the **binj** and **stinj** exchange rates are updated for future transactions, however, the **stinj** exchange rate is not updated correctly as the `update_stinj_exchange_rate`function call is only performed if the bond type is `BondType
```

**Example 5: Failure to enforce minimum oracle stake requirement** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md`
```rust
pub fn handle_payout(
    pre_prices: &[PrePrice<T::PriceValue, T::BlockNumber, T::AccountId>],
    price: T::PriceValue,
    asset_id: T::AssetId,
) {
    for answer in pre_prices {
        let accuracy: Percent;
        if answer.price < price {
            accuracy = PerThing::from_rational(answer.price, price);
        } else {
            let adjusted_number = price.saturating_sub(answer.price - price);
            accuracy = PerThing::from_rational(adjusted_number, price);
        }
        let min_accuracy = AssetsInfo::<T>::get(asset_id).threshold;
        if accuracy < min_accuracy {
            let slash_amount = T::SlashAmount::get();
            let try_slash = T::Currency::can_slash(&answer.who, slash_amount);
            if !try_slash {
                log::warn!("Failed to slash {:?}", answer.who);
            }
            T::Currency::slash(&answer.who, slash_amount);
            Self::deposit_event(Event::UserSlashed(
                answer.who.clone(),
                asset_id,
                slash_amount,
            ));
        }
    }
}
```

**Variant: Timing Race Condition - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md`
> - `reports/cosmos_cometbft_findings/failure-to-enforce-minimum-oracle-stake-requirement.md`
> - `reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in timing race condition logic allows exploitation through missing validation, i
func secureTimingRaceCondition(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 15 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 9
- **Affected Protocols**: Berachain Beaconkit, The Graph Timeline Aggregation Audit, Babylon chain launch (phase-2), Advanced Blockchain, Fusaka Upgrade
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Timing Epoch Snapshot
grep -rn 'timing|epoch|snapshot' --include='*.go' --include='*.sol'
# Timing Cooldown Bypass
grep -rn 'timing|cooldown|bypass' --include='*.go' --include='*.sol'
# Timing Timestamp Boundary
grep -rn 'timing|timestamp|boundary' --include='*.go' --include='*.sol'
# Timing Unbonding Change
grep -rn 'timing|unbonding|change' --include='*.go' --include='*.sol'
# Timing Epoch Duration Break
grep -rn 'timing|epoch|duration|break' --include='*.go' --include='*.sol'
# Timing Expiration Bypass
grep -rn 'timing|expiration|bypass' --include='*.go' --include='*.sol'
# Timing Block Time
grep -rn 'timing|block|time' --include='*.go' --include='*.sol'
# Timing Race Condition
grep -rn 'timing|race|condition' --include='*.go' --include='*.sol'
```

## Keywords

`abusing`, `accounted`, `active`, `adding`, `affect`, `allows`, `appchain`, `availability`, `balance`, `between`, `blobsidecars`, `block`, `blocks`, `boundary`, `break`, `btcstaking`, `bypass`, `bypassed`, `bypassing`, `cache`, `causes`, `chains`, `change`, `changes`, `changing`, `channel`, `check`, `close`, `coinbase`, `completely`

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

`AddBTCDelegationInclusionProof`, `BTCUndelegate`, `Indexers`, `_initializeValidatorStakeUpdate`, `_wasActiveAt`, `appchain`, `block.timestamp`, `block_time`, `calcAndCacheStakes`, `cooldown_bypass`, `cosmos`, `defi`, `epoch_duration_break`, `epoch_snapshot`, `epoch_timing_vulnerabilities`, `epoch_transition`, `expiration_bypass`, `handlers`, `msg.sender`, `race_condition`, `staking`, `that`, `timestamp_boundary`, `timing`, `unbonding_change`
