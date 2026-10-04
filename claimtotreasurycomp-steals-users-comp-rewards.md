---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: deposit/reward_tokens

# Attack Vector Details
attack_type: deposit/reward_tokens
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6913
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
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
  - deposit/reward_tokens
  - business_logic

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

claimToTreasury(COMP) steals users' COMP rewards

### Overview


This bug report is about the claimToTreasury function in the MorphoGovernance.sol#L414 contract. This function sends a market's underlying tokens that have been accumulated in the contract to the treasury. This is intended to be used for the reserve amounts that accumulate in the contract from P2P matches. However, Compound also pays out rewards in COMP and COMP is a valid Compound market. Sending the COMP reserves will also send the COMP rewards, which is bad because anyone can claim COMP rewards on the behalf of Morpho at any time and the rewards will be sent to the contract. An attacker could even frontrun a claimToTreasury(cCOMP) call with a Comptroller.claimComp(morpho, [cComp]) call to sabotage the reward system.

The recommendation is that if Morpho wants to support the COMP market, they should consider separating the COMP reserve from the COMP rewards. Morpho decided not to implement this due to the changes to do and the small likelihood to set a reserve factor for the COMP asset and the awareness on their side about this. Spearbit acknowledged this.

### Original Finding Content

## Security Report

## Severity
**Medium Risk**

## Context
`compound/MorphoGovernance.sol#L414`

## Description
The `claimToTreasury` function can send a market's underlying tokens that have been accumulated in the contract to the treasury. This is intended to be used for the reserve amounts that accumulate in the contract from P2P matches. However, Compound also pays out rewards in COMP, and COMP is a valid Compound market. 

Sending the COMP reserves will also send the COMP rewards. This is especially concerning as anyone can claim COMP rewards on behalf of Morpho at any time, and the rewards will be sent to the contract. An attacker could even frontrun a `claimToTreasury(cCOMP)` call with a `Comptroller.claimComp(morpho, [cComp])` call to sabotage the reward system, resulting in users being unable to claim their rewards.

## Recommendation
If Morpho wants to support the COMP market, consider separating the COMP reserve from the COMP rewards.

## Morpho Response
Given the changes required and the small likelihood of setting a reserve factor for the COMP asset, and our awareness of this issue, we have decided not to implement it.

## Spearbit Response
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`Deposit/Reward tokens, Business Logic`

