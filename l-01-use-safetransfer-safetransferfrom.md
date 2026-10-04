---
# Core Classification
protocol: Rwa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48934
audit_firm: Kann
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
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
  - Kann Audits
---

## Vulnerability Title

[L-01] Use safeTransfer & safeTransferFrom

### Overview


The report states that there is a problem with some ERC-20 tokens not behaving as expected. Specifically, these tokens are not reverting transactions when they fail and some are not returning any value at all. This means that not all tokens are following the standard for ERC-20 tokens.

### Original Finding Content

**Description**

Some ERC-20 tokens will return on failure instead of reverting a transaction, Some tokens will even not return any value. not all tokens adhere to the standart of ERC-20

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Rwa |
| Report Date | N/A |
| Finders | Kann Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

