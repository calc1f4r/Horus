---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46157
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/11615402-c0bc-4170-bf3d-595af10f2ce1
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_airdrops_december2024.pdf
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
finders_count: 2
finders:
  - Eric Wang
  - RustyRabbit
---

## Vulnerability Title

Handling empty arrays by reverting with an explicit custom error 

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

## Context
- **Helpers.sol#L31**
- **Helpers.sol#L64**
- **SablierBatchLockup.sol#L123-L125**
- **SablierBatchLockup.sol#L338-L340**

## Description
An array out-of-bounds access error may be triggered in the following code:

1. In the `SablierLockup.createWithDurationsLT()` function, if the input `tranchesWithDuration` is an empty array, `Helpers.calculateTrancheTimestamps()` will cause an out-of-bounds access error when accessing `tranchesWithTimestamps[0]`. The same issue also exists in `Helpers.calculateSegmentTimestamps()`.

2. In the `createWithTimestampsLD()` and `createWithTimestampsLT()` functions of the `SablierBatchLockup` contract, since `batch[i].segments` (or `batch[i].tranches`) can be an empty array, the calculation of its length - 1 may overflow and cause an out-of-bounds access error.

## Recommendation
Consider reverting with a custom error in the empty array cases for better error handling and debugging purposes.

## Acknowledgments
- **Sablier:** Thank you for your submission. We agree that the lack of array length validation can result in an out-of-bounds access error. However, since the transaction will ultimately revert and the user will be unable to create a stream, we have opted not to include array length validation and keep the gas cost as it is. Acknowledged.
  
- **Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Eric Wang, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_airdrops_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/11615402-c0bc-4170-bf3d-595af10f2ce1

### Keywords for Search

`vulnerability`

