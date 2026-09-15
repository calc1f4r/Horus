---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4986
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: #l-05-missing-input-validations-and-timelocks

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing input validations and timelocks

### Overview

See description below for full details.

### Original Finding Content


The following instances are missing checks for zero addresses and or valid ranges for values. Even if the DAO is the one setting these values, it's important to add sanity checks in case someone does a fat-finger operation that is missed by DAO participants who may not be very technical. There are also no timelocks involved, which [should be rectified](https://discord.com/channels/810916927919620096/986765994049564682/990255967847460894)

*There are 5 instances of this issue.*



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: #l-05-missing-input-validations-and-timelocks
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

