---
# Core Classification
protocol: Sudoswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6781
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Mudit Gupta
  - Gerard Persoon
---

## Vulnerability Title

Error codes of Quote functions are unchecked

### Overview


This bug report is related to the contracts LSSVMPair.sol and LSSVMRouter.sol. The functions getBuyNFTQuote() and getSellNFTQuote() from LSSVMPair.sol are used in several functions in LSSVMRouter.sol, but the error return values from these functions are not checked in LSSVMRouter.sol, while other functions in LSSVMPair.sol do check for error==CurveErrorCodes.Error.OK. The current Curve contracts, which implement the getBuyNFTQuote() and getSellNFTQuote() functions, have a limited number of potential errors, but future Curve contracts may add additional error codes.

The recommendation is to check the error code of functions getBuyNFTQuote() and getSellNFTQuote() in contract LSSVMRouter.sol. This issue has been addressed in a branch, and the LSSVMRouter now reverts if the Error is not Error.OK for a normal swap, or it skips performing the swap during a robust swap operation.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LSSVMPair.sol` Lines 389-431
- `LSSVMRouter.sol`

## Description
The error return values from functions `getBuyNFTQuote()` and `getSellNFTQuote()` are not checked in contract `LSSVMRouter.sol`, whereas other functions in contract `LSSVMPair.sol` do check for `error==CurveErrorCodes.Err` or `OK`.

```solidity
abstract contract LSSVMPair is Ownable, ReentrancyGuard {
    ...
    function getBuyNFTQuote(uint256 numNFTs) external view returns (CurveErrorCodes.Error error, ...) {
        ...
        (error, ...) = bondingCurve().getBuyInfo(...);
    }

    function getSellNFTQuote(uint256 numNFTs) external view returns (CurveErrorCodes.Error error, ...) {
        ...
        (error, ...) = bondingCurve().getSellInfo(...);
    }

    function swapTokenForAnyNFTs(...) external payable virtual returns (uint256 inputAmount) {
        ...
        (error, ...) = _bondingCurve.getBuyInfo(...);
        require(error == CurveErrorCodes.Error.OK, "Bonding curve error");
        ...
    }
}
```

In `LSSVMRouter.sol` at Line 526:
```solidity
(, , pairOutput, ) = swapList[i].pair.getSellNFTQuote(...);
```

The following contract lines contain the same code snippet:
- `LSSVMRouter.sol` Lines 360, 407, 450, 493, 627, 664
```solidity
(, , pairCost, ) = swapList[i].pair.getBuyNFTQuote(...);
```

**Note:** The current Curve contracts, which implement the `getBuyNFTQuote()` and `getSellNFTQuote()` functions, have a limited number of potential errors. However, future Curve contracts might add additional error codes.

## Recommendation
Check the error code of functions `getBuyNFTQuote()` and `getSellNFTQuote()` in contract `LSSVMRouter.sol`.

## Responses
- **Sudoswap:** Addressed in this branch. `LSSVMRouter` now reverts if the error is not `Error.OK` for a normal swap, or it skips performing the swap during a robust swap operation.
- **Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Max Goodman, Mudit Gupta, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

