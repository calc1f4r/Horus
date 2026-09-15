---
# Core Classification
protocol: Telcoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3635
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/80

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

M-3: `FeeBuyback` native token can not be rescued

### Overview


This bug report was found by WATCHPUG and is related to the `FeeBuyback` contract, which is part of the Telcoin Staking project. The issue is that there is lack of methods to rescue native tokens trapped in the contract. This can happen at the line 77 of the contract, where the `_aggregator` is called with a `msg.value`, which means that the native token can be used as an inToken for the swap. The current implementation of `rescueERC20()` only supports rescue ERC20 tokens, so the leftover native tokens trapped in the contract can not be rescued. To solve this issue, it is recommended to consider adding support to rescue native tokens. The code snippets and tool used for this report are provided in the report.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/80 

## Found by 
WATCHPUG

## Summary

Lack of methods to rescue native tokens trapped in the `FeeBuyback` contract.

## Vulnerability Detail

Like ERC20 tokens, the native token may also get stuck in the `FeeBuyback` contract for all sorts of reasons.

For example, at L77, the `_aggregator` is called with a `msg.value`, which means that the native token can be used as an inToken for the swap. Therefore, part of the input native token can be sent back to the FeeBuyback contract as a leftover.

However, the current implementation of `rescueERC20()` only supports rescue ERC20 tokens.

## Impact

The leftover native tokens trapped in the contract can not be rescued.

## Code Snippet

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L77-L78

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L94-L97

## Tool used

Manual Review

## Recommendation

Consider adding support to rescue native tokens.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/10

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/80
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`vulnerability`

