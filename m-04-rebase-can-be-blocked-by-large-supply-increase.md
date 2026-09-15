---
# Core Classification
protocol: stHYPE_2025-10-13
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63216
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
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

[M-04] `rebase()` can be blocked by large supply increase

### Overview


The bug report discusses a problem with the `rebase()` function in the `Overseer` contract. This function reverts when the calculated APR change since the last rebase exceeds a predefined threshold (`aprThresholdBps`). This threshold is limited to 10,000 basis points (100%), which means that a large increase in the stHYPE supply can cause the `rebase()` function to be blocked for a long time or even permanently. This can happen even if the increase in supply is caused by an attacker. The report recommends removing the restriction on the maximum value of the `aprThresholdBps` parameter to allow governance to prevent the `rebase()` function from being blocked.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

`Overseer.rebase()` reverts when the calculated APR change since the last rebase exceeds a predefined threshold (`aprThresholdBps`).

```solidity
        int256 aprChange = _calculateApr(timeElapsed, currentSupply, newSupply);

        if (aprChange > 0) {
            if (aprChange + 1 >= int256(aprThresholdBps)) {
                revert AprTooHigh(aprChange + 1, aprThresholdBps);
```

As `aprThresholdBps` is limited to 10_000 basis points (100%), a large increase in the stHYPE supply might cause the `rebase()` function to be blocked for a long time, or even permanently.

For example, with a rebase interval of one day, an increase by 0.28% of the stHYPE supply will cause the APR to exceed 100% and the `rebase()` function to revert. And the lower the rebase frequency, the smaller the increase in stHYPE supply is required to block the `rebase()` function. While an attacker would be required to donate that amount, if the stHYPE supply decreases over time (e.g., due to users burning their tokens), the amount required to block the `rebase()` function also decreases.

The result would be that the protocol would not be able to adjust the stHYPE supply for the accrued staking rewards.

## Recommendations

Remove the restriction for the maximum value of the `aprThresholdBps` parameter in the `setAprThresholdBps()` function. This will allow the governance to prevent the `rebase()` function from being blocked by setting a sufficiently high threshold, which, combined with a large `syncInterval` value, can process a high increase in the stHYPE supply without causing a major impact.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | stHYPE_2025-10-13 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

