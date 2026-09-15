---
# Core Classification
protocol: Shield Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55843
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield Finance.md
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
  - Zokyo
---

## Vulnerability Title

Missing mint method

### Overview


The report describes a bug related to the _mint() function in a token's code. This function is being overloaded, meaning that it has multiple definitions with different parameters, but it is only being called from one place in the code. This suggests that either the public mint() function is missing or the overloaded _mint() function is not needed. The recommendation is to clarify the purpose and necessity of both the _mint() and mint() methods in the code.

### Original Finding Content

**Description**

Line 95, _mint() function overloading
Token’s initializer already provides mint for the full maximum supply (line 48, mint for
getMaxTotalSupply()). Though the token can enable burn functionality, so more place for
minting appears. Though, overloaded _mint() function is called from nowhere but from the
initializer, which is called only once. Looks like either public mint() function is absent, or
overload _mint() method is unnecessary.

**Recommendation**:

Clarify the minting logic and the necessity of _mint() and mint() methods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Shield Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

