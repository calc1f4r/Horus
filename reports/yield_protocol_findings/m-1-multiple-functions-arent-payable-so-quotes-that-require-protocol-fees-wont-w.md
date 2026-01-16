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
solodit_id: 8722
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/58
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-sense-judging/issues/28

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
finders_count: 2
finders:
  - Bauer
  - 0x52
---

## Vulnerability Title

M-1: Multiple functions aren't payable so quotes that require protocol fees won't work correctly

### Overview


This bug report was found by Bauer, 0x52 and is related to multiple functions that use quotes but that aren't payable, which breaks their compatibility with some quotes. This issue was found by manual review and can cause wasted gas fees or bad rates for users. The recommendation is to add payable to the external/public functions mentioned. The report was confirmed by jparklev who stated that they had forgotten to add payable to the functions mentioned.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-sense-judging/issues/28 

## Found by 
Bauer, 0x52

## Summary

There are multiple functions that use quotes but that aren't payable. This breaks their compatibility with some quotes. As the [0x docs](https://docs.0x.org/0x-swap-api/guides/use-0x-api-liquidity-in-your-smart-contracts) state: `Certain quotes require a protocol fee, in ETH, to be attached to the swap call`.

The following flows use a quote but the external/public starting function isn't payable:

RollerPeriphery
1) redeem

Periphery
1) removeLiquidity
2) combine
3) swapPT
4) swapYT
5) issue

## Vulnerability Detail

See summary.

## Impact

Functions won't be compatible with certain quotes causing wasted gas fees or bad rates for users

## Code Snippet

https://github.com/sherlock-audit/2023-03-sense/blob/main/auto-roller/src/RollerPeriphery.sol#L104

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L325

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L409

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L433

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L240

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L263

## Tool used

Manual Review

## Recommendation

Add payable to these external/public functions

## Discussion

**jparklev**

Confirmed: We've forgotten to add payable to the functions mentioned

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Sense Update #1 |
| Report Date | N/A |
| Finders | Bauer, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-sense-judging/issues/28
- **Contest**: https://app.sherlock.xyz/audits/contests/58

### Keywords for Search

`vulnerability`

