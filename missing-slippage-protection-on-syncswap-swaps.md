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
solodit_id: 46280
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016
source_link: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
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
finders_count: 2
finders:
  - MiloTruck
  - Víctor Martínez
---

## Vulnerability Title

Missing slippage protection on SyncSwap swaps 

### Overview


The report describes a bug in the SyncSwapper abstract contract that could lead to potential loss of funds. The contract is used to process swaps through SyncSwap's SyncRouter. These swaps are typically subject to a maximum slippage limit to protect against excessive exposure to MEV. However, in this implementation, the slippage is not being accounted for, resulting in both swap executions lacking appropriate parameters. This vulnerability could potentially result in the loss of funds from incentives and compounding rewards during swaps. The recommendation is to introduce a dedicated value to specify the minimum acceptable output for a particular swap. The bug has been acknowledged by both Clave and Cantina Managed and has a medium risk level.

### Original Finding Content

## SyncSwapper Contract Analysis

## Context
(No context files were provided by the reviewer)

## Description
The SyncSwapper abstract contract implements the logic to process swaps via SyncSwap's SyncRouter. Typically, when integrating DEX protocols, a maximum slippage limit is enforced to protect trades from excessive exposure to MEV (Miner Extractable Value). In the case of SyncRouter's swap function, an `amountOutMin` parameter can be provided to cap the maximum allowable slippage, ensuring that swaps (e.g., for incentives or rewards) execute at efficient rates.

However, in this implementation, slippage is not being accounted for, resulting in both swap executions lacking appropriate `amountOutMin` parameters:
- **ClaggBaseAdapter.sol#L464:** `minAmountOut` hardcoded to a fixed value set in the config.
- **ClaggBaseAdapter.sol#L359:** `minAmountOut == 0` means the protocol is fine with receiving no tokens from the swap.

## Impact
This renders the protocol vulnerable to MEV, potentially resulting in the loss of funds from incentives and compounding rewards during swaps.

## Recommendation
Introduce a dedicated value to specify the minimum acceptable output for a particular swap.

## Clave
Acknowledged.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

