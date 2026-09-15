---
# Core Classification
protocol: Bitcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46201
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/dd17f4e2-e240-4848-8b2e-557530a7d372
source_link: https://cdn.cantina.xyz/reports/cantina_bitcorn_december2024.pdf
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
  - Denis Miličević
  - Sujith Somraaj
---

## Vulnerability Title

Vault.initialize lacks some sanity checks for its parameters 

### Overview

See description below for full details.

### Original Finding Content

## Review of Contract Parameters

## Context
- **Files**: 
  - SimpleSwapFacility.sol (Lines 72-79)
  - Vault.sol (Lines 22-31)

## Description
The parameters `swapFacility` and `token` are explicit, lacking zero-address validation. The `token` is implicitly checked; if it is not a valid or at least masquerading ERC20 contract, the function will revert.

However, the `swapFacility` could be set to `address(0)`, which would leave the Vault in an invalid state. This situation would result in a loss of any collateral swapped via the associated SwapFacility contract until an upgrade is performed to correct it.

## Recommendation
- Explicitly implement zero-address validation for `swapFacility`.
- Consider utilizing OpenZeppelin's `isContract` check for `initialAuthority` or any other parameters expected to be pre-deployed contracts, which may also apply to `swapFacility`.
- Additionally, it would be good practice for the `swapFacility` to check that it has a sufficient threshold of transfer approval from the Vault it is initializing.

## Responses
- **Bitcorn**: Acknowledged. Will retain the existing behavior and leverage script-based confirmation of correct parameters prior to deployment.
- **Cantina Managed**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bitcorn |
| Report Date | N/A |
| Finders | Denis Miličević, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bitcorn_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/dd17f4e2-e240-4848-8b2e-557530a7d372

### Keywords for Search

`vulnerability`

