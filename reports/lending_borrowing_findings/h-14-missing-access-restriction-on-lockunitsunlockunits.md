---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42158
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-vader
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/208

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

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-14] Missing access restriction on `lockUnits/unlockUnits`

### Overview


The `Pool.lockUnits` function allows anyone to take pool tokens from one user and give them to themselves. This can be done by any user, without any restrictions. To fix this, it is recommended to add a control system that only allows authorized parties, such as the router, to use this function. This issue has been confirmed by a user named strictly-scarce and is currently being worked on as part of the lending code.

### Original Finding Content


The `Pool.lockUnits` allows anyone to steal pool tokens from a `member` and assign them to `msg.sender`. Anyone can steal pool tokens from any other user.

Recommend adding access control and require that `msg.sender` is the router or another authorized party.

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/208#issuecomment-828478127):**
> Valid, although this is part of the partially-complete lending code.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/208
- **Contest**: https://code4rena.com/reports/2021-04-vader

### Keywords for Search

`vulnerability`

