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
solodit_id: 45048
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

Missing Validation for chainID in TokenBridge Contract ✓ Fixed

### Overview


The Linea team has fixed a problem in their `TokenBridge` contract that could cause incorrect or unintended operations. The issue was in the `initialize` function, where the source and target chain IDs were not checked to make sure they were different and not set to zero. This could lead to errors in the bridge's functionality. The recommendation is to add validation for the chain IDs to prevent this issue from occurring. The fix for this issue can be found in [PR 380](https://github.com/Consensys/linea-monorepo/pull/380).

### Original Finding Content

#### Resolution

The Linea team has fixed the finding in [PR 380](https://github.com/Consensys/linea-monorepo/pull/380).


#### Description

In the `initialize` function of the `TokenBridge` contract, the source `chainID`(`_initializationData.sourceChainId`) and target chain ID (`_initializationData.targetChainId`) of the bridge is not validated to be distinct and neither is set to zero. As a result, incorrect chain ID will be set or identical chain IDs for the source and target chains, which fundamentally compromises the functionality of the bridge by allowing for the possibility of erroneous or unintended bridge operations.

#### Examples

**contracts/contracts/tokenBridge/TokenBridge.sol:L160-L161**

```
sourceChainId = _initializationData.sourceChainId;
targetChainId = _initializationData.targetChainId;

```
#### Recommendation

Add the validation for source and target chain ID to ensure they are distinct and non-zero.

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

