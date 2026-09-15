---
# Core Classification
protocol: Linea Rollup Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45049
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/12/linea-rollup-update/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Vladislav Yaroshuk
                        
  - Rai Yang
---

## Vulnerability Title

Missing Validation for defaultAdmin in Contract Initialization ✓ Fixed

### Overview


This bug report is about an issue with the `initialize` function in two contracts, `LineaRollup` and `TokenBridge`. The report states that the contracts are granting the `DEFAULT_ADMIN_ROLE` role to a designated account, but there is no check to ensure that this account is not a zero address. This could potentially compromise the permission management system and leave the contracts vulnerable to unauthorized access. The report recommends adding a validation check for non-zero addresses in the `initialize` function for both contracts. The bug has been fixed in a recent pull request.

### Original Finding Content

#### Resolution

The Linea team has fixed the finding in [PR 374](https://github.com/Consensys/linea-monorepo/pull/374)


#### Description

In the `initialize` function of both the `LineaRollup` and `TokenBridge` contract, the `DEFAULT_ADMIN_ROLE` role of the contract is granted to `_initializationData.defaultAdmin`, which is presumed to be security council account. However there is no validation checks to ensure that `_initializationData.defaultAdmin` is not a zero address. The absence of such validation could potentially result in the contracts being initialized without a designated Admin, compromising the permission management system within these contracts and leaving the contracts vulnerable to unauthorized access and manipulation.

#### Examples

**contracts/contracts/LineaRollup.sol:L129**

```
_grantRole(DEFAULT_ADMIN_ROLE, _initializationData.defaultAdmin);

```

**contracts/contracts/tokenBridge/TokenBridge.sol:L155**

```
_grantRole(DEFAULT_ADMIN_ROLE, _initializationData.defaultAdmin);

```
#### Recommendation

Add validation of non zero address for `_initializationData.defaultAdmin` in the `initialize` function for both the `LineaRollup` and `TokenBridge` contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Rollup Update |
| Report Date | N/A |
| Finders |  Vladislav Yaroshuk
                        , Rai Yang |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/12/linea-rollup-update/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

