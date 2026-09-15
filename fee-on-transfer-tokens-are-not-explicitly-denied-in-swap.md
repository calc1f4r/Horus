---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7231
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - fee_on_transfer

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Fee-On-Transfer tokens are not explicitly denied in swap()

### Overview


This bug report pertains to the SwapUtils.sol#L690-L729 file within the Connext protocol. The swap() function is used to swap between local and adopted assets and checks the amount transferred. However, this is not consistent with other swap functions which check that the amount transferred is equal to dx. To fix this, it is recommended to add a require check prior to overwriting dx to ensure fee-on-transfer tokens are not used in the swap. This issue has been solved in PR 1642 and verified by Spearbit.

### Original Finding Content

## Security Assessment Report

## Severity
**Medium Risk**

## Context
`SwapUtils.sol#L690-L729`

## Description
The `theswap()` function is used extensively within the Connext protocol, primarily when swapping between local and adopted assets. When a swap is performed, the function checks the actual amount transferred. However, this is not consistent with other swap functions, which check that the amount transferred is equal to `dx`. As a result, overwriting `dx` with `tokenFrom.balanceOf(address(this)).sub(beforeBalance)` allows for fee-on-transfer tokens to work as intended.

## Recommendation
Consider adding a `require(dx == tokenFrom.balanceOf(address(this)).sub(beforeBalance), "not support fee token");` check prior to overwriting `dx` to ensure fee-on-transfer tokens are not used in the swap.

## Connext
Solved in PR 1642, in this commit.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Fee On Transfer`

