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
solodit_id: 27697
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#3-incorrect-parameters-passed-to-fee-calculation
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

Incorrect parameters passed to fee calculation

### Overview


A bug was recently found in the CurveFi Stableswap-ng code, which affects how the 'xs' variable is calculated. 'xs' is calculated using token balances from four different locations in the code, while 'ys' is calculated using balances and rates. The issue is that 'xs' is calculated without taking into account the 'rates' variable, which can lead to users paying more fees than they should. 

To fix this issue, it is recommended that 'xs' be multiplied by 'rates'. This will ensure that the fees are calculated correctly and users will not be overcharged.

### Original Finding Content

##### Description
`xs` is calculated using token balances in the following places:
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L700
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L827
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapNG.vy#L589
https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapNG.vy#L712.
`ys` is calculated using balances * rates (D / N_COINS ~ balance[i] * rate[i] / PRECISION). As `ys` is calculated with `rates` and `xs` is calculated without them, the fees will be higher than they should be and users will pay more (if rates >> PRECISION e.g. if token decimals < 18).

##### Recommendation
We recommend multiplying `xs` by `rates`.


***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#3-incorrect-parameters-passed-to-fee-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

