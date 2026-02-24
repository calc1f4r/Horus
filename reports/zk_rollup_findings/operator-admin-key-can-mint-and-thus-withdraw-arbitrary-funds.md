---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40299
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c2a14eb1-a159-4fd8-8494-a4ead69ec097
source_link: https://cdn.cantina.xyz/reports/cantina_layern_l2rollup_jul2024.pdf
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
finders_count: 3
finders:
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Operator admin key can mint (and thus withdraw) arbitrary funds 

### Overview


This bug report discusses an issue with the rollup.rs code, specifically in line 189. The problem is that there is no way to check if a deposit is valid or not, which could lead to the admin being able to steal funds. The recommendation is to add a check either in Rollman or the deposit contract to prevent this from happening. This issue has been acknowledged and will be addressed in a future proposal to improve the deposit process. 

### Original Finding Content

## Rollup Validity Check Issue

**Context:** rollup.rs#L189

**Description:**  
There is no validity check or way to challenge a bad deposit (showing it doesn't exist). Rather, the process of challenging (as described in the design document supplied by the client) has no step which would check the existence of the receipts. Hence, if the admin signs off on a deposit, then it is considered valid and they can steal funds.

**Recommendation:**  
Ensure, either in Rollman or on the deposit contract side, that the admin cannot sign off on a bad deposit.

**Layer N:** Acknowledged. This will be fixed as part of a proposal we are implementing for having more robust deposits.

**Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_l2rollup_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c2a14eb1-a159-4fd8-8494-a4ead69ec097

### Keywords for Search

`vulnerability`

