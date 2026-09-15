---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: immutable

# Attack Vector Details
attack_type: immutable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7035
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
rarity_score: 4

# Context Tags
tags:
  - immutable
  - hardcoded_address

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

Hardcode bridge addresses via immutable

### Overview


This bug report is about the potential risk of calling unexpected functions in the bridge contracts of the OmniBridgeFacet and AxelarFacet. This could be done if the bridge address is supplied as a parameter, which is inherently unsafe. The AxelarFacet sets the bridge address in initAxelar(), but this is relatively expensive. The recommendation is to set the bridge addresses in the constructor, store them as immutable variables, and use the Diamond pattern. This suggestion is also relevant for other addresses like the WETH address in AccrossFacet. The LiFi and Spearbit have been fixed and verified respectively.

### Original Finding Content

## Severity: High Risk

**Context:** 
- OmniBridgeFacet.sol#L34-L106
- AxelarFacet.sol#L18-L23

**Description:**  
Most bridge facets call bridge contracts where the bridge address has been supplied as a parameter. This is inherently unsafe because any address could be called. Luckily, the called function signature is hardcoded, which reduces risk. However, it is still possible to call an unexpected function due to the potential collisions of function signatures. Users might be tricked into signing a transaction for the LiFi protocol that calls unexpected contracts. 

One exception is the AxelarFacet which sets the bridge addresses in `initAxelar()`, however this is relatively expensive as it requires an SLOAD to retrieve the bridge addresses. 

*Note: also see "Facets approve arbitrary addresses for ERC20 tokens".*

```solidity
function startBridgeTokensViaOmniBridge(..., BridgeData calldata _bridgeData) ... {
    ...
    _startBridge(_lifiData, _bridgeData, _bridgeData.amount, false);
}

function _startBridge(..., BridgeData calldata _bridgeData, ...) ... {
    IOmniBridge bridge = IOmniBridge(_bridgeData.bridge);
    if (LibAsset.isNativeAsset(_bridgeData.assetId)) {
        bridge.wrapAndRelayTokens{ ... }(...);
    } else {
        ...
        bridge.relayTokens(...);
    }
    ...
}

contract AxelarFacet {
    function initAxelar(address _gateway, address _gasReceiver) external {
        ...
        s.gateway = IAxelarGateway(_gateway);
        s.gasReceiver = IAxelarGasService(_gasReceiver);
    }

    function executeCallViaAxelar(...) ... {
        ...
        s.gasReceiver.payNativeGasForContractCall{ ... }(...);
        s.gateway.callContract(destinationChain, destinationAddress, payload);
    }
}
```

**Recommendation:**  
Set bridge addresses in a constructor and store them as immutable variables. The gas costs are low and this approach also works with delegatecall and thus the Diamond pattern.

*Note:* 
- The Hop bridge protocol has a separate bridge contract for each token, which will require more complicated code, like a mapping from `sendingAssetId` to bridge address. See `hopt.ts`.
- The Omni bridge facet calls the functions `relayTokens()` and `wrapAndRelayTokens()` which are implemented in different contracts. Thus, this requires some additional code, see: `WETHOmnibridgeRouter.sol#L50`, `WETHOmnibridgeRouter`, bridge.
- This suggestion is also relevant for other addresses that are used, like the WETH address in `AccrossFacet`, see `AcrossFacet.sol#L102`.

**LiFi:** Fixed with PR #105 and PR #79.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Immutable, Hardcoded Address`

