---
# Core Classification
protocol: Zkdx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37511
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
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

Missing zero address check in `setGov()` of `VaultPriceFeed`

### Overview

See description below for full details.

### Original Finding Content

**Severity** : Low

**Status** : Resolved

**Description** : 

VaultPriceFeed.sol has missing zero address check in `setGov()` for `_gov` address parameter. This can lead to the gov being accidentally set as zero address, leading to `onlyGov` function being uncallable forever. 
The same issue exists in the VaultSettings contract which the Vault.sol contract inherits. Setting gov as zero address here would lead to `withdrawFees()` being uncallable amongst other functions, leading to stuck fees in the Vault. 

**Recommendation**: 

It is advised to add a zero address check for the same.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zkdx |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

