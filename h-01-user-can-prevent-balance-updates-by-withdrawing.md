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
solodit_id: 38489
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-01] User can prevent balance updates by withdrawing

### Overview


This bug report describes a problem where the value of `creditedNodeETH` is not being updated correctly when the `finishWithdraw()` function is called. This can lead to an incorrect balance for users and can also be exploited by malicious users to prevent balance updates. The report recommends updating the value of `creditedNodeETH` in the `finishWithdraw()` function to fix the issue. The severity of this bug is medium and the likelihood of it occurring is high.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When `finishWithdraw()` is called the ETH amount is transferred from the native node contract's balance but the code doesn't decrease the value of the `creditedNodeETH` so its value would be higher than it should be and `_startSnapshot()` would revert because of underflow:

```solidity
        // Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```

The issue would happen to all users who withdraw tokens and malicious users can do it intentionally to prevent balance updates (when they are slashed in the beacon chain)

## Recommendations

Update the value of the `creditedNodeETH` in `finishWithdraw()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
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

