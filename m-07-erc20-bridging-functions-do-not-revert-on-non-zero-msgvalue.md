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
solodit_id: 24683
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-lifinance
source_link: https://code4rena.com/reports/2022-03-lifinance
github_link: https://github.com/code-423n4/2022-03-lifinance-findings/issues/53

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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] ERC20 bridging functions do not revert on non-zero msg.value

### Overview


A bug has been reported in the Li.Fi finance project which affects the AnyswapFacet, CBridgeFacet, HopFacet and NXTPFacet functions. This bug allows native funds to be mistakenly sent along with plain ERC20 bridging calls, resulting in the funds being frozen on the contract balance and potentially lost. The severity of the bug has been rated as medium, as it is possible for user funds to be frozen or lost in combination with other issues. 

The bug is caused by the functions not checking that the `msg.value` is zero. The recommended mitigation step is to consider reverting when bridging functions with non-native targets are called with non-zero native amount added. The bug has been fixed in the lifinance/lifi-contracts@a8d6336c2ded97bdbca65b64157596b33f18f70d commit and has been confirmed by the sponsor.

### Original Finding Content

_Submitted by hyh, also found by danb, kirk-baird, and pmerkleplant_

Any native funds mistakenly sent along with plain ERC20 bridging calls will be lost. AnyswapFacet, CBridgeFacet, HopFacet and NXTPFacet have this issue.

For instance, swapping function might use native tokens, but the functions whose purpose is bridging solely have no use of native funds, so any mistakenly sent native funds to be frozen on the contract balance.

Placing the severity to be medium as in combination with other issues there is a possibility for user funds to be frozen for an extended period of time (if WithdrawFacet's issue plays out) or even lost (if LibSwap's swap native tokens one also be triggered).

In other words, the vulnerability is also a wider attack surface enabler as it can bring in the user funds to the contract balance.

Medium despite the fund loss possibility as the native funds in question here are mistakenly sent only, so the probability is lower compared to direct leakage issues.

### Proof of Concept

startBridgeTokensViaAnyswap doesn't check that `msg.value` is zero:

[AnyswapFacet.sol#L38-L48](https://github.com/code-423n4/2022-03-lifinance/blob/main/src/Facets/AnyswapFacet.sol#L38-L48)<br>

startBridgeTokensViaCBridge also have no such check:

[CBridgeFacet.sol#L59-L66](https://github.com/code-423n4/2022-03-lifinance/blob/main/src/Facets/CBridgeFacet.sol#L59-L66)<br>

startBridgeTokensViaHop the same:

[HopFacet.sol#L66-L71](https://github.com/code-423n4/2022-03-lifinance/blob/main/src/Facets/HopFacet.sol#L66-L71)<br>

In NXTPFacet completion function does the check, but startBridgeTokensViaNXTP doesn't:

[NXTPFacet.sol#L54-L59](https://github.com/code-423n4/2022-03-lifinance/blob/main/src/Facets/NXTPFacet.sol#L54-L59)<br>

### Recommended Mitigation Steps

Consider reverting when bridging functions with non-native target are called with non-zero native amount added.

**[H3xept (Li.Fi) commented](https://github.com/code-423n4/2022-03-lifinance-findings/issues/53#issuecomment-1095009690):**
 > Fixed in lifinance/lifi-contracts@a8d6336c2ded97bdbca65b64157596b33f18f70d

**[gzeon (judge) commented](https://github.com/code-423n4/2022-03-lifinance-findings/issues/53#issuecomment-1100704372):**
 > Sponsor confirmed with fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-lifinance
- **GitHub**: https://github.com/code-423n4/2022-03-lifinance-findings/issues/53
- **Contest**: https://code4rena.com/reports/2022-03-lifinance

### Keywords for Search

`vulnerability`

