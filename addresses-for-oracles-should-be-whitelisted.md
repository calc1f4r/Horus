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
solodit_id: 27690
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#1-addresses-for-oracles-should-be-whitelisted
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

Addresses for oracles should be whitelisted

### Overview


This bug report is about the current implementation of the Pools Factory, which allows users to create pools with user-supplied oracles to determine prices of assets. This could lead to imbalanced pools where a malicious user can steal assets via swaps or liquidity removes. Moreover, if developers don't pay enough attention to the security of their price oracle, Curve LPs will lose value. To prevent this, the report recommends adding a whitelist for oracles' addresses. This whitelist would allow the community to assess the quality of new oracles and prevent pools with volatile oracles from leading to permanent losses for LPs.

### Original Finding Content

##### Description
The current implementation of the Pools Factory allows users to create pools with user-supplied oracles to determine prices of assets:
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapFactoryNG.vy#L531
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapFactoryNG.vy#L657
This allows malicious users to create pools with oracles that can change their returned values. This could lead to imbalanced pools where a malicious user can steal assets via swaps or liquidity removes. However, the pools created by malicious users should not accumulate any liquidity since these pools will not be accepted by the community and LPs in these pools will not be rewarded with CRV tokens. 
But there is one more dangerous scenario that can lead to lost value by Curve users. Let's imagine a situation where a new protocol builds an integration with Curve and deploys a stable pool with some custom mechanics, which is allowed because of the user-supplied oracles. But developers didn't pay enough attention to the security of their price oracle, and a hack took place with the manipulation of the price oracle (flashloan manipulation, donation attack, price control in the pool, etc.) set by that team in the pool. In this case, Curve LPs will lose value.
In our opinion, it is impossible to control the quality of price oracles in an automated way (it is impossible to build this type of check inside any function) which is why we recommend adding a whitelist for oracles so the community can assess the quality of new oracles. Moreover, pools with volatile oracles will lead to permanent losses for LPs (if someone decides to create a wETH/wBTC pool with an oracle that sets the price from wETH to wBTC).

##### Recommendation
We recommend adding a whitelist for oracles' addresses.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#1-addresses-for-oracles-should-be-whitelisted
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

