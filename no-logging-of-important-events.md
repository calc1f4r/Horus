---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28336
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#2-no-logging-of-important-events
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

No logging of important events

### Overview


This bug report is about the lack of logging of important events in a smart contract. Logging these events makes it easier to maintain the project. The issue is present in two external functions, `start_next_rewards_period()` and `set_rewards_period_duration()`, which can be found in the RewardsManager.vy file on GitHub. It is recommended to add logging of these important events.

### Original Finding Content

##### Description
Logging important actions makes it easier to maintain the project.
But in this smart contract it is not done for some important events.
At lines https://github.com/lidofinance/1inch-rewards-manager/blob/c2cd9665666deda9452fa9e3461fbf3537413945/contracts/RewardsManager.vy#L100-L120 for the `start_next_rewards_period()` external function this event logging is lacking.
At lines https://github.com/lidofinance/1inch-rewards-manager/blob/c2cd9665666deda9452fa9e3461fbf3537413945/contracts/RewardsManager.vy#L124-L131 for the external function `set_rewards_period_duration()` this event is not logged.

##### Recommendation
It is recommended to add logging of important events.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#2-no-logging-of-important-events
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

