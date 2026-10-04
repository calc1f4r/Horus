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
solodit_id: 18287
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

changeSpotPriceAndDelta() only uses ERC721 version of balanceOf()

### Overview


A bug has been identified in the StandardSettings.sol#L227-L294 code of a software system. The bug affects the function changeSpotPriceAndDelta() which uses the ERC721 variant of the balanceOf() function with one parameter only. To support ERC1155, a second parameter for the NFT id has to be supplied. The recommendation is to detect the use of ERC1155 and use the appropriate balanceOf() version. Sudorandom Labs solved the bug in PR#30 and Spearbit verified that the bug has been fixed.

### Original Finding Content

## Security Analysis Report

## Severity
**High Risk**

## Context
`StandardSettings.sol#L227-L294`

## Description
The function `changeSpotPriceAndDelta()` uses `balanceOf()` with one parameter. This is the ERC721 variant. In order to support ERC1155, a second parameter of the NFT id has to be supplied.

```solidity
function changeSpotPriceAndDelta(address pairAddress, ...) public {
    ...
    if ((newPriceToBuyFromPair < priceToBuyFromPair) && pair.nft().balanceOf(pairAddress) >= 1) {
        ...
    }
}
```

## Recommendation
Detect the use of ERC1155 and use the appropriate `balanceOf()` version.

## Audit Status
- **Sudorandom Labs**: Solved in PR#30.
- **Spearbit**: Verified that this is fixed by PR#30.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

