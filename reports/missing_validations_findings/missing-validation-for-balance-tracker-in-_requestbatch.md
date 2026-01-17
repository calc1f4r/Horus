---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49372
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ff3a291b-4cdd-4ebb-9828-c0ebc7f21edf
source_link: https://cdn.cantina.xyz/reports/cantina_valory_january2025.pdf
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
  - Saw-mon and Natalie
  - slowfi
---

## Vulnerability Title

Missing validation for balance tracker in _requestBatch 

### Overview

See description below for full details.

### Original Finding Content

## MechMarketplace Audit Report

## Context
MechMarketplace.sol#L286

## Description
The function `_requestBatch` in `MechMarketplace.sol` retrieves the balance tracker contract from `mapPaymentTypeBalanceTrackers[paymentType]`. However, there is no validation ensuring that a valid contract address is assigned before usage. If this mapping has not been properly set, the contract will attempt to call `checkAndRecordDeliveryRates` on `address(0)`, leading to a revert.

While it is expected that the governance correctly configures payment types and their corresponding balance trackers, enforcing an explicit validation would improve contract robustness and avoid unintended reverts in edge cases.

## Recommendation
To ensure contract stability, an explicit check can be added before calling functions on the balance tracker. If the mapping does not contain a valid contract address, the function could revert early with a clear error message, preventing unnecessary execution costs and improving error management.

## Valory
Fixed on PR 93.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Olas |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, slowfi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_valory_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ff3a291b-4cdd-4ebb-9828-c0ebc7f21edf

### Keywords for Search

`vulnerability`

