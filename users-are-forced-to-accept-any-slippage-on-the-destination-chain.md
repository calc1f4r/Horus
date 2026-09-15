---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7133
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
  - slippage
  - bridge

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

Users are forced to accept any slippage on the destination chain

### Overview


This bug report is about a high risk issue with the BridgeFacet.sol codebase. The documentation mentions a cancel function on the destination domain, which would allow users to send funds back to the origin domain if they don't want to accept the high slippage rate on the destination domain. However, this feature is not found in the current codebase. This means that users may be stuck with the high slippage rate. To solve this issue, the cancel function should be implemented on the destination domain. The bug has been solved in PR 2456 and verified by Spearbit.

### Original Finding Content

## Severity: High Risk

## Context
BridgeFacet.sol#L28

## Description
The documentation mentioned that there is a cancel function on the destination domain that allows users to send the funds back to the origin domain, accepting the loss incurred by slippage from the origin pool. However, this feature is not found in the current codebase. If the high slippage rate persists continuously on the destination domain, the users will be forced to accept the high slippage rate. Otherwise, their funds will be stuck in Connext.

## Recommendation
Implement the cancel function on the destination domain to allow users to send funds back to the origin domain if they choose not to accept the high slippage rate on the destination domain.

## Connext
Solved in PR 2456.

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

`Slippage, Bridge`

