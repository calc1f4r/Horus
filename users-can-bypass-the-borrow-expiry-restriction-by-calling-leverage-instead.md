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
solodit_id: 46033
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/eeda9a4d-2065-4ea6-a3f1-b22e36beef3c
source_link: https://cdn.cantina.xyz/reports/cantina_eggs_february2025.pdf
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
finders_count: 2
finders:
  - Kaden
  - Optimum
---

## Vulnerability Title

Users can bypass the borrow expiry restriction by calling leverage() instead 

### Overview


The bug report states that there is an issue with the leverage() function in the Eggs Finance and Cantina Managed systems. The function combines the buy() and borrow() functions, but it does not have a check in place to restrict users from taking loans for more than a year. This means that users can bypass the restriction and potentially cause problems. The recommendation is to add this check to the leverage() function. This issue has been fixed in the Eggs Finance system in commit 2f02fb77 and in the Cantina Managed system as recommended.

### Original Finding Content

## Review Summary

## Context
(No context files were provided by the reviewer)

## Description
The `leverage()` function acts as a function that combines both `buy()` and `borrow()`. The `borrow()` function restricts the user from taking loans for a period of more than a year:

```solidity
require(
    numberOfDays < 366,
    "Max borrow/extension must be 365 days or less"
);
```

However, `leverage()` lacks this kind of check, effectively allowing users to bypass it.

## Recommendation
Consider adding this check to `leverage()` as well.

## Status
- **Eggs Finance**: Fixed in commit 2f02fb77.
- **Cantina Managed**: Fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

