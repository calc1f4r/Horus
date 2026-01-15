---
# Core Classification
protocol: Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1585
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-foundation-contest
source_link: https://code4rena.com/reports/2022-02-foundation
github_link: https://github.com/code-423n4/2022-02-foundation-findings/issues/85

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-07] _getCreatorPaymentInfo() is Not Equipped to Handle Reverts on an Unbounded _recipients Array

### Overview


This bug report is about a vulnerability in the `_getCreatorPaymentInfo()` function used by `_distributeFunds()` whenever an NFT sale is made. The function uses `try` and `catch` statements to handle bad API endpoints, but if the function reverts inside of a `try` statement, the revert is not handled and it will not fall through to the empty `catch` statement. This results in valid and honest NFT contracts reverting if the call runs out of gas due to an unbounded `_recipients` array. The bug was identified using manual code review. The recommended mitigation step is to consider bounding the number of iterations to `MAX_ROYALTY_RECIPIENTS_INDEX` as this is already enforced by `_distributeFunds()`. It is also suggested to identify other areas where the `try` statement will not handle reverts on internal calls.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-02-foundation/blob/main/contracts/mixins/NFTMarketCreators.sol#L49-L251


## Vulnerability details

## Impact

The `_getCreatorPaymentInfo()` function is utilised by `_distributeFunds()` whenever an NFT sale is made. The function uses `try` and `catch` statements to handle bad API endpoints. As such, a revert in this function would lead to NFTs that are locked in the contract. Some API endpoints receive an array of recipient addresses which are iterated over. If for whatever reason the function reverts inside of a `try` statement, the revert is actually not handled and it will not fall through to the empty `catch` statement.

## Proof of Concept

The end result is that valid and honest NFT contracts may revert if the call runs out of gas due to an unbounded `_recipients` array. `try` statements are only able to handle external calls.

## Tools Used

Manual code review.

## Recommended Mitigation Steps

Consider bounding the number of iterations to `MAX_ROYALTY_RECIPIENTS_INDEX` as this is already enforced by `_distributeFunds()`. It may be useful to identify other areas where the `try` statement will not handle reverts on internal calls.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Foundation |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-foundation
- **GitHub**: https://github.com/code-423n4/2022-02-foundation-findings/issues/85
- **Contest**: https://code4rena.com/contests/2022-02-foundation-contest

### Keywords for Search

`vulnerability`

