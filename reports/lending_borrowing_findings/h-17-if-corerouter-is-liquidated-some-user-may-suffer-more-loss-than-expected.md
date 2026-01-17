---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58386
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/824

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
finders_count: 6
finders:
  - xiaoming90
  - 0xgh0st
  - jokr
  - t.aksoy
  - h2134
---

## Vulnerability Title

H-17: If CoreRouter is liquidated, some user may suffer more loss than expected

### Overview


This bug report discusses an issue found by multiple individuals in the CoreRouter code. The problem is that when a user redeems tokens, the amount they receive is calculated based on the exchange rate, but this does not take into account the possibility of CoreRouter being liquidated in LToken. This means that if CoreRouter is liquidated, the users who redeem earlier will receive their full amount, while the last users will suffer more loss than expected. The report suggests that when a user redeems, the received amount should be calculated based on CoreRouter's collateral in LToken to mitigate this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/824 

## Found by 
0xgh0st, h2134, jokr, t.aksoy, xiaoming90, zxriptor

### Summary

If CoreRouter is liquidated, some users may suffer more loss than expected.

### Root Cause

When a user redeem tokens from `CoreRouter`,  the underlying token amount to be received is calculated as `user amount * exchange rate`.

[CoreRouter.sol#L117-L118)](https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/main/Lend-V2/src/LayerZero/CoreRouter.sol#L117-L118):
```solidity
        // Calculate expected underlying tokens
        uint256 expectedUnderlying = (_amount * exchangeRateBefore) / 1e18;
```

The problem is that `CoreRouter` acts as both a supplier and borrower to `LToken`, therefore it's possible that `CoreRouter` is liquidated in `LToken` if its collateral is less than borrowed amount.

If `CoreRouter` is liquidated, it will have less collateral in `LToken` than before, however, such situation is not took into consideration when user s redeem, as a result, the users who redeem earlier can fully redeem, leaving the last users suffer the loss.

### Internal Pre-conditions

NA

### External Pre-conditions

`CoreRouter` is liquidated in `LToken`.

### Attack Path

NA

### Impact

User suffer more loss than expected.

### PoC

_No response_

### Mitigation

When user redeems, the received amount should be calculated based on `CoreRouter`'s collateral in `LToken`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | xiaoming90, 0xgh0st, jokr, t.aksoy, h2134, zxriptor |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/824
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

