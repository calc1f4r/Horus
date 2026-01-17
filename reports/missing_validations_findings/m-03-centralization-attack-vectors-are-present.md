---
# Core Classification
protocol: Bloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20597
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
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

[M-03] Centralization attack vectors are present

### Overview


This bug report is about a vulnerability in the SwapFacility protocol which allows the owner to set the pool variable to any value, potentially breaking the protocol for users. It also mentions that the setSpreadPrice method does not do any input validation, meaning the spreadPrice can be set to a huge number that is bigger than the token prices, which will make the swap transactions revert every time. The likelihood of this vulnerability being exploited is low as it requires a malicious or a compromised owner. The impact of this vulnerability is high as it can break the protocol for users.

To fix this vulnerability, the report recommends making the setPool callable only once and putting an upper bound of the spreadPrice value. This way, the pool variable won't be able to be set to any value and the spreadPrice won't be able to be set to a huge number, thus preventing the protocol from being broken.

### Original Finding Content

**Impact:**
High, as it can break the protocol for users

**Likelihood:**
Low, as it requires a malicious or a compromised owner

**Description**

The `owner` of `SwapFacility` can change the `pool` variable any time, meaning it can be set to `address(0)` for example, breaking the protocol's `swap` functionality. Another such issue is that the `setSpreadPrice` method does not do any input validation, meaning the `spreadPrice` can be set to a huge number that is bigger than the token prices, which will make the spread subtraction revert the `swap` transactions every time.

**Recommendations**

Make `setPool` callable only once and also put an upper bound of the `spreadPrice` value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bloom |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

