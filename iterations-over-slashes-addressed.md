---
# Core Classification
protocol: Skale Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13846
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/01/skale-token/
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
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Shayan Eskandari
---

## Vulnerability Title

Iterations over slashes ✓ Addressed

### Overview


This bug report is about an issue in the Skale Network Manager, which is a system for managing user's balances and delegations. The problem is that if there are a lot of slashes (penalties) in the system, every user would be forced to iterate over all of them even if the user is only trading tokens and only calls the `transfer` function. This could cause the system to hit the block gas limit, resulting in a system halt. 

The bug has been partially mitigated by optimizing the `sendSlashingSignals` function so that it aggregates slashes per `holder`. Additionally, two recommendations were made to further reduce the issue. The first is to remove signals functionality and just aggregate the changes for the `Punisher`, and the second is to merge the two pipelines into one.

### Original Finding Content

#### Resolution



Partially mitigated in [skalenetwork/skale-manager#163](https://github.com/skalenetwork/skale-manager/pull/163) . `sendSlashingSignals` function is now aggregating slashes per `holder` (if it’s sorted by `holder`), which optimises gas cost.


#### Description


Every user should iterate over each slash (but only once) and process them in order to determine whether this slash impacted his delegations or not.


However, the check is done during almost every action that the user does because it updates the current state of the user’s balance. The downside of this method is that if there are a lot of slashes in the system, every user would be forced to iterate over all of them even if the user is only trading tokens and only calls `transfer` function.


If the number of slashes is huge, checking them all in one function would impossible due to the block gas limit. It’s possible to call the checking function separately and process slashes in batches. So this attack should not result in system halt and can be mitigated with manual intervention.


Also, there are two separate pipelines for iterating over slashes. One pipeline is for iterating over months to determine amount of slashed tokens in separate delegations. This one can potentially hit gas limit in many-many years. The other one is for modifying aggregated delegation values.


#### Recommendation


Try to avoid all the unnecessary iterations over a potentially unlimited number of items. Additionally, it’s possible to optimize some calculations:


1. When slashing signals are processed, all of them always have the same `holder`. There’s no reason for having an array of signals with the same holder (always with predefined length and values will most likely be zero). It seems possible to remove signals functionality and just aggregate the changes for the `Punisher`.
2. Try merge two pipelines into one.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Skale Token |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/01/skale-token/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

