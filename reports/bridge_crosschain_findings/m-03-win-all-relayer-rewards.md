---
# Core Classification
protocol: Althea Gravity Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 725
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-gravity-bridge-contest
source_link: https://code4rena.com/reports/2021-08-gravitybridge
github_link: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/7

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
  - bridge
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - nascent
---

## Vulnerability Title

[M-03] Win all relayer rewards

### Overview


This bug report is about a vulnerability which can affect relayers and not the oracle. It occurs when there are large validator sets and rapid validator set updates, which can freeze the bridge or relayer. This means that valid attestations can be made, but no other relayers can participate in the execution. As a result, the attacker can win all batch, logic, and valset rewards as their node is the only relayer running. This is possible because the `find_latest_valset` function is run in the main relayer loop and it tries for 5000 blocks of logs. This vulnerability is a major issue as it can allow the attacker to gain unfair rewards.

### Original Finding Content

_Submitted by nascent_

"Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or Relayer" can affect just the relayers & not affect the oracle in certain circumstances. This could result in valid attestations, but prevent any of the other relayers from being able to participate in the execution. While the other relayers are down from the other attack, the attacker can win all batch, logic, and valset rewards as their node is the only relayer running. This is possible because `find_latest_valset` is run in the main relayer loop and everytime tries for 5000 blocks of logs.

**[jkilpatr (Althea) confirmed](https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/7#issuecomment-917140352):**
 > This is a reasonable consequence of #6
>
> I consider it medium risk because it reduces the number of relayers active, not because of the reward assignment



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Althea Gravity Bridge |
| Report Date | N/A |
| Finders | nascent |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-gravitybridge
- **GitHub**: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/7
- **Contest**: https://code4rena.com/contests/2021-08-gravity-bridge-contest

### Keywords for Search

`vulnerability`

