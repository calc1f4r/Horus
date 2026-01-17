---
# Core Classification
protocol: Mint Gold Dust
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56072
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint Gold Dust.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Missing zero check during initialization

### Overview

See description below for full details.

### Original Finding Content

**Description**

contracts/OrderBook.sol#48, withdrawAddress
The variable is actively used in the contract, though is not checked against the zero address.
Since there is no ability to change the value and since the initialization is performed only in the
initializer the issue is classified as Low.

**Recommendation**:

Add check that the address is not zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Mint Gold Dust |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint Gold Dust.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

