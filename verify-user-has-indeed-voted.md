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
solodit_id: 6859
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
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

Verify user has indeed voted

### Overview


This bug report is about the MultiMerkleDistributor.sol, which is a high risk issue. The bug is that if an error is made in the merkle trees (either by accident or on purpose), a user that did not vote (in that period for that gauge) might get rewards assigned to him. The Paladin documentation states that the Curve DAO contract does not offer a mapping of votes for each Gauge for each Period, but it might still be possible to verify that a user has voted if the account, gauge and period are known.

The recommendation is to check that a user has voted by interrogating the gauge contracts at reward retrieval time. The Paladin argued against this recommendation, saying that if users want to pile up rewards in order to claim them all at once, then the only vote that can be fetched from the Curve Gauge Controller is the last vote from the user since the previous ones were removed. This would mean that user past claims would be locked, and never claimed.

Spearbit acknowledged the recommendation but it has not been implemented, therefore the risk still exists.

### Original Finding Content

## Vulnerability Report

**Severity:** High Risk  
**Context:** MultiMerkleDistributor.sol  

## Description
If an error is made in the merkle trees (either by accident or on purpose), a user that did not vote (in that period for that gauge) might get rewards assigned to them. Although the Paladin documentation states: "the Curve DAO contract does not offer a mapping of votes for each Gauge for each Period," it might still be possible to verify that a user has voted if the account, gauge, and period are known.  

**Note:** Set to high risk because the likelihood of this happening is medium, but the impact is high.  

## Recommendation
Check that a user has voted by interrogating the gauge contracts at reward retrieval time.  

## Paladin Perspective
We carefully considered this issue throughout the development cycle, and the main argument against the recommendation is as follows:  
If users want to pile up rewards in order to claim them all at once (e.g., because of gas fees), then the only vote we can fetch from the Curve Gauge Controller is the last vote from the user since the previous ones were removed, and no checkpoints of past votes exist in the Gauge Controller. That would mean user past claims would be locked and never claimed. Because of this, we are trying to ensure the most trustworthy MerkleTree generation so that this type of issue does not appear.  

## Spearbit Perspective
Acknowledged, recommendation not implemented; therefore, risk still exists.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

