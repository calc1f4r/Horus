---
# Core Classification
protocol: Geode
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44063
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Geode-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-05] Missing Zero Address Check for `changeSenate` Function

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

Contract GeodeModule is missing address validation for the setter function - `changeSenate()`.
It is possible to configure the address(0), which may cause issues during execution.

For instance, if address(0) is passed to `changeSenate()` function, it will
not be possible to change this address in the future.

## Location of Affected Code

File: [`contracts/Portal/modules/GeodeModule/GeodeModule.sol#L241-L243`](https://github.com/Geodefi/Portal-Eth/blob/e626ed341a723095c6d22fbfc84081cf7b999e1b/contracts/Portal/modules/GeodeModule/GeodeModule.sol#L241-L243)

```solidity
function changeSenate(address _newSenate) external virtual override {
  GEODE.changeSenate(_newSenate);
}
```

## Recommendation

Add a zero-address check on `_newSenate` parameter of `changeSenate()`.

## Team Response

Acknowledged, will be mitigated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Geode |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Geode-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

