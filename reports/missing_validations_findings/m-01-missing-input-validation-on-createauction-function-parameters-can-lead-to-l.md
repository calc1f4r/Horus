---
# Core Classification
protocol: Rolling Dutch Auction
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20551
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-Rolling Dutch Auction.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Missing input validation on `createAuction` function parameters can lead to loss of value

### Overview


This bug report discusses an issue with the input validation in the `createAuction` function. The problems are related to the timestamp values, which can be equal to one another, too far in the future, or both. If these issues are not mitigated, the initial reserves and/or bids could be stuck in the protocol forever. The recommendation is to use a minimal and maximum duration value and to ensure the auction does not start more than a certain number of days after it has been created. The impact of this bug is high, but the likelihood of it occurring is low due to user error or misconfiguration.

### Original Finding Content

**Impact:**
High, as it can lead to stuck funds

**Likelihood:**
Low, as it requires user error/misconfiguration

**Description**

There are some problems with the input validation in `createAuction`, more specifically related to the timestamp values.

1. `endTimestamp` can be equal to `startTimestamp`, so `duration` will be 0
2. `endTimestamp` can be much further in the future than `startTimestamp`, so `duration` will be a huge number and the auction may never end
3. Both `startTimestamp` and `endTimestamp` can be much further in the future, so auction might never start

Those possibilities should all be mitigated, as they can lead to the initial reserves and/or the bids being stuck in the protocol forever.

**Recommendations**

Use a minimal `duration` value, for example 1 day, as well as a max value, for example 20 days. Make sure auction does not start more than X days after it has been created as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Rolling Dutch Auction |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-Rolling Dutch Auction.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

