---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: bridge

# Attack Vector Details
attack_type: bridge
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7155
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
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

RootManager.propagate does not operate in a fail-safe manner

### Overview


This bug report is about the RootManager.sol#L147-L173 function of the Connext messaging network. The function calls the AMB contract of six different chains (Arbitrum, Gnosis, Multichain, Optimism, Polygon, and ZKSync) in order to send the latest aggregated root. If one of the function calls to the chain's AMB contract reverts, the entire RootManager.propagate function will revert and the messaging network will stop working until the problem is manually resolved. 

The risk of this issue occurring increases as more chains are added to the Connext messaging network. To address this issue, the RootManager.propagate function should be made fail-safe by using try-catch or address.call, as the AMB contracts are considered external and beyond the control of Connext.

Connext has solved this issue in PR 2430 and it has been verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
RootManager.sol#L147-L173

## Description
A bridge failure on one of the supported chains will cause the entire messaging network to break down.

When the `RootManager.propagate` function is called, it will loop through the hub connector of all six chains (Arbitrum, Gnosis, Multichain, Optimism, Polygon, ZKSync) and attempt to send over the latest aggregated root by making a function call to the respective chain's AMB contract. There is a tight dependency between the chain's AMB and hub connector.

The problem is that if one of the function calls to the chain's AMB contract reverts (e.g. one of the bridges is paused), the entire `RootManager.propagate` function will revert, and the messaging network will stop working until someone figures out the problem and manually removes the problematic hub connector.

As Connext grows, the number of chains supported will increase, and the risk of this issue occurring will also increase.

## Recommendation
The `RootManager.propagate` function should operate in a fail-safe manner (e.g. using try-catch or `address.call`). Chain's AMB contracts are considered external third-party and beyond Connext's control. Thus, the `RootManager.propagate` function should not assume that function calls to these third-party bridge contracts will always succeed and will not revert.

- **Connext:** Solved in PR 2430.
- **Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

`Bridge`

