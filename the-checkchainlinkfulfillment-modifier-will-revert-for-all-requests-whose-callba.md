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
solodit_id: 53794
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

The checkChainlinkFulfillment Modifier Will Revert for All Requests Whose Callback is not the Calling Contract

### Overview

See description below for full details.

### Original Finding Content

## Description

A Chainlinked contract stores a mapping of `unfulfilledRequests`. The modifier `cancelChainlinkRequest()` checks this mapping to ensure the `msg.sender` is the Oracle of the request. This only functions correctly if the request was made from the current contract.

Consider two Chainlinked contracts, one as the requester and one as the callback contract to receive fulfilled requests. The requester’s `unfulfilledRequests` mapping will store the requests made; however, the callback contract’s mapping will not. If the callback contract were to utilize the `checkChainlinkFulfillment` modifier, requests will always revert due to the mapping being empty. (We assume the callback contract is not also sending requests of its own.)

## Recommendations

This issue is related to LNK-01, LNK-02, and LNK-07 in that it arises from the general ability to specify arbitrary contracts to fulfill the data. A restrictive approach would be to enforce that the contract making the request be the callback contract, as discussed in LNK-01.

As long as this modifier is not used in this scenario (which is fundamentally an implementation issue), there are no immediate related security risks. Thus, this issue could be acknowledged, and we recommend adding comments that indicate that the `checkChainlinkFulfillment` modifier is only to be used for contracts that are both the requester and the callback contract.

## Resolution

A new function, `addExternalRequest()` on line [94] has been added, which allows Chainlinked contracts to add external requests, allowing for other contracts to make requests on their behalf.

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

