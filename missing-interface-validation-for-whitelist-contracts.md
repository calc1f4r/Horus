---
# Core Classification
protocol: Managed Optimistic Oracle Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62057
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/managed-optimistic-oracle-audit
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

Missing Interface Validation for Whitelist Contracts

### Overview

See description below for full details.

### Original Finding Content

The [`ManagedOptimisticOracleV2`](https://github.com/UMAprotocol/managed-oracle/blob/fc03083eca91c880efa8918c6d9532af9362f00d/src/optimistic-oracle-v2/implementation/ManagedOptimisticOracleV2.sol) contract includes several functions that accept external contract addresses expected to implement the `DisableableAddressWhitelistInterface`, such as the [`setDefaultProposerWhitelist`](https://github.com/UMAprotocol/managed-oracle/blob/fc03083eca91c880efa8918c6d9532af9362f00d/src/optimistic-oracle-v2/implementation/ManagedOptimisticOracleV2.sol#L216), [`setRequesterWhitelist`](https://github.com/UMAprotocol/managed-oracle/blob/fc03083eca91c880efa8918c6d9532af9362f00d/src/optimistic-oracle-v2/implementation/ManagedOptimisticOracleV2.sol#L225), and [`requestManagerSetProposerWhitelist`](https://github.com/UMAprotocol/managed-oracle/blob/fc03083eca91c880efa8918c6d9532af9362f00d/src/optimistic-oracle-v2/implementation/ManagedOptimisticOracleV2.sol#L304) functions. However, these functions do not verify whether the provided addresses actually implement the expected interface, which can result in runtime errors or incorrect behavior if an invalid contract is passed.

Consider supporting the [ERC-165 standard](https://eips.ethereum.org/EIPS/eip-165) in both the `AddressWhitelist` and `DisableableAddressWhitelist` contracts to facilitate safe and standardized interface detection. In addition, consider enforcing interface compliance through runtime checks to ensure that the provided whitelist contracts implement the `DisableableAddressWhitelistInterface`.

***Update:** Resolved in [pull request #17](https://github.com/UMAprotocol/managed-oracle/pull/17) at commit [7bb517c](https://github.com/UMAprotocol/managed-oracle/pull/17/commits/7bb517c71a94bd6d2aef2b661efb3e0e79de75dd). The `DisableableAddressWhitelist` contract was replaced with `DisabledAddressWhitelist`, thereby changing the implementation from an owner-controlled toggle for the enforcement of the list to a hard-coded implementation that can be set in the `ManagedOptimisticOracleV2` contract. Both the `DisabledAddressWhitelist` and `AddressWhitelist` contract now extend `ERC165` while `ManagedOptimisticOracleV2` performs runtime checks whenever a whitelist is set.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Managed Optimistic Oracle Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/managed-optimistic-oracle-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

