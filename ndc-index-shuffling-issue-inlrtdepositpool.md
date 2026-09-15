---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53633
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
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

NDC Index Shuffling Issue InLRTDepositPool

### Overview


The `removeNodeDelegatorContractFromQueue()` function in the LRTDepositPool contract has two issues: a race condition and incorrect NDC operation. These issues occur when trying to remove a Node Delegator Contract (NDC) by swapping it with the last NDC in the list. The development team recommends using a more stable indexing mechanism or a mapping structure to avoid these issues. They also suggest implementing checks to handle ongoing operations during the removal process. The issue has been closed by the development team, who will update their documentation and take care of operations.

### Original Finding Content

## Description

The `removeNodeDelegatorContractFromQueue()` function in the LRTDepositPool contract employs a mechanism to remove a Node Delegator Contract (NDC) by swapping the target NDC with the last in the list on line [336], potentially altering NDC indices. This approach can lead to two primary issues:

1. **Race Condition**  
   Operations like `transferAssetToNodeDelegator()` or `transferETHToNodeDelegator()` may revert if they target the last NDC index which gets removed or swapped during execution.

2. **Incorrect NDC Operation**  
   If an NDC other than the last one is removed, subsequent operations might act on an incorrect NDC due to the shift in indices.

## Recommendations

Consider implementing a more stable indexing mechanism that does not rely on the position within an array or explore the possibility of using a mapping structure to track NDCs, which inherently avoids the problem of shifting indices. Additionally, introducing checks or mechanisms to handle ongoing operations gracefully during the removal process could prevent potential race conditions and ensure operational accuracy.

## Resolution

The development team has closed the issue with the following comment:  
"We are fine with this design. Removing an NDC is a very rare event. We will update our NDC indices in our docs and take care of operations."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf

### Keywords for Search

`vulnerability`

