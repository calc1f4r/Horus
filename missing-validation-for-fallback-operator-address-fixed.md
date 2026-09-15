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
solodit_id: 45047
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

Missing Validation for Fallback Operator Address ✓ Fixed

### Overview


The Linea team has fixed a bug in their code related to the `initialize` function in the `LineaRollup` contract. This bug caused the fallback operator address to not be properly validated, which could result in the fallback operator failing to work if Linea stops submitting blobs and finalizing for 6 months. The team has recommended adding a validation for the fallback operator address to ensure it is non-zero. This issue has been resolved in a pull request (PR 374).

### Original Finding Content

#### Resolution

The Linea team has fixed the finding in [PR 374](https://github.com/Consensys/linea-monorepo/pull/374).


#### Description

In the `initialize` function of the `LineaRollup` contract, there is no validation for fallback operator address(`_initializationData.fallbackOperator`) to be non zero. As a result, the fall back operator would fail to work in case of Linea stops submitting blobs and finalizing for 6 months.

#### Examples

**contracts/contracts/LineaRollup.sol:L135**

```
fallbackOperator = _initializationData.fallbackOperator;

```
#### Recommendation

Add the missing non-zero validation for fallback operator address.

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

