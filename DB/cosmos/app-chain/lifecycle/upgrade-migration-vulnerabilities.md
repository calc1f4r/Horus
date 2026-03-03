---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: lifecycle
vulnerability_type: upgrade_migration_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - upgrade_procedure_error
  - migration_data_loss
  - initialization_error
  - storage_gap_error
  - proxy_upgrade_error
  - deployment_parameter_error
  - module_registration_missing
  - state_migration_error

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - lifecycle
  - upgrade
  - migration
  - initialization
  - storage_gap
  - proxy
  - deployment
  - module_registration
  - genesis
  
language: go
version: all
---

## References
- [dos-attack-on-the-nomad-homesol-contract.md](../../../../reports/cosmos_cometbft_findings/dos-attack-on-the-nomad-homesol-contract.md)
- [improper-implementation-of-cosmos-sdk-upgrade-procedures.md](../../../../reports/cosmos_cometbft_findings/improper-implementation-of-cosmos-sdk-upgrade-procedures.md)
- [m-02-boldupgradeactionsol-will-fail-to-upgrade-contracts-due-to-error-in-the-per.md](../../../../reports/cosmos_cometbft_findings/m-02-boldupgradeactionsol-will-fail-to-upgrade-contracts-due-to-error-in-the-per.md)
- [loadversion-failure-on-history-queries.md](../../../../reports/cosmos_cometbft_findings/loadversion-failure-on-history-queries.md)
- [m-30-incorrect-deployment-parameters.md](../../../../reports/cosmos_cometbft_findings/m-30-incorrect-deployment-parameters.md)
- [m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md](../../../../reports/cosmos_cometbft_findings/m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md)
- [storage-gap-variables-slightly-off-from-the-intended-size-fixed.md](../../../../reports/cosmos_cometbft_findings/storage-gap-variables-slightly-off-from-the-intended-size-fixed.md)

## Vulnerability Title

**Upgrade, Migration and Initialization Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 7 audit reports (2 HIGH, 5 MEDIUM severity) across 7 protocols by 6 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Upgrade Procedure Error

**Frequency**: 3/7 reports | **Severity**: HIGH | **Validation**: Strong (3 auditors)
**Protocols affected**: Arbitrum Foundation, Connext, AppChain Modules

This bug report is about a vulnerability in the Home.sol and Queue.sol contracts. When the xcall() function is called, a message is dispatched via Nomad and a hash of this message is inserted into the merkle tree. The new root is added at the end of the queue. The improperUpdate() function checks th

**Example 1.1** [HIGH] — Connext
Source: `dos-attack-on-the-nomad-homesol-contract.md`
```solidity
// ❌ VULNERABLE: Upgrade Procedure Error
function improperUpdate(..., bytes32 _newRoot, ... ) public notFailed returns (bool) {
    ...
    // if the _newRoot is not currently contained in the queue,
    // slash the Updater and set the contract to FAILED state
    if (!queue.contains(_newRoot)) {
        _fail();
        ...
    }
    ...
}
```

**Example 1.2** [HIGH] — Connext
Source: `dos-attack-on-the-nomad-homesol-contract.md`
```solidity
// ❌ VULNERABLE: Upgrade Procedure Error
function contains(Queue storage _q, bytes32 _item) internal view returns (bool) {
    for (uint256 i = _q.first; i <= _q.last; i++) {
        if (_q.queue[i] == _item) {
            return true;
        }
    }
    return false;
}
```

#### Pattern 2: Migration Data Loss

**Frequency**: 1/7 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Sei DB

A bug has been reported in the scStore function of the DB instance. The issue arises when the DB options do not include the Readonly flag, causing the LockFile to be locked by the DB instance opened for cms. This results in the LoadVersion function always failing alongside the queries. To fix this i

**Example 2.1** [MEDIUM] — Sei DB
Source: `loadversion-failure-on-history-queries.md`
```solidity
// ❌ VULNERABLE: Migration Data Loss
func (rs *Store) Query(req abci.RequestQuery) abci.ResponseQuery {
    [...]
    if !req.Prove && version < rs.lastCommitInfo.Version && rs.ssStore != nil {
        [...]
    } else if version < rs.lastCommitInfo.Version {
        // Serve abci query from historical sc store if proofs needed
        scStore, err := rs.scStore.LoadVersion(version, true)
        [...]
    } else {
        [...]
    }
}
```

**Example 2.2** [MEDIUM] — Sei DB
Source: `loadversion-failure-on-history-queries.md`
```solidity
// ❌ VULNERABLE: Migration Data Loss
func OpenDB(logger logger.Logger, targetVersion int64, opts Options) (*DB, error) {
    [...]
    if !opts.ReadOnly {
        fileLock, err = LockFile(filepath.Join(opts.Dir, LockFileName))
        if err != nil {
            return nil, fmt.Errorf("fail to lock db: %w", err)
        }
        [...]
    }
    [...]
}
```

#### Pattern 3: Deployment Parameter Error

**Frequency**: 1/7 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: veToken Finance

This bug report describes an issue with the deployment scripts for G-Uni tokens, which are not up to date. This issue could have an impact on the address of G-Uni tokens. As a proof of concept, for agEUR/USDC, the address is 0xedecb43233549c51cc3268b5de840239787ad56c instead of 0x2bD9F7974Bc0E4Cb19B

#### Pattern 4: Module Registration Missing

**Frequency**: 1/7 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: ZetaChain Cross-Chain

This bug report discusses an issue found in the `codec.go` file of the `node/x/authority` module in the Cosmos SDK. The `codec.go` file is responsible for registering message and interface types with the Amino codec and Protobuf interface registry. However, two message types, `AddAuthorization` and 

**Example 4.1** [MEDIUM] — ZetaChain Cross-Chain
Source: `m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md`
```solidity
// ❌ VULNERABLE: Module Registration Missing
func RegisterCodec(cdc *codec.LegacyAmino) {
	cdc.RegisterConcrete(&MsgUpdatePolicies{}, "authority/UpdatePolicies", nil)
	cdc.RegisterConcrete(&MsgUpdateChainInfo{}, "authority/UpdateChainInfo", nil)
	cdc.RegisterConcrete(&MsgRemoveChainInfo{}, "authority/RemoveChainInfo", nil)
}

func RegisterInterfaces(registry cdctypes.InterfaceRegistry) {
	registry.RegisterImplementations((*sdk.Msg)(nil),
		&MsgUpdatePolicies{},
		&MsgUpdateChainInfo{},
		&MsgRemoveChainInfo{},
	)

	msgservice.RegisterMsgServiceDesc(registry, &_Msg_serviceDesc)
}
```

#### Pattern 5: Storage Gap Error

**Frequency**: 1/7 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Forta Delegated Staking

The Forta staking system uses upgradeable proxies for its deployment strategy. To avoid storage collisions between contract versions during upgrades, `uint256[] private __gap` array variables are introduced to create a storage buffer. The `__gap` variable is present in the `BaseComponentUpgradeable`

**Example 5.1** [MEDIUM] — Forta Delegated Staking
Source: `storage-gap-variables-slightly-off-from-the-intended-size-fixed.md`
```solidity
// ❌ VULNERABLE: Storage Gap Error
uint64 private _withdrawalDelay;

    // treasury for slashing
    address private _treasury;
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 2 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 7
- HIGH severity: 2 (28%)
- MEDIUM severity: 5 (71%)
- Unique protocols affected: 7
- Independent audit firms: 6
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

> `upgrade`, `migration`, `initialization`, `storage-gap`, `proxy`, `deployment`, `module-registration`, `genesis`, `state-migration`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
