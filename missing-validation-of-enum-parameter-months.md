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
solodit_id: 45828
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

Missing Validation of Enum Parameter months

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

The contract accepts a months parameter of type MONTHS (an enum) in several functions without validating that the value is within the valid range. Enums in Solidity are represented as uint8, and users can pass invalid values outside the defined enum range.

**Scenario**

A user calls the deposit function with an invalid months value:
singleLiquidityProvider.deposit(stableAddress, amount, MONTHS(255), true);
The MONTHS enum only defines values for SIX, TWELVE, and EIGHTEEN.
Passing MONTHS(255) could cause calculateLockedPeriod to default to unexpected behaviour.

**Recommendation**:

Validate months Parameter to Ensure It's Within Defined Enum Values
Create a function to check if months is a valid enum value.Reject any months value outside the defined enum range.

**Comment**: 

the MONTHS parameter is not supplied by the user anymore.

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

