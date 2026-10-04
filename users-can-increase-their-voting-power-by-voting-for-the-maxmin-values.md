---
# Core Classification
protocol: 1inch Liquidity Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13569
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Users can “increase” their voting power by voting for the max/min values

### Overview


This bug report is about the governance mechanism of a system, which determines parameters based on the weighted average of all votes that stakeholders make. The issue is that users are incentivized to vote for the max or min value instead of their desired value, which could lead to manipulation of the system. However, the severity of the issue is not high since the parameters have max value limitations. The recommendation is to reconsider the voting mechanism.

### Original Finding Content

#### Description


Many parameters in the system are determined by the complicated governance mechanism. These parameters are calculated as a result of the voting process and are equal to the weighted average of all the votes that stakeholders make. The idea is that every user is voting for the desired value. But if the result value is smaller (larger) than the desired, the user can change the vote for the max (min) possible value. That would shift the result towards the desired one and basically “increase” this stakeholder’s voting power. So every user is more incentivized to vote for the min/max value than for the desired one.


The issue’s severity is not high because all parameters have reasonable max value limitations, so it’s hard to manipulate the system too much.


#### Recommendation


Reconsider the voting mechanism.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | 1inch Liquidity Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

