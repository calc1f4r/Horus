---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28438
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/SNX/README.md#3-handling-losses-from-underlying-vault
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

Handling losses from underlying vault

### Overview


This bug report is about SUSD vault, which is a type of vault that holds SNX. It has been reported that the underlying SUSD vault may suffer a permanent loss, leading to a loss of the corresponding SNX. The issue with this is that the loss is not fairly distributed across vault users, meaning that on the first withdrawals no loss will be reported, but on later withdrawal attempts the strategy will report major losses to any users.

The recommendation is to implement some mechanics to fairly redistribute the losses. This would ensure that all users are not unfairly affected by the losses and that the losses are more evenly distributed. This would help to make sure that all users are not adversely affected by the losses and that the losses are more evenly spread out.

### Original Finding Content

##### Description
The underlying SUSD vault may suffer a permanent loss. This will lead to a loss of corresponding SNX. However, such loss is not fairly distributed across vault users. On the first withdrawals no loss will be reported but on a later withdrawal attempts the strategy will report major losses to any users.

##### Recommendation
To implement some mechanics to fairly redistribute a losses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/SNX/README.md#3-handling-losses-from-underlying-vault
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

