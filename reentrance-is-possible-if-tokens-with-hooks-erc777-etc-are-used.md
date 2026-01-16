---
# Core Classification
protocol: Tide
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37343
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-26-Tide.md
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

Reentrance is possible if tokens with hooks (ERC777, etc.) are used

### Overview


The bug report is about a medium severity issue that has been resolved. The issue was found in a contract called WaveContract.sol, where a method called executeRuffle() was sending rewards to the winner. However, if the reward token being used had certain features, the winner could exploit the method and repeatedly receive rewards. To fix this, it is recommended to use a modifier called nonReentrant() from a library called OpenZeppelin's ReentrancyGuard.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In Contract WaveContract.sol, the method executeRuffle(...) sends rewards to the winner but if the reward token is ERC77& or any token with hooks, the winner can reenter the executeRuffle() method to win the rewards again and again. 

**Recommend**: 

It is advised to use OpenZeppelin’s ReentrancyGuard’s nonReentrant() modifier here.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tide |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-26-Tide.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

