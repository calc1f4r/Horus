---
# Core Classification
protocol: Sweep n Flip
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46498
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e
source_link: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
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
finders_count: 2
finders:
  - slowfi
  - Sujith Somraaj
---

## Vulnerability Title

debug_forceReceiveMessage is dangerous and could be abused 

### Overview


The bug report is about a function called "debug_forceReceiveMessage" in the LayerZeroAdapter contract. This function allows certain people to send messages directly to the Bridge contract, bypassing the usual process through LayerZero. This could potentially lead to NFTs being stolen and minted without restrictions, which goes against the security purpose of LayerZero. The recommendation is to remove this function. The bug has been fixed in a specific version of the contract and has been verified by Cantina Managed.

### Original Finding Content

## LayerZeroAdapter.sol#L77

## Description
The `debug_forceReceiveMessage` function in `LayerZeroAdapter` is a restricted function that allows privileged actors to deliver arbitrary messages to the Bridge contract. For example, a privileged actor could deliver a random payload to the Bridge contract without sending it through LayerZero. This ability could lead to stealing NFTs from the Bridge contract and minting them without constraints. This also undermines the security offered by LayerZero as a cross-chain communication protocol.

## Recommendation
Consider removing the `debug_forceReceiveMessage` function.

## Sweep n' Flip
Fixed in `snf-bridge-contracts-v1 PR 15`.

## Cantina Managed
Verified fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sweep n Flip |
| Report Date | N/A |
| Finders | slowfi, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sweepnflip_bridge_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8d400356-5bf2-4bd4-91e2-93f0a785406e

### Keywords for Search

`vulnerability`

