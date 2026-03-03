---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: dos
vulnerability_type: unbounded_iteration_dos

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - unbounded_loop_beginblock
  - unbounded_loop_endblock
  - unbounded_array_iteration
  - unmetered_iteration
  - reward_plan_iteration
  - undelegation_iteration
  - token_transfer_iteration
  - state_iteration_dos

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - dos
  - unbounded_iteration
  - loop_DoS
  - linear_iteration
  - gas_exhaustion
  - BeginBlock
  - EndBlock
  - unmetered
  - array_size
  
language: go
version: all
---

## References
- [evasion-of-validation-check-on-early-stop.md](../../../../reports/cosmos_cometbft_findings/evasion-of-validation-check-on-early-stop.md)
- [improper-input-validation-in-repair_oos_account.md](../../../../reports/cosmos_cometbft_findings/improper-input-validation-in-repair_oos_account.md)
- [possible-denial-of-service-in-migration-functionality.md](../../../../reports/cosmos_cometbft_findings/possible-denial-of-service-in-migration-functionality.md)
- [m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md](../../../../reports/cosmos_cometbft_findings/m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md)
- [unbounded-size-of-request-in-covenant-signer-service.md](../../../../reports/cosmos_cometbft_findings/unbounded-size-of-request-in-covenant-signer-service.md)

## Vulnerability Title

**Unbounded Iteration and Loop-Based DoS Vulnerabilities**

### Overview

This entry documents 3 distinct vulnerability patterns extracted from 5 audit reports (1 HIGH, 3 MEDIUM severity) across 4 protocols by 4 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: State Iteration Dos

**Frequency**: 3/5 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Sei OCC, Tokensfarm

This bug report discusses a vulnerability in the early stopping mechanism of the store::validateIterator function. This mechanism stops the iteration loop when encountering a specific key, but it does not confirm if all expected keys have been iterated. This can lead to a validation failure, as seen

**Example 1.1** [HIGH] — Sei OCC
Source: `evasion-of-validation-check-on-early-stop.md`
```solidity
// ❌ VULNERABLE: State Iteration Dos
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

**Example 1.2** [UNKNOWN] — unknown
Source: `improper-input-validation-in-repair_oos_account.md`
```solidity
// ❌ VULNERABLE: State Iteration Dos
for (let i = 0; i < receivedBestVote.account_id.length; i++) {
  if (receivedBestVote.account_id[i] === accountID) {
    if (receivedBestVote.account_state_hash_after[i] !== calculatedAccountHash) {
      nestedCountersInstance.countEvent('accountPatcher', `repair_oos_accounts: account hash mismatch for txId: ${txId}`)
      accountHashMatch = false
    } else {
      accountHashMatch = true
    }
       break
    }
}
```

#### Pattern 2: Reward Plan Iteration

**Frequency**: 1/5 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Virtuals Protocol

Bug Summary:

The `AgentVeToken` contract allows users to stake their tokens and delegate their voting power to someone else. However, there is a loophole that allows non-validators to be delegated voting power, which breaks the core functionality of the contract. This also results in no rewards for

**Example 2.1** [MEDIUM] — Virtuals Protocol
Source: `m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md`
```solidity
// ❌ VULNERABLE: Reward Plan Iteration
function stake(uint256 amount, address receiver, address delegatee) public {
        // . . . Rest of the code . . .

        if (totalSupply() == 0) {
            initialLock = amount;
        }

        registry.addValidator(virtualId, delegatee);        <<@ -- // Validators are added to the registry every time a stake happens.

        IERC20(assetToken).safeTransferFrom(sender, address(this), amount);
        _mint(receiver, amount);
        _delegate(receiver, delegatee);
        _balanceCheckpoints[receiver].push(clock(), SafeCast.toUint208(balanceOf(receiver)));
    }
```

**Example 2.2** [MEDIUM] — Virtuals Protocol
Source: `m-14-votesupgradeabledelegate-bypasses-the-addvalidator-call-leads-to-a-non-vali.md`
```solidity
// ❌ VULNERABLE: Reward Plan Iteration
AgentVeToken -> ERC20Votes -> ERC20VotesUpgradeable -> VotesUpgradeable
```

#### Pattern 3: Unbounded Array Iteration

**Frequency**: 1/5 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Babylonchain

The Covenant Signer service, which is responsible for providing valid signatures for staking, is vulnerable to a denial-of-service (DoS) attack. This is because the service does not limit the size of HTTP requests, allowing an attacker to crash the server by sending multiple large requests. This can

**Example 3.1** [MEDIUM] — Babylonchain
Source: `unbounded-size-of-request-in-covenant-signer-service.md`
```solidity
// ❌ VULNERABLE: Unbounded Array Iteration
#### Then, import the following attacking script in `exploit-dos.py`:
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 1 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 5
- HIGH severity: 1 (20%)
- MEDIUM severity: 3 (60%)
- Unique protocols affected: 4
- Independent audit firms: 4
- Patterns with 3+ auditor validation (Strong): 1

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

> `unbounded-iteration`, `loop-DoS`, `linear-iteration`, `gas-exhaustion`, `BeginBlock`, `EndBlock`, `unmetered`, `array-size`, `O(n)-complexity`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
