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
solodit_id: 33558
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#3-hooks-may-result-in-user-debt-exceeding-the-global_market_debt_ceiling-and-unbacked-tokens-being-minted
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

Hooks may result in user debt exceeding the `global_market_debt_ceiling` and unbacked tokens being minted

### Overview


The bug report is about a problem in a code for a loan system. It mentions that if a user creates a loan and the hook (a function that is called during the loan creation process) returns a negative value, then the system will mint unbacked stablecoins and not account for them in the total debt. This can result in the total debt exceeding the debt ceiling, which is the maximum amount of debt allowed in the system.

The report also mentions another scenario where if a user provides a negative value for the debt change in the adjust_loan() function and the hook adjusts it to a positive value, then the total debt can increase without being checked against the debt ceiling. This can also result in the total debt exceeding the debt ceiling.

The recommendation is to check the total debt against the debt ceiling when the debt adjustment is positive in the adjust_loan() function. It is also recommended to account for stablecoins that are not included in the total debt and are not backed.

### Original Finding Content

##### Description
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L718
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L768-L794


If a user creates a loan and the hook returns a negative value, then `minted > debt_increase` and unbacked stablecoins will be minted and not accounted in `_assert_below_debt_ceiling(total_debt)`:
```
def create_loan(
  ...
  debt_amount: uint256,
  ...
):
  ...
  hook_adjust: int256 = self._call_hooks(
    ...
  )
  debt_amount_final: uint256 = self._uint_plus_int(debt_amount, hook_adjust)
  ...
  debt_increase: uint256 = MarketOperator(market).create_loan(account, 
  coll_amount, debt_amount_final, n_bands)

  total_debt: uint256 = self.total_debt + debt_increase
  self._assert_below_debt_ceiling(total_debt)

  self.total_debt = total_debt
  self.minted += debt_amount
```
https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L718


In another scenario, if a user provides a negative `debt_change` to the `adjust_loan()` and the hook adjusts it to a positive value, then the original `debt_change < 0` but `debt_adjustment > 0`. In that case the `total_debt` is increased, but we don't fall into the `if debt_change > 0` statement and do not check for the debt ceiling:
```
debt_change_final: int256 = self._call_hooks(...) + debt_change
...
debt_adjustment: int256 = MarketOperator(market).adjust_loan(account, 
coll_change, debt_change_final, max_active_band)
...
total_debt: uint256 = self._uint_plus_int(self.total_debt, debt_adjustment)

if debt_change != 0:
    debt_change_abs: uint256 = convert(abs(debt_change), uint256)
    if debt_change > 0:
        self._assert_below_debt_ceiling(total_debt)
        self.minted += debt_change_abs
        STABLECOIN.mint(msg.sender, debt_change_abs)
    else:
        self.redeemed += debt_change_abs
        STABLECOIN.burn(msg.sender, debt_change_abs)
```
https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L768-L794


##### Recommendation
We recommend checking the `total_debt` against the debt ceiling when the `debt_adjustment > 0` in the `adjust_loan()` function. We also recommend taking into account stablecoins which are not included in the `total_debt` and are not backed.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#3-hooks-may-result-in-user-debt-exceeding-the-global_market_debt_ceiling-and-unbacked-tokens-being-minted
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

