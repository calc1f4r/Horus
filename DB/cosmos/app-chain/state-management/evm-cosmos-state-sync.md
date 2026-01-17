---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: state_management
vulnerability_type: state_synchronization

# Attack Vector Details
attack_type: state_desync
affected_component: evm_cosmos_bridge

# Technical Primitives
primitives:
  - StateDB
  - commitCtx
  - stateDB.Commit
  - cache_context
  - WriteCache
  - precompile
  - nonce

# Impact Classification
severity: high
impact: double_spend
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - ethermint
  - minievm
  - statedb
  - precompile
  - state_sync
  - nonce
  - double_spend
  
language: go
version: all
---

## References
- [m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md](../../reports/cosmos_cometbft_findings/m-07-nonce-can-be-manipulated-by-inserting-a-contract-creation-ethereumtx-messag.md)
- [m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md](../../reports/cosmos_cometbft_findings/m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md)
- [m-26-zeta-token-supply-keeps-growing-on-failed-onreceive-contract-calls.md](../../reports/cosmos_cometbft_findings/m-26-zeta-token-supply-keeps-growing-on-failed-onreceive-contract-calls.md)
- [h-01-delegatecall-to-staking-precompile-allows-theft-of-zeta-tokens.md](../../reports/cosmos_cometbft_findings/h-01-delegatecall-to-staking-precompile-allows-theft-of-zeta-tokens.md)

## Vulnerability Title

**EVM-Cosmos State Synchronization Vulnerabilities**

### Overview

Cosmos chains with EVM integration (Ethermint, MiniEVM, Nibiru) must carefully synchronize state between the EVM statedb and Cosmos module keepers. Failures in state synchronization can lead to nonce manipulation, lost rewards, double-spend opportunities, and inconsistent state between the two execution environments. Critical areas include precompile execution, cache context management, and reward claiming flows.

### Root Cause

1. **Dirty state not committed**: EVM statedb changes not committed before Cosmos operations
2. **Nonce desync**: Account nonces inconsistent between EVM and Cosmos state
3. **Cache context mismanagement**: Temporary contexts committed or discarded incorrectly
4. **Precompile state leakage**: Precompile operations affect EVM state without proper isolation
5. **Reward claiming gaps**: Native token rewards not added to EVM statedb after Cosmos claims

### Impact Analysis

#### Technical Impact
- Account nonce manipulation enabling replay attacks
- Token balances inconsistent between EVM and bank module
- Staking rewards lost or double-credited
- Precompile state persisted when transactions fail
- Cache context leaking uncommitted state

#### Business Impact
- Direct fund loss through double-spend
- Users losing staking rewards
- Protocol state corruption
- Exploit opportunities for sophisticated attackers

### Audit Checklist
- EVM statedb committed before any Cosmos state operations
- Account nonces synchronized after EVM transactions
- Cache contexts properly created and committed/reverted
- Precompile operations isolated from EVM state mutations
- Native token rewards explicitly added to EVM statedb
- Failed transactions properly revert all state changes

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Initia MiniEVM | Code4rena | MEDIUM | Nonce manipulation via contract creation |
| ZetaChain | Sherlock | MEDIUM | ZETA rewards lost in precompile claims |
| ZetaChain | Sherlock | MEDIUM | Token supply grows on failed onReceive |
| ZetaChain | Sherlock | HIGH | DELEGATECALL to staking precompile |

### Keywords

state_synchronization, StateDB, commitCtx, stateDB.Commit, cache_context, WriteCache, precompile, nonce, double_spend, EVM, Cosmos, Ethermint, MiniEVM, staking_precompile, reward_claiming, state_desync
