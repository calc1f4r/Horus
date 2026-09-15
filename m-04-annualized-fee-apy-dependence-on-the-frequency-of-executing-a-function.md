---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6526
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/280

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Czar102
---

## Vulnerability Title

[M-04] Annualized fee APY dependence on the frequency of executing a function

### Overview


This bug report is about the Annual Percentage Yield (APY) of an annualized fee, which is dependent on the frequency of the execution of the BasketFacet::chargeOutstandingAnnualizedFee(). If the execution is done more frequently, the compounding will be more frequent and the APY will be higher. However, if the execution is done less frequently, the compounding will be at a lower rate, resulting in a lower APY. The bug was identified through manual analysis. The recommended mitigation step is to consider calculating the fee as the compounding was continuous or with a constant compounding period.

### Original Finding Content


_Submitted by Czar102_

#### Impact

The APY of the annualized fee is dependent on the frequency of the execution of the [`BasketFacet::chargeOutstandingAnnualizedFee()`](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/facets/Basket/BasketFacet.sol#L265-L279). If it is called more frequently, the compounding is more frequent and the APY is higher. For less used baskets, the APY might be lower, because the compounding will happen at lower rate.

#### Recommended Mitigation Steps

Consider [calculating the fee](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/facets/Basket/BasketFacet.sol#L259-L262) as the compounding was continous or with a constant compounding period.

**[loki-sama (Amun) acknowledged](https://github.com/code-423n4/2021-12-amun-findings/issues/280)** 

**[0xleastwood (Judge) commented](https://github.com/code-423n4/2021-12-amun-findings/issues/280#issuecomment-1019036751):**

> Nice find!



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | Czar102 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/280
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

