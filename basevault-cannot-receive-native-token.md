---
# Core Classification
protocol: Aera Contracts v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58292
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Slowfi
  - Eric Wang
  - High Byte
---

## Vulnerability Title

BaseVault Cannot Receive Native Token

### Overview


A medium risk vulnerability has been found in the BaseVault contract, specifically in the submit function at line 108 and the CallbackHandler contract at line 51. The contract allows for native token transfers through the use of the `ctx.value` field, but it is not capable of receiving ETH due to two limitations. The submit function is not marked as payable and the contract does not have a `receive()` or `payable` fallback function. This means that even if `ctx.value` is greater than zero, the contract will revert upon receiving ETH. To fix this, the submit function should be marked as payable or a `receive()` function should be added. This will allow the vault to support ETH-based workflows as intended. The issue has been fixed in PR 223 by creating a `receive()` function. The submit function should not be marked as payable as it is not intended for the guardian to send funds. The vulnerability has been verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity 
**Medium Risk**

## Context 
- BaseVault.sol#L108 
- CallbackHandler.sol#L51

## Description 
The BaseVault contract appears to support native token flows through its submit function by way of the `ctx.value` field. This field allows specifying an ETH value to be sent with specific operations. However, the contract itself is not capable of receiving ETH due to two related limitations:

1. The submit function is not marked payable.
2. The contract does not expose a `receive()` or `payable` fallback function.

As a result, even if `ctx.value` is greater than zero, the contract will revert upon receiving ETH. This renders any strategy involving native token transfers infeasible under normal execution paths. The only way ETH could be transferred into the contract would be through `selfdestruct`, which is not practical or safe in most DeFi use cases.

## Recommendation 
Consider marking the submit function as payable, since it is the intended gateway for guardian-submitted operations. Additionally (or alternatively), exposing a `receive()` function or marking the existing fallback as payable would enable native token reception. Either approach would resolve the inconsistency and allow the vault to support ETH-based workflows as designed.

## Aera 
Fixed in PR 223 by creating `receive` function. The submit function should not be marked as payable as the guardian should not send funds themselves.

## Spearbit 
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Aera Contracts v3 |
| Report Date | N/A |
| Finders | Slowfi, Eric Wang, High Byte |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf

### Keywords for Search

`vulnerability`

