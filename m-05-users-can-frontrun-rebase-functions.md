---
# Core Classification
protocol: Dinari_2024-12-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49123
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
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

[M-05] Users can frontrun rebase functions

### Overview


The report states that there is a bug in the UsdPlus Contract which allows users to exploit the `rebaseAdd`, `rebaseMul`, and `rebaseSub` functions. These functions can be used by an address with the `OPERATOR_ROLE` to adjust the value of `$._balancePerShare`. This can be exploited in two ways: front-running a positive rebase to acquire tokens at a lower rate, and front-running a negative rebase to avoid losses. To prevent such exploits, the report suggests implementing a small withdrawal fee and introducing a delay between deposit and withdrawal requests.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The UsdPlus Contract contains the `rebaseAdd`, `rebaseMul`, and `rebaseSub` functions, which allow an address with the `OPERATOR_ROLE` to perform a rebase. These functions adjust the value of `$._balancePerShare`, either increasing or decreasing it depending on the action executed.

```solidity
    function rebaseAdd(uint128 value) external onlyRole(OPERATOR_ROLE) {
        uint256 _supply = totalSupply();
        uint128 _balancePerShare = uint128(FixedPointMathLib.fullMulDiv(balancePerShare(), _supply + value, _supply));
        UsdPlusStorage storage $ = _getUsdPlusStorage();
        $._balancePerShare = _balancePerShare;
        emit BalancePerShareSet(_balancePerShare);
    }
```

This functionality can be exploited in the following ways:

Users can front-run a positive rebase to acquire tokens at a lower rate. Once the rebase is executed, they can submit a withdrawal request, locking in the higher rate. Although the redemption process can take up to three days, the `request` function locks the rate in the user’s request ticket, allowing them to secure profits.

Users can also front-run a negative rebase by submitting a withdrawal request before the rebase is executed, locking in the rate prior to the update. This allows them to avoid losses associated with the negative rebase, effectively bypassing the intended impact of the rebase adjustment.

## Recommendations

A small withdrawal fee could be implemented to make such exploit attempts less desirable. Additionally, a delay could also be introduced between deposit and withdrawal requests.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dinari_2024-12-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dinari-security-review_2024-12-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

