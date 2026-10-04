---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7135
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

No way to update a Stable Swap once assigned to a key

### Overview


This bug report is about the SwapAdminFacet.sol#L109, which is a high risk issue. The problem is that once a Stable Swap is assigned to a key (which is a hash of the canonical id and domain for token), it cannot be updated or deleted. This could be a security risk if the Swap is hacked, or if there is an improved version released. The recommendation is to add a privileged removeSwap() function to remove a Swap already assigned to a key. In case a Swap has to be updated, it can be deleted and then initialized. This issue has been solved in PR 2354 and verified by Spearbit.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
`SwapAdminFacet.sol#L109`

## Description
Once a Stable Swap is assigned to a key (the hash of the canonical id and domain for token), it cannot be updated nor deleted. A Swap can be hacked or an improved version may be released which will warrant updating the Swap for a key.

## Recommendation
Add a privileged `removeSwap()` function to remove a Swap already assigned to a key. In case a Swap has to be updated, it can be deleted and then initialized.

## Connext
Solved in PR 2354.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

