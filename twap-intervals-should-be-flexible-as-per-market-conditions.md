---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: hardcoded_setting

# Attack Vector Details
attack_type: hardcoded_setting
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6930
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
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
  - hardcoded_setting

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

TWAP intervals should be flexible as per market conditions

### Overview


A bug report has been filed regarding the SwapManagerUniV3.sol. The protocol is currently using the same TWAP_INTERVAL for both the weth-morpho and weth-reward token pools, even though their liquidity and activity may be different. This poses a medium risk to the protocol. It is recommended that the TWAP_INTERVAL value should be changeable by the admin/owner, as it is dependent upon market conditions and activity. This recommendation has been followed in the PR #557.

### Original Finding Content

## Security Report

## Severity
**Medium Risk**

## Context
`SwapManagerUniV3.sol#L140-L149`

## Description
The protocol is using the same `TWAP_INTERVAL` for both `weth-morpho` and `weth-reward` token pools while their liquidity and activity might be different. It should use separate appropriate values for both pools.

## Recommendation
The `TWAP_INTERVAL` value should be changeable (and not constant) by the admin/owner since it is dependent upon market conditions and activity (for example, a 1-hour TWAP might lag considerably in sudden movements).

## Responses
- **Morpho:** Valid issue, will fix.
- **Spearbit:** Recommendation has been followed in the PR #557.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Hardcoded Setting`

