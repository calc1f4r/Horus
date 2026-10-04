---
# Core Classification
protocol: Elytra_2025-07-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63577
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
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

[M-02] Price change limit can cause system DoS

### Overview


This bug report is about a problem in the Elytra system where the price of a share can drop by 10% and block users from depositing or withdrawing their assets. The admin wants to fix this by increasing the price limit or removing it altogether, but there is an issue with the function that updates the price limit. This causes the transaction to fail and the admin loses the ability to recover the system. The report recommends not updating the function that causes this issue.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

In Elytra, we will have one default price percentage limit, 10%. If the difference between the current price and updated price exceeds the price limit, deposit/withdraw will be blocked.

If there is something wrong with one LST, which causes the share's price drops, e.g 10%. This will block deposit/withdraw. This is one expected behavior. 

As the admin, we wish to increase the price percentage or remove the limit to allow users withdraw their assets. The problem here is that in the function `setPricePercentageLimit`, we will try to update the price. This transaction will be reverted again. The admin will lose the ability to recover the system.

```solidity
    function setPricePercentageLimit(uint256 _limit) external override onlyElytraAdmin {
@>        this.updateElyAssetPrice();
        pricePercentageLimit = _limit;
        emit PricePercentageLimitUpdated(_limit);
    }
```

## Recommendations

It's not necessary to update `updateElyAssetPrice`.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

