---
# Core Classification
protocol: Aspida Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29900
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Aspida%20Network/README.md#1-slashing-and-strategy-losses-have-not-been-taken-into-design
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

Slashing and strategy losses have not been taken into design

### Overview


The bug report discusses an issue where if a validator is penalized or losses occur within a strategy, there is no system in place to distribute these losses among all users. This can result in the supply of `aETH` falling below the amount of `ETH` locked in the project, which prevents some users from redeeming their tokens. This also means that new users who contribute `ETH` to the project after these events may unknowingly assume these risks, which goes against an optimal economic model. The report recommends implementing a mechanism to fairly distribute the losses among existing users and protect new users from bearing the losses incurred before their participation. This issue is classified as `high` due to its impact on both directly and indirectly involved users.

### Original Finding Content

##### Description
Currently, if a validator is slashed or losses occur within a strategy, there is no established mechanism to distribute these losses among all users. As a result, the supply of `aETH` may fall below the amount of `ETH` locked into the project, preventing some users from redeeming their tokens. Furthermore, users who contribute `ETH` to the project after such events inadvertently assume these risks, which is a deviation from an optimal economic model. 

This issue is classified as `high` due to the inequitable distribution of losses, affecting both directly and indirectly involved users.
##### Recommendation
We recommend implementing a mechanism that equitably distributes the consequences of slashing among existing users, while safeguarding new users from bearing the losses incurred prior to their participation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Aspida Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Aspida%20Network/README.md#1-slashing-and-strategy-losses-have-not-been-taken-into-design
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

