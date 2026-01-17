---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28402
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V1/README.md#2-missing-validation-on-relation
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

Missing validation on relation

### Overview


This bug report relates to the code found in the lines https://github.com/aave/governance-crosschain-bridges/blob/7f56e7ae63f30ba8dcd7ced6a11a34c2eb865a1d/contracts/BridgeExecutorBase.sol#L34-L39. The code works with two variables, `minimumDelay` and `maximumDelay`, but there is no comparison between them. The bug report suggests that a check should be added to compare the values of these two variables. This check would help to ensure that the code is functioning correctly and accurately.

### Original Finding Content

##### Description
At the lines https://github.com/aave/governance-crosschain-bridges/blob/7f56e7ae63f30ba8dcd7ced6a11a34c2eb865a1d/contracts/BridgeExecutorBase.sol#L34-L39 are working with the variables `minimumDelay` and `maximumDelay`. But nowhere is there a comparison of these variables with each other.

##### Recommendation
It is recommended to add a check for comparing the values of variables between each other.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V1/README.md#2-missing-validation-on-relation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

