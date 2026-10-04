---
# Core Classification
protocol: Megapot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64154
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-11-megapot
source_link: https://code4rena.com/reports/2025-11-megapot
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.80
financial_impact: low

# Scoring
quality_score: 4
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] Missing Validation for Normal Ball Max Range Causes Critical Function Failures Due to Combination Library Limits and Underflow

### Overview

See description below for full details.

### Original Finding Content


The `normalBallMax` parameter can be set to values that break critical functions. The [`Combinations::choose`](https://github.com/code-423n4/2025-11-megapot/blob/5cda5779d1a157f847dd13700282dc09558806e4/contracts/lib/Combinations.sol# L16) function has an artificial limit:
```

        assert(n >= k);
        assert(n <= 128); // Artificial limit to avoid overflow
```

Setting `normalBallMax` above 128 causes `Combinations.choose(normalBallMax, NORMAL_BALL_COUNT)` to revert with a panic. This affects:

1. `_calculateLpPoolCap()` - called during `setNormalBallMax()`:

   
```

       uint256 maxAllowableTickets = Combinations.choose(_normalBallMax, NORMAL_BALL_COUNT) * (MAX_BIT_VECTOR_SIZE - _normalBallMax);
   
```

2. `_setNewDrawingState()` - called by `initializeJackpot()`:

   
```

       uint256 combosPerBonusball = Combinations.choose(normalBallMax, NORMAL_BALL_COUNT);
   
```

Additionally, setting `normalBallMax` below `NORMAL_BALL_COUNT` (5) causes an underflow in `_calculateTierTotalWinningCombos()`:
```

            return Combinations.choose(NORMAL_BALL_COUNT, _matches) * Combinations.choose(_normalMax - NORMAL_BALL_COUNT, NORMAL_BALL_COUNT - _matches);
```

The calculation `_normalMax - NORMAL_BALL_COUNT` underflows when `normalBallMax < 5`, breaking drawing settlement.

Currently, `normalBallMax` is only constrained by the `uint8` type (1-255) in the constructor and `setNormalBallMax()`, with no validation for the effective range of 5-128.

### Impact Details

Setting `normalBallMax` outside the valid range (5-128) breaks:

* `initializeJackpot()` - Cannot initialize new drawings if `normalBallMax > 128` or `< 5`
* `calculateAndStoreDrawingUserWinnings()` - Cannot calculate payouts during drawing settlement
* `scaledEntropyCallback()` - Cannot finalize drawings due to combination calculation failures

This can permanently disable drawing initialization and settlement.

### Recommendations

Add validation to enforce `normalBallMax` is between `NORMAL_BALL_COUNT` (5) and 128 in both the constructor and `setNormalBallMax()`:
```

function setNormalBallMax(uint8 _normalBallMax) external onlyOwner {
    if (_normalBallMax < NORMAL_BALL_COUNT) revert JackpotErrors.InvalidNormalBallMax();
    if (_normalBallMax > 128) revert JackpotErrors.InvalidNormalBallMax();
    // ... rest of function
}
```

Similarly, add validation in the constructor to prevent invalid initialization.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 4/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | Megapot |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-11-megapot
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-11-megapot

### Keywords for Search

`vulnerability`

