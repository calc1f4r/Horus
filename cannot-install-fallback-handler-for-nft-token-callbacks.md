---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43822
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Cannot install fallback handler for NFT token callbacks

### Overview


Severity: Medium Risk
Context: ModuleManager.sol#L72
Description: The receiverFallback modifier in ModuleManager.sol does not allow for custom fallback handlers for certain NFT receiver functions. This means that although fallback handlers can be installed without errors, they will never be executed. This can cause issues for smart wallets that cannot selectively reject NFTs.
Recommendation: Developers should check for fallback handlers first before checking if it matches one of the NFT receiver functions. This will prevent any conflicts and ensure that the fallback handler is properly executed.
Biconomy: The bug has been fixed in PR 132.
Spearbit: The bug has also been fixed.

### Original Finding Content

## Medium Risk Report

## Severity
**Medium Risk**

## Context
ModuleManager.sol#L72

## Description
Note that the `receiverFallback` modifier performs a call context return when the following conditions are met:

- `msig.sig` equals one of:
  - `onERC721Received(address,address,uint256,bytes)`
  - `onERC1155Received(address,address,uint256,uint256,bytes)`
  - `onERC1155BatchReceived(address,address,uint256[],uint256[],bytes)`

Therefore, these function types cannot use custom fallback handlers. While fallback handlers for these function types can be installed without errors, they will never be executed. Smart wallets cannot selectively reject NFTs.

## Recommendation
Consider checking for fallback handlers first. Only if there's no fallback handler installed, check if it matches one of the NFT receiver functions.

## Fixes
- **Biconomy**: Fixed in PR 132.
- **Spearbit**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

