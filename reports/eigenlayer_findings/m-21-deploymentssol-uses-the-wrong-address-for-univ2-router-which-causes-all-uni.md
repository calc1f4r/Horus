---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3346
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/32

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - uniswap
  - hardcoded_address

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-21: Deployments.sol uses the wrong address for UNIV2 router which causes all Uniswap V2 calls to fail

### Overview


This bug report is about an issue found in the Deployments.sol contract. The issue is that the address for UNIV2 router was set incorrectly, causing Uniswap V2 calls to fail. This was found during a manual review by 0x52. The wrong address was causing Uniswap V2 to be totally unusable. The code snippet for the issue can be found at Deployments.sol#L25. The recommendation is to change the UNIV2_ROUTER address to the address of the V2 router, which is 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D. This issue has since been fixed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/32 

## Found by 
0x52

## Summary

Deployments.sol accidentally uses the Uniswap V3 router address for UNIV2_ROUTER which causes all Uniswap V2 calls to fail

## Vulnerability Detail

    IUniV2Router2 internal constant UNIV2_ROUTER = IUniV2Router2(0xE592427A0AEce92De3Edee1F18E0157C05861564);

The constant UNIV2_ROUTER contains the address for the Uniswap V3 router, which doesn't contain the "swapExactTokensForTokens" or "swapTokensForExactTokens" methods. As a result, all calls made to Uniswap V2 will revert.

## Impact

Uniswap V2 is totally unusable

## Code Snippet

[Deployments.sol#L25](https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/global/Deployments.sol#L25)

## Tool used

Manual Review

## Recommendation

Change UNIV2_ROUTER to the address of the V2 router:

    IUniV2Router2 internal constant UNIV2_ROUTER = IUniV2Router2(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);

## Discussion

**jeffywu**

@weitianjie2000 I believe this has been fixed subsequently

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/32
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`Uniswap, Hardcoded Address`

