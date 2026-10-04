---
# Core Classification
protocol: Arcade.xyz
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40689
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b2f35a21-b116-4ed6-95e6-37405749a716
source_link: https://cdn.cantina.xyz/reports/cantina_competition_arcade_mar2024.pdf
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
  - jesjupyter
---

## Vulnerability Title

lender may incur losses on a loan if the borrower repays it quickly, considering the lender- principlefee 

### Overview


The bug report is about a potential issue with the InterestCalculator function in a smart contract called InterestCalculator.sol. The problem is that there is no minimum time limit for a borrower to repay their debt, which can result in a loss of funds for the lender. This is because the interest earned by the lender may not cover the fees they have to pay for the loan. The report recommends implementing a minimum interest requirement to address this issue.

### Original Finding Content

## Interest Calculator Overview

## Context
`InterestCalculator.sol#L65`

## Description
There is no minimum time limit for a borrower to repay the debt. If the borrower calls `repayFull` not soon after the loan is signed, this may incur a loss of funds for the lender. The lender has to pay the following fees:

```
Principal * (LENDER_ORIGINATION_FEE + LENDER_PRINCIPAL_FEE) / Constants.BASIS_POINTS_DENOMINATOR;
```

And the lender will receive the following:

```
interest * (Constants.BASIS_POINTS_DENOMINATOR - lenderInterestFee) / Constants.BASIS_POINTS_DENOMINATOR;
```

However, the interest here isn’t fixed. It is calculated using the following formula in `InterestCalculator::getProratedInterestAmount`:

```
Principal * timeSinceLastPayment * interestRate / (Constants.BASIS_POINTS_DENOMINATOR * Constants.SECONDS_IN_YEAR);
```

If the borrower calls `repayFull` not soon after the loan is signed, `timeSinceLastPayment` would be quite small, and the interest they receive may not be able to cover the fees they paid for the loan. Thus, this may incur a loss of funds for the lender. The uncertainty of income and principal losses hinders the motivation and information for lenders to participate in lending.

## Recommendation
To properly deal with this issue, a minimum interest to pay during the whole loan from the borrower should be considered.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Arcade.xyz |
| Report Date | N/A |
| Finders | jesjupyter |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_arcade_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b2f35a21-b116-4ed6-95e6-37405749a716

### Keywords for Search

`vulnerability`

