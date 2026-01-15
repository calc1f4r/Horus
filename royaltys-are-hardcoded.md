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
solodit_id: 21026
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

ROYALTY's are hardcoded

### Overview


This bug report is about the percentage of royalty or service fee being hardcoded. This means that the developers or community cannot update the percentage of fee collected in the future if they decide to do so. The recommendation to resolve this bug is to add a function to update the percentage of fee collected, protected by the Owner. This bug has been resolved.

### Original Finding Content

**Description:** 

The percentage of royalty or service fee is hardcoded. In future,if the developers or the community decide to update the percentage via governance etc.,it will be not be possible. 

**Recommendations:**

Add a function to update the percentage of fee collected protected by Owner.

**Status:** Resolved

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

