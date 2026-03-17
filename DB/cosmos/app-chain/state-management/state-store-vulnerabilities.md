---
protocol: generic
chain: cosmos
category: state_management
vulnerability_type: state_store_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: state_management_logic

primitives:
  - store_error
  - iterator_error
  - pruning_error
  - snapshot_error
  - migration_error

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - state_management
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | state_management_logic | state_store_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _transferToSlashStore
  - balanceOf
  - iterator_error
  - migration_error
  - pruning_error
  - snapshot_error
  - store_error
  - validateIterator
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### State Store Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Allow List Entries Can Be Added and Removed by Any State All | `reports/cosmos_cometbft_findings/allow-list-entries-can-be-added-and-removed-by-any-state-allower.md` | HIGH | Quantstamp |
| BlobSidecars data availability race condition | `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md` | MEDIUM | Spearbit |
| DoS on stake accounting functions by bloating `operatorNodes | `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md` | MEDIUM | Cyfrin |
| [H-03] A `DoS` on snapshots due to a rounding error in calcu | `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md` | HIGH | Code4rena |
| Lack Of Signature Verification | `reports/cosmos_cometbft_findings/lack-of-signature-verification.md` | HIGH | OtterSec |
| [M-01] `setBeforeSendHook` can never delete an existing stor | `reports/cosmos_cometbft_findings/m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md` | MEDIUM | Code4rena |
| [M-03] Inconsistent State Restoration in `cancelWithdrawal`  | `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md` | MEDIUM | Code4rena |
| [M-03] `xfeemarket` module is not wired up, resulting in non | `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md` | MEDIUM | Code4rena |

### State Iterator Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Evasion Of Validation Check On Early Stop | `reports/cosmos_cometbft_findings/evasion-of-validation-check-on-early-stop.md` | HIGH | OtterSec |

### State Snapshot Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] A `DoS` on snapshots due to a rounding error in calcu | `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md` | HIGH | Code4rena |
| [H-03] `ExecuteRequest`’s are not properly removed from the  | `reports/cosmos_cometbft_findings/h-03-executerequests-are-not-properly-removed-from-the-context-queue.md` | HIGH | Code4rena |
| [M-10] Unsafe casting from `uint256` to `uint128` in Rewards | `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md` | MEDIUM | Code4rena |

### State Migration Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Transactions can occur during the upgrade process | `reports/cosmos_cometbft_findings/transactions-can-occur-during-the-upgrade-process.md` | MEDIUM | TrailOfBits |

---

# State Store Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for State Store Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [State Store Error](#1-state-store-error)
2. [State Iterator Error](#2-state-iterator-error)
3. [State Snapshot Error](#3-state-snapshot-error)
4. [State Migration Error](#4-state-migration-error)

---

## 1. State Store Error

### Overview

Implementation flaw in state store error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 11 audit reports with severity distribution: HIGH: 3, MEDIUM: 8.

> **Key Finding**: The client has marked a bug as "Fixed" and provided an explanation. The issue was related to the `AddToAllowlistEntry` and `RemoveFromAllowlistEntry` instructions not properly validating the `allower` signer value. This allowed a malicious user to whitelist themselves for any stake pool by creating 



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | state_management_logic | state_store_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `state_management_logic`
- High-signal code keywords: `_transferToSlashStore`, `balanceOf`, `iterator_error`, `migration_error`, `pruning_error`, `snapshot_error`, `store_error`, `validateIterator`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
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

Implementation flaw in state store error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies state store error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to state operations

### Vulnerable Pattern Examples

**Example 1: Allow List Entries Can Be Added and Removed by Any State Allower** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/allow-list-entries-can-be-added-and-removed-by-any-state-allower.md`
```go
address = state.allower @ ErrorCode::OnlyAllower
```

**Example 2: BlobSidecars data availability race condition** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md`
```
// Vulnerable pattern from Berachain Beaconkit:
## Medium Risk Severity Report

**Context:** `beacon/blockchain/process.go#L74-L78`
```

**Example 3: DoS on stake accounting functions by bloating `operatorNodesArray` with irremova** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```go
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 4: [H-03] A `DoS` on snapshots due to a rounding error in calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md`
```solidity
function _transferToSlashStore(address nodeOwner) internal {
        ...

430     uint256 slashedAssets = node.totalRestakedETH - convertToAssets(balanceOf(nodeOwner));
        ...
```

**Example 5: Lack Of Signature Verification** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-signature-verification.md`
```go
// Code snippet from the context
func FindSuperMajorityVoteExtension(ctx context.Context, currentHeight int64, extCommit abci.ExtendedCommitInfo, valStore baseapp.ValidatorStore, chainID string) (types.VoteExtension, error) {
    // Check if the max voting power is greater than 2/3 of the total voting power
    if requiredVP := ((totalVP * 2) / 3) + 1; maxVotingPower < requiredVP {
        return types.VoteExtension{}, fmt.Errorf("%d < %d: %w", maxVotingPower, requiredVP, types.ErrInsufficientVotingPowerVE)
    }

    var voteExt types.VoteExtension
    err := json.Unmarshal(highestVoteExtensionBz, &voteExt)
    if err != nil {
        return types.VoteExtension{}, err
    }

    // Verify the super majority VE has valid values
    if (voteExt.EthBlockHeight == 0) || (voteExt.EthBlockHash == common.Hash{}) {
        return types.VoteExtension{}, fmt.Errorf("super majority VE is invalid")
    }
    return voteExt, nil
}
```

**Variant: State Store Error - MEDIUM Severity Cases** [MEDIUM]
> Found in 8 reports:
> - `reports/cosmos_cometbft_findings/blobsidecars-data-availability-race-condition.md`
> - `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
> - `reports/cosmos_cometbft_findings/m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in state store error logic allows exploitation through missing validation, incor
func secureStateStoreError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 11 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 8
- **Affected Protocols**: Ditto, Ethos Cosmos, Berachain Beaconkit, Liquid Collective - Solana, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 2. State Iterator Error

### Overview

Implementation flaw in state iterator error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This bug report discusses a vulnerability in the early stopping mechanism of the store::validateIterator function. This mechanism stops the iteration loop when encountering a specific key, but it does not confirm if all expected keys have been iterated. This can lead to a validation failure, as seen

### Vulnerability Description

#### Root Cause

Implementation flaw in state iterator error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies state iterator error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to state operations

### Vulnerable Pattern Examples

**Example 1: Evasion Of Validation Check On Early Stop** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/evasion-of-validation-check-on-early-stop.md`
```go
func (s *Store) validateIterator(index int, tracker iterationTracker) bool {
    [...]
    for ; mergeIterator.Valid(); mergeIterator.Next() {
        [...]
        // remove from expected keys
        foundKeys += 1
        // delete(expectedKeys, string(key))
        // if our iterator key was the early stop, then we can break
        if bytes.Equal(key, iterationTracker.earlyStopKey) {
            returnChan <- true
            return
        }
    }
    [...]
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in state iterator error logic allows exploitation through missing validation, in
func secureStateIteratorError(ctx sdk.Context) error {
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
- **Affected Protocols**: Sei OCC
- **Validation Strength**: Single auditor

---

## 3. State Snapshot Error

### Overview

Implementation flaw in state snapshot error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This bug report discusses a potential issue with creating a snapshot due to a rounding error in the calculations. The report includes a proof of concept which demonstrates how the error can occur and provides a recommended mitigation step to fix the issue. The report also includes comments from the 

### Vulnerability Description

#### Root Cause

Implementation flaw in state snapshot error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies state snapshot error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to state operations

### Vulnerable Pattern Examples

**Example 1: [H-03] A `DoS` on snapshots due to a rounding error in calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md`
```solidity
function _transferToSlashStore(address nodeOwner) internal {
        ...

430     uint256 slashedAssets = node.totalRestakedETH - convertToAssets(balanceOf(nodeOwner));
        ...
```

**Example 2: [H-03] `ExecuteRequest`’s are not properly removed from the context queue** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-executerequests-are-not-properly-removed-from-the-context-queue.md`
```go
287: messages := ctx.Value(types.CONTEXT_KEY_EXECUTE_REQUESTS).(*[]types.ExecuteRequest)
288: *messages = append(*messages, types.ExecuteRequest{
289: 	Caller: caller,
290: 	Msg:    sdkMsg,
291:
292: 	AllowFailure: executeCosmosArguments.Options.AllowFailure,
293: 	CallbackId:   executeCosmosArguments.Options.CallbackId,
294: })
```

**Example 3: [M-10] Unsafe casting from `uint256` to `uint128` in RewardsManager** [MEDIUM]
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
// Addresses: Implementation flaw in state snapshot error logic allows exploitation through missing validation, in
func secureStateSnapshotError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: Karak, Ajna Protocol, Initia
- **Validation Strength**: Single auditor

---

## 4. State Migration Error

### Overview

Implementation flaw in state migration error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a low difficulty error found in the NMR_monorepo/scripts/test/migrationProcedure.js file. The problem is that the current process for upgrading does not take into account transactions that could occur during an upgrade, which could lead to data loss and an invalid system sta

### Vulnerability Description

#### Root Cause

Implementation flaw in state migration error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies state migration error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to state operations

### Vulnerable Pattern Examples

**Example 1: Transactions can occur during the upgrade process** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/transactions-can-occur-during-the-upgrade-process.md`
```
// Vulnerable pattern from Numerai:
## Error Reporting

**Type:** Error Reporting  
**Target:** NMR_monorepo/scripts/test/migrationProcedure.js  

**Difficulty:** Low
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in state migration error logic allows exploitation through missing validation, i
func secureStateMigrationError(ctx sdk.Context) error {
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
- **Affected Protocols**: Numerai
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# State Store Error
grep -rn 'state|store|error' --include='*.go' --include='*.sol'
# State Iterator Error
grep -rn 'state|iterator|error' --include='*.go' --include='*.sol'
# State Snapshot Error
grep -rn 'state|snapshot|error' --include='*.go' --include='*.sol'
# State Migration Error
grep -rn 'state|migration|error' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `added`, `allow`, `allower`, `appchain`, `availability`, `bloating`, `blobsidecars`, `calculations`, `casting`, `check`, `condition`, `context`, `cosmos`, `data`, `during`, `early`, `entries`, `error`, `evasion`, `from`, `functions`, `irremovable`, `iterator`, `list`, `migration`, `nodes`, `occur`, `process`, `properly`

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

`_transferToSlashStore`, `appchain`, `balanceOf`, `cosmos`, `defi`, `iterator_error`, `migration_error`, `pruning_error`, `snapshot_error`, `staking`, `state_management`, `state_store_vulnerabilities`, `store_error`, `validateIterator`
