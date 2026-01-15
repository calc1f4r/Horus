---
# Core Classification
protocol: CLOBER
chain: everychain
category: uncategorized
vulnerability_type: ownership

# Attack Vector Details
attack_type: ownership
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7262
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
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
  - ownership

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Lack of two-step role transfer

### Overview


A bug was identified in the MarketFactory.sol smart contract, which affects the ownership transfer of the contract and the change of market's host. This bug does not properly account for the case when the address receiving the role is inaccessible, meaning that anyone who created the market could unintentionally or intentionally brick fees collection. To address this issue, it is recommended to implement a two-step role transfer process, whereby the role recipient is set and then the recipient has to claim that role to finalise the role transfer. This bug was fixed in PR 322 and verified by Spearbit, with two-step role transfers added for contract's owner and market's host.

### Original Finding Content

## Security Advisory

## Severity
**Medium Risk**

## Context
- `MarketFactory.sol#L146-L152`
- `MarketFactory.sol#L137-L140`

## Description
The contracts lack two-step role transfer functionality. Both the ownership of the `MarketFactory` and the change of a market's host are implemented as single-step functions. The basic validation checks whether the address is not a zero address for a market, but it does not properly account for scenarios where the address receiving the role is inaccessible.

Given that `handOverHost` can be invoked by anyone who created the market, it is possible to unintentionally or intentionally make a typo. An attacker could exploit this situation to disrupt fees collection, as the host affects `collectFees` in `OrderBook` (which is documented as a separate issue).

While ownership transfer should ideally be less error-prone—being conducted by a DAO with care—implementing a two-step role transfer remains preferable.

## Recommendation
It is recommended to implement a two-step role transfer where:
1. The role recipient is set.
2. The recipient must then claim that role to finalize the transfer.

## Clober
Fixed in PR 322.

## Spearbit
Verified. Two-step role transfers added for the contract's owner and the market's host.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`Ownership`

