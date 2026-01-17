---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: payable

# Attack Vector Details
attack_type: payable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7225
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
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
  - payable
  - business_logic

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

Executor reverts on receiving native tokens from BridgeFacet

### Overview


This bug report details an issue encountered when using the Executor.sol BridgeFacet.sol#L696, AssetLogic.sol#L127-L151 functions. When the Executor.execute function is called, the BridgeFacet transfers native token to the Executor contract, which does not have a fallback/ receive function. As a result, the transaction reverts. 

The recommended solution is to add a receive function to the Executor contract. This would allow the native token to be sent to the Executor contract. Alternatively, the native asset could be unwrapped and sent along with the call to the Executor.

Connext and Spearbit have both verified two alternate approaches to solving the issue. The first approach is to send Ether along with the call, which was implemented in PR 1532. The second approach is to remove native asset handling, which was implemented in PR 31.

### Original Finding Content

## Severity: High Risk

## Context
- **File:** Executor.sol 
- **Line:** BridgeFacet.sol#L696, AssetLogic.sol#L127-L151

## Description
When doing an external call in `execute()`, the `BridgeFacet` provides liquidity into the `Executor` contract before calling `Executor.execute`. The `BridgeFacet` transfers a native token when an `address(wrapper)` is provided. However, the `Executor` does not have a fallback or receive function. Hence, the transaction will revert when the `BridgeFacet` tries to send the native token to the `Executor` contract.

```solidity
function _handleExecuteTransaction(
    ...
    AssetLogic.transferAssetFromContract(_asset, address(s.executor), _amount);
    (bool success, bytes memory returnData) = s.executor.execute(...);
    ...
}
```

```solidity
function transferAssetFromContract(...) {
    ...
    if (_assetId == address(s.wrapper)) {
        // If dealing with wrapped assets, make sure they are properly unwrapped
        // before sending from contract
        s.wrapper.withdraw(_amount);
        Address.sendValue(payable(_to), _amount);
    } else {
        ...
    }
}
```

## Recommendation
It is recommended to add a receive function in the `Executor` contract:

```solidity
receive() payable external {
    require(msg.sender == connext);
}
```

Alternatively, unwrap the native asset and send it along with the call to the executor.

- **Connext:** Ether sent along with the call. Solved in PR 1532.
- **Spearbit:** Verified.
- **Connext:** Alternate approach: removed native asset handling. Implemented in PR 31.
- **Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Payable, Business Logic`

