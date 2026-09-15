---
# Core Classification
protocol: apDAO_2024-10-03
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44396
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
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

[C-02] The winner of a bid can brick the auction house

### Overview


The bug report discusses a high severity issue that occurs when an auction ends. The issue involves the `_settleAuction()` function, specifically when there is a bidder for the auction. The problem arises when the bidder is a contract that does not properly implement the `onERC721Received()` function. This can result in a revert, causing the auction house to become unusable and the NFT and funds to be stuck. The report recommends using `transferFrom()` instead of `safeTransferFrom()` to avoid this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Whenever an auction is over, `_settleAuction()` is called. We have 2 main flows there - when no one has bid for the auction and when there is a bidder for the auction. We will focus on the latter. One of the lines we have for that flow is this one:

```solidity
apiologyToken.safeTransferFrom(address(this), _auction.bidder, _auction.apdaoId);
```

It uses `safeTransferFrom()` to transfer the NFT from the contract to the bidder. Thus, if the bidder is a contract that either maliciously or accidentally doesn't properly implement the `onERC721Received()` function, then it will lead to a revert leading to the auction house being bricked. The NFT will be stuck as well as the funds paid by the bidder for it.

## Recommendations

Consider using `transferFrom()` instead of `safeTransferFrom()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | apDAO_2024-10-03 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

