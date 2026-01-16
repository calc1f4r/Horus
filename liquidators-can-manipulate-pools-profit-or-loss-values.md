---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19382
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Liquidators Can Manipulate Pool’s Profit or Loss Values

### Overview


This bug report is about a vulnerability in the CreditFacade.liquidateCreditAccount() protocol that allows liquidators to manipulate the protocol’s profit and loss accounting, which can lead to theft of funds from the pool. The vulnerability occurs when a liquidator borrows additional funds before closing the target credit account, resulting in the total value being under-represented in comparison to the borrowed amount with interest. This causes the CreditManager._calcClosePaymentsPure() to miscalculate the loss amount, allowing an attacker to continually burn diesel tokens held by the treasury at no cost to the attacker. The attacker can recover the tokens that they added to the borrower account. 

The development team mitigated this issue by only allowing external calls in _multicall when called from liquidateCreditAccount(). The checks in the commit were modified significantly in the final retesting target to the same effect.

### Original Finding Content

## Description

Liquidators can manipulate the protocol’s profit and loss accounting in `CreditFacade.liquidateCreditAccount()`, which can lead to theft of funds from the pool. 

The call to `_multicall()` is done after `totalValue` is calculated. Hence, if a liquidator borrows additional funds before closing the target credit account, `totalValue` will be under-represented in comparison to `borrowedAmountWithInterest`. 

This causes `CreditManager._calcClosePaymentsPure()` to miscalculate the loss amount as `amountToPool >= totalFunds`, which means `amountToPool = totalFunds`. The `totalFunds` will be less than `borrowedAmountWithInterest`, therefore the loss amount will be calculated as `borrowedAmountWithInterest - amountToPool`. 

This vulnerability allows an attacker to continually burn diesel tokens held by the treasury at no cost to the attacker. The attacker can recover the tokens that they added to the borrower account.

## Recommendations

Alter the logic of `CreditManager._calcClosePaymentsPure()` to reliably compute correct payment amounts in the case of liquidations.

## Resolution

The development team mitigated this issue in commit `bdbabc` by only allowing external calls in `_multicall` when called from `liquidateCreditAccount()`. 

Note that the checks in the above commit were modified significantly in the final retesting target to the same effect.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`

