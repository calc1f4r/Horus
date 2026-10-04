---
# Core Classification
protocol: Vibe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27829
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#9-royalty-parameters-are-not-checked
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Royalty parameters are not checked

### Overview


This bug report concerns the `royaltyRate_` and `BPS` parameters used to calculate fees paid to a royalty receiver. These parameters are found in the VibeERC721.sol file on the Github repository. If the `royaltyRate_` is greater than `BPS`, then the royalty payment will revert. 

It is recommended that checks for these royalty parameters are added in order to prevent the payment from reverting. This will ensure that the payment is processed correctly and the royalty receiver receives the correct amount of fees.

### Original Finding Content

##### Description
Royalty parameters are used to calculate how much fees should be paid to the royalty receiver https://github.com/vibexyz/vibe-contract/blob/d08057edbaf83b00d94dcaca2a05e3c44a45e4d9/contracts/tokens/VibeERC721.sol#L205-L210. If `royaltyRate_` is greater than `BPS` then royalty payment will revert.

##### Recommendation
We recommend adding checks for royalty parameters.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Vibe |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#9-royalty-parameters-are-not-checked
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

