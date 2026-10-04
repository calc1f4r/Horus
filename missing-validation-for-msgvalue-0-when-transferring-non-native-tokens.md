---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46294
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016
source_link: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
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
  - MiloTruck
  - Víctor Martínez
---

## Vulnerability Title

Missing Validation for msg.value == 0 When Transferring Non-Native Tokens 

### Overview

See description below for full details.

### Original Finding Content

## ClaggBaseAdapter.sol#L540

## Description
The `_transferFromCaller` function in the Base Adapter does not enforce `msg.value == 0` when transferring non-native tokens. This omission could result in ETH being locked in the protocol. It is considered a best practice to enforce this check, so it is recommended to implement it to prevent potential issues.

## Recommendation
Consider adding a check for `msg.value == 0` when the token is not native (ETH) to ensure ETH is not accidentally locked in the protocol.

## Clave
Fixed at commit d724825b.

## Cantina Managed
Verified, the recommended fix was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | MiloTruck, Víctor Martínez |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016

### Keywords for Search

`vulnerability`

