---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53329
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-11] Pending withdrawal tokens in `redeem()` affect share price

### Overview


The report describes a bug in the `redeem()` function that affects the share price calculation in a vault. This bug can lead to incorrect valuations and distribution of funds among users. The severity is high and the likelihood is medium. The recommendation is to update the share price calculation to exclude pending withdrawal tokens until they are finalized.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

Pending withdrawal tokens in the `redeem()` function are still considered in the share price calculations.
Since `totalSupply` and `_totalAssets` are not updated to reflect the pending withdrawals:

```solidity
        // Transfer shares from owner to vault
        balanceOf[owner] -= shares;
        balanceOf[address(this)] += shares;
```

The share price would be incorrect for profit/loss that happens later. When the pending withdrawals are finalized (by calling `topOff`), the share price will adjust to account for the withdrawals that were not previously considered. This could lead to inconsistencies in share valuation, causing wrong fund distributions among users over time.

## Recommendations

Update the share price calculation to exclude pending withdrawal tokens until they are finalized. This will ensure that `totalSupply` and `totalAssets` accurately reflect the current state of the vault and provide an accurate share price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

