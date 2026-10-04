---
# Core Classification
protocol: LI.FI
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7040
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - reentrancy
  - external_call
  - access_control

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

Too generic calls in GenericBridgeFacet allow stealing of tokens

### Overview


This bug report is about a vulnerability in the GenericBridgeFacet and LibSwap contracts. It has been found that with these contracts, anyone can call the transferFrom() function, allowing them to steal tokens from users who have given a large allowance to the LiFi protocol. Additionally, this vulnerability also allows someone to call the Lifi Diamond itself, cancel transfers of other users, call functions that are protected by a check on this, and more. 

The recommendation is to whitelist the external call addresses and function signatures for both the dexes and the bridges. Alternatively, the code can be removed from the repository and/or a warning can be added inside the code itself. LiFi has removed the code from all contract deployments since the exploit and do not plan to enable it again, so they plan to remove it from the repository. Spearbit has solved the issue by deleting the GenericBridgeFacet contract.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
- `GenericBridgeFacet.sol#L69-L120`
- `LibSwap.sol#L30-L68`

## Description
With the contract `GenericBridgeFacet`, the functions `swapAndStartBridgeTokensGeneric()` (via `LibSwap.swap()`) and `_startBridge()` allow arbitrary function calls, which enable anyone to call `transferFrom()` and steal tokens from users who have provided a large allowance to the LiFi protocol. This vulnerability has been exploited in the past.

### Additional Risks
- Ability to call the LiFi Diamond itself via functions that don’t have `nonReentrant`.
- Potential cancellation of transfers for other users.
- Calling functions protected by checks on `this`, such as `completeBridgeTokensViaStargate`.

```solidity
contract GenericBridgeFacet is ILiFi, ReentrancyGuard {
    function swapAndStartBridgeTokensGeneric(
        ...
        LibSwap.swap(_lifiData.transactionId, _swapData[i]);
        ...
    )
    
    function _startBridge(BridgeData memory _bridgeData) internal {
        ...
        (bool success, bytes memory res) = _bridgeData.callTo.call{ value: value }(_bridgeData.callData);
        ...
    }
}

library LibSwap {
    function swap(bytes32 transactionId, SwapData calldata _swapData) internal {
        ...
        (bool success, bytes memory res) = _swapData.callTo.call{ value: nativeValue }(_swapData.callData);
        ...
    }
}
```

## Recommendation
Whitelist the external call addresses and function signatures for both the decentralized exchanges and the bridges. Note: `SwapperV2` already includes whitelist functionality for exchanges, but it isn’t utilized within this contract.

Alternatively, ensure this code is no longer integrated into the LiFi Diamond. This can be accomplished by removing the code from the repository or adding a warning within the code itself.

### LiFi Status
The feature has been removed from all contract deployments since the exploit. We do not intend to re-enable it, so it can be removed from the repository. See PR #4 for details.

### Spearbit Status
The issue is resolved by deleting the `GenericBridgeFacet` contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Reentrancy, External Call, Access Control`

