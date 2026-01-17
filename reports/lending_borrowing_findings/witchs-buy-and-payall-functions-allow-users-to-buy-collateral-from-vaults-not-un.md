---
# Core Classification
protocol: Yield V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16980
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
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
finders_count: 2
finders:
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Witch’s buy and payAll functions allow users to buy collateral from vaults not undergoing auctions

### Overview


This bug report outlines a vulnerability in the buy and payAll functions in the Witch contract in the Yield Protocol. These functions enable users to buy collateral at an auction, but do not check if there is an active auction for the collateral of a vault. This issue creates an arbitrage opportunity, as an attacker can buy the collateral of an overcollateralized vault at a below-market price and turn a profit. 

The exploit scenario given in the report is that Alice, a user of the Yield Protocol, opens an overcollateralized vault. Attacker Bob then calls payAll on Alice's vault, resulting in the vault being liquidated and Alice losing the excess collateral.

To address this issue, it is recommended that the buy and payAll functions should fail if they are called on a vault with no active auction. In the long term, all functions should be reverted if the system is in a state in which they are not allowed to be called.

### Original Finding Content

## Diﬃculty: Low

## Type: Undeﬁned Behavior

## Description
The buy and payAll functions in the Witch contract enable users to buy collateral at an auction. However, neither function checks whether there is an active auction for the collateral of a vault. As a result, anyone can buy collateral from any vault. This issue also creates an arbitrage opportunity, as the collateral of an overcollateralized vault can be bought at a below-market price. An attacker could drain vaults of their funds and turn a profit through repeated arbitrage.

## Exploit Scenario
Alice, a user of the Yield Protocol, opens an overcollateralized vault. Attacker Bob calls payAll on Alice’s vault. As a result, Alice’s vault is liquidated, and she loses the excess collateral (the portion that made the vault overcollateralized).

## Recommendations
**Short term:** Ensure that buy and payAll fail if they are called on a vault for which there is no active auction.

**Long term:** Ensure that all functions revert if the system is in a state in which they are not allowed to be called.

## Trail of Bits
Yield V2  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yield V2 |
| Report Date | N/A |
| Finders | Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf

### Keywords for Search

`vulnerability`

