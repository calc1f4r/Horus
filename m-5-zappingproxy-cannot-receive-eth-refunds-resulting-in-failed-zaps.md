---
# Core Classification
protocol: USG - Tangent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63051
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1073
source_link: none
github_link: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/150

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - 0xShoonya
  - tobi0x18
  - jayjoshix
  - kimnoic
  - holtzzx
---

## Vulnerability Title

M-5: `ZappingProxy` cannot receive ETH refunds resulting in failed zaps

### Overview


The bug report is about an issue found in the `ZappingProxy` contract, which is used to forward `msg.value` to routers. However, the contract does not have a payable receive or fallback function, which causes router ETH refunds to revert. This results in failed zaps for ETH paths that expect refunds. The root cause of this issue is that when `zapProxy` is called with `tokenIn == CHAIN_COIN` and a positive `msg.value`, it forwards ETH to the router, but there is no function in the contract to handle refunds. This can lead to the entire zap failing. To fix this issue, a payable ETH acceptance path needs to be added to the contract. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/150 

## Found by 
0xShoonya, covey0x07, deadmanwalking, holtzzx, jayjoshix, kimnoic, tobi0x18

## Summary

 `ZappingProxy` forwards `msg.value` to routers but has no payable receive/fallback, so router ETH refunds to the proxy will revert. This causes failed zaps for ETH paths that expect refunds.

## Root Cause

When `zapProxy` is called with `tokenIn == CHAIN_COIN` and a positive `msg.value`, it forwards ETH to the router:
[ZappingProxy.sol#L39-L76](https://github.com/sherlock-audit/2025-08-usg-tangent/blob/main/tangent-contracts/src/USG/Utilities/ZappingProxy.sol#L39-L76)
```js
uint256 bal = tokenOut.balanceOf(receiver);

(bool isRouterCallSuccess, bytes memory data) = router.call{value: msg.value}(zap.routerCall);

require(isRouterCallSuccess, ZapCallError(data));
```
If there is unspent ETH, router refund unspent ETH to caller/msg.sender.

This is the logic present in `zapProxy` to sweep any ETH balance to the treasury:
```js
} else {
    balanceTokenInLeft = address(this).balance;
    if (0 != balanceTokenInLeft) {
        payable(controlTower.feeTreasury()).transfer(balanceTokenInLeft);
    }
}
```
But there is no payable `receive()` or `fallback()` in `ZappingProxy`, so ETH refunds to the proxy will revert.

## Internal pre-conditions

.

## External pre-conditions

.

## Attack Scenario

.

## Impact

Because `ZappingProxy` lacks a payable `receive()/fallback()`, the refund reverts, causing the entire zap to revert.

## Mitigation

Add a payable ETH acceptance path (receive/fallback) so router refunds don’t revert.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USG - Tangent |
| Report Date | N/A |
| Finders | 0xShoonya, tobi0x18, jayjoshix, kimnoic, holtzzx, covey0x07, deadmanwalking |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/150
- **Contest**: https://app.sherlock.xyz/audits/contests/1073

### Keywords for Search

`vulnerability`

