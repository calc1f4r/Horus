---
# Core Classification
protocol: Teahouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45725
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
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

Insufficient Sanity Checks of Liquidity Parameters

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational 

**Status**: Acknowledged

**Description**:

The addLiquidity() function relies on the manager to provide appropriate values for _tickLower, _tickUpper, and _liquidity. If the manager provides invalid or extreme values, it could result in failed transactions or unintended behavior. Additionally, there's a risk of rounding errors due to the adjustments made to the liquidity amount (roundUpX12Liquidity).

**Recommendation**:

Implement validation checks on the liquidity parameters provided by the manager. This could include:
Ensuring that _tickLower is less than _tickUpper.
Verifying that the _liquidity amount is within acceptable bounds.
Handling rounding adjustments carefully to prevent significant discrepancies.

**Client comment**: We left the checking of the parameters to Ambient’s contracts. They should revert if the parameters are incorrect.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Teahouse |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

