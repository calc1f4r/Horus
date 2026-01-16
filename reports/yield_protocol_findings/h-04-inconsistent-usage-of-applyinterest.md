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
solodit_id: 42150
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-marginswap
source_link: https://code4rena.com/reports/2021-04-marginswap
github_link: https://github.com/code-423n4/2021-04-marginswap-findings/issues/64

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

[H-04] Inconsistent usage of `applyInterest`

### Overview


The function `applyInterest` is causing confusion as it is not clear if it should return a new balance with the interest applied or just the accrued interest. This inconsistency is causing incorrect values to be returned for both the balance and accrued interest. It is recommended to make the function consistent in all cases when it is called.

### Original Finding Content


It is unclear if the function `applyInterest` is supposed to return a new balance with the interest applied or only the accrued interest? There are various usages of it, some calls add the return value to the old amount:

```solidity
return
bond.amount +
applyInterest(bond.amount, cumulativeYield, yieldQuotientFP);
and some not:

balanceWithInterest = applyInterest(
balance,
yA.accumulatorFP,
yieldQuotientFP
);
```

This makes the code misbehave and return the wrong values for the balance and accrued interest.

Recommend making it consistent in all cases when calling this function.



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
- **GitHub**: https://github.com/code-423n4/2021-04-marginswap-findings/issues/64
- **Contest**: https://code4rena.com/reports/2021-04-marginswap

### Keywords for Search

`vulnerability`

