---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18305
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Missing override in authAllowedForToken prevents authorized admins from toggling settings and reclaiming pairs

### Overview


This bug report is about reclaiming pairs in the LSSVMPairFactory.sol and RoyaltyEngine.sol contracts. The issue is that Manifold admins are not allowed by authAllowedForToken to toggle settings and reclaim their authorized pairs in the protocol context. The problem is that authAllowedForToken only checks for admin overrides from Nifty, Foundation, Digitalax, and ArtBlocks, but the protocol also supports royalties from Manifold, Rarible, SuperRare, and Zora. The recommendation is to add admin support for Manifold and other marketplaces, if available, that are recognized by the protocol. Sudorandom Labs and Spearbit have both acknowledged the issue and agreed not to make any changes for now.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LSSVMPairFactory.sol#L330-L377`
- `RoyaltyEngine.sol#L38-L46`

## Description
Manifold admins are incorrectly not allowed by `authAllowedForToken` to toggle settings and reclaim their authorized pairs in the protocol context. `authAllowedForToken` checks for different admin overrides including admin interfaces of NFT marketplaces Nifty, Foundation, Digitalax, and ArtBlocks. However, the protocol supports royalties from other marketplaces of Manifold, Rarible, SuperRare, and Zora. Of those, Manifold does have a `getAdmins()` interface which is not considered in `authAllowedForToken`. And it is not certain that the others don't.

## Recommendation
Add admin support for Manifold and other marketplaces (Rarible, SuperRare, and Zora), if available, that are recognized by the protocol.

## Sudorandom Labs
Acknowledged, no change for now. Adherence to the manifold code is preferred over extending the admin surface for now. The Manifold implementation contract uses `AdminControlUpgradeable`, which contains an `isAdmin` function. This function is covered by line `LSSVMPairFactory.sol#L338`.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

