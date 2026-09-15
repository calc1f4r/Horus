---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54425
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6
source_link: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
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
  - Liam Eastwood
  - Sujith Somraaj
---

## Vulnerability Title

LiquidityPool does not conform to ERC4626 

### Overview

See description below for full details.

### Original Finding Content

## LiquidityPool.sol Overview

## Context
LiquidityPool.sol tries to conform to ERC-4626, a vault standard that makes the vault interface optimized for integrators. However, the current LiquidityPool contract behaves in a way that is significantly different from a typical ERC-4626 implementation.

## Description
- The `previewDeposit()` function works on the user's average `state.depositPrice`, but the `deposit()` function will always fail since the user should call `requestDeposit()` before calling the actual `deposit()` function.
- This effectively leads to the `previewDeposit()` function returning unrelated values, even when the `deposit()` function will revert for all possible combinations of amount inputs.
- Similar effects persist on `mint()` and `redeem()` functions as well. This poses a risk for integrators, as their protocol cannot make any ERC-4626-based assumptions.

## Recommendation
- Add clear directions to integrators that the vault is not ERC-4626 compliant but just uses similar function signatures.
- Ensure the preview functions work as a normal ERC-4626 vault and revert in the following execution function calls: `mint`, `deposit`, `redeem`.

## Status
- **Centrifuge:** Fixed in commit `bda5ba6e`.
- **Cantina:** Verified fix. Preview methods have been removed to comply with a new async vault token standard, EIP-7540.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Liam Eastwood, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6

### Keywords for Search

`vulnerability`

