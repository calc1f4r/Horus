---
# Core Classification
protocol: Lotaheros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21023
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
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
  - AuditOne
---

## Vulnerability Title

Missing input validation for various functions

### Overview


This bug report is about a potential vulnerability in a system where an attacker can set an arbitrary address as the token address. This could lead to funds being sent to the attacker or other unintended consequences. The report recommends input validation to ensure that the inputted address is not a zero/malicious address. This can be done by adding a require statement at the beginning of each function to check whether the inputted address is valid. This is an important security measure to prevent attackers from exploiting this vulnerability.

### Original Finding Content

**Description:**

The functions above do not explicitly check whether the inputted address is a zero address or a malicious address. This can allow an attacker to set an arbitrary address as the token address, potentially leading to funds being sent to the attacker or other unintended consequences. **Recommendations:** It would be a good practice to add input validation to ensure that the inputted address is not a zero/malicious address. This can be done by adding a require statement at the beginning of each function to check whether the inputted address is valid. For example:

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Lotaheros |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

