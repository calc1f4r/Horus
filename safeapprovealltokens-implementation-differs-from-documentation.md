---
# Core Classification
protocol: Origin Balancer MetaPool Strategy Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32985
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-balancer-metapool-audit
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

safeApproveAllTokens Implementation Differs From Documentation

### Overview


The `safeApproveAllTokens` function does not properly approve the transfer of supported assets to the Balancer pool and does not approve the wrapping of `stEth` and `frxEth` tokens. Additionally, it allows for an unlimited number of BPTs to be withdrawn from the Balancer vault and Aura rewards pool. This issue has been fixed in pull request #1776. 

### Original Finding Content

The `safeApproveAllTokens` function [comments](https://github.com/OriginProtocol/origin-dollar/blob/eb11498c376b65696c90981757221b076d6226aa/contracts/contracts/strategies/balancer/BalancerMetaPoolStrategy.sol#L421) specify that the function should approve the Balancer pool to transfer all supported assets from the strategy, as well as approve the `wstEth` and `sfrxEth` contracts to pull `stEth` and `frxEth` from the Strategy for wrapping purposes. However, the function does not perform the necessary approvals to wrap the tokens, and additionally, it approves the Balancer vault and Aura rewards pool to [withdraw an unlimited number of BPTs](https://github.com/OriginProtocol/origin-dollar/blob/eb11498c376b65696c90981757221b076d6226aa/contracts/contracts/strategies/balancer/BalancerMetaPoolStrategy.sol#L431).


Consider correcting the `safeApproveAllTokens` function to follow its intended behavior. 


***Update:** Resolved in [pull request #1776](https://github.com/OriginProtocol/origin-dollar/pull/1776).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Balancer MetaPool Strategy Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-balancer-metapool-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

