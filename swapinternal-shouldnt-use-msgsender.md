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
solodit_id: 7129
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

swapInternal() shouldn't use msg.sender

### Overview


This bug report is about a high-risk issue that was reported by the Connext team. The issue was that when attempting to execute a stable swap, the internal stable swap was checking if msg.sender had sufficient funds, which it normally wouldn't have. This was occurring in the functions execute(), _handleExecuteLiquidity(), swapFromLocalAssetIfNeeded(), and _swapAsset() in the files BridgeFacet.sol, AssetLogic.sol, and SwapUtils.sol respectively. 

The recommendation was to not use the balance of msg.sender when attempting to execute a stable swap. The Connext team solved the issue in a pull request, and Spearbit verified it.

### Original Finding Content

## Severity: High Risk

## Context
- BridgeFacet.sol#L337-L369
- BridgeFacet.sol#L659-L750
- AssetLogic.sol#L150-L182
- AssetLogic.sol#L229-L262
- SwapUtils.sol#L798-L826

## Description
As reported by the Connext team, the internal stable swap checks if `msg.sender` has sufficient funds in `onexecute()`. This `msg.sender` is the relayer which normally wouldn't have these funds, so the swaps would fail. The local funds should come from the Connext diamond itself.

### BridgeFacet.sol
```solidity
function execute(ExecuteArgs calldata _args) external nonReentrant whenNotPaused returns (bytes32) {
    ...
    (uint256 amountOut, address asset, address local) = _handleExecuteLiquidity(...);
    ...
}
```

### AssetLogic.sol
```solidity
function swapFromLocalAssetIfNeeded(...) ... {
    ...
    return _swapAsset(...);
}
```

### SwapUtils.sol
```solidity
function swapInternal(...) ... {
    IERC20 tokenFrom = self.pooledTokens[tokenIndexFrom];
    require(dx <= tokenFrom.balanceOf(msg.sender), "more than you own"); // msg.sender is the relayer
    ...
}
```

## Recommendation
Don't use the balance of `msg.sender`.

## Connext
Solved in PR 2120.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Business Logic`

