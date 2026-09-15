---
# Core Classification
protocol: Eggs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46030
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/eeda9a4d-2065-4ea6-a3f1-b22e36beef3c
source_link: https://cdn.cantina.xyz/reports/cantina_eggs_february2025.pdf
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
finders_count: 2
finders:
  - Kaden
  - Optimum
---

## Vulnerability Title

repay does not decrease borrowed amount as expected 

### Overview


The report is about a bug in the code for a function called "repay" in the "Eggs" contract. This function is used to allow borrowers to repay a portion of the borrowed funds. However, there is an error in the code which causes the borrowed value to not decrease even though the borrower has successfully made a payment. This means that the borrower will lose the funds that they have repaid. 

The recommended solution for the short term is to change one line of code in the function. For the long term, it is suggested to improve the test coverage to catch these types of issues. The bug has been fixed in the "Eggs Finance" and "Cantina Managed" contracts. The severity of this bug is considered to be high risk.

### Original Finding Content

## Context
**File:** Eggs.sol#L342  

## Description
The `repay` function allows the borrower to repay a portion of the borrowed funds. The function successfully receives the SONIC payment but does not decrease the corresponding value of borrowed in the Loan struct as we can see:

```solidity
uint256 newBorrow = borrowed - msg.value;
Loans[msg.sender].borrowed - newBorrow;
```

This error will result in the caller losing these funds.

## Recommendation
**Short term:** Consider changing the issued line to:

```solidity
Loans[msg.sender].borrowed = newBorrow;
```

**Long term:** Consider improving test coverage to detect these kinds of issues.

## Eggs Finance
Fixed in commit `2f02fb77`.

## Cantina Managed
Fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eggs |
| Report Date | N/A |
| Finders | Kaden, Optimum |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eggs_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/eeda9a4d-2065-4ea6-a3f1-b22e36beef3c

### Keywords for Search

`vulnerability`

