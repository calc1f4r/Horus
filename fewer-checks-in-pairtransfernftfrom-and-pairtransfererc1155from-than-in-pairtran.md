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
solodit_id: 18300
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

Fewer checks in pairTransferNFTFrom() and pairTransferERC1155From() than in pairTransferERC20From()

### Overview


This bug report is about the functions pairTransferNFTFrom(), pairTransferERC1155From() and pairTransferERC20From() in the LSSVMRouter.sol#L491-L543 and VeryFastRouter.sol#L344-L407. The functions pairTransferNFTFrom() and pairTransferERC1155From() don't verify that the correct type of pair is used, whereas pairTransferERC20From() does. This means that actions could be attempted on the wrong type of pairs, which can succeed if a NFT is used that supports both ERC721 and ERC1155.

The recommended solution is to add comparable checks as in pairTransferERC20From() to the functions pairTransferNFTFrom() and pairTransferERC1155From(). Sudorandom Labs has solved the issue in PR#30 and Spearbit verified that the problem is fixed by PR#30.

### Original Finding Content

## Severity: Medium Risk

## Context
- LSSVMRouter.sol#L491-L543
- VeryFastRouter.sol#L344-L407

## Description
The functions `pairTransferNFTFrom()` and `pairTransferERC1155From()` don't verify that the correct type of pair is used, whereas `pairTransferERC20From()` does. This means actions could be attempted on the wrong type of pairs. These could succeed, for example, if an NFT is used that supports both ERC721 and ERC1155.

**Note:** Also see issue "pairTransferERC20From only supports ERC721 NFTs."

The following code is present in both LSSVMRouter and VeryFastRouter:

```solidity
function pairTransferERC20From(...) ... {
    require(factory.isPair(msg.sender, variant), "Not pair");
    ...
    require(variant == ILSSVMPairFactoryLike.PairVariant.ERC721_ERC20, "Not ERC20 pair");
    ...
}

function pairTransferNFTFrom(...) ... {
    require(factory.isPair(msg.sender, variant), "Not pair");
    ...
}

function pairTransferERC1155From(...) ... {
    require(factory.isPair(msg.sender, variant), "Not pair");
    ...
}
```

## Recommendation
Add comparable checks as in `pairTransferERC20From()` to the functions `pairTransferNFTFrom()` and `pairTransferERC1155From()`.

## Sudorandom Labs
Solved in PR#30.

## Spearbit
Verified that this is fixed by PR#30.

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

