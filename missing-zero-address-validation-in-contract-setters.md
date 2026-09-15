---
# Core Classification
protocol: Entangle Trillion
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51411
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
source_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
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
  - Halborn
---

## Vulnerability Title

Missing Zero Address Validation in Contract Setters

### Overview

See description below for full details.

### Original Finding Content

##### Description

Several contracts within the system lack necessary validations to prevent the assignment of the zero address (0x0) in their setter functions, specifically in `setBalanceManager` and `setFeeCollector` methods. This oversight could lead to issues, where critical functionalities could be disabled or misdirected to an address that is not usable, resulting in loss of control over the contract's intended behaviors. The absence of such checks increases the risk of accidental or malicious misconfiguration, potentially leading to loss of funds or access control.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

It is recommended to implement checks within the setter functions to ensure that the address being set is not the zero address.

  

**Remediation Plan:** The Entangle team acknowledged the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Entangle Trillion |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/entangle-trillion
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/entangle-trillion

### Keywords for Search

`vulnerability`

