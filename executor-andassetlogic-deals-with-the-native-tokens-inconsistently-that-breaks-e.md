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
solodit_id: 7224
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
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Executor andAssetLogic deals with the native tokens inconsistently that breaks execute()

### Overview


This bug report is about the inconsistency of how native tokens are represented in the codebase of the BridgeFacet, Executor and AssetLogic contracts. When dealing with an external callee, the BridgeFacet will transfer liquidity to the Executor before calling Executor.execute. In order to send the native token, the Executor checks for _args.assetId == address(0). However, AssetLogic.transferAssetFromContract() disallows address(0). This causes the BridgeFacet to not be able to handle external callees when using native tokens.

The recommendation is for the team to go through the whole codebase and make sure it is used consistently. This was solved in PR 1532, and an alternate approach was implemented in PR 1641, which removed native asset handling. Both solutions have been verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity: High Risk

### Context
- `Executor.sol#L142`
- `AssetLogic.sol#L127-L151`
- `BridgeFacet.sol#L644-L718`

### Description
When dealing with an external callee, the `BridgeFacet` will transfer liquidity to the `Executor` before calling `Executor.execute`.

In order to send the native token:
- The `Executor` checks for `_args.assetId == address(0)`.
- `AssetLogic.transferAssetFromContract()` disallows `address(0)`.

**Note:** Also see the issue: "Executor reverts on receiving native tokens from BridgeFacet."

```solidity
contract BridgeFacet is BaseConnextFacet {
    function _handleExecuteTransaction() ... {
        ...
        AssetLogic.transferAssetFromContract(_asset, address(s.executor), _amount); // _asset may not be 0, !
        (bool success, bytes memory returnData) = s.executor.execute(
            IExecutor.ExecutorArgs(
                ...
                _asset, // assetId parameter from ExecutorArgs // must be 0 for Native asset
                ...
            )
        );
        ...
    }
}
```

```solidity
library AssetLogic {
    function transferAssetFromContract(address _assetId, ...) {
        ...
        // No native assets should ever be stored on this contract
        if (_assetId == address(0)) revert AssetLogic__transferAssetFromContract_notNative();
        if (_assetId == address(s.wrapper)) {
            // If dealing with wrapped assets, make sure they are properly unwrapped before sending from contract
            s.wrapper.withdraw(_amount);
            Address.sendValue(payable(_to), _amount);
        }
    }
}
```

```solidity
contract Executor is IExecutor {
    function execute(ExecutorArgs memory _args) external payable override onlyConnext returns (bool, bytes memory) {
        ...
        bool isNative = _args.assetId == address(0);
        ...
    }
}
```

The `BridgeFacet` cannot handle external callees when using native tokens.

### Recommendation
The native tokens are either represented as `address(0)` or `address(wrapper)` throughout the whole codebase, causing this inconsistency to be error prone. It is recommended that the team review the entire codebase and ensure consistent usage.

### Additional Notes
- **Connext:** Solved in PR 1532.
- **Spearbit:** Verified.
- **Connext:** Alternate approach: removed native asset handling. Implemented in PR 1641.
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

`Validation, Business Logic`

