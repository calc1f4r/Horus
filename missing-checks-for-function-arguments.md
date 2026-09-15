---
# Core Classification
protocol: Matter Labs Guardian Recovery Validator Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56748
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/matter-labs-guardian-recovery-validator-audit
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Missing Checks for Function Arguments

### Overview

See description below for full details.

### Original Finding Content

When operations with `address` parameters are performed, it is crucial to ensure that the address is not set to zero. Setting an address to zero is problematic because it has special burn/renounce semantics. Thus, this action should be handled by a separate function to prevent accidental loss of access during value or ownership transfers.

Within `GuardianRecoveryValidator`, multiple instances of missing zero address checks were identified:

* The [`_webAuthValidator`](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/validators/GuardianRecoveryValidator.sol#L77) operation
* The [`newGuardian`](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/validators/GuardianRecoveryValidator.sol#L117) operation
* The [`accountToGuard`](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/validators/GuardianRecoveryValidator.sol#L171) operation
* The [`accountToRecover`](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/validators/GuardianRecoveryValidator.sol#L208) operation

Likewise, in the [`addValidationKey` function](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/validators/WebAuthValidator.sol#L94) of `WebAuthValidator`, there is no validation for `credentialId` and `originDomain`, allowing them to be empty or have arbitrary lengths. Furthermore, the [constructor](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/c7714c0fe0a33a23acce5aa20355f088d330b4f7/src/AAFactory.sol#L32-L35) of `AAFactory` currently lacks validation checks for its input parameters. This absence of validation may cause unexpected contract reverts during operation. For instance, if `_beaconProxyBytecodeHash` is set to an empty value, the `ContractDeployer` will consistently revert, rendering the factory unusable and requiring redeployment.

Consider adding appropriate validation checks for the arguments before assigning them to a state variable.

***Update:** Resolved in [pull request #349](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/349) at commit [b65d4cf](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/349/commits/b65d4cff6a6120a7dcd6dd71c70e7abdfb20a5a9) and [pull request #333](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/333) at commit [c9c8e79](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/333/commits/c9c8e79bf03f286b2adbf8454084aaf6eabd7608).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Matter Labs Guardian Recovery Validator Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/matter-labs-guardian-recovery-validator-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

