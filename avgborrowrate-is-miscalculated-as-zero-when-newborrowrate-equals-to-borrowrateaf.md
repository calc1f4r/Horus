---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54433
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c9a9dc9-d39d-4018-a61b-d7b43619180e
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_blue_irm_oct2023.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Jonah Wu
  - StErMi
---

## Vulnerability Title

avgBorrowRate is miscalculated as zero when newBorrowRate equals to borrowRateAfterJump 

### Overview


This bug report is about an issue in the `SpeedJumpIrm.sol` file on line 147. The `SpeedJumpIrm` calculates the interest rate using two factors, `SpeedFactor` and `JumpFactor`. However, there is a problem when `linearVariation` is small but not zero, resulting in an incorrect `avgBorrowRate` being returned. This issue is related to another issue called "avgBorrowRate can blow-up for small linearVariation". To fix this, the report recommends using a simpler formula to calculate the average borrow rate when `linearVariation` is small.

### Original Finding Content

## SpeedJumpIrm.sol Overview

## Context
**File:** SpeedJumpIrm.sol  
**Line:** 147

## Description
The `SpeedJumpIrm` calculates the interest rate based on `SpeedFactor` and `JumpFactor`. According to the document, at any time `t`, the level of the rate is given by the formula:

\[ r(t) = r(last(t)) \times jump(t) \times speed(t) \]

For Morpho blue to calculate the interests during two interactions of IRM, the `SpeedJumpIrm` calculates the `avgBorrowRate` as 

\[ \text{uint256}\left(\left(\text{int256(newBorrowRate)} - \text{int256(borrowRateAfterJump)}\right).\text{wDivDown(linearVariation)}\right) \]

Here, `borrowRateAfterJump` is the interest rate applied by the `JumpFactor` and `newBorrowRate` is the end interest rate applied by both `SpeedFactor` and `JumpFactor`.

In the `SpeedJumpIrm` implementation, two variables are calculated as follows:

- **Lines 134-139 in SpeedJumpIrm.sol:**
    ```solidity
    int256 linearVariation = speed * int256(elapsed);
    uint256 variationMultiplier = MathLib.wExp(linearVariation);
    // newBorrowRate = prevBorrowRate * jumpMultiplier * variationMultiplier.
    uint256 borrowRateAfterJump = marketIrm[id].prevBorrowRate.wMulDown(jumpMultiplier);
    uint256 newBorrowRate = borrowRateAfterJump.wMulDown(variationMultiplier);
    ```

- ...
    ```solidity
    uint256 avgBorrowRate;
    if (linearVariation == 0) 
        avgBorrowRate = borrowRateAfterJump; // Safe "unchecked" cast to uint256 because linearVariation < 0 <=> newBorrowRate <= borrowRateAfterJump
    else 
        avgBorrowRate = uint256((int256(newBorrowRate) - int256(borrowRateAfterJump)).wDivDown(linearVariation));
    ```

Since the `speed` variable depends on the error of the current utilization rate and the target utilization rate, it can yield very small results, resulting in `linearVariation` being very small or zero. Thus, in the implementation, `avgBorrowRate` is returned as `borrowRateAfterJump` when `linearVariation` is zero.

However, there's an edge case when `linearVariation` is small but not zero. In this case, `borrowRateAfterJump.wMulDown(variationMultiplier)` equals `borrowRateAfterJump` because of rounding down, resulting in the wrong `avgBorrowRate` at `SpeedJumpIrm.sol#L149` since:

\[ linearVariation = 0 \]

## Recommendation
This issue is closely related to the issue "avgBorrowRate can blow-up for small linearVariation". Both describe the approximation error when `linearVariation` is small. 

It is recommended to use a simpler formula to approximate the average borrow rate when `linearVariation` is small. The recommended mitigation of "avgBorrowRate can blow-up for small linearVariation" works in two cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Jonah Wu, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_blue_irm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c9a9dc9-d39d-4018-a61b-d7b43619180e

### Keywords for Search

`vulnerability`

