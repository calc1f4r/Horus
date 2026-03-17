---
protocol: generic
chain: cosmos
category: node_operator
vulnerability_type: minipool_node_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: node_operator_logic

primitives:
  - deposit_theft
  - cancel_error
  - slash_avoidance
  - finalization
  - replay
  - registration_frontrun
  - reward_leak
  - key_fundable
  - deregistration

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - node_operator
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | node_operator_logic | minipool_node_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - any
  - block.number
  - block.timestamp
  - cancelMinipool
  - cancel_error
  - createMinipool
  - deposit
  - deposit_theft
  - deregistration
  - disableOperator
  - finalization
  - key_fundable
  - msg.sender
  - refund
  - registration_frontrun
  - removeOperator
  - replay
  - requestUnstake
  - reward_leak
  - slash_avoidance
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Minipool Deposit Theft
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-04] Hijacking of node operators minipool causes loss of s | `reports/cosmos_cometbft_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md` | HIGH | Code4rena |

### Minipool Cancel Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-12] Cancellation of minipool may skip MinipoolCancelMorat | `reports/cosmos_cometbft_findings/m-12-cancellation-of-minipool-may-skip-minipoolcancelmoratoriumseconds-checking-.md` | MEDIUM | Code4rena |

### Minipool Slash Avoidance
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-06] MinipoolManager: node operator can avoid being slashe | `reports/cosmos_cometbft_findings/h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md` | HIGH | Code4rena |
| RocketMinipoolDelegate - Sandwiching of Minipool calls can h | `reports/cosmos_cometbft_findings/rocketminipooldelegate-sandwiching-of-minipool-calls-can-have-unintended-side-ef.md` | HIGH | ConsenSys |
| RocketNodeStaking - Node operators can reduce slashing impac | `reports/cosmos_cometbft_findings/rocketnodestaking-node-operators-can-reduce-slashing-impact-by-withdrawing-exces.md` | HIGH | ConsenSys |

### Minipool Finalization
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RocketMinipoolDelegate - Redundant refund() call on forced f | `reports/cosmos_cometbft_findings/rocketminipooldelegate-redundant-refund-call-on-forced-finalization-fixed.md` | MEDIUM | ConsenSys |
| RocketMinipoolDelegateOld - Node operator may reenter finali | `reports/cosmos_cometbft_findings/rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md` | HIGH | ConsenSys |

### Minipool Replay
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Replay CREATE2 On Destroyed Minipools | `reports/cosmos_cometbft_findings/replay-create2-on-destroyed-minipools.md` | HIGH | SigmaPrime |

### Operator Registration Frontrun
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H08] Endpoint registration can be frontrun | `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md` | HIGH | OpenZeppelin |

### Operator Reward Leak
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Node Operator Rewards Unevenly Leaked | `reports/cosmos_cometbft_findings/node-operator-rewards-unevenly-leaked.md` | MEDIUM | SigmaPrime |

### Operator Key Fundable
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Operators._hasFundableKeys returns true for operators that d | `reports/cosmos_cometbft_findings/operators_hasfundablekeys-returns-true-for-operators-that-do-not-have-fundable-k.md` | HIGH | Spearbit |
| OperatorsRegistry._getNextValidatorsFromActiveOperators can  | `reports/cosmos_cometbft_findings/operatorsregistry_getnextvalidatorsfromactiveoperators-can-dos-alluvial-staking-.md` | HIGH | Spearbit |
| OperatorsRegistry._getNextValidatorsFromActiveOperators shou | `reports/cosmos_cometbft_findings/operatorsregistry_getnextvalidatorsfromactiveoperators-should-not-consider-stopp.md` | MEDIUM | Spearbit |

### Operator Deregistration
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A malicious staker can force validator withdrawals by instan | `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md` | HIGH | Cyfrin |
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| Insufficient Delay forRocketNodeStaking.withdrawRPL() | `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md` | MEDIUM | SigmaPrime |
| Insufficient validation in `AvalancheL1Middleware::removeOpe | `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md` | MEDIUM | Cyfrin |
| [M-03] In a mass slashing event, node operators are incentiv | `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md` | MEDIUM | ZachObront |
| A malicious operator will control consensus without risking  | `reports/cosmos_cometbft_findings/m-7-a-malicious-operator-will-control-consensus-without-risking-stake-stake-exit.md` | MEDIUM | Sherlock |
| Potential Misallocation of Validators in `_getDepositsAlloca | `reports/cosmos_cometbft_findings/potential-misallocation-of-validators-in-_getdepositsallocation-function.md` | MEDIUM | MixBytes |

---

# Minipool Node Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Minipool Node Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Minipool Deposit Theft](#1-minipool-deposit-theft)
2. [Minipool Cancel Error](#2-minipool-cancel-error)
3. [Minipool Slash Avoidance](#3-minipool-slash-avoidance)
4. [Minipool Finalization](#4-minipool-finalization)
5. [Minipool Replay](#5-minipool-replay)
6. [Operator Registration Frontrun](#6-operator-registration-frontrun)
7. [Operator Reward Leak](#7-operator-reward-leak)
8. [Operator Key Fundable](#8-operator-key-fundable)
9. [Operator Deregistration](#9-operator-deregistration)

---

## 1. Minipool Deposit Theft

### Overview

Implementation flaw in minipool deposit theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: A bug has been found in the GoGoPool smart contract, which allows anyone to hijack a minipool of any node operator that finished the validation period or had an error. This could lead to the node operator losing their staked funds, as well as the hacker gaining rewards without hosting a node.

The p



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | node_operator_logic | minipool_node_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `node_operator_logic`
- High-signal code keywords: `any`, `block.number`, `block.timestamp`, `cancelMinipool`, `cancel_error`, `createMinipool`, `deposit`, `deposit_theft`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `at.function -> of.function`
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

Implementation flaw in minipool deposit theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies minipool deposit theft in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to minipool operations

### Vulnerable Pattern Examples

**Example 1: [H-04] Hijacking of node operators minipool causes loss of staked funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md`
```solidity
function createMinipool(
		address nodeID,
		uint256 duration,
		uint256 delegationFee,
		uint256 avaxAssignmentRequest
	) external payable whenNotPaused {
---------
		// Create or update a minipool record for nodeID
		// If nodeID exists, only allow overwriting if node is finished or canceled
		// 		(completed its validation period and all rewards paid and processing is complete)
		int256 minipoolIndex = getIndexOf(nodeID);
		if (minipoolIndex != -1) {
			requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
			resetMinipoolData(minipoolIndex);
----------
		setUint(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".status")), uint256(MinipoolStatus.Prelaunch));
----------
		setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.sender);
----------
	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in minipool deposit theft logic allows exploitation through missing validation, 
func secureMinipoolDepositTheft(ctx sdk.Context) error {
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
- **Affected Protocols**: GoGoPool
- **Validation Strength**: Single auditor

---

## 2. Minipool Cancel Error

### Overview

Implementation flaw in minipool cancel error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a vulnerability found in the code of the project 2022-12-gogopool. The vulnerability allows a user to cancel a minipool immediately after it is recreated, which should not be allowed. The user should wait for the minimum wait period before canceling the minipool.

The code o

### Vulnerability Description

#### Root Cause

Implementation flaw in minipool cancel error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies minipool cancel error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to minipool operations

### Vulnerable Pattern Examples

**Example 1: [M-12] Cancellation of minipool may skip MinipoolCancelMoratoriumSeconds checkin** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-12-cancellation-of-minipool-may-skip-minipoolcancelmoratoriumseconds-checking-.md`
```solidity
/// @notice Owner of a minipool can cancel the (prelaunch) minipool
	/// @param nodeID 20-byte Avalanche node ID the Owner registered with
	function cancelMinipool(address nodeID) external nonReentrant {
		Staking staking = Staking(getContractAddress("Staking"));
		ProtocolDAO dao = ProtocolDAO(getContractAddress("ProtocolDAO"));
		int256 index = requireValidMinipool(nodeID);
		onlyOwner(index);
		// make sure they meet the wait period requirement
		if (block.timestamp - staking.getRewardsStartTime(msg.sender) < dao.getMinipoolCancelMoratoriumSeconds()) {
			revert CancellationTooEarly();
		}
		_cancelMinipoolAndReturnFunds(nodeID, index);
	}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in minipool cancel error logic allows exploitation through missing validation, i
func secureMinipoolCancelError(ctx sdk.Context) error {
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
- **Affected Protocols**: GoGoPool
- **Validation Strength**: Single auditor

---

## 3. Minipool Slash Avoidance

### Overview

Implementation flaw in minipool slash avoidance logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 3.

> **Key Finding**: This bug report is about a vulnerability in the code of the GogoPool project. The vulnerability occurs when a node operator creates a minipool with a duration of more than 365 days. This causes the amount to be slashed to be greater than the GGP balance the node operator has staked, leading to an un

### Vulnerability Description

#### Root Cause

Implementation flaw in minipool slash avoidance logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies minipool slash avoidance in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to minipool operations

### Vulnerable Pattern Examples

**Example 1: [H-06] MinipoolManager: node operator can avoid being slashed** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md`
```go
// No rewards means validation period failed, must slash node ops GGP.
if (avaxTotalRewardAmt == 0) {
    slash(minipoolIndex);
}
```

**Example 2: RocketMinipoolDelegate - Sandwiching of Minipool calls can have unintended side ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/rocketminipooldelegate-sandwiching-of-minipool-calls-can-have-unintended-side-ef.md`
```solidity
function \_slash() private {
    // Get contracts
    RocketNodeStakingInterface rocketNodeStaking = RocketNodeStakingInterface(getContractAddress("rocketNodeStaking"));
    // Slash required amount and reset storage value
    uint256 slashAmount = nodeSlashBalance;
    nodeSlashBalance = 0;
    rocketNodeStaking.slashRPL(nodeAddress, slashAmount);
    // Record slashing
    slashed = true;
}
```

**Example 3: RocketNodeStaking - Node operators can reduce slashing impact by withdrawing exc** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/rocketnodestaking-node-operators-can-reduce-slashing-impact-by-withdrawing-exces.md`
```go
rocketMinipoolManager.setMinipoolWithdrawalBalances(\_minipoolAddress, \_stakingEndBalance, nodeAmount);
// Apply node penalties by liquidating RPL stake
if (\_stakingEndBalance < userDepositBalance) {
    RocketNodeStakingInterface rocketNodeStaking = RocketNodeStakingInterface(getContractAddress("rocketNodeStaking"));
    rocketNodeStaking.slashRPL(minipool.getNodeAddress(), userDepositBalance - \_stakingEndBalance);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in minipool slash avoidance logic allows exploitation through missing validation
func secureMinipoolSlashAvoidance(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 3
- **Affected Protocols**: GoGoPool, Rocket Pool Atlas (v1.2), Rocketpool
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Minipool Finalization

### Overview

Implementation flaw in minipool finalization logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report is about an issue with the `RocketMinipoolDelegate.refund` function in the code of the RocketPool project. The function will force finalization if a user previously distributed the pool, however, the `_finalise()` function already calls `_refund()` if there is a node refund balance t

### Vulnerability Description

#### Root Cause

Implementation flaw in minipool finalization logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies minipool finalization in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to minipool operations

### Vulnerable Pattern Examples

**Example 1: RocketMinipoolDelegate - Redundant refund() call on forced finalization ✓ Fixed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/rocketminipooldelegate-redundant-refund-call-on-forced-finalization-fixed.md`
```solidity
function refund() override external onlyMinipoolOwnerOrWithdrawalAddress(msg.sender) onlyInitialised {
    // Check refund balance
    require(nodeRefundBalance > 0, "No amount of the node deposit is available for refund");
    // If this minipool was distributed by a user, force finalisation on the node operator
    if (!finalised && userDistributed) {
        \_finalise();
    }
    // Refund node
    \_refund();
}
```

**Example 2: RocketMinipoolDelegateOld - Node operator may reenter finalise() to manipulate a** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md`
```go
finalise() --> 
  status == MinipoolStatus.Withdrawable  //<-- true
  withdrawalBlock > 0  //<-- true
  _finalise() -->
     !finalised  //<-- true
        _refund()
            nodeRefundBalance = 0  //<-- reset refund balance
              ---> extCall: nodeWithdrawalAddress
                     ---> reenter: finalise()
                        status == MinipoolStatus.Withdrawable  //<-- true
                        withdrawalBlock > 0  //<-- true
                        _finalise() -->
                             !finalised  //<-- true
                             nodeRefundBalance > 0  //<-- false; no refund()
                             address(this).balance to RETH
                             RocketTokenRETHInterface(rocketTokenRETH).depositExcessCollateral()
                             rocketMinipoolManager.incrementNodeFinalisedMinipoolCount(nodeAddress)  //<-- 1st time
                             eventually call rocketDAONodeTrusted.decrementMemberUnbondedValidatorCount(nodeAddress); 
                             finalised = true;
                   <--- return from reentrant call
        <--- return from _refund()
     address(this).balance to RETH  //<-- NOP as balance was sent to RETH already
     RocketTokenRETHInterface(rocketTokenRETH).depositExcessCollateral();   //<-- does not revert
     rocketMinipoolManager.incrementNodeFinalisedMinipoolCount(nodeAddress);  //<-- no revert, increases
     'node.minipools.finalised.count', 'minipools.finalised.count', reduces 'eth.matched.node.amount' one to
     many times
     eventually call rocketDAONodeTrusted.decrementMemberUnbondedValidatorCount(nodeAddress);  //<-- manipulates
     'member.validator.unbonded.count' by +1
     finalised = true;  //<-- is already 'true', gracefully continues
<--- returns
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in minipool finalization logic allows exploitation through missing validation, i
func secureMinipoolFinalization(ctx sdk.Context) error {
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
- **Affected Protocols**: Rocket Pool Atlas (v1.2)
- **Validation Strength**: Single auditor

---

## 5. Minipool Replay

### Overview

Implementation flaw in minipool replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The bug report discusses a vulnerability in the Rocket Pool Protocol which allows a malicious operator to exploit the CREATE2 opcode to create a new contract at a deterministically generated address. The attacker can then deposit 33 ETH (1 ETH in the Eth2 deposit contract, 2 x 16 ETH for each deposi

### Vulnerability Description

#### Root Cause

Implementation flaw in minipool replay logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies minipool replay in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to minipool operations

### Vulnerable Pattern Examples

**Example 1: Replay CREATE2 On Destroyed Minipools** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/replay-create2-on-destroyed-minipools.md`
```go
require (rocketMinipoolManager.getMinipoolByPubkey(_validatorPubkey) == address(this), "Validator pubkey is not correct");
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in minipool replay logic allows exploitation through missing validation, incorre
func secureMinipoolReplay(ctx sdk.Context) error {
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
- **Affected Protocols**: Rocketpool
- **Validation Strength**: Single auditor

---

## 6. Operator Registration Frontrun

### Overview

Implementation flaw in operator registration frontrun logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: This bug report is about a malicious actor frontrunning an honest service provider’s call to the `ServiceProviderFactory.register` function. The attacker can monitor the mempool for calls to the `register` function, then frontrun them with their own call using the same `_endpoint` parameter. This re

### Vulnerability Description

#### Root Cause

Implementation flaw in operator registration frontrun logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies operator registration frontrun in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to operator operations

### Vulnerable Pattern Examples

**Example 1: [H08] Endpoint registration can be frontrun** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h08-endpoint-registration-can-be-frontrun.md`
```
// Vulnerable pattern from Audius Contracts Audit:
An honest service provider’s call to the [`ServiceProviderFactory.register` function](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/ServiceProviderFactory.sol#L141) can be frontrun by a malicious actor in order to prevent any honest user from being able to register any endpoint.


The attacker can monitor the mempool for any calls to the `register` function, then frontrun them with their own call to the `register` function 
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in operator registration frontrun logic allows exploitation through missing vali
func secureOperatorRegistrationFrontrun(ctx sdk.Context) error {
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
- **Affected Protocols**: Audius Contracts Audit
- **Validation Strength**: Single auditor

---

## 7. Operator Reward Leak

### Overview

Implementation flaw in operator reward leak logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a problem with the Lido platform, where a portion of staking rewards are distributed as a fee to the staking node operators. When rewards are distributed, an integer division is done which results in a small remainder that stays with the NodeOperatorRegistry. This remainder 

### Vulnerability Description

#### Root Cause

Implementation flaw in operator reward leak logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies operator reward leak in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to operator operations

### Vulnerable Pattern Examples

**Example 1: Node Operator Rewards Unevenly Leaked** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/node-operator-rewards-unevenly-leaked.md`
```go
uint256 perValReward = _totalReward.div(effectiveStakeTotal);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in operator reward leak logic allows exploitation through missing validation, in
func secureOperatorRewardLeak(ctx sdk.Context) error {
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
- **Affected Protocols**: Lido
- **Validation Strength**: Single auditor

---

## 8. Operator Key Fundable

### Overview

Implementation flaw in operator key fundable logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This bug report is related to the Alluvial staking contract of the Operators.sol file. The bug occurs when an operator, who has 'keys' = 10, 'limit' = 10, 'funded' = 10, and 'stopped' = 10, is validated and returns true. This happens because of a logic error in the _hasFundableKeys function which us

### Vulnerability Description

#### Root Cause

Implementation flaw in operator key fundable logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies operator key fundable in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to operator operations

### Vulnerable Pattern Examples

**Example 1: Operators._hasFundableKeys returns true for operators that do not have fundable ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/operators_hasfundablekeys-returns-true-for-operators-that-do-not-have-fundable-k.md`
```
// Vulnerable pattern from Liquid Collective:
## Critical Risk Report
```

**Example 2: OperatorsRegistry._getNextValidatorsFromActiveOperators can DOS Alluvial staking** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/operatorsregistry_getnextvalidatorsfromactiveoperators-can-dos-alluvial-staking-.md`
```go
uint256 selectedOperatorIndex = 0;
for (uint256 idx = 1; idx < operators.length;) {
    if (
        operators[idx].funded - operators[idx].stopped <
        operators[selectedOperatorIndex].funded - operators[selectedOperatorIndex].stopped
    ) {
        selectedOperatorIndex = idx;
    }
    unchecked {
        ++idx;
    }
}
```

**Example 3: OperatorsRegistry._getNextValidatorsFromActiveOperators should not consider stop** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/operatorsregistry_getnextvalidatorsfromactiveoperators-should-not-consider-stopp.md`
```
// Vulnerable pattern from Liquid Collective:
## Severity: Medium Risk
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in operator key fundable logic allows exploitation through missing validation, i
func secureOperatorKeyFundable(ctx sdk.Context) error {
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
- **Affected Protocols**: Liquid Collective
- **Validation Strength**: Single auditor

---

## 9. Operator Deregistration

### Overview

Implementation flaw in operator deregistration logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 7 audit reports with severity distribution: HIGH: 2, MEDIUM: 5.

> **Key Finding**: The bug report describes an issue where a user can exploit the system by repeatedly depositing and withdrawing ETH, causing unnecessary withdrawals from the Beacon Chain. This results in a loss of potential rewards for genuine stakers and is also costly for the protocol. The report recommends implem

### Vulnerability Description

#### Root Cause

Implementation flaw in operator deregistration logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies operator deregistration in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to operator operations

### Vulnerable Pattern Examples

**Example 1: A malicious staker can force validator withdrawals by instantly staking and unst** [HIGH]
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

**Example 2: Denial Of Slashing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/denial-of-slashing.md`
```solidity
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

**Example 3: Insufficient Delay forRocketNodeStaking.withdrawRPL()** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
```go
require ( block.number.sub(getNodeRPLStakedBlock(msg.sender)) >= rocketDAOProtocolSettingsRewards.getRewardsClaimIntervalBlocks(),
" The withdrawal cooldown period has not passed ");
```

**Example 4: Insufficient validation in `AvalancheL1Middleware::removeOperator` can create pe** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`
```solidity
// AvalancheL1Middleware.sol
  function disableOperator(
        address operator
    ) external onlyOwner updateGlobalNodeStakeOncePerEpoch {
        operators.disable(operator); //@note disable an operator - this only works if operator exists
    }
function removeOperator(
    address operator
) external onlyOwner updateGlobalNodeStakeOncePerEpoch {
    (, uint48 disabledTime) = operators.getTimes(operator);
    if (disabledTime == 0 || disabledTime + SLASHING_WINDOW > Time.timestamp()) {
        revert AvalancheL1Middleware__OperatorGracePeriodNotPassed(disabledTime, SLASHING_WINDOW);
    }
    operators.remove(operator); // @audit no check
}
```

**Example 5: [M-03] In a mass slashing event, node operators are incentivized to get slashed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md`
```
// Vulnerable pattern from Obol:
When the `OptimisticWithdrawalRecipient` receives funds from the beacon chain, it uses the following rule to determine the allocation:

> If the amount of funds to be distributed is greater than or equal to 16 ether, it is assumed that it is a withdrawal (to be returned to the principal, with a cap on principal withdrawals of the total amount they deposited).

> Otherwise, it is assumed that the funds are rewards.

This value being as low as 16 ether protects against any predictable attack the n
```

**Variant: Operator Deregistration - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/insufficient-validation-in-avalanchel1middlewareremoveoperator-can-create-perman.md`
> - `reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in operator deregistration logic allows exploitation through missing validation,
func secureOperatorDeregistration(ctx sdk.Context) error {
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
- **Affected Protocols**: Symbiotic Relay, Rocketpool, Lido, Ethos EVM, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Minipool Deposit Theft
grep -rn 'minipool|deposit|theft' --include='*.go' --include='*.sol'
# Minipool Cancel Error
grep -rn 'minipool|cancel|error' --include='*.go' --include='*.sol'
# Minipool Slash Avoidance
grep -rn 'minipool|slash|avoidance' --include='*.go' --include='*.sol'
# Minipool Finalization
grep -rn 'minipool|finalization' --include='*.go' --include='*.sol'
# Minipool Replay
grep -rn 'minipool|replay' --include='*.go' --include='*.sol'
# Operator Registration Frontrun
grep -rn 'operator|registration|frontrun' --include='*.go' --include='*.sol'
# Operator Reward Leak
grep -rn 'operator|reward|leak' --include='*.go' --include='*.sol'
# Operator Key Fundable
grep -rn 'operator|key|fundable' --include='*.go' --include='*.sol'
# Operator Deregistration
grep -rn 'operator|deregistration' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `alluvial`, `anoperator`, `appchain`, `avoid`, `avoidance`, `before`, `being`, `call`, `calls`, `cancel`, `cancellation`, `cancelled`, `causes`, `checking`, `consider`, `cosmos`, `delay`, `denial`, `deposit`, `deregistration`, `destroyed`, `effects`, `endpoint`, `error`, `excess`, `finalization`, `fixed`, `force`, `forced`

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

`any`, `appchain`, `block.number`, `block.timestamp`, `cancelMinipool`, `cancel_error`, `cosmos`, `createMinipool`, `defi`, `deposit`, `deposit_theft`, `deregistration`, `disableOperator`, `finalization`, `key_fundable`, `minipool_node_vulnerabilities`, `msg.sender`, `node_operator`, `refund`, `registration_frontrun`, `removeOperator`, `replay`, `requestUnstake`, `reward_leak`, `slash_avoidance`, `staking`
