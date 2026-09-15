---
# Core Classification
protocol: 1Inch
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28116
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/1inch/Farming/README.md#3-rebasable-as-reward-tokens-breaks-logic
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Rebasable as reward tokens breaks logic

### Overview


A bug has been identified in the calculation of farmed rewards when using rebasable reward tokens. This is because the calculation relies on a strict amount of distributed tokens, while the underlying reward balance will float. A recommendation has been made to warn developers against using rebasable tokens as reward tokens. This bug can be found in the FarmAccounting.sol file on the 1inch Github repository.

### Original Finding Content

##### Description
With rebasable reward tokens, the calculation of farmed rewards will be incorrect because it relies on a strict amount of distributed tokens while the underlying reward balance will float. 
https://github.com/1inch/farming/blob/7a007ec7784cca2899889e99e46cf06d5788a7d9/contracts/accounting/FarmAccounting.sol#L21
##### Recommendation
We recommend warning developers not to use rebasable tokens as reward tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | 1Inch |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/1inch/Farming/README.md#3-rebasable-as-reward-tokens-breaks-logic
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

