---
# Core Classification
protocol: Zunami Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30985
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami ProtocolV2.md
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
  - Oxorio
---

## Vulnerability Title

[FIXED] Latency of APS logic in `CrvUsdApsConvexCurveStratBase`, `FraxApsConvexCurveStratBase`

### Overview


The bug report highlights an issue with the functions `inflate` and `deflate` in the contracts `CrvUsdApsConvexCurveStratBase` and `FraxApsConvexCurveStratBase`. These functions can only be called by the DAO, which has a delay of 7 days before executing proposals. This can cause a temporary depegging of the `zunUSD` token. The recommendation is to implement an emergency APS mechanism that can be activated without any delay. This bug has been fixed in the latest commit `9ffa8e1b6128d1ade8459a4e492cee669ed241a1`.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[CrvUsdApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol#L90 "/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol") | contract `CrvUsdApsConvexCurveStratBase` > function `inflate` | 90
[CrvUsdApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol#L125 "/contracts/strategies/curve/convex/aps/crvUSD/CrvUsdApsConvexCurveStratBase.sol") | contract `CrvUsdApsConvexCurveStratBase` > function `deflate` | 125
[FraxApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol#L91 "/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol") | contract `FraxApsConvexCurveStratBase` > function `inflate` | 91
[FraxApsConvexCurveStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol#L121 "/contracts/strategies/curve/convex/aps/crvFrax/FraxApsConvexCurveStratBase.sol") | contract `FraxApsConvexCurveStratBase` > function `deflate` | 121

##### Description
The functions `inflate` and `deflate` in the contracts `CrvUsdApsConvexCurveStratBase` and `FraxApsConvexCurveStratBase` can only be called by the DAO. The DAO mechanism involves significant latency between the start of voting and the execution of proposals. For instance, if the governance voting period is 7 days, then all APS strategy functions (`inflate` and `deflate`) are executed with a 7-day delay. This could lead to the temporary depegging of the `zunUSD` token.

##### Recommendation
We recommend implementing an emergency APS mechanism that can be activated without any latency.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Zunami Protocol |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami ProtocolV2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

