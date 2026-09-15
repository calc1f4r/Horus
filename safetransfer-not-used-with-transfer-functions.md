---
# Core Classification
protocol: Interest Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19418
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
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

safeTransfer() not used with transfer functions

### Overview


This bug report is about three smart contracts, CappedFeeOnTransferToken, CappedGovToken and SlowRoll, which do not use the safeTransfer() functions. Instead, they call _underlying.transferFrom() on line 96 for CappedFeeOnTransferToken, line 84 for CappedGovToken, and takeFrom(), which in turn calls _pointsToken.transferFrom() on line 149 for SlowRoll. This could lead to reverted transactions if the underlying token does not properly implement the ERC20 standard. The token known for not complying to this standard is USDT, which could be used in one of these token wrappers. To fix this issue, the development team recommends using safeTransferFrom() from SafeERC20Upgradeable instead of transferFrom() in the mentioned locations. The issue was resolved in commit b447c19. For SlowRoll, the team is aware of the issue and do not intend to use any affected tokens.

### Original Finding Content

## Description

CappedFeeOnTransferToken, CappedGovToken, and SlowRoll do not use `safeTransfer()` functions:

- CappedFeeOnTransferToken calls `_underlying.transferFrom()` on line [96].
- CappedGovToken calls `_underlying.transferFrom()` on line [84].
- SlowRoll calls `takeFrom()`, which in turn calls `_pointsToken.transferFrom()` on line [149].

This may cause reverted transactions if the underlying token does not properly implement the ERC20 standard. Note that the token best known for not complying to this standard is USDT, which does have code capable of implementing a fee on transfer facility, and so could conceivably be contained in one of these token wrappers.

## Recommendations

Use `safeTransferFrom()` from `SafeERC20Upgradeable` in place of `transferFrom()` in the locations mentioned above.

## Resolution

Resolved in commit [b447c19]. In the case of SlowRoll, the development team is aware of the issue and does not intend to use any affected tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Interest Protocol |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf

### Keywords for Search

`vulnerability`

