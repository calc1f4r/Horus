---
# Core Classification
protocol: Chainlink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53795
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/chainlink/chainlink-1/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/chainlink/chainlink-1/review.pdf
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

cancelChainlinkRequest Reverts for All Requests whose Callback Address is not the Calling Contract

### Overview

See description below for full details.

### Original Finding Content

## Description

The Chainlinked contract provides a number of helper functions designed to be inherited by contracts using the Chainlink platform. One of these functions, `cancelChainlinkRequest()` (see line [54]) will only operate as expected if the `_callbackAddress` of the request is the current contract. This is due to the require on line [123] of `Oracle.sol`.

Thus, if requests are made with callback addresses that have not explicitly implemented a `cancelChainLinkRequest()` function, these requests will be impossible to cancel. We acknowledge that the purpose of this may be to make the requests generic, i.e., the callback address may be another contract which inherits the Chainlinked contract; however, due to LNK-06, this kind of setup will also revert.

A noteworthy point is that this structure gives a non-intuitive return of tokens. By this, we mean the contract that paid for the request does not necessarily get refunded if the request gets cancelled. Only the callback contract can initiate the cancel and is the one that will receive the cancelled tokens. We raise this issue primarily to ensure that it is known by the authors.

## Recommendations

This issue is related to LNK-01, LNK-02, and LNK-06 in that it arises from the general ability to specify arbitrary contracts to fulfill the data. 

A restrictive approach would be to enforce that the contract making the request be the contract that can cancel the request. This may be too restrictive, in which case an `or` statement could be added to the require on line [54] of `Oracle.sol`, allowing the caller to also cancel the request. This would also involve adding another field to the `Callback` struct, which would also store the `msg.sender` of the request.

Alternatively, this may be a known issue and no modification may be desired.

## Resolution

As in LNK-06, a new function, `addExternalRequest()` on line [94], has been added, which allows Chainlinked contracts to add external requests, allowing for other contracts to make requests on their behalf.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Chainlink |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/chainlink/chainlink-1/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/chainlink/chainlink-1/review.pdf

### Keywords for Search

`vulnerability`

