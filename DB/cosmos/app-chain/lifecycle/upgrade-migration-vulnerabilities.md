---
protocol: generic
chain: cosmos
category: lifecycle
vulnerability_type: upgrade_migration_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: lifecycle_logic

primitives:
  - upgrade_error
  - migration_failure
  - init_error
  - storage_gap
  - module_registration
  - genesis_error
  - deployment_param
  - state_export
  - version_compat

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - lifecycle
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Lifecycle Upgrade Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Improper Implementation of Cosmos SDK Upgrade Procedures | `reports/cosmos_cometbft_findings/improper-implementation-of-cosmos-sdk-upgrade-procedures.md` | HIGH | Halborn |
| [M-04] Incorrect names provided in `RegisterConcrete` calls  | `reports/cosmos_cometbft_findings/m-04-incorrect-names-provided-in-registerconcrete-calls-break-legacyamino-signin.md` | MEDIUM | Code4rena |
| Transactions can occur during the upgrade process | `reports/cosmos_cometbft_findings/transactions-can-occur-during-the-upgrade-process.md` | MEDIUM | TrailOfBits |

### Lifecycle Migration Failure
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| LoadVersion Failure On History Queries | `reports/cosmos_cometbft_findings/loadversion-failure-on-history-queries.md` | MEDIUM | OtterSec |
| Transactions can occur during the upgrade process | `reports/cosmos_cometbft_findings/transactions-can-occur-during-the-upgrade-process.md` | MEDIUM | TrailOfBits |

### Lifecycle Init Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Denial Of Slashing | `reports/cosmos_cometbft_findings/denial-of-slashing.md` | HIGH | OtterSec |
| [M-03] `xfeemarket` module is not wired up, resulting in non | `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md` | MEDIUM | Code4rena |
| Missing _grantRole for GOVERNANCE_ROLE will prevent calling  | `reports/cosmos_cometbft_findings/missing-_grantrole-for-governance_role-will-prevent-calling-of-onlygovernor-func.md` | HIGH | Spearbit |
| Missing _grantRole for KEEPER_ROLE will prevent calling of c | `reports/cosmos_cometbft_findings/missing-_grantrole-for-keeper_role-will-prevent-calling-of-critical-keeper-funct.md` | HIGH | Spearbit |
| Missing Balance Deduction in Unstaking Functions Allows Cont | `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md` | HIGH | Quantstamp |

### Lifecycle Storage Gap
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Storage gap variables slightly off from the intended size ✓  | `reports/cosmos_cometbft_findings/storage-gap-variables-slightly-off-from-the-intended-size-fixed.md` | MEDIUM | ConsenSys |

### Lifecycle Module Registration
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Add/remove authorization messages are not usable due to miss | `reports/cosmos_cometbft_findings/m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md` | MEDIUM | Sherlock |
| Missing Message Type Registrations in Regulation Module | `reports/cosmos_cometbft_findings/missing-message-type-registrations-in-regulation-module.md` | HIGH | Halborn |

### Lifecycle Genesis Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incomplete Zero-Height Genesis Preparation in Allora Network | `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md` | MEDIUM | Sherlock |

### Lifecycle Deployment Param
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-30] Incorrect deployment parameters | `reports/cosmos_cometbft_findings/m-30-incorrect-deployment-parameters.md` | MEDIUM | Code4rena |

### Lifecycle State Export
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] `xfeemarket` module is not wired up, resulting in non | `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md` | MEDIUM | Code4rena |
| Incomplete Zero-Height Genesis Preparation in Allora Network | `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md` | MEDIUM | Sherlock |

### Lifecycle Version Compat
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deprecated GetSigners Usage | `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md` | HIGH | OtterSec |
| Incompatibility with blobs lead to halt of block processing | `reports/cosmos_cometbft_findings/incompatibility-with-blobs-lead-to-halt-of-block-processing.md` | HIGH | Halborn |

---

# Upgrade Migration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Upgrade Migration Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Lifecycle Upgrade Error](#1-lifecycle-upgrade-error)
2. [Lifecycle Migration Failure](#2-lifecycle-migration-failure)
3. [Lifecycle Init Error](#3-lifecycle-init-error)
4. [Lifecycle Storage Gap](#4-lifecycle-storage-gap)
5. [Lifecycle Module Registration](#5-lifecycle-module-registration)
6. [Lifecycle Genesis Error](#6-lifecycle-genesis-error)
7. [Lifecycle Deployment Param](#7-lifecycle-deployment-param)
8. [Lifecycle State Export](#8-lifecycle-state-export)
9. [Lifecycle Version Compat](#9-lifecycle-version-compat)

---

## 1. Lifecycle Upgrade Error

### Overview

Implementation flaw in lifecycle upgrade error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: The Scallop Bank chain has a problem with its regulation module not following the recommended upgrade procedures for the Cosmos SDK. The module's ConsensusVersion() method is not properly managed and could cause issues during upgrades. This is because the method returns a hard-coded value and there 

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle upgrade error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle upgrade error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Improper Implementation of Cosmos SDK Upgrade Procedures** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/improper-implementation-of-cosmos-sdk-upgrade-procedures.md`
```go
func (AppModule) ConsensusVersion() uint64 { return 2 }
```

**Example 2: [M-04] Incorrect names provided in `RegisterConcrete` calls break `LegacyAmino` ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-incorrect-names-provided-in-registerconcrete-calls-break-legacyamino-signin.md`
```
// Vulnerable pattern from Canto:
One of the breaking changes introduced with the Cosmos SDK v0.50.x upgrade is [a change in the codec used for Amino JSON
(de)serialization](https://github.com/cosmos/cosmos-sdk/blob/release/v0.50.x/UPGRADING.md#protobuf). To ensure the
new codec behaves as the abandoned one did, the team added `amino.name` tags to the `message` types defined in the Canto
modules' ".proto" files.

There are however many instances where these tags are inconsistent with the `RegisterConcrete` calls made by the
in-s
```

**Example 3: Transactions can occur during the upgrade process** [MEDIUM]
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
// Addresses: Implementation flaw in lifecycle upgrade error logic allows exploitation through missing validation,
func secureLifecycleUpgradeError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: AppChain Modules, Canto, Numerai
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Lifecycle Migration Failure

### Overview

Implementation flaw in lifecycle migration failure logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: A bug has been reported in the scStore function of the DB instance. The issue arises when the DB options do not include the Readonly flag, causing the LockFile to be locked by the DB instance opened for cms. This results in the LoadVersion function always failing alongside the queries. To fix this i

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle migration failure logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle migration failure in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: LoadVersion Failure On History Queries** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/loadversion-failure-on-history-queries.md`
```go
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

**Example 2: Transactions can occur during the upgrade process** [MEDIUM]
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
// Addresses: Implementation flaw in lifecycle migration failure logic allows exploitation through missing validat
func secureLifecycleMigrationFailure(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: Numerai, Sei DB
- **Validation Strength**: Moderate (2 auditors)

---

## 3. Lifecycle Init Error

### Overview

Implementation flaw in lifecycle init error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 4, MEDIUM: 1.

> **Key Finding**: This report discusses a vulnerability in the verifyDoubleSigning function, which can be exploited by a malicious operator to evade slashing. This vulnerability is due to the linear complexity of the function, which can be increased indefinitely by repeatedly calling the updateDelegation function. Th

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle init error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle init error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Denial Of Slashing** [HIGH]
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

**Example 2: [M-03] `xfeemarket` module is not wired up, resulting in non-working CLI command** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md`
```go
308: keys := storetypes.NewKVStoreKeys(
309: 	authtypes.StoreKey, banktypes.StoreKey, stakingtypes.StoreKey, crisistypes.StoreKey,
310: 	minttypes.StoreKey, distrtypes.StoreKey, slashingtypes.StoreKey,
311: 	govtypes.StoreKey, paramstypes.StoreKey, consensusparamtypes.StoreKey, upgradetypes.StoreKey, feegrant.StoreKey,
312: 	evidencetypes.StoreKey,
313: 	circuittypes.StoreKey,
314: 	authzkeeper.StoreKey,
315: 	nftkeeper.StoreKey,
316: 	group.StoreKey,
317: 	// non sdk store keys
318: 	capabilitytypes.StoreKey, ibcexported.StoreKey, ibctransfertypes.StoreKey, ibcfeetypes.StoreKey,
319: 	wasmtypes.StoreKey,
320: 	ratelimittypes.StoreKey,
321: 	tokenfactorytypes.StoreKey, taxtypes.StoreKey,
322: 	ibchookstypes.StoreKey,
323: 	feemarkettypes.StoreKey, oracletypes.StoreKey, marketmaptypes.StoreKey,
324: )
```

**Example 3: Missing _grantRole for GOVERNANCE_ROLE will prevent calling of onlyGovernor func** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-_grantrole-for-governance_role-will-prevent-calling-of-onlygovernor-func.md`
```
// Vulnerable pattern from Infrared Contracts:
## Upgrades

**Severity:** Critical Risk  
**Context:** (No context files were provided by the reviewer)  
**Summary:** Missing the granting of role for `GOVERNANCE_ROLE` to any privileged address will prevent calling of onlyGovernor functions including upgrades across InfraredBERA contracts along with Voter and BribeCollector core contracts of Infrared.
```

**Example 4: Missing Balance Deduction in Unstaking Functions Allows Contract Drainage and Lo** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `4a45a4a`.

![Image 26: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `f647099b7988fa4d01fac6a9f3481d25e748527a`. The client provided the following explanation:

> The vulnerability in the unstaking functions was fixed by implementing proper balance deduction and
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle init error logic allows exploitation through missing validation, in
func secureLifecycleInitError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 1
- **Affected Protocols**: MANTRA, Ethos EVM, Infrared Contracts, Sapien
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Lifecycle Storage Gap

### Overview

Implementation flaw in lifecycle storage gap logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The Forta staking system uses upgradeable proxies for its deployment strategy. To avoid storage collisions between contract versions during upgrades, `uint256[] private __gap` array variables are introduced to create a storage buffer. The `__gap` variable is present in the `BaseComponentUpgradeable`

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle storage gap logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle storage gap in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Storage gap variables slightly off from the intended size ✓ Fixed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/storage-gap-variables-slightly-off-from-the-intended-size-fixed.md`
```go
uint64 private _withdrawalDelay;

    // treasury for slashing
    address private _treasury;
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle storage gap logic allows exploitation through missing validation, i
func secureLifecycleStorageGap(ctx sdk.Context) error {
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
- **Affected Protocols**: Forta Delegated Staking
- **Validation Strength**: Single auditor

---

## 5. Lifecycle Module Registration

### Overview

Implementation flaw in lifecycle module registration logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue found in the `codec.go` file of the `node/x/authority` module in the Cosmos SDK. The `codec.go` file is responsible for registering message and interface types with the Amino codec and Protobuf interface registry. However, two message types, `AddAuthorization` and 

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle module registration logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle module registration in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Add/remove authorization messages are not usable due to missing registration** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-7-addremove-authorization-messages-are-not-usable-due-to-missing-registration.md`
```go
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

**Example 2: Missing Message Type Registrations in Regulation Module** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-message-type-registrations-in-regulation-module.md`
```go
func RegisterInterfaces(registry types.InterfaceRegistry) {

    registry.RegisterImplementations((*sdk.Msg)(nil),

        &MsgTransferAuthority{},

        &MsgAllowAddress{},

        &MsgDisallowAddress{},

    )

    msgservice.RegisterMsgServiceDesc(registry, &_Msg_serviceDesc)

}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle module registration logic allows exploitation through missing valid
func secureLifecycleModuleRegistration(ctx sdk.Context) error {
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
- **Affected Protocols**: AppChain Modules, ZetaChain Cross-Chain
- **Validation Strength**: Moderate (2 auditors)

---

## 6. Lifecycle Genesis Error

### Overview

Implementation flaw in lifecycle genesis error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: Issue M-10 is a bug in the Allora Network's implementation of prepForZeroHeightGenesis, which is used to export the state of the network at a specific height. The current implementation is missing several key steps that are present in the reference implementation, potentially leading to inconsistent

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle genesis error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle genesis error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Incomplete Zero-Height Genesis Preparation in Allora Network** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md`
```
// Vulnerable pattern from Allora:
Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/43
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle genesis error logic allows exploitation through missing validation,
func secureLifecycleGenesisError(ctx sdk.Context) error {
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
- **Affected Protocols**: Allora
- **Validation Strength**: Single auditor

---

## 7. Lifecycle Deployment Param

### Overview

Implementation flaw in lifecycle deployment param logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report describes an issue with the deployment scripts for G-Uni tokens, which are not up to date. This issue could have an impact on the address of G-Uni tokens. As a proof of concept, for agEUR/USDC, the address is 0xedecb43233549c51cc3268b5de840239787ad56c instead of 0x2bD9F7974Bc0E4Cb19B

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle deployment param logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle deployment param in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: [M-30] Incorrect deployment parameters** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-30-incorrect-deployment-parameters.md`
```
// Vulnerable pattern from veToken Finance:
_Submitted by Picodes_

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/migrations/25_deploy_angle_pools.js#L68>

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/migrations/25_deploy_angle_pools.js#L80>

### Impact

The address of G-Uni tokens in the deployment scripts are not up to date.

### Proof of Concept

For example for agEUR/USDC it is 0xedecb43233549c51cc3268b5de840239787ad56c and not 0x2bD9F7974Bc
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle deployment param logic allows exploitation through missing validati
func secureLifecycleDeploymentParam(ctx sdk.Context) error {
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
- **Affected Protocols**: veToken Finance
- **Validation Strength**: Single auditor

---

## 8. Lifecycle State Export

### Overview

Implementation flaw in lifecycle state export logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This report discusses a bug in a Cosmos SDK app where a custom module called `xfeemarket` is not properly registered. This results in the module's CLI commands not being available and the module's state not being exported or initialized. This prevents the module from being fully functional, particul

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle state export logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle state export in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: [M-03] `xfeemarket` module is not wired up, resulting in non-working CLI command** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md`
```go
308: keys := storetypes.NewKVStoreKeys(
309: 	authtypes.StoreKey, banktypes.StoreKey, stakingtypes.StoreKey, crisistypes.StoreKey,
310: 	minttypes.StoreKey, distrtypes.StoreKey, slashingtypes.StoreKey,
311: 	govtypes.StoreKey, paramstypes.StoreKey, consensusparamtypes.StoreKey, upgradetypes.StoreKey, feegrant.StoreKey,
312: 	evidencetypes.StoreKey,
313: 	circuittypes.StoreKey,
314: 	authzkeeper.StoreKey,
315: 	nftkeeper.StoreKey,
316: 	group.StoreKey,
317: 	// non sdk store keys
318: 	capabilitytypes.StoreKey, ibcexported.StoreKey, ibctransfertypes.StoreKey, ibcfeetypes.StoreKey,
319: 	wasmtypes.StoreKey,
320: 	ratelimittypes.StoreKey,
321: 	tokenfactorytypes.StoreKey, taxtypes.StoreKey,
322: 	ibchookstypes.StoreKey,
323: 	feemarkettypes.StoreKey, oracletypes.StoreKey, marketmaptypes.StoreKey,
324: )
```

**Example 2: Incomplete Zero-Height Genesis Preparation in Allora Network** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-incomplete-zero-height-genesis-preparation-in-allora-network.md`
```
// Vulnerable pattern from Allora:
Source: https://github.com/sherlock-audit/2024-06-allora-judging/issues/43
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle state export logic allows exploitation through missing validation, 
func secureLifecycleStateExport(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: MANTRA, Allora
- **Validation Strength**: Moderate (2 auditors)

---

## 9. Lifecycle Version Compat

### Overview

Implementation flaw in lifecycle version compat logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: The bug report discusses an issue with the GetSigners() method in the MsgSubmitConsumerMisbehaviour and MsgSubmitConsumerDoubleVoting messages. This method is no longer supported and is incompatible with newer versions of the Cosmos SDK. The problem arises because the Cosmos SDK has evolved and now 

### Vulnerability Description

#### Root Cause

Implementation flaw in lifecycle version compat logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies lifecycle version compat in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to lifecycle operations

### Vulnerable Pattern Examples

**Example 1: Deprecated GetSigners Usage** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deprecated-getsigners-usage.md`
```go
// File: ethos-chain/x/ccv/provider/types/msg.go
func (msg MsgSubmitConsumerMisbehaviour) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}

func (msg MsgSubmitConsumerDoubleVoting) GetSigners() []sdk.AccAddress {
    addr, err := sdk.AccAddressFromBech32(msg.Submitter)
    if err != nil {
        // same behavior as in cosmos-sdk
        panic(err)
    }
    return []sdk.AccAddress{addr}
}
```

**Example 2: Incompatibility with blobs lead to halt of block processing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incompatibility-with-blobs-lead-to-halt-of-block-processing.md`
```go
err = retryForever(ctx, func(ctx context.Context) (bool, error) {
	status, err := pushPayload(ctx, s.engineCl, payload)
	if err != nil || isUnknown(status) {
		// We need to retry forever on networking errors, but can't easily identify them, so retry all errors.
		log.Warn(ctx, "Verifying proposal failed: push new payload to evm (will retry)", err,
			"status", status.Status)

		return false, nil // Retry
	} else if invalid, err := isInvalid(status); invalid {
		return false, errors.Wrap(err, "invalid payload, rejecting proposal") // Don't retry
	} else if isSyncing(status) {
		// If this is initial sync, we need to continue and set a target head to sync to, so don't retry.
		log.Warn(ctx, "Can't properly verifying proposal: evm syncing", err,
			"payload_height", payload.Number)
	}

	return true, nil // We are done, don't retry.
})
if err != nil {
	return nil, err
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in lifecycle version compat logic allows exploitation through missing validation
func secureLifecycleVersionCompat(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: Layer 1 Assessment, Ethos Cosmos
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Lifecycle Upgrade Error
grep -rn 'lifecycle|upgrade|error' --include='*.go' --include='*.sol'
# Lifecycle Migration Failure
grep -rn 'lifecycle|migration|failure' --include='*.go' --include='*.sol'
# Lifecycle Init Error
grep -rn 'lifecycle|init|error' --include='*.go' --include='*.sol'
# Lifecycle Storage Gap
grep -rn 'lifecycle|storage|gap' --include='*.go' --include='*.sol'
# Lifecycle Module Registration
grep -rn 'lifecycle|module|registration' --include='*.go' --include='*.sol'
# Lifecycle Genesis Error
grep -rn 'lifecycle|genesis|error' --include='*.go' --include='*.sol'
# Lifecycle Deployment Param
grep -rn 'lifecycle|deployment|param' --include='*.go' --include='*.sol'
# Lifecycle State Export
grep -rn 'lifecycle|state|export' --include='*.go' --include='*.sol'
# Lifecycle Version Compat
grep -rn 'lifecycle|version|compat' --include='*.go' --include='*.sol'
```

## Keywords

`allora`, `appchain`, `authorization`, `blobs`, `block`, `break`, `calling`, `calls`, `compat`, `cosmos`, `denial`, `deployment`, `deprecated`, `during`, `error`, `export`, `failure`, `fixed`, `from`, `functions`, `gap`, `genesis`, `getsigners`, `halt`, `history`, `implementation`, `improper`, `including`, `incompatibility`, `incomplete`
