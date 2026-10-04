---
# Core Classification
protocol: Numa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45281
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/554
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/53

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
  - juaan
---

## Vulnerability Title

M-4: No RWAs have a chainlink feed in ETH, so RWAs cannot be minted as nuAssets

### Overview


The bug report states that there is an issue with the protocol that prevents Real World Assets (RWAs) from being minted as synthetic nuAssets. This is because the protocol only works with chainlink feeds that use ETH as the pricing asset, but most RWAs on chainlink are only available with USD pairs. This means that the protocol cannot currently support RWAs. The report suggests a solution of converting the USD pairs into ETH using the ETH/USD price feed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/53 

## Found by 
juaan

### Summary

A key intention of the protocol is to allow RWAs with chainlink feeds to be represented with synthetic nuAssets.

The issue is that the protocol only works with chainlink feeds where the asset is priced with ETH.

All the RWAs like gold, oil, etc on chainlink are only available with USD pairs, not ETH.

### Root Cause

The protocol only works with chainlink feeds where the asset is priced with ETH, but all the RWAs like gold, crude oil, etc on chainlink are only available with USD pairs, not ETH.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Protocol in it's current form cannot work with RWAs. 

### PoC

_No response_

### Mitigation

Have a way to convert the ASSET/USD pairs into ASSET/ETH using the ETH/USD price feed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Numa |
| Report Date | N/A |
| Finders | juaan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/53
- **Contest**: https://app.sherlock.xyz/audits/contests/554

### Keywords for Search

`vulnerability`

