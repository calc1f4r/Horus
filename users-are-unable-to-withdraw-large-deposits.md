---
# Core Classification
protocol: Spool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56559
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
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
  - Zokyo
---

## Vulnerability Title

Users are unable to withdraw large deposits.

### Overview


The bug report states that there is an issue with the redeemUser() function when a user has deposited a large amount of tokens (around 50). This causes an overflow error and prevents the user from withdrawing their funds. The recommendation is to check if it is possible to withdraw all deposits.

### Original Finding Content

**Description**

In case user has deposited a big deposit(starting with 50 tokens approximately), redeemUser()
function fails with overflow error, which prevents the user from withdrawing funds.

**Recommendation**:

Verify, that it is possible to withdraw all deposits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Spool |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-30-Spool.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

