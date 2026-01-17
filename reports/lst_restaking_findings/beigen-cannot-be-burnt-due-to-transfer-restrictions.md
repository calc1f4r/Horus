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
solodit_id: 53582
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
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

bEIGEN Cannot Be Burnt Due To Transfer Restrictions

### Overview

See description below for full details.

### Original Finding Content

## Description

The `burn()` function cannot be called by non-whitelisted accounts if transfer restrictions are enabled, preventing users from burning their bEIGEN tokens.

The `burn()` function calls `_beforeTokenTransfer()`, which has the following check:

```solidity
// if transfer restrictions are enabled
if (block.timestamp <= transferRestrictionsDisabledAfter) {
    // if both from and to are not whitelisted
    require(
        allowedFrom[from] || allowedTo[to] || from == address(0),
        "BackingEigen._beforeTokenTransfer: from or to must be whitelisted"
    );
}
```

Since the user is not in the `allowedFrom` mapping, burning bEIGEN tokens is disabled as long as transfer restrictions are enabled.

## Recommendations

- If this behavior is intentional, consider adding documentation and Natspec comments to the `burn()` function to clarify this behavior.
- If this behavior is not intentional, consider adding another condition for `to == address(0)` in the `require()` function to allow users to burn their bEIGEN tokens:

```solidity
// if transfer restrictions are enabled
if (block.timestamp <= transferRestrictionsDisabledAfter) {
    // if both from and to are not whitelisted
    require(
        allowedFrom[from] || allowedTo[to] || from == address(0) || to == address(0),
        "BackingEigen._beforeTokenTransfer: from or to must be whitelisted"
    );
}
```

## Resolution

The EigenLayer team has acknowledged this issue with the following comment:

> We are fine with this behavior as transfer restrictions will be lifted before the token upgrade is completed.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_EigenLabs_EigenLayer_EIGEN_Rewards_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

