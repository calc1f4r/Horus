---
# Core Classification
protocol: Marginswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42151
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-marginswap
source_link: https://code4rena.com/reports/2021-04-marginswap
github_link: https://github.com/code-423n4/2021-04-marginswap-findings/issues/24

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-06] Users are credited more tokens when paying back debt with `registerTradeAndBorrow`

### Overview


The `registerTradeAndBorrow` function is causing a bug where users are receiving double the amount they should when paying back their debt. This is because the function is incorrectly crediting the full `outAmount` as a deposit instead of only crediting `outAmount - extinguishableDebt`. This allows users to repeatedly withdraw and profit from the extra funds until the account is empty. The `registerDeposit` function correctly handles this scenario.

### Original Finding Content


The `registerTradeAndBorrow` is called with the results of a trade (`inAmount`, `outAmount`). It first tries to pay back any debt with the `outAmount`. However, the **full** `outAmount` is credited to the user again as a deposit in the `adjustAmounts(account, tokenFrom, tokenTo, sellAmount, outAmount);` call. As the user pays back their debt and is credited the same amount again, they are essentially credited twice the `outAmount`, making a profit of one `outAmount`. This can be withdrawn and the process can be repeated until the funds are empty.

In the `adjustAmounts` call, it should only credit `outAmount - extinguishableDebt` as a deposit like in `registerDeposit`.
The `registerDeposit` function correctly handles this case.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Marginswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-marginswap
- **GitHub**: https://github.com/code-423n4/2021-04-marginswap-findings/issues/24
- **Contest**: https://code4rena.com/reports/2021-04-marginswap

### Keywords for Search

`vulnerability`

