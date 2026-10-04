---
# Core Classification
protocol: DeFi Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33556
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#1-the-amm-rate-is-not-updated-in-certain-cases
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

The AMM rate is not updated in certain cases

### Overview


The bug report highlights an issue in the DFM Core code where changing the monetary policy does not immediately update the interest rate for the Automated Market Maker (AMM). This can result in users experiencing losses or missed profits if they are inactive in the market. The report recommends implementing a mechanism to update the rate when the policy is changed and monitoring for significant losses for lenders and borrowers.

### Original Finding Content

##### Description
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L1085-L1092
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L1097-L1104

If the admin changes monetary policy via `MainController.change_existing_monetary_policy()` or `MainController.change_market_monetary_policy()`, the interest rate of the AMM is not set to the new one until someone interacts with AMM via the following operations:
- `create_loan()`
- `adjust_loan()`
- `close_loan()`
- `liquidate()`
- `collect_fees()`

Thus, if the new monetary policy rate for a market is high and users in that market are inactive, their positions will remain at the old low rate,  potentially causing the protocol to miss out on additional profits. Conversely, if the new rate is low, positions in a low-activity market may continue at the old high rate with extra losses for borrowers.

##### Recommendation
We recommend calling `_update_rate()` when the monetary policy is changed. We also recommend implementing monitoring mechanisms to check that lenders and borrowers do not accumulate significant losses due to unsynchronized rates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DeFi Money |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#1-the-amm-rate-is-not-updated-in-certain-cases
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

