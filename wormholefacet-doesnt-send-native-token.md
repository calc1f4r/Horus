---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: payable

# Attack Vector Details
attack_type: payable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7047
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
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
  - payable
  - fund_lock

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

WormholeFacet doesn’t send native token

### Overview


This bug report is about a contract called WormholeFacet that allows sending the native token, however it does not actually send it across the bridge, causing the native token to get lost for the sender. The recommendation is to remove the payable keyword and/or check msg.value == 0. Alternatively, support sending the native token can be done via wrapAndTransferETH() of the wormhole bridge. This issue has been fixed with a pull request #76 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`WormholeFacet.sol#L36-L103`

## Description
The functions of `WormholeFacet` allow sending the native token; however, they don’t actually send it across the bridge, causing the native token to stay stuck in the LiFi Diamond and get lost for the sender.

```solidity
contract WormholeFacet is ILiFi, ReentrancyGuard, Swapper {
    function startBridgeTokensViaWormhole(... ) ... payable ... { // is payable
        LibAsset.depositAsset(_wormholeData.token, _wormholeData.amount); // allows native token
        _startBridge(_wormholeData);
        ...
    }

    function _startBridge(WormholeData memory _wormholeData) private {
        ...
        LibAsset.maxApproveERC20(...); // geared towards ERC20, also works when `msg.value `is set
        IWormholeRouter(_wormholeData.wormholeRouter).transferTokens(...); // no { value : .... }
    }
}
```

## Recommendation
Remove the `payable` keyword and/or check `msg.value == 0`. Alternatively, support sending the native token. This can be done via `wrapAndTransferETH()` of the wormhole bridge.

**Note:** also see issue "Consider using wrapped native token"

## LiFi
Fixed with PR #76.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

`Payable, Fund Lock`

