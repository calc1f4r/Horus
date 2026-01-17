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
solodit_id: 62739
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1029
source_link: none
github_link: https://github.com/sherlock-audit/2025-07-malda-judging/issues/1477

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
finders_count: 2
finders:
  - 10ap17
  - holtzzx
---

## Vulnerability Title

M-16: Bridges don't support all of the listed assets

### Overview


This bug report discusses an issue with the Malda Protocol, specifically with the support for certain assets. The report was found by two users, 10ap17 and holtzzx. The root cause of the issue is that two platforms, Across and Everclear, do not fully support all of the assets that are listed as supported. This results in the inability to rebalance markets for those specific tokens. There are no specific attack paths identified, but the impact is that rebalancing will be impossible for those markets. The report does not include a Proof of Concept or any suggested mitigation strategies. However, the protocol team has fixed the issue in a recent pull request on GitHub. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-07-malda-judging/issues/1477 

## Found by 
10ap17, holtzzx

### Summary

/

### Root Cause

Across and Everclear,  don't support all of the assets that are listed as supported. That will result in inability to rebalance markets for that specific tokens

### Internal Pre-conditions

/

### External Pre-conditions

/

### Attack Path

No specific attack path, since the bridge don't support these assets

### Impact

Rebalancing will be impossible for those markets.

### PoC

_No response_

### Mitigation

_No response_

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/malda-protocol/malda-lending/pull/100







### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Malda |
| Report Date | N/A |
| Finders | 10ap17, holtzzx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-07-malda-judging/issues/1477
- **Contest**: https://app.sherlock.xyz/audits/contests/1029

### Keywords for Search

`vulnerability`

