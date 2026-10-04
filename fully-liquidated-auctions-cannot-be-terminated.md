---
# Core Classification
protocol: Derive
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38535
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Fully Liquidated Auctions Cannot Be Terminated

### Overview


The bug report discusses an issue where auctions can become stuck in a state where they cannot be terminated or started. This is caused by a condition in the code that is not being properly met, resulting in the auction not being terminated even though it has been fully liquidated. This can potentially be exploited by attackers to perform high risk actions without being liquidated, which could increase the risk of the platform becoming insolvent. The recommended solution is to change the condition in the code to ensure that fully liquidated auctions can be terminated. This issue has been addressed in a recent code update.

### Original Finding Content

## Description

It is possible to lock auctions in a state where it is impossible to terminate or start a new auction.

On line [482] in `DutchAuction.sol`, there is the condition `if (convertedPercentage > maxOfCurrent)`. If this condition is true, then the auction is terminated.

For an auction that can be fully liquidated, `maxOfCurrent` will equal `1e18`, and if the liquidator wants to fully liquidate an auction in a single bid, they will input `1e18` when calling `bid()` as the parameter for `percentOfAccount`. This will result in `convertedPercentage` equal to `1e18`.

However, in this situation, the condition `convertedPercentage > maxOfCurrent` will be FALSE, which results in the auction not being terminated even though it has been fully liquidated.

In this state, if another user attempts to call `bid()` on this auction, the function will revert with `Division or modulo by 0`. Additionally, the auction cannot be terminated with `terminateAuction()`, nor can a new auction be started for that `SubAccount`.

An attacker can potentially use this to perform high-risk actions in the Derive protocol without any prospect of being liquidated. This can significantly increase the risk of Derive becoming insolvent.

## Recommendations

Change the condition to `convertedPercentage >= maxOfCurrent`.

## Resolution

This issue has been addressed in pull request #270. The development team has adjusted the code on line [510] as per the recommendation, ensuring that fully liquidated auctions can be terminated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Derive |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/derive/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/derive/review.pdf

### Keywords for Search

`vulnerability`

