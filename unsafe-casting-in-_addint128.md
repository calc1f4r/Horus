---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53549
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Unsafe Casting in _addInt128()

### Overview

See description below for full details.

### Original Finding Content

## Description

The _addInt128() function can silently overflow due to unsafe casting, resulting in an attacker being able to allocate more magnitude than intended.

The _addInt128() function can overflow due to unsafe casting from `int128` to `uint128` when the casted value is negative, and from `uint128` to `uint64`.

## AllocationManager.sol::_addInt128()

```solidity
function _addInt128(uint64 a, int128 b) internal pure returns (uint64) {
    return uint64(uint128(int128(uint128(a)) + b));
}
```

This allows an attacker to manipulate their `currentMagnitude` to be out of bounds and higher than their `maxMagnitude`. This actual vulnerability is rated high impact and likelihood as it allows the operator to allocate without limits. However, this issue is rated as informational severity in the report, as it was made aware to the testing team by the EigenLayer team during the engagement.

## Recommendations

Consider using safe casting and reverting in the case of an underflow in _addInt128().

## Resolution

The EigenLayer team has used the SafeCastUpgradeable library to ensure that the _addInt128() function does not overflow when casting to `uint64`. This issue has been resolved in PR #1027.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

