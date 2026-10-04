---
# Core Classification
protocol: Devve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37642
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
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

Missing Sanity checks in multiple functions at Treasury

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

It was identified that multiple functions in Treasury.sol smart contract do not include checks to validate the provided parameters are not zero. Although this is not critical, failing to perform this validation can lead to unexpected behaviors
Examples of functions missing event emissions include:

`setUSDTAddress`
`setDesignatedSigner`
`setOwners`
`setplatformFee`

**Recommendation**: 

it is recommended to implement a check within these functions to ensure that the provided parameters are not zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Devve |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

