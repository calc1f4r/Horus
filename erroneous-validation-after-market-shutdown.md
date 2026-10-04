---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35164
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
github_link: none

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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Erroneous Validation After Market Shutdown

### Overview


The bug report discusses an issue in the `RizRegistry` contract where the `updateLendingPoolStatus` function is not properly setting the `_isValidAddressProvider` flag to false when a market is shutdown. This results in the `setImplementation` function not skipping any elements, which can cause problems with the implementations of proxies for shutdown pools. The report suggests setting the flag to false when the status is false and handling that state when used. The issue has been resolved in a recent pull request.

### Original Finding Content

When a market is [shutdown](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the [`updateLendingPoolStatus` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L117) from the `RizRegistry` contract is called. In it, the implementation checks if the [`addressProvider` address](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L118) is a valid address in the `_isValidAddressProvider` mapping and whether the [pool was registered](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L130) in the `_lendingPools` mapping, and proceeds to [set it to the `false` state](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L134). However, since the flag in the `_isValidAddressProvider` mapping is not set to `false`, a ["skipping" check](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L186) done in the `setImplementation` function will never skip a single element. This will result in modifying the implementations of proxies for shutdown pools.


Consider setting the `_isValidAddressProvider` mapping to `false` when [`status == false` within `updateLendingPoolStatus`](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/RizRegistry.sol#L117) and handling that state when used.


***Update:** Resolved in [pull request \#89](https://github.com/radiant-capital/riz/pull/89) at commit [d2728a7](https://github.com/radiant-capital/riz/pull/89/commits/d2728a71201c5195a147725d128ad661ff4a1093).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

