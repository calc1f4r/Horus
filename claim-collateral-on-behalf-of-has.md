---
# Core Classification
protocol: Angle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19186
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Claim Collateral on Behalf of HAs

### Overview


This bug report is about a vulnerability in the InCollateralSettlerERC20 function claimHA(). This function allows any user to make a claim for the perpetual owner, and the user can specify how much governance tokens are to be attached. This vulnerability allows a malicious user to claim other users' perpetuals with zero governance tokens attached, which gives them a higher priority when it comes to redeeming the tokens.

To resolve this issue, the function was changed so that it can only be called by the perpetual owner or an approved account. This was done by adding a check to the code with the require() function. The bug has been fixed in commit 9065e85.

### Original Finding Content

## Description

When a collateral pool is being revoked, users are able to make claims over the collateral. These claims are paid out based on preference. Users are able to attach governance tokens to their claims to give the claims a higher preference.

In `CollateralSettlerERC20`, the function `claimHA()` may be called by any user and will make a claim for the perpetual owner. As part of this function, the user is able to specify how many governance tokens are to be attached. Since there are no requirements for who the message sender is when claiming a perpetual, a malicious user may claim other users' perpetuals with zero governance tokens attached.

The benefit of this attack is that the malicious user would have a higher priority when it comes to redeeming the tokens if they have attached governance tokens when claiming their perpetual.

## Recommendations

Consider only allowing users who are either approved or the owner of a perpetual to be allowed to claim a perpetual. This can be achieved through a public getter of the function `PerpetualManagerInternal._isApprovedOrOwner()`.

## Resolution

This has been resolved in commit `9065e85`. The function can only be called by the perpetual owner or an approved account. The check is implemented in the following code from line [301]:

```solidity
require(perpetualManager.isApprovedOrOwner(msg.sender, perpetualID), "not approved");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Angle |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf

### Keywords for Search

`vulnerability`

