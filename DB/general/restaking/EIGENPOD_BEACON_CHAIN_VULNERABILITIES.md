---
# Core Classification (Required)
protocol: eigenlayer
chain: ethereum
category: restaking
vulnerability_type: eigenpod_beacon_chain_verification

# Attack Vector Details (Required)
attack_type: proof_forgery|state_manipulation|upgrade_breakage
affected_component: eigenpod|beacon_chain_proofs|merkle_verification|validator_status

# Technical Primitives (Required)
primitives:
  - beacon_state_root
  - merkle_proof
  - withdrawal_proof
  - validator_fields
  - balance_container
  - historical_summaries
  - ssz_container
  - tree_height
  - withdrawal_credentials
  - stakedButUnverifiedNativeETH
  - verifyAndProcessWithdrawals
  - verifyWithdrawalCredentials
  - verifyBalanceUpdate

# Impact Classification (Required)
severity: critical|high|medium
impact: fund_loss|proof_forgery|dos|upgrade_breakage
exploitability: 0.6
financial_impact: critical

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - beacon_chain
  - consensus_layer
  - merkle_proof
  - ethereum_upgrade
  - deneb
  - electra
  - fulu

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Proof Forgery / Missing Validation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Withdrawal Proofs Forged (Missing Index Check) | `reports/eigenlayer_findings/eig-10-withdrawal-proofs-can-be-forged-due-to-missing-index-bit-size-check.md` | CRITICAL | Hexens |
| Slot/Block Proofs Not Required | `reports/eigenlayer_findings/h-01-slot-and-block-number-proofs-not-required-for-verification-of-withdrawal-mu.md` | HIGH | Code4rena |
| EigenPods Restake Without Proving | `reports/eigenlayer_findings/eig-14-m1-eigenpods-can-restake-and-withdraw-without-proving-and-burning-shares.md` | CRITICAL | Hexens |

### Beacon State Root Upgrade Breakage
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Proofs Break After Electra Upgrade | `reports/eigenlayer_findings/proofs-based-on-beaconstateroot-break-after-electra-upgrade.md` | HIGH | SigmaPrime |
| Withdrawal Verification Breaks After Deneb | `reports/eigenlayer_findings/verifying-beacon-chain-withdrawals-break-after-deneb.md` | HIGH | SigmaPrime |
| Compounding Credentials Not Supported Post-Electra | `reports/eigenlayer_findings/lack-of-support-for-compounding-withdrawal-credentials-after-electra-upgrade.md` | MEDIUM | SigmaPrime |
| Validator Status Wrong After Electra | `reports/eigenlayer_findings/validator-status-incorrectly-set-to-withdrawn-after-electra-upgrade.md` | MEDIUM | SigmaPrime |
| Nimbus Stale Metadata After Fulu Fork | `reports/eigenlayer_findings/m-2-nimbus-may-use-stale-metadata-information-after-fulu-fork-transition.md` | MEDIUM | Sherlock |

### stakedButUnverifiedNativeETH Accounting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect stakedButUnverifiedNativeETH Accounting | `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md` | HIGH | SigmaPrime |
| Variable Never Decremented | `reports/eigenlayer_findings/variable-stakedbutunverifiednativeeth-is-never-decremented.md` | HIGH | SigmaPrime |
| No Balance Verification on NodeDelegator Removal | `reports/eigenlayer_findings/lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigen.md` | MEDIUM | MixBytes |

### Balance Update / Permission Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Permissionless verifyAndProcessWithdrawals | `reports/eigenlayer_findings/anyone-can-submit-proofs-via-eigenpod-verifyandprocesswithdrawals-to-break-the-a.md` | HIGH | Cyfrin |
| Balance Update Must Be Permissioned | `reports/eigenlayer_findings/eig-19-the-eigenpod-balance-update-function-has-to-be-permissioned.md` | MEDIUM | Hexens |
| Beacon Withdrawals at lastWithdrawalTimestamp Lost | `reports/eigenlayer_findings/beacon-chain-withdrawals-that-occur-at-lastwithdrawaltimestamp-will-be-lost.md` | HIGH | Cantina |

### Slashing Factor Calculation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Withdrawable Shares After Combined Slashing | `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md` | HIGH | SigmaPrime |
| Over-Slashing of BeaconChainETH Shares | `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md` | HIGH | SigmaPrime |
| Queued Withdrawals Excluded from Slashable Shares | `reports/eigenlayer_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` | MEDIUM | SigmaPrime |

### Other
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| EigenPod Initialization Issue | `reports/eigenlayer_findings/the-possible-inability-to-initialize-the-eigenpod-field.md` | MEDIUM | MixBytes |

---

# EigenPod & Beacon Chain Verification Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for EigenLayer Native Restaking Security Audits**

---

## Table of Contents

1. [Proof Forgery via Missing Bounds Checks](#1-proof-forgery-via-missing-bounds-checks)
2. [Beacon State Root Upgrade Breakage](#2-beacon-state-root-upgrade-breakage)
3. [stakedButUnverifiedNativeETH Accounting Bugs](#3-stakedbutunverifiednativeeth-accounting-bugs)
4. [Permissionless Proof Verification Bypass](#4-permissionless-proof-verification-bypass)
5. [Slashing Factor Miscalculation](#5-slashing-factor-miscalculation)
6. [Timestamp Boundary Errors](#6-timestamp-boundary-errors)

---

## 1. Proof Forgery via Missing Bounds Checks

### Overview

EigenLayer's beacon chain proof verification uses multi-tree Merkle traversal with concatenated sub-indexes. Missing upper-bound checks on any sub-index allow the combined index to overflow into adjacent beacon state subtrees, enabling forged withdrawal proofs and replay attacks.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/eig-10-withdrawal-proofs-can-be-forged-due-to-missing-index-bit-size-check.md` (EigenLayer - Hexens)
> - `reports/eigenlayer_findings/h-01-slot-and-block-number-proofs-not-required-for-verification-of-withdrawal-mu.md` (EigenLayer - Code4rena)
> - `reports/eigenlayer_findings/eig-14-m1-eigenpods-can-restake-and-withdraw-without-proving-and-burning-shares.md` (EigenLayer - Hexens)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **Merkle proof indices lack proper size validation**. The beacon chain proof system constructs a combined index by bitwise OR of multiple sub-indexes (`historySummaryIndex`, `blockRootIndex`, `withdrawalIndex`). While some indexes are bounds-checked, others are not, allowing overflow into arbitrary beacon state fields.

Additionally, empty proofs pass verification when `leaf == root` (Merkle library returns `true` for zero-length proofs), enabling replay of the same withdrawal with different slot/block values.

**Frequency:** Common (3/18 reports)
**Validation:** Strong — 2 independent audit firms (Hexens CRITICAL, Code4rena HIGH)

### Vulnerable Pattern Examples

**Example 1: Unbounded historySummaryIndex Enables Proof Forgery** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/eig-10-withdrawal-proofs-can-be-forged-due-to-missing-index-bit-size-check.md`
```solidity
// ❌ VULNERABLE: historySummaryIndex has no upper-bound check
function verifyWithdrawal(
    bytes32 beaconStateRoot,
    WithdrawalProof calldata proof
) internal view {
    // blockRootIndex IS checked:
    require(proof.blockRootIndex < 2 ** BLOCK_ROOTS_TREE_HEIGHT, "Invalid blockRootIndex");
    
    // BUG: historySummaryIndex is NOT checked
    // No: require(proof.historySummaryIndex < 2 ** HISTORICAL_SUMMARIES_TREE_HEIGHT);
    
    // Combined index via bitwise OR — oversized historySummaryIndex
    // overflows into HISTORICAL_SUMMARIES_INDEX constant bits
    uint256 historicalBlockHeaderIndex = 
        (HISTORICAL_SUMMARIES_INDEX << ((BLOCK_ROOTS_TREE_HEIGHT + 1) + ...)) |
        (uint256(proof.historySummaryIndex) << ((BLOCK_ROOTS_TREE_HEIGHT + 1) + ...)) |
        (STATE_SUMMARY_INDEX << (BLOCK_ROOTS_TREE_HEIGHT + 1)) |
        (uint256(proof.blockRootIndex));
    
    // Attacker can traverse into arbitrary beacon state fields
}
```

**Example 2: Empty Proofs Pass Verification** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-01-slot-and-block-number-proofs-not-required-for-verification-of-withdrawal-mu.md`
```solidity
// ❌ VULNERABLE: Merkle library returns true for empty proofs when leaf == root
function verifyInclusionSha256(
    bytes memory proof,
    bytes32 root,
    bytes32 leaf,
    uint256 index
) internal pure returns (bool) {
    if (proof.length == 0) {
        return leaf == root; // TRUE when leaf equals root!
    }
    // ...normal verification
}

// Attack: Set slotProof = bytes(""), slotRoot = blockHeaderRoot
// Same withdrawal proven multiple times with different slot values
```

**Example 3: Free Share Minting Without Proof** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/eig-14-m1-eigenpods-can-restake-and-withdraw-without-proving-and-burning-shares.md`
```solidity
// ❌ VULNERABLE: nonBeaconChainETHBalanceWei not reset on withdrawal
function _processWithdrawalBeforeRestaking(address podOwner) internal {
    mostRecentWithdrawalTimestamp = uint32(block.timestamp);
    _sendETH_AsDelayedWithdrawal(podOwner, address(this).balance);
    // BUG: nonBeaconChainETHBalanceWei NOT zeroed
}

// receive() increments nonBeaconChainETHBalanceWei for ALL incoming ETH
receive() external payable {
    nonBeaconChainETHBalanceWei += msg.value;
    // Including ETH from validator exits via beacon chain
}

// Attack loop: deposit → withdrawBeforeRestaking → activateRestaking
//            → verifyCredentials → exit validator → withdrawNonBeaconChainETH
// Result: infinite free share minting
```

### Impact Analysis

#### Technical Impact
- Forged withdrawals from any EigenPod (CRITICAL)
- Same withdrawal proven/claimed multiple times
- Infinite share minting without actual deposits
- Zeroing victim withdrawal timestamps to permanently lock their ETH

#### Business Impact
- Complete protocol fund drainage possible via forged proofs
- EigenLayer security model fundamentally broken
- **Financial impact observed:** Entire protocol TVL exploitable

### Secure Implementation

**Fix 1: Bounds Check All Sub-Indexes**
```solidity
// ✅ SECURE: Validate every sub-index in the combined Merkle path
function verifyWithdrawal(WithdrawalProof calldata proof) internal view {
    require(
        proof.historySummaryIndex < 2 ** HISTORICAL_SUMMARIES_TREE_HEIGHT,
        "Invalid historySummaryIndex"
    );
    require(
        proof.blockRootIndex < 2 ** BLOCK_ROOTS_TREE_HEIGHT,
        "Invalid blockRootIndex"
    );
    require(
        proof.withdrawalIndex < 2 ** WITHDRAWALS_TREE_HEIGHT,
        "Invalid withdrawalIndex"
    );
    // ... continue with verification
}
```

**Fix 2: Require Non-Empty Proofs**
```solidity
// ✅ SECURE: Enforce minimum proof lengths
function verifyWithdrawalProofs(...) internal view {
    require(proof.slotProof.length >= 32, "Empty slot proof");
    require(proof.blockNumberProof.length >= 32, "Empty block proof");
    require(proof.withdrawalProof.length >= 32, "Empty withdrawal proof");
    // ... continue with Merkle verification
}
```

**Fix 3: Reset All Counters on withdrawBeforeRestaking**
```solidity
// ✅ SECURE: Zero ALL balance counters when withdrawing
function _processWithdrawalBeforeRestaking(address podOwner) internal {
    mostRecentWithdrawalTimestamp = uint32(block.timestamp);
    nonBeaconChainETHBalanceWei = 0; // Clear non-beacon balance
    _sendETH_AsDelayedWithdrawal(podOwner, address(this).balance);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `require(index < 2**HEIGHT)` present for some sub-indexes but not all
- Pattern 2: Merkle verification that returns true for zero-length proofs
- Pattern 3: Balance/counter variables incremented in receive() but never zeroed on withdrawal
- Pattern 4: Bitwise OR combination of sub-indexes without complete bounds checks
```

#### Audit Checklist
- [ ] Are ALL sub-indexes in Merkle proof validation bounds-checked against their tree heights?
- [ ] Does the Merkle library require non-empty proofs?
- [ ] Are all counter variables (nonBeaconChainETHBalanceWei, etc.) properly reset on every withdrawal path?
- [ ] Can the same withdrawal be proven more than once?

---

## 2. Beacon State Root Upgrade Breakage

### Overview

Every Ethereum consensus layer hard fork that adds fields to `BeaconState`, `ExecutionPayload`, or changes deposit/withdrawal mechanics breaks EigenLayer's proof verification due to hardcoded SSZ tree heights. This is a recurring, systemic vulnerability.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/verifying-beacon-chain-withdrawals-break-after-deneb.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/proofs-based-on-beaconstateroot-break-after-electra-upgrade.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/lack-of-support-for-compounding-withdrawal-credentials-after-electra-upgrade.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/validator-status-incorrectly-set-to-withdrawn-after-electra-upgrade.md` (EigenLayer - SigmaPrime)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **Merkle tree heights and SSZ container layouts are hardcoded** as constants. Each consensus fork that adds fields changes container sizes and tree depths:

| Fork | Change | Impact |
|------|--------|--------|
| Deneb | ExecutionPayload: 4→5 tree height (blob fields added) | Withdrawal proofs rejected; second pre-image attack possible |
| Electra | BeaconState: 5→6 tree height (28→37 fields via EIP-7251) | All validator/balance verification fails |
| Electra | `0x02` compounding withdrawal credentials (EIP-7251) | Compounding validators can't be verified |
| Electra | Pending balance deposits create zero-balance window | Active validators falsely marked WITHDRAWN |
| Fulu | New custody requirements (data columns) | Stale peer metadata; data availability failures |

**Frequency:** Very Common (5/18 reports)
**Validation:** Strong — 2 independent auditors consistently finding this across multiple forks

### Vulnerable Pattern Examples

**Example 1: Hardcoded ExecutionPayload Tree Height (Pre-Deneb)** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/verifying-beacon-chain-withdrawals-break-after-deneb.md`
```solidity
// ❌ VULNERABLE: Tree height hardcoded — breaks when Deneb adds blob fields
uint256 internal constant EXECUTION_PAYLOAD_HEADER_FIELD_TREE_HEIGHT = 4;
// Deneb adds excessBlobGas and blobGasUsed → new tree height = 5

// Impact 1: Valid post-Deneb withdrawal proofs are rejected
// Impact 2: Second pre-image attack — intermediate nodes can be used as leaves
//           to verify non-existent withdrawals
```

**Example 2: Hardcoded BeaconState Tree Height (Pre-Electra)** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/proofs-based-on-beaconstateroot-break-after-electra-upgrade.md`
```solidity
// ❌ VULNERABLE: BeaconState tree height hardcoded
uint256 internal constant BEACON_STATE_TREE_HEIGHT = 5;
// BeaconState grows from 28 fields (phase 0) to 37 fields (Electra)
// SSZ tree depth: ceil(log2(37)) = 6, not 5

// All verifyValidatorFields() and verifyBalanceContainer() calls fail
// No validator verification possible post-Electra
```

**Example 3: Only 0x01 Withdrawal Credentials Supported** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/lack-of-support-for-compounding-withdrawal-credentials-after-electra-upgrade.md`
```solidity
// ❌ VULNERABLE: Only generates 0x01 prefix credentials
function _podWithdrawalCredentials() internal view returns (bytes memory) {
    return abi.encodePacked(
        bytes1(uint8(1)),    // Only 0x01 — no 0x02 support
        bytes11(0),
        address(this)
    );
    // EIP-7251 introduces 0x02 compounding credentials
    // Validators with 0x02 credentials can't be verified by EigenPod
}
```

**Example 4: Pending Balance Deposits Create False WITHDRAWN Status** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/validator-status-incorrectly-set-to-withdrawn-after-electra-upgrade.md`
```solidity
// ❌ VULNERABLE: Zero balance during pending deposit window marks validator as WITHDRAWN
function verifyCheckpointProofs(...) external {
    // Electra EIP-7251: new validators have effectiveBalance = 0 during pending deposit phase
    if (validatorBalance == 0 && validatorStatus == ACTIVE) {
        // BUG: Assumes zero balance = exited validator
        validatorStatus = WITHDRAWN; // False! Validator is still active
    }
}
```

### Impact Analysis

#### Technical Impact
- Complete proof verification failure after consensus upgrades (5/18 reports)
- Second pre-image attacks enable verification of non-existent withdrawals
- Validators with new credential types cannot be restaked
- Active validators falsely marked as exited, losing AVS rewards during recovery

#### Business Impact
- EigenLayer becomes non-functional after each major fork until updated
- Window of vulnerability between fork activation and contract upgrade
- Could require emergency upgrade or protocol freeze
- **Financial impact observed:** Entire native restaking TVL at risk during each fork

### Secure Implementation

**Fix 1: Dynamic Tree Heights Based on Fork Timestamps**
```solidity
// ✅ SECURE: Select tree height based on fork timestamp
uint256 internal constant EXECUTION_PAYLOAD_HEADER_FIELD_TREE_HEIGHT_PRE_DENEB = 4;
uint256 internal constant EXECUTION_PAYLOAD_HEADER_FIELD_TREE_HEIGHT_POST_DENEB = 5;
uint256 internal constant DENEB_FORK_TIMESTAMP = 1710338135;

function _getExecutionPayloadTreeHeight(uint256 timestamp) internal pure returns (uint256) {
    if (timestamp >= DENEB_FORK_TIMESTAMP) {
        return EXECUTION_PAYLOAD_HEADER_FIELD_TREE_HEIGHT_POST_DENEB;
    }
    return EXECUTION_PAYLOAD_HEADER_FIELD_TREE_HEIGHT_PRE_DENEB;
}
```

**Fix 2: Support Multiple Withdrawal Credential Types**
```solidity
// ✅ SECURE: Support both 0x01 and 0x02 credential prefixes
function _podWithdrawalCredentials(bool compounding) internal view returns (bytes memory) {
    bytes1 prefix = compounding ? bytes1(uint8(2)) : bytes1(uint8(1));
    return abi.encodePacked(prefix, bytes11(0), address(this));
}

function verifyWithdrawalCredentials(...) external {
    bytes memory expectedCreds01 = _podWithdrawalCredentials(false);
    bytes memory expectedCreds02 = _podWithdrawalCredentials(true);
    require(
        keccak256(validatorCreds) == keccak256(expectedCreds01) ||
        keccak256(validatorCreds) == keccak256(expectedCreds02),
        "Invalid credentials"
    );
}
```

**Fix 3: Guard Against Zero-Balance Active Validators**
```solidity
// ✅ SECURE: Require non-zero balance before marking as withdrawn
function verifyCheckpointProofs(...) external {
    if (validatorBalance == 0 && validatorStatus == ACTIVE) {
        // Only mark WITHDRAWN if validator is truly exited
        require(
            validatorExitEpoch <= currentEpoch,
            "Validator still active with pending deposit"
        );
        validatorStatus = WITHDRAWN;
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Constants named `*_TREE_HEIGHT` without fork-conditional selection
- Pattern 2: `bytes1(uint8(1))` in withdrawal credential construction (no 0x02 support)
- Pattern 3: Balance == 0 used as indicator for validator exit (fragile post-Electra)
- Pattern 4: SSZ field count assumptions that don't match latest fork specs
```

#### Audit Checklist
- [ ] Are ALL tree height constants fork-aware (Deneb, Electra, future forks)?
- [ ] Are both `0x01` and `0x02` withdrawal credential types supported?
- [ ] Is validator exit detection robust against zero-balance-while-active scenarios?
- [ ] Is there a documented process for updating proof constants on each CL fork?
- [ ] Are pre-image attack vectors considered (intermediate nodes as leaves)?

---

## 3. stakedButUnverifiedNativeETH Accounting Bugs

### Overview

`stakedButUnverifiedNativeETH` is a transitional accounting variable that bridges the gap between ETH staked on the beacon chain and ETH verified via EigenLayer proofs. Any path that changes staking state without updating this variable creates phantom assets in the protocol's TVL.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md` (Kelp - SigmaPrime)
> - `reports/eigenlayer_findings/variable-stakedbutunverifiednativeeth-is-never-decremented.md` (Kelp - SigmaPrime)
> - `reports/eigenlayer_findings/lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigen.md` (KelpDAO - MixBytes)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **stakedButUnverifiedNativeETH tracks only one direction** of the validator lifecycle. It's incremented by 32 ETH on `stake32ETH()` but either decremented by the wrong amount (effective balance instead of 32 ETH) or never decremented at all during unstaking/withdrawal.

**Frequency:** Common (3/18 reports)
**Validation:** Strong — 2 independent auditors (SigmaPrime, MixBytes)

### Vulnerable Pattern Examples

**Example 1: Asymmetric Increment/Decrement** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md`
```solidity
// ❌ VULNERABLE: Increment by 32 ETH, decrement by effective balance
function stake32ETH(bytes calldata pubkey, ...) external {
    stakedButUnverifiedNativeETH += 32 ether; // Always +32
}

function verifyWithdrawalCredentials(uint64 effectiveBalance) external {
    // BUG: Effective balance can be < 32 ETH (validator slashed before verification)
    stakedButUnverifiedNativeETH -= (effectiveBalance * 1e9); // Maybe 31.5 ETH
    // Residual: 0.5 ETH phantom remains in stakedButUnverifiedNativeETH
    // Over time, this accumulates → inflated rsETH price
}
```

**Example 2: Never Decremented on Withdrawal** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/variable-stakedbutunverifiednativeeth-is-never-decremented.md`
```solidity
// ❌ VULNERABLE: No decrement on any withdrawal path
function stake32Eth(bytes calldata pubkey, ...) external {
    stakedButUnverifiedNativeETH += 32 ether;
}

function initiateNativeEthWithdrawBeforeRestaking() external {
    // BUG: stakedButUnverifiedNativeETH is NOT decremented
    // Withdrawn ETH still counted as protocol assets
}

function claimNativeEthWithdraw() external {
    // BUG: stakedButUnverifiedNativeETH is NOT decremented here either
    // Protocol has phantom 32 ETH per unstaked validator
}
```

**Example 3: NodeDelegator Removal Without Balance Check** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigen.md`
```solidity
// ❌ VULNERABLE: Doesn't check for remaining staked ETH in eigenPod
function removeNodeDelegatorContractFromQueue(uint256 index) external onlyAdmin {
    address nodeDelegator = nodeDelegatorQueue[index];
    // BUG: No check that nodeDelegator's eigenPod balance is 0
    // stakedButUnverifiedNativeETH and eigenPod balance silently orphaned
    nodeDelegatorQueue[index] = nodeDelegatorQueue[length - 1];
    nodeDelegatorQueue.pop();
}
```

### Impact Analysis

#### Technical Impact
- Inflated `totalETHInPool` and consequently inflated rsETH/LRT price (3/18 reports)
- Phantom assets accumulate over time, growing with each staked validator
- Protocol slowly becomes insolvent as withdrawals at inflated rates drain real assets

#### Business Impact
- Gradual protocol insolvency as phantom assets accumulate
- Later withdrawers receive less than their fair share
- **Financial impact observed:** 32 ETH phantom per unstaked validator; compounds linearly

### Secure Implementation

**Fix 1: Symmetric Decrement (Per-Validator, Not Per-Balance)**
```solidity
// ✅ SECURE: Decrement by 32 ETH per validator, not by effective balance
function verifyWithdrawalCredentials(bytes32 validatorPubkeyHash, ...) external {
    // Always decrement by the same amount that was incremented
    stakedButUnverifiedNativeETH -= 32 ether;
    // Actual balance difference tracked separately
}
```

**Fix 2: Decrement on All Withdrawal Paths**
```solidity
// ✅ SECURE: Update on every path that changes staking state
function initiateNativeEthWithdraw(uint256 validatorCount) external {
    stakedButUnverifiedNativeETH -= (validatorCount * 32 ether);
}
```

**Fix 3: Zero-Balance Check on NodeDelegator Removal**
```solidity
// ✅ SECURE: Verify no assets remain before removal
function removeNodeDelegatorContractFromQueue(uint256 index) external onlyAdmin {
    address nodeDelegator = nodeDelegatorQueue[index];
    require(
        INodeDelegator(nodeDelegator).getETHEigenPodBalance() == 0 &&
        INodeDelegator(nodeDelegator).stakedButUnverifiedNativeETH() == 0,
        "Non-zero balance remaining"
    );
    // Safe to remove
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `stakedButUnverifiedNativeETH += 32 ether` without corresponding `-= 32 ether`
- Pattern 2: Decrement using `effectiveBalance` (variable) instead of `32 ether` (constant)
- Pattern 3: Withdrawal/unstaking functions that don't modify the transitional variable
- Pattern 4: Admin removal functions that don't check for zero balances
```

#### Audit Checklist
- [ ] Is `stakedButUnverifiedNativeETH` decremented on EVERY path that changes staking state?
- [ ] Is the decrement amount symmetric with the increment (32 ETH per validator)?
- [ ] Are node delegators checked for zero balance before removal?
- [ ] Does `totalAssets()` correctly handle validators that were staked but withdrawn before verification?

---

## 4. Permissionless Proof Verification Bypass

### Overview

EigenLayer's proof verification functions are permissionless by design — anyone with a valid beacon chain proof can call them. Protocols that wrap EigenLayer and add accounting logic around these calls are vulnerable when external actors call the EigenPod functions directly, bypassing the wrapper's accounting.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/anyone-can-submit-proofs-via-eigenpod-verifyandprocesswithdrawals-to-break-the-a.md` (Casimir - Cyfrin)
> - `reports/eigenlayer_findings/eig-19-the-eigenpod-balance-update-function-has-to-be-permissioned.md` (EigenLayer - Hexens)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **wrapping protocols assume proof verification will flow through their contracts**, but EigenPod functions like `verifyAndProcessWithdrawals()` and `verifyBalanceUpdate()` are callable by anyone with valid proofs.

**Frequency:** Moderate (2/18 reports)
**Validation:** Moderate — 2 independent auditors (Cyfrin, Hexens)

### Vulnerable Pattern Examples

**Example 1: Direct Proof Submission Bypasses Manager Accounting** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/anyone-can-submit-proofs-via-eigenpod-verifyandprocesswithdrawals-to-break-the-a.md`
```solidity
// ❌ VULNERABLE: Manager tracks rewards internally, but proofs are submitted directly
contract CasimirManager {
    uint256 public delayedRewards;
    
    function withdrawRewards(bytes[] proofs) external {
        // Updates delayedRewards BEFORE calling EigenPod
        delayedRewards += expectedRewards;
        eigenPod.verifyAndProcessWithdrawals(proofs);
    }
}

// BUG: Anyone can call eigenPod.verifyAndProcessWithdrawals() directly
// delayedRewards is never updated → rewardStakeRatioSum permanently wrong
// All subsequent reward withdrawals revert with arithmetic underflow
```

**Example 2: Adversarial Balance Update on Exited Validators** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/eig-19-the-eigenpod-balance-update-function-has-to-be-permissioned.md`
```solidity
// ❌ VULNERABLE: Anyone can update validator balance to 0
// verifyBalanceUpdate() is permissionless
// Adversary calls it for an exited validator (balance = 0) BEFORE pod owner
// can call verifyAndProcessWithdrawals (requires ~27h delay)
// Result: shares massively reduced without proper withdrawal processing
```

### Secure Implementation

```solidity
// ✅ SECURE: Track state from EigenLayer directly, don't assume call flow
contract SecureManager {
    function syncRewards() external {
        // Read actual state from EigenLayer rather than tracking internally
        uint256 actualDelayed = delayedWithdrawalRouter.getUserDelayedWithdrawals(eigenPod);
        uint256 actualCompleted = delayedWithdrawalRouter.getClaimableUserDelayedWithdrawals(eigenPod);
        // Reconcile with internal state
        delayedRewards = actualDelayed - actualCompleted;
    }
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Does the protocol add accounting logic before/after calling EigenPod functions?
- [ ] Can those EigenPod functions be called directly by anyone, bypassing the protocol's accounting?
- [ ] Does the protocol read state directly from EigenLayer rather than maintaining shadow copies?

---

## 5. Slashing Factor Miscalculation

### Overview

When multiple scaling factors exist (deposit scaling, operator magnitude, beacon chain slashing factor), calculations that update one factor must correctly account for all others. Missing scaling leads to over- or under-slashing depending on operation ordering.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md` (EigenLayer - SigmaPrime)
> - `reports/eigenlayer_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` (EigenLayer - SigmaPrime)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`_reduceSlashingFactor()` uses unscaled restaked balances**, ignoring existing `maxMagnitude` and `depositScalingFactor`. The formula `newBCSF = prevBCSF * (newBalance / prevBalance)` should use balances scaled by `maxMagnitude * dsf`, but doesn't.

**Frequency:** Common (3/18 reports)
**Validation:** Strong — single expert auditor (SigmaPrime) identified consistently

### Vulnerable Pattern Examples

**Example 1: Under-Slashing After Combined AVS + Beacon Slashing** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`
```solidity
// ❌ VULNERABLE: Uses unscaled balances for slashing factor calculation
function _reduceSlashingFactor(
    uint64 prevRestakedBalanceGwei,
    uint64 newRestakedBalanceGwei,
    uint64 prevBCSF
) internal returns (uint64 newBCSF) {
    // BUG: prevRestakedBalanceGwei is not scaled by maxMagnitude * dsf
    // After operator slashing (maxMagnitude reduced), this calculation
    // gives incorrect result
    newBCSF = prevBCSF * newRestakedBalanceGwei / prevRestakedBalanceGwei;
    
    // Example: 16 ETH beacon slash should reduce withdrawable by 16 ETH
    // But with existing 50% operator slash, only reduces by 8 ETH (under-slashing)
}
```

**Example 2: Over-Slashing Due to Operation Order** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md`
```solidity
// ❌ VULNERABLE: Same root cause, but from over-slashing perspective
// When second validator is verified AFTER operator slashing, the
// slashing factor reduction is too aggressive
// Scenario A (verify before checkpoint): 40 ETH withdrawable ✓
// Scenario B (verify after checkpoint): 36 ETH withdrawable ✗
// Result depends on timing of operations — inconsistent and unfair
```

### Secure Implementation

```solidity
// ✅ SECURE: Scale balances by all relevant factors
function _reduceSlashingFactor(
    uint64 prevRestakedBalanceGwei,
    uint64 newRestakedBalanceGwei,
    uint64 prevBCSF,
    uint64 maxMagnitude,
    uint256 depositScalingFactor
) internal returns (uint64 newBCSF) {
    // Scale by maxMagnitude and depositScalingFactor
    uint256 scaledPrev = uint256(prevRestakedBalanceGwei)
        .mulWad(maxMagnitude)
        .mulWad(depositScalingFactor);
    uint256 scaledNew = uint256(newRestakedBalanceGwei)
        .mulWad(maxMagnitude)
        .mulWad(depositScalingFactor);
    
    newBCSF = uint64(uint256(prevBCSF) * scaledNew / scaledPrev);
}
```

### Detection Patterns

#### Audit Checklist
- [ ] When calculating slashing factors, are ALL scaling factors (maxMagnitude, dsf, bcsf) accounted for?
- [ ] Does the result depend on the order of operations (verify before/after checkpoint)?
- [ ] Are queued beaconChainETHStrategy shares included in slashable share calculations?

---

## 6. Timestamp Boundary Errors

### Overview

Strict greater-than (`>`) checks on withdrawal timestamps instead of greater-than-or-equal (`>=`) cause edge cases where withdrawals occurring in the same block as certain operations are permanently lost.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/beacon-chain-withdrawals-that-occur-at-lastwithdrawaltimestamp-will-be-lost.md` (EigenLayer - Cantina)

### Vulnerable Pattern Examples

**Example 1: Strict > Instead of >=** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/beacon-chain-withdrawals-that-occur-at-lastwithdrawaltimestamp-will-be-lost.md`
```solidity
// ❌ VULNERABLE: Uses > instead of >= for timestamp comparison
function proofIsForValidTimestamp(uint256 timestamp) internal view returns (bool) {
    return timestamp > mostRecentWithdrawalTimestamp; // Should be >=
}

// If user calls activateRestaking() in same block as a beacon chain withdrawal:
// - withdrawBeforeRestaking already called (ETH was sent)
// - Beacon withdrawal happens (same block, same timestamp)
// - Proof for beacon withdrawal: timestamp == mostRecentWithdrawalTimestamp
// - proofIsForValidTimestamp returns FALSE → ETH permanently lost
```

### Secure Implementation

```solidity
// ✅ SECURE: Use >= to handle same-block withdrawals
function proofIsForValidTimestamp(uint256 timestamp) internal view returns (bool) {
    return timestamp >= mostRecentWithdrawalTimestamp;
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Bounds-check ALL sub-indexes in Merkle proof verification
2. Prepare fork-conditional tree heights BEFORE each consensus layer upgrade
3. Use `>=` for timestamp comparisons involving same-block operations
4. Track transitional accounting variables symmetrically (increment/decrement by same amount)
5. Read state directly from EigenLayer rather than maintaining shadow state
6. Scale all balance calculations by all relevant factors (maxMagnitude, dsf, bcsf)
7. Require non-empty Merkle proofs
8. Support new withdrawal credential types (`0x02` compounding)

#### Testing Requirements
- Unit tests for: each CL fork's tree height changes, zero-balance active validators, same-timestamp withdrawals
- Integration tests for: combined AVS + beacon chain slashing, direct EigenPod calls bypassing wrapper, validator lifecycle transitions
- Fuzzing targets: Merkle proof index boundaries, slashing factor calculations with multiple scaling factors

### Keywords for Search

> These keywords enhance vector search retrieval:

`eigenpod`, `beacon chain`, `beacon state root`, `merkle proof`, `withdrawal proof`, `validator fields`, `balance container`, `historical summaries`, `ssz container`, `tree height`, `withdrawal credentials`, `stakedButUnverifiedNativeETH`, `verifyAndProcessWithdrawals`, `verifyWithdrawalCredentials`, `verifyBalanceUpdate`, `slashing factor`, `beaconChainSlashingFactor`, `maxMagnitude`, `depositScalingFactor`, `deneb`, `electra`, `fulu`, `eip-7251`, `compounding`, `proof forgery`, `second pre-image`, `restaking`, `native restaking`, `eigenlayer`, `kelp`, `renzo`, `puffer`, `casimir`, `consensus upgrade`

### Related Vulnerabilities

- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [Restaking Slashing Mechanism](RESTAKING_SLASHING_VULNERABILITIES.md)
- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)
