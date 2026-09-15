---
# Core Classification
protocol: Omni Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53666
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20-%20AVS%20And%20Token%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20-%20AVS%20And%20Token%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

syncWithOmni() Can Surpass Ethereum Block Gas Limit

### Overview

See description below for full details.

### Original Finding Content

## Description

Due to the use of for-loops when calling the `_getOperators()` function, it is possible for calls to the `syncWithOmni()` function to use more gas than the Ethereum block gas limit (30 million), which results in the call reverting. Tests demonstrate this is possible with 98 registered operators staking in 24 EigenLayer strategies each, where all strategies have strategy parameters in OmniAVS.

## Recommendations

There are two proposed solutions to resolve the issue:

1. Reduce the gas usage of `_getTotalDelegations()` and `_getSelfDelegations()` and avoid iterating through arrays where possible.
2. Limit the amount of strategy parameters and number of operators such that `syncWithOmni()` can no longer surpass the Ethereum block gas limit in gas usage.

## Resolution

The project team has acknowledged the issue with the following comment:

> "For our initial mainnet release, we will maintain a small list of allowed operators and strategies. Operators will not exceed 30, and supported strategies will not exceed 10. Gas optimizations would require non-trivial refactoring, adding complexity for (under these stricter conditions) marginal benefit. Gas optimizations will be considered in a future release when these conditions are less strict."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20-%20AVS%20And%20Token%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20-%20AVS%20And%20Token%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf

### Keywords for Search

`vulnerability`

