---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53481
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-22] Rebase Limiter isLimitReached will almost always return false due to rounding error

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** PositiveTokenRebaseLimiter.sol:isLimitReached#L103-L115

**Description:**

The function `isLimitReached` is used in `getSharesToBurnLimit` to provide an early return if the rebase limit is already reached and it can just return 0. However, we found that this function will almost always return `false`, due to rounding errors.

In `isLimitReached`, the difference between the current ETH and pre-total ETH is taken as the accumulated ETH. This accumulated ETH is then divided over the pre-total ETH to get the new rebase. The result of the function is whether this new rebase is greater than the rebase limit.

But this will almost never be the case, because `increaseEther` is the only function that increases the current ETH and already takes the maximum against the rebase limit. This calculation is rounded down and as a result will always be smaller than the actual maximum if it's not a perfect division without remainder.

Secondly, the calculation for the new rebase in `isLimitReached` is also rounded down and will also almost always be smaller than the rebase limit.

As a result, the check becomes redundant in its current form.
```
function isLimitReached(TokenRebaseLimiterData memory _limiterState) internal pure returns (bool) {
    if (_limiterState.positiveRebaseLimit == UNLIMITED_REBASE) return false;
    if (_limiterState.currentTotalPooledEther < _limiterState.preTotalPooledEther) return false;

    uint256 accumulatedEther = _limiterState.currentTotalPooledEther - _limiterState.preTotalPooledEther;
    uint256 accumulatedRebase;

    if (_limiterState.preTotalPooledEther > 0) {
        accumulatedRebase = accumulatedEther * LIMITER_PRECISION_BASE / _limiterState.preTotalPooledEther;
    }

    return accumulatedRebase >= _limiterState.positiveRebaseLimit;
}
```

**Remediation:**  We would recommend to either remove the check, as the limit is already enforced in `increaseEther` or to round the calculations up.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

