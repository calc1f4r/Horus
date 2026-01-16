---
# Core Classification
protocol: Rivus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58231
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Function `rebase()` apply wrong APR in RivusTAO

### Overview

The function `rebase()` is not working properly and is causing a high impact on the system. This is because the code is using the wrong formula to calculate the burn amount, resulting in a larger amount being burned than intended. This can cause a significant increase in the token to share price ratio, leading to incorrect reward rates and potential theft of tokens. The recommended solution is to use a different formula to calculate the burn amount.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The function `rebase()` is supposed to apply daily APR to the share price by decreasing the total share amount. The issue is that the code uses `totalSharesAmount * apr` to calculate `burnAmount` so the burned amount would be bigger than what it should be. This is the POC:

1. Suppose there are 100 shares and 100 tokens.
2. Admin wants to apply a 20% increase for one day.
3. Code would calculate the burn amount as `100 * 20% = 20` and the new total share would be 80.
4. Now the token to share price would be `100/80 = 1.25` and as you can see the ratio increases by 25%.
5. This would cause a wrong reward rate and those who withdraw sooner would steal others tokens.

## Recommendations

Code should use `totalSharesAmount * apr / (1 +apr)` to calculate the burn amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Rivus |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

