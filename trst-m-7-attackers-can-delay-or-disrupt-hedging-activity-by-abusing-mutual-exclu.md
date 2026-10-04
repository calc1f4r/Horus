---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18902
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
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
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-7 attackers can delay or disrupt hedging activity by abusing mutual exclusion with updateCollateral()

### Overview


The PoolHedger is a system used to offset exposure. It has an engine, hedgeDelta(), that is used to manage position requests from users. GMX keeper will execute all requests in a batch every few seconds. When there is a pending action, `hedgeDelta()` and `updateCollateral()` cannot be called. The latter function triggers the correction of the leverage ratio on GMX to the target. 

The issue is that there are no DOS-preventions put in place, which allow attackers to continually call `updateCollateral()` as soon as the previous request completes, keeping the Hedger ever busy perfecting the leverage ratio, albeit not hedging properly. This could lead to an increased insolvency risk for the protocol as it is not delta-neutral.

To mitigate this issue, one option is to make sure the delta correction is significant for it to succeed, preventing the DOS. Another option is to refactor the code to have only one entry point. This will guarantee the prioritization of delta-neutrality over reaching the target leverage ratio. The team has fixed this issue.

### Original Finding Content

**Description:**
`hedgeDelta()` is the engine behind the PoolHedger.sol used to offset exposure.
 GMX increase / decrease position requests are performed in two steps to minimize slippage attacks. Firstly, 
users call `increasePositionRequest()`. Every short period (usually several seconds), GMX keeper 
will execute all requests in a batch. The PoolHedger deals with this pending state using the 
**pendingOrderKey** parameter. When it is not 0, it is the key received from the last GMX 
position request. When there is a pending action, `hedgeDelta()` as well as `updateCollateral()` 
cannot be called. The latter function is another permissionless entry point, which triggers the 
correction of the leverage ratio on GMX to the target. The issue stems from the fact there are 
no DOS-preventions put in place, which allow attackers to continually call `updateCollateral()` 
as soon as the previous request completes, keeping the Hedger ever busy perfecting the 
leverage ratio, albeit not hedging properly. If done for a long enough period, the impact is an 
increased insolvency risk for the protocol as it is not delta-neutral.

**Recommended mitigation:**
One option is to make sure the delta correction is significant for it to succeed, preventing the 
DOS. Another option is to refactor the code to have only one entry point. This will guarantee 
the prioritization of delta-neutrality over reaching the target leverage ratio.

**Team response:**
Fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

