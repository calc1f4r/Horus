---
# Core Classification
protocol: Uniswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42030
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/bb7b6aad-b04d-40e2-b8bb-937f9e96730b
source_link: https://cdn.cantina.xyz/reports/cantina_uniswapx_september2024.pdf
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
finders_count: 3
finders:
  - m4rio
  - shw
  - Jonatas Martins
---

## Vulnerability Title

Lack of validation of the curve in NonlinearDutchDecayLib 

### Overview

See description below for full details.

### Original Finding Content

## Context: NonlinearDutchDecayLib.sol#L58-L78

## Description
The `NonlinearDutchDecay.curve` is a user input parameter signed by the user. However, there are limited validations for the `relativeAmount` and `relativeBlocks` parameters. The only check is that the `relativeAmount` length is less than 16. There's no validation to ensure these two arrays have equal lengths, nor that the `relativeBlock` values are in ascending order.

### Here are examples of incorrect inputs that could be executed:
1. `relativeBlocks = [2,6,8]`, `relativeAmounts = [5,10,5,15]` // Incorrect length
2. `relativeBlocks = [2,8,6]`, `relativeAmounts = [5,10,5]` // Not increasing

Although the values are bounded by minimum and maximum, these inputs won't function properly.

## Recommendation
Consider validating the curve inputs:
- `blocks.length == amounts.length`
- Blocks are in ascending order.

While an invalid curve could be considered a user error, it's still sensible to include this check on-chain.

## UniswapX
These checks were intentionally excluded for gas savings. We have a client SDK that will perform these types of validations. Acknowledged.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Uniswap |
| Report Date | N/A |
| Finders | m4rio, shw, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_uniswapx_september2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/bb7b6aad-b04d-40e2-b8bb-937f9e96730b

### Keywords for Search

`vulnerability`

