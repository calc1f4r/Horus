---
# Core Classification
protocol: Malda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62729
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1029
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-malda-judging/issues/177

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
finders_count: 21
finders:
  - Sa1ntRobi
  - BusinessShotgun
  - 0xDemon
  - ZanyBonzy
  - dan\_\_vinci
---

## Vulnerability Title

M-6: `EverclearBridge` does not pull tokens from the Rebalancer, causing all rebalancing operations to fail

### Overview


Summary: 
A bug was found in the `EverclearBridge` contract where it does not transfer tokens from the Rebalancer contract before attempting to perform bridging operations. This results in a denial of service for cross-chain liquidity movement and can cause protocol operations to fail. The bug has been fixed by updating the contract to call `safeTransferFrom` and pull the required tokens from the Rebalancer before proceeding with bridging logic.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-malda-judging/issues/177 

## Found by 
0xDemon, 0xmechanic, 0xsai, 10ap17, Angry\_Mustache\_Man, BusinessShotgun, Cybrid, ExtraCaterpillar, IvanFitro, Sa1ntRobi, SafetyBytes, ZanyBonzy, ZeroTrust, Ziusz, bube, bulgari, dan\_\_vinci, davies0212, maigadoh, oxelmiguel, vangrim

### Summary

The `EverclearBridge` contract does not transfer tokens from the Rebalancer contract before attempting to perform bridging operations. It assumes custody of tokens without actually calling `safeTransferFrom` to pull tokens from the Rebalancer. As a result, the bridge contract does not have the required tokens, causing all rebalancing attempts to fail.

### Root Cause

In `EverclearBridge.sol`, the [`sendMsg`](https://github.com/sherlock-audit/2025-07-malda/blob/main/malda-lending/src/rebalancer/bridges/EverclearBridge.sol#L79C4-L123C6) function does not call `IERC20(_token).safeTransferFrom(msg.sender, address(this), params.amount)` to transfer tokens from the Rebalancer to itself. Without this transfer, the bridge cannot perform any bridging logic that requires token custody.

### Internal Pre-conditions

1. The Rebalancer approves the bridge contract to spend tokens.
2. The Rebalancer calls `sendMsg` on the bridge contract without transferring tokens.

### External Pre-conditions

None.

### Attack Path

1. The Rebalancer approves the bridge contract.
2. The bridge contract attempts to perform bridging logic but fails due to lack of token custody.
3. No tokens are bridged and rebalancing fails.

### Impact

All rebalancing operations using the bridge contract will fail, resulting in a complete denial of service for cross-chain liquidity movement. This can halt protocol operations that depend on rebalancing and may lead to liquidity fragmentation or loss of protocol functionality.


### PoC

_No response_

### Mitigation

Update the `EverclearBridge` contract to call `safeTransferFrom` and pull the required tokens from the Rebalancer before proceeding with bridging logic.

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/malda-protocol/malda-lending/pull/105


**CergyK**

Fix looks good. Tokens are now pulled from Rebalancer into EverclearBridge





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Malda |
| Report Date | N/A |
| Finders | Sa1ntRobi, BusinessShotgun, 0xDemon, ZanyBonzy, dan\_\_vinci, 10ap17, ZeroTrust, Angry\_Mustache\_Man, davies0212, maigadoh, IvanFitro, ExtraCaterpillar, bulgari, dan\_\_vinci, bube, SafetyBytes, 0xmechanic, oxelmiguel, Cybrid, 0xsai, Ziusz, vangrim |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-malda-judging/issues/177
- **Contest**: https://app.sherlock.xyz/audits/contests/1029

### Keywords for Search

`vulnerability`

