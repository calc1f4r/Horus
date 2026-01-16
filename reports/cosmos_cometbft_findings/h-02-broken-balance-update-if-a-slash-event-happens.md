---
# Core Classification
protocol: Karak-June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38490
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Broken balance update if a slash event happens

### Overview


This bug report describes a problem where the value of `creditedNodeETH` is not being properly updated when a function called `_transferToSlashStore()` is executed. This results in an incorrect value for `creditedNodeETH` which causes another function called `_startSnapshot()` to fail. The severity of this bug is considered medium and the likelihood of it occurring is high. To fix this issue, the value of `creditedNodeETH` should be updated in the `_transferToSlashStore()` function.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When `_transferToSlashStore()` is called the slash ETH amount is transferred from the native node contract's balance but the code doesn't decrease the value of the `creditedNodeETH` so its value would be higher than it should be and `_startSnapshot()` would revert because of underflow:

```solidity
        // Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```

## Recommendations

Update the value of the `creditedNodeETH` in `_transferToSlashStore()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Karak-June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

