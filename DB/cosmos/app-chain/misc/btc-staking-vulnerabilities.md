---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: misc
vulnerability_type: btc_staking_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - btc_staking_tx_validation
  - btc_unbonding_handling
  - btc_delegation_finality
  - btc_change_output
  - btc_slashable_stake
  - btc_staking_script
  - btc_covenant_signature
  - btc_indexer_error

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - misc
  - BTC_staking
  - Babylon
  - Bitcoin
  - unbonding
  - finality_provider
  - covenant
  - staking_script
  - UTXO
  
language: go
version: all
---

## References
- [its-not-guaranteed-that-users-will-receive-the-rewards.md](../../../../reports/cosmos_cometbft_findings/its-not-guaranteed-that-users-will-receive-the-rewards.md)
- [spending-multiple-unbonding-transactions-is-not-supported-by-the-staking-indexer.md](../../../../reports/cosmos_cometbft_findings/spending-multiple-unbonding-transactions-is-not-supported-by-the-staking-indexer.md)
- [stakingscriptdata-in-the-btc-staking-ts-library-allows-stakerkey-to-be-in-finali.md](../../../../reports/cosmos_cometbft_findings/stakingscriptdata-in-the-btc-staking-ts-library-allows-stakerkey-to-be-in-finali.md)
- [users-can-be-slashed-instantly-when-stakerpkfinalityproviderpk-in-btcstaking-lib.md](../../../../reports/cosmos_cometbft_findings/users-can-be-slashed-instantly-when-stakerpkfinalityproviderpk-in-btcstaking-lib.md)

## Vulnerability Title

**BTC Staking and Babylon Integration Vulnerabilities**

### Overview

This entry documents 3 distinct vulnerability patterns extracted from 4 audit reports (1 HIGH, 3 MEDIUM severity) across 2 protocols by 2 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Btc Delegation Finality

**Frequency**: 2/4 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Babylonchain

This bug report discusses an issue in the btc-staking-ts library where a user can create a staking transaction with their own public key as the finality provider, potentially leading to invalid transactions. This can happen if the user creates an instance of StakingScriptData with their staker key a

**Example 1.1** [MEDIUM] — Babylonchain
Source: `stakingscriptdata-in-the-btc-staking-ts-library-allows-stakerkey-to-be-in-finali.md`
```solidity
// ❌ VULNERABLE: Btc Delegation Finality
export class StakingScriptData {
    #stakerKey: Buffer;
    #finalityProviderKeys: Buffer[];
    #covenantKeys: Buffer[];
    #covenantThreshold: number;
    #stakingTimeLock: number;
    #unbondingTimeLock: number;
    #magicBytes: Buffer;
    
    constructor(
        stakerKey: Buffer,
        finalityProviderKeys: Buffer[],
        covenantKeys: Buffer[],
        covenantThreshold: number,
        stakingTimelock: number,
        unbondingTimelock: number,
        magicBytes: Buffer,
    ) {
        // Check that required input values are not missing when creating an instance of the StakingScriptData class
        if (
            !stakerKey ||
            !finalityProviderKeys ||
            !covenantKeys ||
            !covenantThreshold ||
            !stakingTimelock ||
          
```

**Example 1.2** [MEDIUM] — Babylonchain
Source: `users-can-be-slashed-instantly-when-stakerpkfinalityproviderpk-in-btcstaking-lib.md`
```solidity
// ❌ VULNERABLE: Btc Delegation Finality
func BuildV0IdentifiableStakingOutputsAndTx(
  magicBytes []byte,
  stakerKey *btcec.PublicKey,
  fpKey *btcec.PublicKey,
  covenantKeys []*btcec.PublicKey,
  covenantQuorum uint32,
  stakingTime uint16,
  stakingAmount btcutil.Amount,
  net *chaincfg.Params,
) (*IdentifiableStakingInfo, *wire.MsgTx, error) {
  info, err := BuildV0IdentifiableStakingOutputs(
    magicBytes,
    stakerKey,
    fpKey,
    covenantKeys,
    covenantQuorum,
    stakingTime,
    stakingAmount,
    net,
  )
  if err != nil {
    return nil, nil, err
  }
  // [...]
}
```

#### Pattern 2: Btc Staking Script

**Frequency**: 1/4 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Soonaverse

This bug report concerns a problem with the Staking contract, which is a type of smart contract used for rewards. The issue is that users must trust the contract owner to add rewards after deployment, and if the user stakes and waits to receive a reward, the owner could simply not add the rewards in

#### Pattern 3: Btc Unbonding Handling

**Frequency**: 1/4 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Babylonchain

The report discusses a bug in the getSpentUnbondingTx function, which is used to determine if a transaction has spent an Unbonding transaction. However, the function is unable to retrieve multiple Unbonding transactions spent within a single Bitcoin transaction, causing incorrect data in the offchai

**Example 3.1** [HIGH] — Babylonchain
Source: `spending-multiple-unbonding-transactions-is-not-supported-by-the-staking-indexer.md`
```solidity
// ❌ VULNERABLE: Btc Unbonding Handling
func (si *StakingIndexer) getSpentUnbondingTx(tx *wire.MsgTx) (*indexerstore.StoredUnbondingTransaction, int) {
    for i, txIn := range tx.TxIn {
        // @POC: loop through input transactions
        maybeUnbondingTxHash := txIn.PreviousOutPoint.Hash
        unbondingTx, err := si.GetUnbondingTxByHash(&maybeUnbondingTxHash)
        if err != nil || unbondingTx == nil {
            continue
        }
        return unbondingTx, i // @POC: return only one unbonding transaction, but multiple can be used
    }
    return nil, -1
}
```

**Example 3.2** [HIGH] — Babylonchain
Source: `spending-multiple-unbonding-transactions-is-not-supported-by-the-staking-indexer.md`
```solidity
// ❌ VULNERABLE: Btc Unbonding Handling
func (si *StakingIndexer) HandleConfirmedBlock(b *types.IndexedBlock) error {
    // ...
    for _, tx := range b.Txs {
        msgTx := tx.MsgTx()
        // ...
        // 3. it's not a spending tx from a previous staking tx,
        // check whether it spends a previous unbonding tx, and
        // handle it if so
        unbondingTx, spendingInputIdx := si.getSpentUnbondingTx(msgTx) // @POC: Only one unbonding transaction is retrieved here,→
        if spendingInputIdx >= 0 {
            // this is a spending tx from the unbonding, validate it, and processes it
            if err := si.handleSpendingUnbondingTransaction( // @POC: Only one unbonding transaction is marked as spent here,→
                msgTx, unbondingTx, spendingInputIdx, uint64(b.Height)); err != nil {
               
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
- Total reports analyzed: 4
- HIGH severity: 1 (25%)
- MEDIUM severity: 3 (75%)
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

> `BTC-staking`, `Babylon`, `Bitcoin`, `unbonding`, `finality-provider`, `covenant`, `staking-script`, `UTXO`, `slashable`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
