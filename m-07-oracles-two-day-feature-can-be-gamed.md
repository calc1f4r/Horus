---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: oracle
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: oracle

# Source Information
source: solodit
solodit_id: 5736
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/278

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
  - bypass_limit
  - rounding
  - oracle

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ruhum
---

## Vulnerability Title

[M-07] Oracle’s two-day feature can be gamed

### Overview


This bug report is about how the two-day feature of the oracle can be gamed. The oracle computes the day using a mathematical formula. If the oracle is manipulated at the last block of day X and the first block of day X+1, it bypasses the two-day feature of the oracle. This makes it possible to manipulate the oracle for only two blocks. To fix this issue, the oracle can be increased to a three-day interval, so the oracle has to be manipulated for at least 24 hours.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/main/src/Oracle.sol#L124


## Vulnerability details

## Impact
The two-day feature of the oracle can be gamed where you only have to manipulate the oracle for ~2 blocks.

## Proof of Concept
The oracle computes the day using:
```sol
uint day = block.timestamp / 1 days;
```

Since we're working with `uint` values here, the following is true:
$1728799 / 86400 = 1$
$172800 / 86400 = 2$

Meaning, if you manipulate the oracle at the last block of day $X$, e.g. 23:59:50, and at the first block of day $X + 1$, e.g. 00:00:02, you bypass the two-day feature of the oracle. You only have to manipulate the oracle for two blocks.

This is quite hard to pull off. I'm also not sure whether there were any instances of Chainlink oracle manipulation before. But, since you designed this feature to prevent small timeframe oracle manipulation I think it's valid to point this out.

## Tools Used
none

## Recommended Mitigation Steps
If you increase it to a three-day interval you can fix this issue. Then, the oracle has to be manipulated for at least 24 hours.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | Ruhum |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/278
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Bypass limit, Rounding, Oracle`

