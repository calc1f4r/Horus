---
# Core Classification
protocol: Tren
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45827
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-Tren.md
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

Inadequate Pool Validity Check in suspendDeposit Function

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**: 

The suspendDeposit function allows anyone with ownership control to suspend deposits for a non-existent pool, as there is no check to verify if the given stablecoin address (stable) is valid. This could lead to unexpected behavior or unintentional suspension.

**Recommendation**: 

Add a validation to check if pools[stable] is valid before changing the suspension status
```solidity
 if (!validStables[stable]) revert PoolDoesNotExist();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tren |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-Tren.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

