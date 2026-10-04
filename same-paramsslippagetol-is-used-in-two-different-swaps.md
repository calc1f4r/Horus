---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7240
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
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
  - validation

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Same params.SlippageTol is used in two different swaps

### Overview


This bug report is about the Connext protocol which allows users to do cross-chain transfers with the help of the Nomad protocol. When transferring, users have to convert the adopted token into the local token, which requires two swaps: Adopted -> Local at the source chain and Local -> Adopted at the destination chain. The same slippage tolerance is used for both swaps, which can make users vulnerable to MEV searchers and cause transfers to get stuck during periods of instability.

To solve this issue, it is recommended that users be allowed to set two different slippage tolerances for the two swaps. This was solved in PR 1575 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- `BridgeFacet.sol#L299-L304`
- `BridgeFacet.sol#L637`

## Description
The Connext protocol does a cross-chain transfer with the help of the Nomad protocol. In order to use the Nomad protocol, Connext has to convert the adopted token into the local token. For a cross-chain transfer, users take up two swaps: **Adopted -> Local** at the source chain and **Local -> Adopted** at the destination chain.

### Code References

**BridgeFacet.sol#L299-L304**
```solidity
function xcall(XCallArgs calldata _args)
    external
    payable
    whenNotPaused
    nonReentrant
    returns (bytes32) {
    ...
    // Swap to the local asset from adopted if applicable.
    (uint256 bridgedAmt, address bridged) = AssetLogic.swapToLocalAssetIfNeeded(
        canonical,
        transactingAssetId,
        amount,
        _args.params.slippageTol
    );
    ...
}
```

**BridgeFacet.sol#L637**
```solidity
function _handleExecuteLiquidity(
    bytes32 _transferId,
    bytes32 _canonicalId,
    bool _isFast,
    ExecuteArgs calldata _args
) private returns (uint256, address) {
    ...
    // swap out of mad* asset into adopted asset if needed
    return AssetLogic.swapFromLocalAssetIfNeeded(_canonicalId, _args.local, toSwap,
        _args.params.slippageTol);
}
```

The same slippage tolerance `_args.params.slippageTol` is used in two swaps. In most cases, users cannot set the correct slippage tolerance to protect two swaps.

Assume the Nomad asset is slightly cheaper on both chains. For instance, 1 Nomad asset equals 1.01 adopted asset. An expected swap would be: 

1 adopted -> 1.01 Nomad asset -> 1 adopted. 

The right slippage tolerance should be set at **1.01** and **0.98** respectively. Users cannot set the correct tolerance with a single parameter. This makes users vulnerable to MEV searchers, and user transfers get stuck during periods of instability.

## Recommendation
Allow users to set two different slippage tolerances for the two swaps.

## Connext
Solved in PR 1575.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

