---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7152
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
  - validation

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

Relayer could lose funds

### Overview


This bug report is about a medium risk issue with the BridgeFacet.sol#L828-L835 code. The issue is that the xReceive function on the receiver side can contain unreliable code which Relayer is unaware of. This can lead to a scenario where a call to withdraw function in a foreign contract is made where Relayer A is holding some balance. If this foreign contract is checking tx.origin, then Relayer A's funds will be withdrawn without his permission. 

The recommendation is that relayers should be advised to use an untouched wallet address so that foreign code interaction cannot harm them. It should also be documented that relayers EOA should be single-purpose. This has been acknowledged.

### Original Finding Content

## Security Assessment Report

## Severity
**Medium Risk**

## Context
`BridgeFacet.sol#L828-L835`

## Description
The `xReceive` function on the receiver side can contain unreliable code which the Relayer is unaware of. In the future, more relayers will participate in completing the transaction. 

Consider the following scenario:
1. Say that Relayer A executes the `xReceive` function on the receiver side.
2. In the `xReceive` function, a call to the `withdraw` function in a foreign contract is made where Relayer A is holding some balance.
3. If this foreign contract is checking `tx.origin` (say deposit/withdrawal were done via a third party), then Relayer A's funds will be withdrawn without his permission (since `tx.origin` will be the Relayer).

## Recommendation
Relayers should be advised to use an untouched wallet address so that foreign code interaction cannot harm them.

## Connext
To be documented; relayer's EOA should be single-purpose.

## Spearbit
Acknowledged.

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

`Validation`

