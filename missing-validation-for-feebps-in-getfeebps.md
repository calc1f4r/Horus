---
# Core Classification
protocol: ChainPro
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46220
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/30cdd4ee-e056-4cf0-8104-23bd6119bad2
source_link: https://cdn.cantina.xyz/reports/cantina_chainpro_december2024.pdf
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
finders_count: 2
finders:
  - Cynops
  - slowfi
---

## Vulnerability Title

Missing validation for fee.bps in getFeeBps 

### Overview

See description below for full details.

### Original Finding Content

## Issue Report: Fee Configuration in `getFeeBps` Function

## Context
**File:** `math.ts`  
**Lines:** 5-8

## Description
The `getFeeBps` function in `math.ts` of Ellisiland assumes that the `bps` (basis points) field in the `FeeConfig` object is always set when a fee is provided. However, if `fee.floor` is set but `fee.bps` is undefined, the code on line 7 attempts to call `multiplyBigInt` with `inAmount` and `NaN` as arguments, causing execution to fail.

This scenario can occur when a bridged call to `runTask` is issued with a `swapConfig` containing a fee object where only the `floor` value is defined. The failure occurs because the function does not validate whether `fee.bps` is defined before attempting to use it.

## Recommendation
Update the `getFeeBps` function to validate that both `fee.floor` and `fee.bps` are defined before using them. If either value is missing, the function should return a default or error appropriately.

Additionally, add validation logic in `runTask` and `sendTask` to ensure that the fee object in `swapConfig` contains both `floor` and `bps` before passing it to `getFeeBps`. This will prevent invalid configurations from propagating through the system.

## ChainPro
Fixed in commit `1bfd604f` by defining `fee.bps` to a default value.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | ChainPro |
| Report Date | N/A |
| Finders | Cynops, slowfi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_chainpro_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/30cdd4ee-e056-4cf0-8104-23bd6119bad2

### Keywords for Search

`vulnerability`

