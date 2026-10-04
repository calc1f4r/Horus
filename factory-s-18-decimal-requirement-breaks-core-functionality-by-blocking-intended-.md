---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46270
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
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
  - ladboy233
  - Spearmint
---

## Vulnerability Title

Factory 's 18 decimal requirement breaks core functionality by blocking intended BTC-based collateral tokens 

### Overview


This bug report highlights an issue with the Factory contract's deployNewInstance function. The contract requires all collateral tokens to have 18 decimals, which prevents the use of major Bitcoin-based ERC20 tokens that have 8 decimals. This limitation is a problem because the protocol was designed to support these tokens. The report recommends removing the decimal check to allow for the intended functionality of the protocol.

### Original Finding Content

## Finding Description

## Context
(No context files were provided by the reviewer)

## Issue
In the Factory contract's `deployNewInstance` function, there is a strict requirement that all collateral tokens must have 18 decimals:

```solidity
require(collateralToken.decimals() == BIMA_COLLATERAL_DECIMALS, "Invalid collateral decimals");
```

Where `BIMA_COLLATERAL_DECIMALS` is set to 18. This creates a critical limitation as it prevents the use of major Bitcoin-based ERC20 tokens that the protocol intends to support, since most Bitcoin tokens on EVM chains use 8 decimals to match WBTC's decimal format:

- **WBTC (Wrapped Bitcoin)**: 8 decimals.
- **CbBTC (Coinbase Wrapped BTC)**: 8 decimals.
- **UniBTC**: 8 decimals.
- Other BTC-based tokens typically follow the 8 decimal standard.

### Supporting Evidence
Here is some more proof that the above tokens were meant to be supported:

1. The docs explicitly state, "users lock their assets (e.g., BTC, LST) in exchange for USBD."
2. The testnet deployment on Optimism Sepolia is using a collateral aBTC that has 8 decimals.
3. The protocol developer stated that the protocol intends to support these tokens.

## Conclusion
This mismatch between the intended collateral types and the decimal requirement creates a significant issue as it means the protocol cannot actually support the Bitcoin-based collateral that it was designed for. This severely limits the protocol's functionality and prevents it from serving its core purpose of providing BTC-backed stablecoin loans.

## Recommendation
The decimal check should be removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | ladboy233, Spearmint |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

