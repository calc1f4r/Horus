---
# Core Classification
protocol: HypurrFi_2025-02-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55469
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `DeployUsdxlUtils`: Wrong setting for mint limits

### Overview


The report states that two functions, `_addUsdxlATokenAsEntity()` and `_addUsdxlFlashMinterAsEntity()`, are setting the mint limit to 1 billion instead of 100 million. This can cause issues with the functioning of the code. The recommended solution is to use 1e26 instead of 1e27 to set it to 100 million.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Functions `_addUsdxlATokenAsEntity()` and `_addUsdxlFlashMinterAsEntity()` set mint limit as 1B instead of 100mil:

```solidity
   function _addUsdxlATokenAsEntity(IDeployConfigTypes.HypurrDeployRegistry memory deployRegistry)
        internal
    {
        // pull aToken proxy from reserves config
        _getUsdxlToken().addFacilitator(
          address(_getUsdxlATokenProxy()),
          'HypurrFi Market Loans', // entity label
          1e27 // entity mint limit (100mil)
        );
    }

    function _addUsdxlFlashMinterAsEntity(IDeployConfigTypes.HypurrDeployRegistry memory deployRegistry)
        internal
    {
      _getUsdxlToken().addFacilitator(
        address(flashMinter),
        'HypurrFi Market Flash Loans', // entity label
        1e27 // entity mint limit (100mil)
      );
    }
```

## Recommendations

Use 1e26 instead of 1e27 to set it to 100mil

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | HypurrFi_2025-02-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

