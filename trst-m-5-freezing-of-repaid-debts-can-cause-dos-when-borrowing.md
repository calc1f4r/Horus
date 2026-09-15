---
# Core Classification
protocol: Stella
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19057
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-5 Freezing of repaid debts can cause DoS when borrowing

### Overview


This bug report is about a miscalculation of borrowable funds in the BaseLendingPool.getBorrowableAmount() function. When a debt is repaid, the repaid amount gets frozen via freezeBuckets.addToFreezeBuckets(). In most scenarios, the repaid amount won’t be frozen by the mint freezing mechanism since the amount of time that has passed since the borrowed and repaid amount was deposited will almost always be greater than mintFreezeInterval (which is expected to be 1 day). This can cause a miscalculation of borrowable funds in the BaseLendingPool.getBorrowableAmount() function: in the worst case scenario, freezeBuckets.getLockedAmount() can return a value that’s bigger than the current balance of the pool (the repaid amount will be withdrawn), which will cause a revert and block borrowing. 

The team proposed a mitigation to not freeze repaid funds and fixed the issue by changing the algorithm (unlocking the same amount from the buckets when the user made withdrawals).

### Original Finding Content

**Description:**
When a debt is repaid, the repaid amount gets frozen via 
`freezeBuckets.addToFreezeBuckets()`. In most scenarios, the repaid amount won’t be frozen 
by the mint freezing mechanism since the amount of time that has passed since the borrowed 
and repaid amount was deposited will almost always be greater than **mintFreezeInterval**
(which is expected to be 1 day). Thus, a lender can withdraw a repaid amount while it’s frozen 
in FreezeBuckets. This can cause a miscalculation of borrowable funds in the 
`BaseLendingPool.getBorrowableAmount()` function: in the worst case scenario, 
`freezeBuckets.getLockedAmount()` can return a value that’s bigger (it’ll include the repaid 
amount) than the current balance of the pool (the repaid amount will be withdrawn), which 
will case a revert and block borrowing.

**Recommended Mitigation:**
Consider not freezing repaid funds.

**Team response:**
Fixed

**Mitigation Review:**
The team addressed this issue by changing the algorithm (unlocking the same amount from 
the buckets when the user made withdrawals).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

