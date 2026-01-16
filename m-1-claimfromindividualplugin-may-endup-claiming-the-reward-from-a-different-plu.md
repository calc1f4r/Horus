---
# Core Classification
protocol: Telcoin
chain: everychain
category: uncategorized
vulnerability_type: array_reorder

# Attack Vector Details
attack_type: array_reorder
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3633
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/86

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - array_reorder

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

M-1: `claimFromIndividualPlugin()` may endup claiming the reward from a different plugin with wrong `auxData` when the index as changed due to `removePlugin()`

### Overview


This bug report is about the `claimFromIndividualPlugin()` function in the Telcoin staking contract. The bug occurs when a user calls `claimFromIndividualPlugin()` and the `PLUGIN_EDITOR` removes a plugin before the transaction gets minted. The plugin referred by the `pluginIndex` can be changed to another plugin, and the `auxData` supposed to be supplied to the original plugin is now supplied to another plugin. As a result, the user may end up with lesser rewards as a wrong `auxData` is supplied to the wrong plugin. The code snippet and the tool used to find the bug are provided in the report. The recommendation is to consider using `pluginAddress` instead. The discussion section provides a link to a pull request.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/86 

## Found by 
WATCHPUG

## Summary

When `removePlugin()` happens between the user sends the `claimFromIndividualPlugin()` transaction and before it gets minted, it may lead to lesser rewards as the `auxData` prepared for another plugin will now be used.

## Vulnerability Detail

When a user calls `claimFromIndividualPlugin()`, a `pluginIndex` is used to refer to a plugin.

However, if the `PLUGIN_EDITOR` removed a plugin before the transaction gets minted, the plugin referred by the `pluginIndex` can be changed to another plugin.

As a result, the `auxData` supposed to be supplied to the original plugin is now supplied to another plugin.

## Impact

The user may end up with lesser rewards as a wrong `auxData` is supplied to the wrong plugin.

## Code Snippet

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L420-L429

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/StakingModule.sol#L178-L185

## Tool used

Manual Review

## Recommendation

Consider using `pluginAddress` instead.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/8

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/86
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`Array Reorder`

