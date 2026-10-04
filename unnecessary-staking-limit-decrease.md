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
solodit_id: 28151
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#11-unnecessary-staking-limit-decrease
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

Unnecessary staking limit decrease

### Overview


This bug report is about the staking limit in the NodeOperatorsRegistry.sol code. The code contains an index that is intended to decrease the staking limit, but it is not clear why it should be decreased. It is recommended to not decrease the staking limit, as it would allow all keys of a node operator to be used.

### Original Finding Content

##### Description
Is not clear why staking limit should be decreased to index 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L627 
If we remove key at index 0 then we will have all keys of this node operator to be used.
##### Recommendation
It is recommended to not decrease staking limit.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#11-unnecessary-staking-limit-decrease
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

