---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: evm
vulnerability_type: precompile_state_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - dirty_state_precompile
  - precompile_panic_dos
  - precompile_delegatecall
  - precompile_state_rollback
  - evm_bank_balance_sync
  - cosmos_evm_nonce
  - evm_tx_disguise
  - precompile_outdated_data

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - evm
  - precompile
  - dirty_state
  - delegatecall
  - state_sync
  - EVM_Cosmos
  - bank_module
  - nonce_manipulation
  - state_rollback
  
language: go
version: all
---

## References
- [h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md](../../../../reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md)
- [m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md](../../../../reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md)
- [m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md](../../../../reports/cosmos_cometbft_findings/m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md)

## Vulnerability Title

**EVM Precompile and State Management Vulnerabilities**

### Overview

This entry documents 3 distinct vulnerability patterns extracted from 3 audit reports (1 HIGH, 2 MEDIUM severity) across 2 protocols by 2 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Dirty State Precompile

**Frequency**: 1/3 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: ZetaChain Cross-Chain

The bug report discusses an issue with the ZetaChain platform where changes made to the Ethereum Virtual Machine (EVM) state before a precompile call are not properly reflected in the Cosmos SDK state. This can lead to double-spending of native ZETA tokens and loss of staking rewards. The root cause

**Example 1.1** [HIGH] — ZetaChain Cross-Chain
Source: `h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md`
```solidity
// ❌ VULNERABLE: Dirty State Precompile
82: 	// if caller is not the same as origin it means call is coming through smart contract,
83: 	// and because state of smart contract calling precompile might be updated as well
84: 	// manually reduce amount in stateDB, so it is properly reflected in bank module
85: 	stateDB := evm.StateDB.(precompiletypes.ExtStateDB)
86: 	if contract.CallerAddress != evm.Origin {
87: 		stateDB.SubBalance(stakerAddress, amountUint256)
88: 	}
```

**Example 1.2** [HIGH] — ZetaChain Cross-Chain
Source: `h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md`
```solidity
// ❌ VULNERABLE: Dirty State Precompile
function stakeWithStateUpdate(
        address staker,
        string memory validator,
        uint256 amount
) external onlyOwner returns (bool) {
    counter = counter + 1;
    // transfer full balance
    (bool success, ) = payable(address(0xdead)).call{value: payable(this).balance }("");
    require(success, "transfer to dead address failed");

    success = staking.stake(staker, validator, amount);
    counter = counter + 1;
    return success;
}
```

#### Pattern 2: Cosmos Evm Nonce

**Frequency**: 1/3 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Nibiru

The Ante handler for `MsgEthereumTx` transactions is not properly managing nonces for contract creation and non-contract creation transactions. This allows for a potential exploit where a user can replay a transaction multiple times and reuse their nonces. This can be mitigated by making sure the se

**Example 2.1** [MEDIUM] — Nibiru
Source: `m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md`
```solidity
// ❌ VULNERABLE: Cosmos Evm Nonce
if contractCreation {
		ret, _, st.gas, vmerr = st.evm.Create(sender, st.data, st.gas, st.value)
	} else {
		// Increment the nonce for the next transaction
		st.state.SetNonce(msg.From(), st.state.GetNonce(sender.Address())+1)
		ret, st.gas, vmerr = st.evm.Call(sender, st.to(), st.data, st.gas, st.value)
	}
```

**Example 2.2** [MEDIUM] — Nibiru
Source: `m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md`
```solidity
// ❌ VULNERABLE: Cosmos Evm Nonce
func (evm *EVM) Create(caller ContractRef, code []byte, gas uint64, value *big.Int) (ret []byte, contractAddr common.Address, leftOverGas uint64, err error) {
	contractAddr = crypto.CreateAddress(caller.Address(), evm.StateDB.GetNonce(caller.Address()))
	return evm.create(caller, &codeAndHash{code: code}, gas, value, contractAddr, CREATE)
}
```

#### Pattern 3: Precompile Panic Dos

**Frequency**: 1/3 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: ZetaChain Cross-Chain

The bug report discusses an issue where an attacker can cause multiple pending transactions in the ZetaChain network by exploiting a vulnerability in the precompile caller. This results in the EVM crashing and the Cosmos SDK message failing. The root cause of the issue is that the precompile assumes

**Example 3.1** [MEDIUM] — ZetaChain Cross-Chain
Source: `m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md`
```solidity
// ❌ VULNERABLE: Precompile Panic Dos
92: func (c *Contract) RequiredGas(input []byte) uint64 {
93: 	// get methodID (first 4 bytes)
94: 	var methodID [4]byte
95: 	copy(methodID[:], input[:4])
```

**Example 3.2** [MEDIUM] — ZetaChain Cross-Chain
Source: `m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md`
```solidity
// ❌ VULNERABLE: Precompile Panic Dos
function stakeWithStateUpdate(
    address staker,
    string memory validator,
    uint256 amount
) external onlyOwner returns (bool) {
    counter = counter + 1;
    // transfer full balance
    (bool success, ) = payable(address(0xdead)).call{value: payable(this).balance }("");
    require(success, "transfer to dead address failed");

    success = staking.stake(staker, validator, amount);

    try this.causePanic() {} catch {
        // do nothing
    }

    counter = counter + 1;
    return success;
}

function causePanic() external {
    // call `staking` contract with low level call invalid calldata so that it panics
    address(staking).call(hex"");
}
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
- Total reports analyzed: 3
- HIGH severity: 1 (33%)
- MEDIUM severity: 2 (66%)
- Unique protocols affected: 2
- Independent audit firms: 2
- Patterns with 3+ auditor validation (Strong): 0

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

> `precompile`, `dirty-state`, `delegatecall`, `state-sync`, `EVM-Cosmos`, `bank-module`, `nonce-manipulation`, `state-rollback`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
