---
# Core Classification
protocol: Tangleswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44565
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-Tangleswap.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Exposed to reentrancy

### Overview


This bug report describes a security issue in two smart contracts, FixRange.sol and DynamicRange.sol. The emergencyWithdraw function is vulnerable to reentrancy attacks, meaning an attacker can repeatedly call this function and potentially access sensitive data or manipulate the contract's state. This is a high severity issue and has been resolved by implementing a reentrancy guard using best practices and modifiers. 

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

FixRange.sol & DynamicRange.sol - emergencyWithdraw is exposed to reentrancy due to safeTransfer. An attacker can reenter this method by having a external call implemented in his onERC721Received that will call other functions from the same contract context or different contract context.  Other way is to reenter other methods like withdraw or collectReward.  This can be highly severe because the state is not updated before the reentrancy.

**Recommendation**: 

Apply a wide reentrancy guard using best practices pattern and modifiers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tangleswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-13-Tangleswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

