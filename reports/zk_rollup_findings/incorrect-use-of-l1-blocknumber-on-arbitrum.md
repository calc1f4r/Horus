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
solodit_id: 42023
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/bb7b6aad-b04d-40e2-b8bb-937f9e96730b
source_link: https://cdn.cantina.xyz/reports/cantina_uniswapx_september2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

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

Incorrect use of L1 block.number on Arbitrum 

### Overview


The bug report discusses an issue with the NonlinearDutchDecayLib.sol code on Arbitrum, a blockchain platform. The block.number function on Arbitrum returns the L1 block number instead of the current L2 block number, which has a much shorter block time. This causes problems with orders decaying properly and could be fixed by using a different function to retrieve the L2 block number. The bug has been fixed in the code and verified by Cantina Managed, with a low risk level.

### Original Finding Content

## Context: NonlinearDutchDecayLib.sol#L38

## Description
According to Arbitrum's documentation, `block.number` returns the approximate L1 block number at which the sequencer received the transaction instead of the current L2 block number. Compared to the L1 block time, which is 12 seconds, the L2 block time on Arbitrum is only about 0.25 seconds. Since orders on Arbitrum usually decay within a few seconds (less than 8 seconds at the time of writing), it would be necessary to calculate `blockDelta` based on L2 block numbers to allow the orders to decay as expected and enable more flexible configurations of the decay curve.

## Recommendation
Consider using `ArbSys(100).arbBlockNumber()` to retrieve the L2 block number on Arbitrum.

## UniswapX
Fixed in PR 280.

## Cantina Managed
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
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

