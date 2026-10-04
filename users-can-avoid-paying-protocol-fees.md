---
# Core Classification
protocol: Royco
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46680
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2
source_link: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
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
finders_count: 4
finders:
  - Kurt Barry
  - Yorke Rhodes
  - kankodu
  - 0x4non
---

## Vulnerability Title

Users can avoid paying protocol fees 

### Overview


Bug Report Summary:

The bug is located in the RecipeOrderbook.sol file on line 494. When an IP order is created, the protocolFee is not being applied correctly in the fillLPOrder function. This means that users can avoid paying the protocolFee by using the createLPOrder and fillLPOrder functions instead of the createIPOrder and fillIPOrder functions. The recommended solution is to add the protocolFee calculation in the fillLPOrder function to ensure that fees are consistently applied across all order types. This bug has been fixed in the commits a39f7d01 and has been verified by Cantina Managed.

### Original Finding Content

## Issue Report

## Context
**File**: RecipeOrderbook.sol  
**Line**: 494

## Description
When an IP order is created, the `protocolFee` is assigned to the `protocolFeeRecipient`. However, this `protocolFee` calculation is missing in the `fillLPOrder` function. As a result, users can avoid the `protocolFee` if they match orders using `createLPOrder` + `fillLPOrder` instead of `createIPOrder` + `fillIPOrder`.

## Recommendation
Add the `protocolFee` calculation in the `fillLPOrder` function to ensure consistent fee application across all order types.

## Status
- **Royco**: Fixed in commit `a39f7d01`.
- **Cantina Managed**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Royco |
| Report Date | N/A |
| Finders | Kurt Barry, Yorke Rhodes, kankodu, 0x4non |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2

### Keywords for Search

`vulnerability`

