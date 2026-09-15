---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27694
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#5-incorrect-rewards-distribution
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

Incorrect rewards distribution

### Overview


This bug report is about a problem with rewards being blocked on a contract when they are deposited to an empty gauge. This happens because the `last_update` is updated even when the totalSupply is zero. This issue is classified as HIGH severity, as the reward distributor will be unable to retrieve the blocked rewards. The suggested solution is to update `last_update` only when the totalSupply is greater than zero.

### Original Finding Content

##### Description
Some of the rewards will be blocked on the contract if they were deposited to the empty gauge (when totalSupply == 0) https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/LiquidityGauge.vy#L318 This happens because `last_update` will be updated nevertheless totalSupply is zero. This finding is classified as HIGH severity since the reward distributor will block some rewards on the contract without a possibility ti retrieve them.

##### Recommendation
We recommend updating `last_update` only if totalSupply > 0.


***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#5-incorrect-rewards-distribution
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

