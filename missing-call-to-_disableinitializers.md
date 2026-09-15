---
# Core Classification
protocol: Colend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45916
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-07-Colend.md
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

Missing call to _disableInitializers

### Overview


This bug report describes a medium severity issue that has been resolved. It explains that an attacker can take control of a contract that has not been initialized, which can affect both the contract and its implementation. To prevent this, the report recommends calling a specific function in the constructor of Geyser.sol. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

An uninitialized contract can be taken over by an attacker. This applies to both a proxy and its implementation contract, which may impact the proxy. To prevent the implementation contract from being used, you should invoke the _disableInitializers() function in the constructor to automatically lock it when it is deployed, more information can be found here.

**Recommendation**: 

Consider calling _disableInitializers()in the constructor on Geyser.sol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Colend |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-07-Colend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

