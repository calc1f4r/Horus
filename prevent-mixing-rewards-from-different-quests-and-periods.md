---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6867
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - DefSec
  - Jay Jonah8
  - Gerard Persoon
---

## Vulnerability Title

Prevent mixing rewards from different quests and periods

### Overview


This bug report is about the MultiMerkleDistributor.sol contract which does not verify that the sum of all amounts in the merkle tree are equal to the rewards allocated for that quest and for that period. This could result in tokens from other quests or other periods being claimed, which will cause issues when claims are done for the other quests/periods. The severity of this bug was set to medium risk since the likelihood of this happening is low, but the impact is high. The recommendation was to consider making token buckets per quest (or even per period) in the MultiMerkleDistributor contract. The bug was fixed in #16 and acknowledged.

### Original Finding Content

## Medium Risk Report

## Severity
**Medium Risk**

## Context
`MultiMerkleDistributor.sol#L260-L275`

## Description
The `MultiMerkleDistributor.sol` contract does not verify that the sum of all amounts in the Merkle tree are equal to the rewards allocated for that quest and for that period. This could happen if there is a bug in the Merkle tree creation script. 

If the sum of the amounts is too high, then tokens from other quests or other periods could be claimed, which will cause problems later on when claims are made for the other quests/periods.

**Note:** Set to medium risk because the likelihood of this happening is low, but the impact is high.

## Recommendation
Consider making token buckets per quest (or even per period) in the `MultiMerkleDistributor` contract.

## Paladin
Implemented in #16.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | DefSec, Jay Jonah8, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

