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
solodit_id: 33559
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#4-controllertotal_debt-may-not-be-up-to-date
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

`CONTROLLER.total_debt()` may not be up to date

### Overview


This bug report discusses an issue with the MainController._update_rate() function in the DFM Core project. The function may use an outdated total_debt value, resulting in incorrect calculations for the monetary policy rate. The report recommends updating the total_debt value before calling the _update_rate() function to avoid this issue.

### Original Finding Content

##### Description
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/AggMonetaryPolicy2.vy#L171

The `MainController._update_rate()` calls the monetary policy rate calculation method which may use a not updated `total_debt()`. 

For example, in the `adjust_loan()` method the `_update_rate()` is called before the `total_debt` update (https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L781):
```
debt_adjustment: int256 = MarketOperator(market).adjust_loan(account, 
coll_change, debt_change_final, max_active_band)

self._update_rate(market, c.amm, c.mp_idx) # self.total_debt is not updated

total_debt: uint256 = self._uint_plus_int(self.total_debt, debt_adjustment)
self.total_debt = total_debt
```

In case of large differences, `AggMonetaryPolicy2` may not calculate the new rate correctly.

##### Recommendation
We recommend calling `self._update_rate()` after updating the `MainController.total_debt`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#4-controllertotal_debt-may-not-be-up-to-date
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

