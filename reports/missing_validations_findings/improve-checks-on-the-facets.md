---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7073
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

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

Improve checks on the facets

### Overview

See description below for full details.

### Original Finding Content

## Security Audit Report

## Severity
**Low Risk**

## Context
- `AxelarFacet.sol` #L69
- `CBridgeFacet.sol` #L95-L106
- `GnosisBridgeFacet.sol` #L120
- `HopFacet.sol` #L115-L126
- `HyphenFacet.sol` #L106-L112
- `Executor.sol` #L309

## Description
In the facets, receiver/destination address and amount checks are missing.

- The `symbol` parameter is used to get the address of the token with the gateway’s `tokenAddresses` function. The `tokenAddresses` function obtains the token address via mapping. If the symbol does not exist, the token address can be zero. 
- `AxelarFacet` and `Executor` do not check if the given symbol exists or not.

### AxelarFacet Example
```solidity
contract AxelarFacet {
    function executeCallWithTokenViaAxelar(...) {...} 
    address tokenAddress = s.gateway.tokenAddresses(symbol);
    
    function initAxelar(address _gateway, address _gasReceiver) external {
        s.gateway = IAxelarGateway(_gateway);
        s.gasReceiver = IAxelarGasService(_gasReceiver);
    }
}
```

### Executor Example
```solidity
contract Executor {
    function _executeWithToken(...) {...} 
    address tokenAddress = s.gateway.tokenAddresses(symbol);
}
```

- `GnosisBridgeFacet`, `CBridgeFacet`, `HopFacet`, and `HyphenFacet` are missing receiver address/amount checks.

### CBridgeFacet Example
```solidity
contract CBridgeFacet {
    function _startBridge(...) {...} 
    ...
    _cBridgeData.receiver
    ...
}
```

### GnosisBridgeFacet Example
```solidity
contract GnosisBridgeFacet {
    function _startBridge(...) {...} 
    ...
    gnosisBridgeData.receiver
    ...
}
```

### HopFacet Example
```solidity
contract HopFacet {
    function _startBridge(...) {...} 
    ...
    _hopData.recipient,
    ...
}
```

### HyphenFacet Example
```solidity
contract HyphenFacet {
    function _startBridge(...) {...} 
    ...
    _hyphenData.recipient
    ...
}
```

## Recommendation
Implement necessary checks (receiver address and bridge amount check) on the facets.

## Status
- **LiFi:** Fixed with PR #63.
- **Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

