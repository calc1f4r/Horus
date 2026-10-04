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
solodit_id: 18283
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

pairTransferERC20From() only supports ERC721 NFTs

### Overview


This bug report details an issue with the pairTransferERC20From() function, present in both LSSVMRouter and VeryFastRouter, which only checks for ERC721_ERC20, meaning ERC1155 NFTs are not supported. After the start of this review, the function pairTransferERC20From() was updated in PR#21, as well as PR#30. Spearbit verified that this issue is fixed by PR#21 and PR#30. This issue was classified as high risk, and had the context of LSSVMRouter.sol#L491-L543, VeryFastRouter.sol#L344-L407.

### Original Finding Content

## High Risk Report

**Severity:** High Risk  
**Context:** LSSVMRouter.sol#L491-L543, VeryFastRouter.sol#L344-L407  

## Description
The function `pairTransferERC20From()` is present in both `LSSVMRouter` and `VeryFastRouter`, but it only checks for `ERC721_ERC20`. This means that ERC1155 NFTs are not supported by the routers.

The following code is present in both `LSSVMRouter` and `VeryFastRouter`:

```solidity
function pairTransferERC20From(...) ... {
    require(factory.isPair(msg.sender, variant), "Not pair");
    ...
    require(variant == ILSSVMPairFactoryLike.PairVariant.ERC721_ERC20, "Not ERC20 pair");
    ...
}
```

## Recommendation
After the start of this review, the function `pairTransferERC20From()` has already been updated in PR#21.

Also see issue: "Use of isPair() is not intuitive".

## Sudorandom Labs
Solved in PR#21 and PR#30.

## Spearbit
Verified that this issue is fixed by PR#21 and PR#30.

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

