---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7045
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
  - business_logic

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

Replace createRetryableTicketNoRefundAliasRewrite() with depositEth()

### Overview


This bug report describes an issue with the function _startBridge() of the ArbitrumBridgeFacet. The function uses createRetryableTicketNoRefundAliasRewrite() which, according to the docs, skips some address rewrite magic that depositEth() does. As a result, developers that call the LiFi contracts directly may make mistakes and lose tokens.

The recommendation is to replace createRetryableTicketNoRefundAliasRewrite() with depositEth(). LiFi notes that retryable tickets can be used to deposit Ether, which could be preferable if more flexibility for the destination address is needed. The bug was verified and reverted with PR #79.

### Original Finding Content

## Security Report

## Severity
**Medium Risk**

## Context
`ArbitrumBridgeFacet.sol#L90-L137`

## Description
The function `_startBridge()` of the `ArbitrumBridgeFacet` uses `createRetryableTicketNoRefundAliasRewrite()`. According to the documentation on address aliasing, this method skips some address rewrite logic that `depositEth()` implements. 

Normally, `depositEth()` should be used, as stated in the documentation regarding depositing and withdrawing Ether. Additionally, this method will be deprecated after Nitro, as referenced in `Inbox.sol#L283-L297`. 

While the bridge doesn’t perform the checks that `depositEth()` does, it is easy for developers calling the LiFi contracts directly to make mistakes and lose tokens.

```solidity
function _startBridge(...) {
    ...
    if (LibAsset.isNativeAsset(_bridgeData.assetId)) {
        gatewayRouter.createRetryableTicketNoRefundAliasRewrite{ value: _amount + cost }(...);
    }
    ...
}
```

## Recommendation
Replace `createRetryableTicketNoRefundAliasRewrite()` with `depositEth()`.

## LiFi
In principle, retryable tickets can alternatively be used to deposit Ether; this could be preferable to the special `eth-deposit` message type if, for example, more flexibility for the destination address is needed, or if one wants to trigger the fallback function on the L2 side. Reverted with PR #79.

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

`Business Logic`

