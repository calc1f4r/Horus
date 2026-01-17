---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44992
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Wrong fee estimate in `getlzFee()` function

### Overview


The report states that there is a bug in the function `getlzFee()` which is used to calculate the Layerzero bridge message fee in deposit contracts. The severity of the bug is low, but the likelihood of it occurring is high. The issue is that the code uses the wrong `dataSend` value to estimate the fee, which can cause the bridge transaction to fail. The correct `data` value should include `ASSET_ID` and have 4 variables, but the code only includes 3 variables. This bug is present in all deposit contracts and the recommendation is to use `ASSET_ID` when estimating the fee.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

Function `getlzFee()` is supposed to calculate the Layerzero bridge message fee inside deposit contracts. The issue is that the code uses the wrong `dataSend` value to estimate the bridge fee:

```solidity
        bytes memory dataSend = abi.encode(1, _receiver,nETHShares);
```

The correct data sent through Layerzero has 4 variable and the estimated fee will be lower which can cause the bridge transaction to fail.

```solidity
        bytes memory data = abi.encode(ASSET_ID,1, _receiver,nETHShares);
```

This happens in all the deposit contracts.

## Recommendations

When estimating the fee use `ASSET_ID` too.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

