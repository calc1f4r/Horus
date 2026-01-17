---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45611
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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

Returning position.collateral When pnlWithFees > 0 Might Be Problematic

### Overview


This report discusses a bug in a function called validateLiquidation, which is used to determine if a position can be liquidated or not. The issue lies in the CurrentCollateral function, where it may miscalculate the current collateral if the position has made a profit and received trading fees. This can lead to healthy positions being mistakenly liquidated. The recommendation is to fix the function to return the correct value of position.collateral + pnlWithFees. The severity of this bug is high, but it has been marked as invalid.

### Original Finding Content

**Severity** - High

**Status** - Invalid

**Description**

(Please double check this finding )

_validateLiquidation is a function which is used to check if a position is liquidatable or not , to check this it calculates the current collateral using the CurrentCollateral function , in the current collateral function if the position made a profit and also received trading fee (dependent on the direction of the market ) the calculated collateral can be much higher than the original collateral in the function , 

But in the case for a profit the CurrentCollateral function returns →
```solidity
int256 pnlWithFees = pnl - int256(collectFees(position)) - int256(_liquidationFee) + fundingFee;
        if (pnlWithFees > 0) {
            return (position.collateral);        }
```

It returns position.collateral rather than position.collateral + pnlWithFees , therefore if the position’s collateral made a very good profit and received trading fees to put it out of the liquidation criteria, the function would still return the old collateral which could be subject to liquidation . Hence, healthy positions might get liquidated in the system.


**Recommendation**:

Return position.collateral + pnlWithFees

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

