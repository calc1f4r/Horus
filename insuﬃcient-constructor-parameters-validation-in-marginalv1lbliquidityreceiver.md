---
# Core Classification
protocol: Marginal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40249
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a598d54-c212-4168-acb1-b13c5a08b204
source_link: https://cdn.cantina.xyz/reports/cantina_marginal_aug2024.pdf
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
  - Jeiwan
  - defsec
---

## Vulnerability Title

Insuﬃcient constructor parameters validation in MarginalV1LBLiquidityReceiver 

### Overview

See description below for full details.

### Original Finding Content

## Context
MarginalV1LBLiquidityReceiver.sol#L170

## Description
The `MarginalV1LBLiquidityReceiver.checkParams` validates the constructor parameters of the contract. However, `params.treasuryAddress` and `params.lockOwner` are not validated:

1. `params.treasuryAddress` receives fees from the rewards, thus it should never be the zero address.
2. `params.lockOwner` withdraws liquidity from Uniswap and Marginal, it should never be the zero address (except for when liquidity is locked indefinitely).

## Recommendation
Consider adding the missed checks to `MarginalV1LBLiquidityReceiver.checkParams()`.

## Marginal
Fixed in commit `4eade4df`. Still not checking `lockOwner` is zero address to allow users to burn the LPs if they wish.

## Cantina Managed
Fix is verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Marginal |
| Report Date | N/A |
| Finders | Jeiwan, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_marginal_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3a598d54-c212-4168-acb1-b13c5a08b204

### Keywords for Search

`vulnerability`

