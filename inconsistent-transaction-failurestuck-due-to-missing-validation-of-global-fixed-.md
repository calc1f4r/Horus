---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15947
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-retainer1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-retainer1-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Jonah1005
  - DefSec
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Inconsistent transaction failure/stuck due to missing validation of global fixed native fee rate and execution fee

### Overview

See description below for full details.

### Original Finding Content

## Security Audit Report

## Severity
Low Risk

## Context
DeBridgeFacet.sol#L124

## Description
The current implementation of the facet logic does not validate the global fixed native fee rate and execution fee, which can lead to inconsistent transaction failures or getting stuck in the process. This issue can arise when the fee rate is not set correctly or there are discrepancies between the fee rate used in the smart contract and the actual fee rate. This can result in transactions getting rejected or stuck, causing inconvenience to users and affecting the overall user experience.

## Recommendation
To avoid this issue, it is recommended to include a validation step for the global fixed native fee rate in the transaction logic. This can be done by fetching the current fee rate from a debridge gate and comparing it with the fee rate used in the transaction.

```solidity
uint protocolFee = deBridgeGate.globalFixedNativeFee;
```

## Status
- **LiFi:** Fixed with PR 253.
- **Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-retainer1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-retainer1-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

