---
# Core Classification
protocol: Sense Update #1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8723
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/58
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-sense-judging/issues/29

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - spyrosonic10
  - Bauer
  - 0x52
---

## Vulnerability Title

M-2: Multiple functions may leave excess funds in the contract that should be returned

### Overview


This bug report discusses an issue with multiple functions in the contract that may leave excess funds in the contract that should be returned. The functions include RollerPeriphery#deposit, Periphery#swapForPTs, Periphery#addLiquidity, Periphery#issue, and RollerPeriphery#RollermintFromUnderlying. The issue is that the roller code will mean that previewMint will always perfectly reflect the exact exchange rate into the roller, but adapter.scale varies by adapter and isn't guaranteed to be exact. As a result, _transferFrom may take too much underlying, and since this underlying is wrapped to target, the contract should return all excess target to the receiver. The impact of this issue is that tokens may be left in the contract and lost. The code snippets used to identify this issue can be found in the source link. The recommendation is to return excess tokens at the end of the function, which is something that is already in place for the `_swapSenseToken` function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-sense-judging/issues/29 

## Found by 
Bauer, 0x52, spyrosonic10

## Summary

Periphery#combine may leave excess underlying in the contract due to _fromTarget unwrapping to underlying and the quote may not swap them all.

When using arbitrary tokens to swap to underlying the contract always moves in the full amount specified. There is no guarantee that the quote will consume all tokens. As a result the contract may leave excess sell tokens in the contract but it should return then to the receiver.

These functions include:

RollerPeriphery
1) deposit

Periphery
1) swapForPTs
2) addLiquidity
3) issue

RollerPeriphery#RollermintFromUnderlying uses adapter.scale and previewMint to determine the amount of underlying to transfer. The roller code will mean that previewMint will always perfectly reflect the exact exchange rate into the roller. However adapter.scale varies by adapter and isn't guaranteed to be exact. The result is that _transferFrom may take too much underlying. Since this underlying is wrapped to target the contract should return all excess target to receiver.

## Vulnerability Detail

See summary.

## Impact

Token may be left in the contract and lost

## Code Snippet

https://github.com/sherlock-audit/2023-03-sense/blob/main/auto-roller/src/RollerPeriphery.sol#L175-L186

https://github.com/sherlock-audit/2023-03-sense/blob/main/auto-roller/src/RollerPeriphery.sol#L196

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L178

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L325

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L409

## Tool used

Manual Review

## Recommendation

Return excess tokens at the end of the function

## Discussion

**jparklev**

We have this feature, for example, on `_swapSenseToken`, but not on the cases mentioned.

Our fix will be: Transfer non-used tokens back to the user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Sense Update #1 |
| Report Date | N/A |
| Finders | spyrosonic10, Bauer, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-sense-judging/issues/29
- **Contest**: https://app.sherlock.xyz/audits/contests/58

### Keywords for Search

`vulnerability`

