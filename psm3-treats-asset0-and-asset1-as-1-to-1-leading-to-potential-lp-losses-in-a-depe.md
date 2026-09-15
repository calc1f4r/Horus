---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40277
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/18bed847-07eb-421d-99c5-9571f2885dba
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_aug2024.pdf
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
  - m4rio
  - Christoph Michel
---

## Vulnerability Title

PSM3 treats asset0 and asset1 as 1-to-1 leading to potential LP losses in a depeg event

### Overview

See description below for full details.

### Original Finding Content

## PSM3 Contract Analysis

## Context
**File:** PSM3.sol  
**Lines:** L257-L263

## Description
The PSM3 contract values `asset0` and `asset1` (expected to be USDC and DAI) the same when swapping and for the LPs' `totalAssets()`. When there is a depeg event of one token, there is a natural arbitrage using external markets (similar to other Maker PSMs). The PSM3 will end up filled with the less valuable token only. The LPs (users that called deposit and received shares) will suffer this loss if the assets don't repeg.

## Recommendation
Depositors should be aware of this risk and withdraw liquidity in time to reduce risk if they don't expect the assets to repeg.

## Maker Response
**Acknowledged.** This is expected behavior, similar to the PSM on Mainnet. We rely on kill switches to halt withdrawals during sustained depeg events. 

For example, if a USDC depeg event occurs again in March 2023, we would no longer want users to exit USDC into NST/sNST. Therefore, we would remove all NST/sNST liquidity as the LP and wait for the peg to return (or accept the loss).

Judging temporary vs sustained depeg is very subjective and requires human analysis. The default assumption is that all assets are pegged, with manual intervention required otherwise.

## Cantina Managed
**Acknowledged.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_spark_psm_aug2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/18bed847-07eb-421d-99c5-9571f2885dba

### Keywords for Search

`vulnerability`

