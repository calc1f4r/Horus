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
solodit_id: 64153
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-11-megapot
source_link: https://code4rena.com/reports/2025-11-megapot
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] Missing Validation for Normal and Bonus Ball Sum Exceeding Bit Vector Capacity Causes Incorrect LP Pool Cap Calculation

### Overview

See description below for full details.

### Original Finding Content


In [`_calculateLpPoolCap`](https://github.com/code-423n4/2025-11-megapot/blob/5cda5779d1a157f847dd13700282dc09558806e4/contracts/Jackpot.sol# L1471), the maximum allowable tickets calculation assumes the bit vector can represent all possible ticket combinations:
```

    function _calculateLpPoolCap(uint256 _normalBallMax) internal view returns (uint256) {
        // We use MAX_BIT_VECTOR_SIZE because that's the max number that can be packed in a uint256 bit vector
        uint256 maxAllowableTickets = Combinations.choose(_normalBallMax, NORMAL_BALL_COUNT) * (MAX_BIT_VECTOR_SIZE - _normalBallMax);
```

Tickets are packed using bit vectors where normal balls occupy positions 1 to `normalBallMax`, and the bonusball is stored at position `normalBallMax + bonusball`. Since `MAX_BIT_VECTOR_SIZE = 255`, the maximum usable bit position is 255.

However, there is no validation ensuring that `normalBallMax + bonusballMax` does not exceed 255. The `bonusballMax` is dynamically calculated during drawing initialization:
```

        uint256 combosPerBonusball = Combinations.choose(normalBallMax, NORMAL_BALL_COUNT);
        uint256 minNumberTickets = newPrizePool * PRECISE_UNIT / ((PRECISE_UNIT - lpEdgeTarget) * ticketPrice);
        uint8 newBonusball = uint8(Math.max(bonusballMin, Math.ceilDiv(minNumberTickets, combosPerBonusball)));
        newDrawingState.bonusballMax = newBonusball;
```

If `normalBallMax + bonusballMax > 255`, the bit vector representation becomes invalid, and the `maxAllowableTickets` calculation in `_calculateLpPoolCap` will be incorrect, leading to a lower `lpPoolCap` than intended.

### Impact Details

When `normalBallMax + bonusballMax` exceeds 255, the system cannot correctly pack tickets into bit vectors, causing incorrect `maxAllowableTickets` calculations. This results in an artificially lower `lpPoolCap` than the target, potentially restricting LP deposits and reducing protocol capacity.

### Recommendations

Add boundary validation to enforce that `normalBallMax + bonusballMax` never exceeds 255. Implement checks in two places:

1. In `setNormalBallMax()`: Validate that the new `normalBallMax` plus the maximum possible `bonusballMax` (or a reasonable estimate) does not exceed 255.
2. In `_setNewDrawingState()`: After calculating `newBonusball`, validate that `normalBallMax + newBonusball <= 255`. If it exceeds the limit, either revert or cap `bonusballMax` at `255 - normalBallMax` and adjust the prize pool calculation accordingly.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
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

