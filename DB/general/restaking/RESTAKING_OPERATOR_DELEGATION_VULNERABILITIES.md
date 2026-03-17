---
# Core Classification (Required)
protocol: generic
chain: everychain
category: restaking
vulnerability_type: operator_delegation_management

# Attack Vector Details (Required)
attack_type: privilege_abuse|state_manipulation|access_control
affected_component: delegation_manager|operator_registry|minipool_state_machine|heap|enforcer

# Technical Primitives (Required)
primitives:
  - operator
  - delegation
  - undelegate
  - minipool
  - hijack
  - state_machine
  - heap_corruption
  - delegation_enforcer
  - bypass
  - censorship
  - front_running
  - operator_registry

# Impact Classification (Required)
severity: high
impact: fund_loss|exchange_rate_manipulation|dos|censorship
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - defi
  - restaking
  - eigenlayer
  - delegation
  - operator
  - minipool
  - staking
  - governance
  - access-control

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | delegation_manager | operator_delegation_management

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _remove
  - _verifyDelegated
  - afterAllHook
  - afterHook
  - block.timestamp
  - bypass
  - censorship
  - createMinipool
  - delegation
  - delegation_enforcer
  - deposit
  - depositToBeaconChain
  - front_running
  - getTVLForAsset
  - heap_corruption
  - hijack
  - minipool
  - msg.sender
  - operator
  - operator_registry
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Operator Censorship / Forced Undelegation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| EIG-17: Operator Can Censor Delegated Stakers | `reports/eigenlayer_findings/eig-17-operator-or-delegation-approver-have-the-power-to-censor-delegated-stakers.md` | MEDIUM | Hexens |

### Minipool State Machine Hijacking
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| H-04: Hijacking Minipool Causes Loss of Staked Funds | `reports/eigenlayer_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md` | HIGH | Code4rena |

### Undelegation Breaking LRT Exchange Rate
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| H-3: Malicious Operators Undelegate to Manipulate LRT Exchange Rate | `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md` | HIGH | Sherlock |
| Malicious Operator Undelegation Breaks Ratio | `reports/eigenlayer_findings/malicious-operator-undelegation-can-break-the-ratio.md` | MEDIUM | Halborn |
| Linear Iteration Over Undelegations Causes Chain Halt | `reports/eigenlayer_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-chain-halt.md` | HIGH | Cantina |

### Heap Corruption from Operator Removal
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| H-8: Heap Stores Removed Operator ID, Leading to Division by Zero | `reports/eigenlayer_findings/h-8-heap-incorrectly-stores-the-removed-operator-id-leading-to-division-by-zero.md` | HIGH | Sherlock |

### Delegation Enforcer Bypasses
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Open Delegations + NativeTokenPaymentEnforcer Front-Running | `reports/eigenlayer_findings/open-delegations-nativetokenpaymentenforcer-front-running-bypass.md` | HIGH | ConsenSys |
| TotalBalanceEnforcer Validation Bypass | `reports/eigenlayer_findings/totalbalanceenforcer-validation-bypass-with-state-modifying-enforcers.md` | HIGH | Cyfrin |

### Stakes Not Forwarded Post-Delegation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| C-02: Stakes Not Forwarded, Positions Unwithdrawable | `reports/eigenlayer_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | CRITICAL | Pashov Audit Group |

### Supplementary Findings
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mismanagement of Delegator Funds | `reports/eigenlayer_findings/mismanagement-of-delegator-funds.md` | HIGH | OtterSec |
| No LST Transfer on Node Operator Withdrawals | `reports/eigenlayer_findings/no-lst-transfer-on-node-operator-withdrawals.md` | HIGH | Codehawks |
| Deposits Front-Run by Malicious Operator | `reports/eigenlayer_findings/deposits-front-run-by-malicious-operator.md` | HIGH | Sherlock |

---

# Restaking Operator & Delegation Vulnerabilities — Comprehensive Database

**A Pattern-Matching Guide for Operator/Delegation Security in Restaking Protocols**

---

## Table of Contents

1. [Operator Censorship via Forced Undelegation](#1-operator-censorship-via-forced-undelegation)
2. [Minipool State Machine Hijacking](#2-minipool-state-machine-hijacking)
3. [Undelegation Breaking LRT Exchange Rate](#3-undelegation-breaking-lrt-exchange-rate)
4. [Heap Corruption from Operator Removal](#4-heap-corruption-from-operator-removal)
5. [Delegation Enforcer Bypasses](#5-delegation-enforcer-bypasses)
6. [Stakes Not Forwarded Post-Delegation](#6-stakes-not-forwarded-post-delegation)
7. [Front-Running Operator Registration](#7-front-running-operator-registration)

---

## 1. Operator Censorship via Forced Undelegation

### Overview

Operators and delegation approvers can forcibly undelegate stakers, locking their funds for the withdrawal delay period (~1 week). This can be repeated cyclically to effectively DoS stakers indefinitely.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/eig-17-operator-or-delegation-approver-have-the-power-to-censor-delegated-stakers.md` (EigenLayer - Hexens)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | delegation_manager | operator_delegation_management`
- Interaction scope: `single_contract`
- Primary affected component(s): `delegation_manager|operator_registry|minipool_state_machine|heap|enforcer`
- High-signal code keywords: `_remove`, `_verifyDelegated`, `afterAllHook`, `afterHook`, `block.timestamp`, `bypass`, `censorship`, `createMinipool`
- Typical sink / impact: `fund_loss|exchange_rate_manipulation|dos|censorship`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `address.function -> function.function -> has.function`
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

This vulnerability exists because **`undelegate()` is callable by the operator or delegation approver, not just the staker**, and undelegation forces all funds into a withdrawal limbo for 50400 blocks (~1 week). After the delay, the operator can re-delegate and immediately undelegate again.

**Frequency:** Moderate (2/21 reports, including delegation management variations)
**Validation:** Strong — Hexens (acknowledged by EigenLayer team)

### Vulnerable Pattern Examples

**Example 1: Operator-Triggered Forced Undelegation** [MEDIUM]
> 📖 Reference: `reports/eigenlayer_findings/eig-17-operator-or-delegation-approver-have-the-power-to-censor-delegated-stakers.md`
```solidity
// ❌ VULNERABLE: Operator/approver can force undelegate any staker
function undelegate(address staker) external onlyWhenNotPaused(PAUSED_UNDELEGATION) 
    returns (bytes32 withdrawalRoot) 
{
    require(isDelegated(staker), "staker must be delegated");
    address operator = delegatedTo[staker];
    require(!isOperator(staker), "operators cannot be undelegated");
    require(
        msg.sender == staker ||
            msg.sender == operator ||                                    // operator can force
            msg.sender == _operatorDetails[operator].delegationApprover, // approver can force
        "caller cannot undelegate staker"
    );
    
    // Forces ALL staker assets into withdrawal limbo for withdrawalDelayBlocks
    if (eigenPodManager.podOwnerHasActiveShares(staker)) {
        uint256 podShares = eigenPodManager.forceIntoUndelegationLimbo(staker, operator);
    }
    if (strategyManager.stakerStrategyListLength(staker) != 0) {
        (strategies, strategyShares, withdrawalRoot) = 
            strategyManager.forceTotalWithdrawal(staker);
    }
}
```

### Impact Analysis

#### Technical Impact
- Staker's ETH, cbETH, rETH, stETH locked for ~1 week per undelegation
- Repeated every week → permanent censorship
- No recourse for the staker during the delay period

#### Business Impact  
- Griefing attack with low cost to the operator
- Loss of staking rewards during forced undelegation periods
- Undermines trust in the delegation model

### Secure Implementation

```solidity
// ✅ SECURE: Only staker can initiate undelegation
function undelegate(address staker) external {
    require(msg.sender == staker, "Only staker can undelegate");
    // ... proceed with undelegation
}

// Or: Operator can request undelegation with cooldown and staker veto
function requestUndelegation(address staker) external {
    require(msg.sender == delegatedTo[staker], "Only operator");
    undelegationRequests[staker] = block.timestamp + VETO_PERIOD;
}
```

---

## 2. Minipool State Machine Hijacking

### Overview

Automated staking state machines that allow minipool re-creation allow attackers to hijack existing minipools by overwriting ownership when the minipool is in a terminal state (Withdrawable or Error).

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md` (GoGoPool - Code4rena)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`createMinipool()` allows anyone to call it with any `nodeID`, and the state machine permits `Withdrawable → Prelaunch` and `Error → Prelaunch` transitions**, which resets the minipool data and overwrites the `owner` to `msg.sender`.

**Frequency:** Rare (1/21 reports) but CRITICAL impact
**Validation:** Strong — 35+ individual finders (Code4rena), Quality 5/5, Rarity 4/5

### Vulnerable Pattern Examples

**Example 1: Ownership Overwrite via State Transition** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md`
```solidity
// ❌ VULNERABLE: No ownership check when re-creating existing minipool
function createMinipool(
    address nodeID,
    uint256 duration,
    uint256 delegationFee,
    uint256 avaxAssignmentRequest
) external payable whenNotPaused {
    int256 minipoolIndex = getIndexOf(nodeID);
    
    if (minipoolIndex != -1) {
        // Only checks state transition is valid — NOT ownership!
        requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
        resetMinipoolData(minipoolIndex);
        // Falls through to set new owner...
    }
    
    // Owner set to msg.sender — could be ANYONE, not original operator
    setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.sender);
    setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".status")), 
            uint256(MinipoolStatus.Prelaunch));
}
```

### Attack Scenario

1. Legitimate operator creates minipool for `node-123`, stakes 1000 AVAX
2. Validation period completes → minipool transitions to `Withdrawable`
3. Attacker calls `createMinipool(node-123)` with 1000 AVAX → becomes new owner
4. Attacker calls `cancelMinipool(node-123)` → gets 1000 AVAX back
5. Original operator calls `withdrawMinipoolFunds(node-123)` → **REVERT** (not owner)
6. Original 1000 AVAX permanently locked

### Impact Analysis

#### Technical Impact
- Complete ownership takeover of any minipool in terminal state
- Original operator loses all staked funds (permanent)
- State machine allows the invalid transition without ownership validation

#### Business Impact
- **Direct fund loss:** Entire minipool stake (1000+ AVAX per attack)
- Every completed validation cycle creates a hijacking window
- Undermines trust in the entire staking system

### Secure Implementation

```solidity
// ✅ SECURE: Verify ownership when re-creating existing minipools
function createMinipool(address nodeID, ...) external payable whenNotPaused {
    int256 minipoolIndex = getIndexOf(nodeID);
    
    if (minipoolIndex != -1) {
        // Check that caller is the original owner
        address currentOwner = getAddress(
            keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner"))
        );
        require(msg.sender == currentOwner, "Not minipool owner");
        requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
        resetMinipoolData(minipoolIndex);
    }
    
    setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.sender);
}
```

---

## 3. Undelegation Breaking LRT Exchange Rate

### Overview

When operators undelegate from LRT protocols, EigenPod shares are set to zero, causing the LRT's Total Value Locked (TVL) calculation to collapse. This creates a massive exchange rate manipulation vector.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md` (Rio Network - Sherlock)
> - `reports/eigenlayer_findings/malicious-operator-undelegation-can-break-the-ratio.md` (Inception LRT - Halborn)
> - `reports/eigenlayer_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-chain-halt.md` (MilkyWay - Cantina)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`DelegationManager.undelegate()` sets EigenPod shares to 0 and queues withdrawals, but the LRT's TVL calculation reads `getEigenPodShares()` which now returns 0**, collapsing the exchange rate. The OperatorDelegator contract has no implementation to complete the queued withdrawals.

**Frequency:** Common (5/21 reports across different protocols)
**Validation:** Strong — 3 independent auditors (Sherlock, Halborn, Cantina)

### Vulnerable Pattern Examples

**Example 1: EigenPod Shares Wiped on Undelegation** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md`
```solidity
// ❌ VULNERABLE: TVL depends on EigenPod shares that operator can wipe
function getTVLForAsset(address asset) public view returns (uint256) {
    if (asset == ETH_ADDRESS) {
        // Aggregates EigenPod shares for all operator delegators
        for (uint i = 0; i < operators.length; i++) {
            totalETH += uint256(operators[i].getEigenPodShares());
            // After undelegate(): getEigenPodShares() returns 0!
        }
    }
    return totalETH;
}

// PoC: Before undelegation
assertEq(uint256(delegatorContract.getEigenPodShares()), 32 * 5 * 1e18); // 160 ETH
assertEq(reETH.assetRegistry.getTVLForAsset(ETH_ADDRESS), 160010000000000000000);

// After undelegation by operator
delegationManager.undelegate(operatorDelegator);
assertEq(uint256(delegatorContract.getEigenPodShares()), 0); // WIPED
assertEq(reETH.assetRegistry.getTVLForAsset(ETH_ADDRESS), 10000000000000000); // ~0.01 ETH
```

**Example 2: Multi-Denom Undelegation Causes Chain Halt** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-chain-halt.md`
```solidity
// ❌ VULNERABLE: Unmetered EndBlock processing amplified by multi-denom
// For 10 denoms: metered undelegate = 48,764 gas; unmetered EndBlock = 109,380 gas (>2x)
// For 20 denoms: >3x amplification
// Attack: Accumulate multi-denom delegations → batch-undelegate 
// → EndBlock processing doubles each block → chain halts
```

### Impact Analysis

#### Technical Impact
- TVL drops >99.99% (e.g., 160 ETH → 0.01 ETH)
- Exchange rate manipulation enables near-infinite dilution of existing holders
- OperatorDelegator cannot complete queued withdrawals → funds stuck

#### Business Impact
- **Financial impact observed:** 160 ETH in deposits exploitable for near-total dilution
- All LRT holders' value can be extracted by new depositors
- ~1 week recovery window during EigenLayer withdrawal delay

### Secure Implementation

```solidity
// ✅ SECURE: Include queued withdrawal value in TVL calculation
function getTVLForAsset(address asset) public view returns (uint256) {
    if (asset == ETH_ADDRESS) {
        for (uint i = 0; i < operators.length; i++) {
            totalETH += uint256(operators[i].getEigenPodShares());
            totalETH += operators[i].getQueuedWithdrawalValue(); // Include queued!
        }
    }
    return totalETH;
}

// ✅ SECURE: Verify all operators still delegated before deposits
function _verifyDelegated() internal view {
    for (uint i = 0; i < restakers.length; i++) {
        require(
            delegationManager.isDelegatedTo(restakers[i], expectedOperator[i]),
            "Operator undelegated"
        );
    }
}
```

---

## 4. Heap Corruption from Operator Removal

### Overview

When operators are removed from a utilization heap by setting their strategy cap to 0, stale data remains in the heap array, causing division by zero on subsequent operations that try to compute utilization ratios.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/h-8-heap-incorrectly-stores-the-removed-operator-id-leading-to-division-by-zero.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`_remove()` decrements `self.count` and copies the last element to the removed position, but doesn't zero out the now-stale last slot**. When stored back, the stale entry persists. On next load, `numActiveOperators` includes the stale entry whose `cap = 0`, causing `allocation.divWad(cap)` to revert with division by zero.

**Frequency:** Rare (1/21 reports) but permanent DoS
**Validation:** Strong — 6 independent finders (Sherlock), escalated from Medium to High

### Vulnerable Pattern Examples

**Example 1: Stale Heap Entry Causes Division by Zero** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/h-8-heap-incorrectly-stores-the-removed-operator-id-leading-to-division-by-zero.md`
```solidity
// ❌ VULNERABLE: _remove doesn't zero-out last slot
function _remove(Data memory self, uint8 i) internal pure {
    self.operators[i] = self.operators[self.count--];
    // BUG: self.operators[old count] still contains removed operator ID!
    // When stored back to storage + loaded next time, stale entry persists
}

// On next load, stale operator with cap=0 triggers:
for (i = 0; i < numActiveOperators; ++i) {
    uint8 operatorId = operators.get(i);
    if (operatorId == 0) break;
    operatorShares = s.operatorDetails[operatorId].shareDetails[strategy];
    heap.operators[i + 1] = OperatorUtilizationHeap.Operator({
        id: operatorId,
        utilization: operatorShares.allocation.divWad(operatorShares.cap) // DIV BY ZERO!
    });
}
```

### Impact Analysis

- All deposits and withdrawals for the affected strategy permanently bricked
- `DivWadFailed()` revert on every rebalance attempt
- **No recovery path** without contract upgrade

### Secure Implementation

```solidity
// ✅ SECURE: Zero out last slot after removal
function _remove(Data memory self, uint8 i) internal pure {
    uint8 lastIndex = self.count;
    self.operators[i] = self.operators[lastIndex];
    self.operators[lastIndex] = Operator({id: 0, utilization: 0}); // Clear stale entry!
    self.count = lastIndex - 1;
}
```

---

## 5. Delegation Enforcer Bypasses

### Overview

Delegation frameworks that use enforcer chains for access control can be bypassed through front-running (open delegations) or state-ordering attacks (cleanup before validation).

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/open-delegations-nativetokenpaymentenforcer-front-running-bypass.md` (MetaMask - ConsenSys)
> - `reports/eigenlayer_findings/totalbalanceenforcer-validation-bypass-with-state-modifying-enforcers.md` (MetaMask - Cyfrin)

### Vulnerability Description

#### Root Cause (Pattern A - Front-Running)

For open delegations (`delegate = ANY_DELEGATE`), the `delegationHash` is identical regardless of who redeems. An attacker can watch the mempool, front-run, and use a victim's payment delegation to pay for the attacker's own use of the open delegation.

#### Root Cause (Pattern B - Cleanup-Before-Validation)

When multiple `TotalBalanceChangeEnforcer` instances are chained, the first instance's `afterAllHook` validates and then `delete balanceTracker[hashKey_]`. Subsequent enforcers find `expectedIncrease == 0 && expectedDecrease == 0` and return early without validation.

**Frequency:** Moderate (4/21 reports across delegation enforcer variants)
**Validation:** Strong — 2 independent auditors (ConsenSys, Cyfrin)

### Vulnerable Pattern Examples

**Example 1: Front-Running Open Delegation Payment** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/open-delegations-nativetokenpaymentenforcer-front-running-bypass.md`
```solidity
// ❌ VULNERABLE: delegationHash identical regardless of redeemer
// DelegationManager.sol:L154
if (delegations_[0].delegate != msg.sender && delegations_[0].delegate != ANY_DELEGATE) {
    // ...
}
// When delegate == ANY_DELEGATE, attacker's delegationHash == victim's delegationHash
// Attacker front-runs and uses victim's payment delegation D2 for their own D1
```

**Example 2: TotalBalanceEnforcer Delete-Before-Validate** [HIGH]
> 📖 Reference: `reports/eigenlayer_findings/totalbalanceenforcer-validation-bypass-with-state-modifying-enforcers.md`
```solidity
// ❌ VULNERABLE: First enforcer cleans up, subsequent enforcers skip validation
function afterAllHook(bytes calldata, bytes calldata, ...) public override {
    BalanceTracker memory balanceTracker_ = balanceTracker[hashKey_];
    
    // After first enforcer deletes tracker:
    if (balanceTracker_.expectedIncrease == 0 && balanceTracker_.expectedDecrease == 0) {
        return; // BYPASSED — no validation!
    }
    
    // ... validation logic ...
    
    delete balanceTracker[hashKey_]; // Cleanup enables bypass for next enforcer
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Include redeemer in payment validation
function afterHook(bytes calldata, bytes calldata, address redeemer, ...) public {
    require(redeemer == expectedRedeemer, "Invalid redeemer for payment");
}

// ✅ SECURE: Track remaining validations
function afterAllHook(...) public override {
    require(validationsRemaining[hashKey_] > 0, "No validations pending");
    validationsRemaining[hashKey_]--;
    
    // Only clean up after ALL enforcers validated
    if (validationsRemaining[hashKey_] == 0) {
        delete balanceTracker[hashKey_];
    }
}
```

---

## 6. Stakes Not Forwarded Post-Delegation

### Overview

After governance delegation, new stakes are not forwarded to the DelegationSurrogate, creating an accounting mismatch that makes positions unwithdrawable.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` (BOB Staking - Pashov)

### Vulnerability Description

#### Root Cause

This vulnerability exists because **`stake()` transfers tokens to `address(this)` regardless of delegation state**, but `unbond()` and `instantWithdraw()` assume all staked tokens reside in the DelegationSurrogate. When `governanceDelegatee != address(0)`, new stakes should be forwarded to the surrogate.

**Frequency:** Rare (1/21 reports) but CRITICAL severity
**Validation:** Moderate — Pashov Audit Group

### Vulnerable Pattern Examples

**Example 1: New Stakes Not Forwarded to Surrogate** [CRITICAL]
> 📖 Reference: `reports/eigenlayer_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
```solidity
// ❌ VULNERABLE: No forwarding when governance delegate is set
function stake(uint256 _amount) external {
    IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
    stakers[receiver].amountStaked += _amount;
    // BUG: When governanceDelegatee != 0, tokens stay in staking contract
    // But unbond/withdraw will try to pull from surrogate
}

// Exit paths assume ALL tokens are in surrogate:
function unbond(uint256 amount) external {
    // Tries to pull amountStaked from surrogate — but surrogate doesn't hold new stakes!
    safeTransferFrom(surrogate, address(this), amount); // REVERTS
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Forward to surrogate when delegate is set
function stake(uint256 _amount) external {
    IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
    stakers[receiver].amountStaked += _amount;
    
    if (stakers[receiver].governanceDelegatee != address(0)) {
        DelegationSurrogate s = storedSurrogates[stakers[receiver].governanceDelegatee];
        IERC20(stakingToken).safeTransfer(address(s), _amount);
    }
}
```

---

## 7. Front-Running Operator Registration

### Overview

Malicious operators can front-run legitimate deposits by depositing to the beacon chain with the same validator pubkey but attacker-controlled withdrawal credentials, stealing the entire deposit amount.

> **📚 Source Reports for Deep Dive:**
> - `reports/eigenlayer_findings/deposits-front-run-by-malicious-operator.md` (Rio Network - Sherlock)

### Vulnerability Description

#### Root Cause

The protocol checks only operator pubkey validity but doesn't verify withdrawal credentials against the expected contract address before forwarding deposits to the beacon deposit contract. An operator can pre-register with attacker-controlled credentials.

**Frequency:** Rare (1/21 reports) but CRITICAL impact  
**Validation:** Moderate — Sherlock finders

### Impact Analysis

- **32 ETH stolen per validator** (entire deposit goes to attacker's withdrawal address)
- Protocol cannot recover funds once deposited to beacon chain
- Operator can repeat for every subsequent deposit

### Secure Implementation

```solidity
// ✅ SECURE: Verify withdrawal credentials point to expected contract
function depositToBeaconChain(bytes pubkey, bytes withdrawal_credentials) external {
    require(
        withdrawal_credentials == abi.encodePacked(
            bytes1(0x01), bytes11(0), address(operatorDelegator)
        ),
        "Invalid withdrawal credentials"
    );
}
```

---

### Prevention Guidelines

#### Development Best Practices
1. Restrict `undelegate()` to staker-only, or add cooldown + veto for operator-initiated
2. Add ownership checks on state machine transitions that re-create entities
3. Include queued withdrawal value in TVL calculations
4. Zero-out stale heap entries after removal
5. Track remaining enforcer validations before cleanup
6. Forward stakes to delegation surrogates when governance delegate is set
7. Verify withdrawal credentials before beacon chain deposits
8. Verify all operators remain delegated before accepting deposits

#### Testing Requirements
- State machine fuzzing: test all possible state transitions, especially terminal→initial
- Ownership invariant tests: verify entity ownership cannot change without authorization
- TVL consistency tests: total TVL before and after operator actions
- Heap integrity tests: add/remove operators and verify heap correctness

### Keywords for Search

> These keywords enhance vector search retrieval:

`operator`, `delegation`, `undelegate`, `forced undelegation`, `minipool`, `hijack`, `state machine`, `ownership overwrite`, `heap corruption`, `division by zero`, `DivWadFailed`, `delegation enforcer`, `TotalBalanceEnforcer`, `NativeTokenPaymentEnforcer`, `ANY_DELEGATE`, `open delegation`, `front-running`, `withdrawal credentials`, `DelegationSurrogate`, `governance delegate`, `restaking`, `eigenlayer`, `GoGoPool`, `Rio Network`, `MetaMask`, `MilkyWay`, `Karak`

### Related Vulnerabilities

- [Restaking Withdrawal Vulnerabilities](RESTAKING_WITHDRAWAL_VULNERABILITIES.md)
- [Restaking Slashing Mechanisms](RESTAKING_SLASHING_VULNERABILITIES.md)
- [LRT Share Accounting Errors](LRT_SHARE_ACCOUNTING_VULNERABILITIES.md)

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

`_remove`, `_verifyDelegated`, `access-control`, `afterAllHook`, `afterHook`, `block.timestamp`, `bypass`, `censorship`, `createMinipool`, `defi`, `delegation`, `delegation_enforcer`, `deposit`, `depositToBeaconChain`, `eigenlayer`, `front_running`, `getTVLForAsset`, `governance`, `heap_corruption`, `hijack`, `minipool`, `msg.sender`, `operator`, `operator_delegation_management`, `operator_registry`, `restaking`, `staking`, `state_machine`, `undelegate`
