---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7050
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
  - fund_lock
  - bridge

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

Funds can be locked during the recovery stage

### Overview


This bug report is about the AmarokFacet smart contract, specifically at line 133. The recovery parameter is hardcoded as msg.sender, which can lead to unexpected behaviour in certain cases. If the msg.sender is a smart contract, it may not be available on the destination chain, and if it is, the contract may not have a function to withdraw native tokens. This can result in funds being locked if an execution fails. The recommendation is to consider taking the recovery parameter as an argument. The LiFi issue was fixed with a pull request, and Spearbit has verified the fix.

### Original Finding Content

## Security Report

## Severity
**Low Risk**

## Context
`AmarokFacet.sol#L133`

## Description
The recovery address is intended to receive funds if the execution fails on the destination domain. This approach ensures that funds are never lost due to failed calls. However, in the `AmarokFacet`, it is hardcoded as `msg.sender`. Several unexpected behaviors can be observed with this implementation:

- If the `msg.sender` is a smart contract, it might not be available on the destination chain.
- If the `msg.sender` is a smart contract deployed on another chain, the contract may not have a function to withdraw the native token.

As a result of this implementation, funds can be locked when an execution fails.

```solidity
contract AmarokFacet is ILiFi, SwapperV2, ReentrancyGuard {
...
IConnextHandler.XCallArgs memory xcallArgs = IConnextHandler.XCallArgs({
    params: IConnextHandler.CallParams({
        to: _bridgeData.receiver,
        callData: _bridgeData.callData,
        originDomain: _bridgeData.srcChainDomain,
        destinationDomain: _bridgeData.dstChainDomain,
        agent: _bridgeData.receiver,
        recovery: msg.sender,
        forceSlow: false,
        receiveLocal: false,
        callback: address(0),
        callbackFee: 0,
        relayerFee: 0,
        slippageTol: _bridgeData.slippageTol
    }),
    transactingAssetId: _bridgeData.assetId,
    amount: _amount
});
...
}
```

## Recommendation
Consider taking the recovery parameter as an argument.

## LiFi
Fixed with PR #28.

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

`Fund Lock, Bridge`

