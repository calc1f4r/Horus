---
# Core Classification
protocol: Stella
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19053
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-1 markLiquidationStatus() may cause the liquidator to lose premium

### Overview


A bug report was filed concerning a problem with the markLiquidationStatus() function in a position. When the debtRatioE18 of a position is greater than 1 and less than 1.03 (unmark), the liquidator can call markLiquidationStatus() to accumulate timeDiscountMultiplierE18 by making pos.startLiqTimestamp == block.timestamp. However, this could result in a liquidated person frontrunning the liquidator, making them lose premium.

The team proposed a mitigation to this problem by allowing markLiquidationStatus() to set the startLiqTimestamp only when debtRatioE18 >= 1.03 (unmark), or allowing the liquidator to set the minimum acceptable discount. The team then reviewed the mitigation and changed the unmark value to ~0.97. This bug report was then fixed.

### Original Finding Content

**Description:**
When the **debtRatioE18** of a position is greater than 1 and less than 1.03 (unmark), the 
liquidator can call `markLiquidationStatus()` to accumulate **timeDiscountMultiplierE18** by 
making **pos.startLiqTimestamp == block.timestamp**. The liquidated person can also call 
markLiquidationStatus() to reset **pos.startLiqTimestamp** to clear 
**timeDiscountMultiplierE18**, which results in that when the debtRatioE18 of a position 
hovers between 1.0 and 1.03, the liquidated person can front run the liquidator to make the 
liquidator lose premium.

Consider the following scenarios:
1. Alice's position has **debtRatioE18** greater than 1.0 and less than 1.03 (unmark).

2. Bob calls `markLiquidationStatus()` to initialize the **startLiqTimestamp** of Alice's position, 
and after some time, **timeDiscountMultiplierE18** accumulates to 50%, Bob calls 
liquidatePosition() to liquidate Alice's position.

3. Alice observes Bob's transaction and frontruns a call to `markLiquidationStatus()` to reset 
**startLiqTimestamp, timeDiscountMultiplierE18** is also reset to 0. 

4. Bob's transaction is executed and the premium paid by Bob may be less than the profit 
received, in the extreme case, if **debtRatioE18 = 1e18**, Bob will not have any profit and will 
pay premium.

**Recommended Mitigation:**
Consider allowing markLiquidationStatus() to set the startLiqTimestamp only when 
debtRatioE18 >= 1.03(unmark), or allowing the liquidator to set the minimum acceptable 
discount.
```solidity
        - if (debtRatioE18 >= ONE_E18 && startLiqTimestamp == 0) {
            + if (debtRatioE18 >= IBasePositionViewer(_positionViewer).unmarkLiqDebtRatioE18() && 
              startLiqTimestamp == 0) {
        // mark liquidatable if the position is unhealthy and is not marked yet
        pos.startLiqTimestamp = block.timestamp.toUint32();
        } else if (
          startLiqTimestamp != 0 &&
              debtRatioE18 < IBasePositionViewer(_positionViewer).unmarkLiqDebtRatioE18()
        ) {
        // unmark liquidatable if the position is already marked and debt ratio falls below "unmark debt ratio"
        pos.startLiqTimestamp = 0;
        } else {
          // revert otherwise
              revert MarkLiquidationStatusFailed();
          }
```

**Team response:**
Fixed

**Mitigation Review:**
The team addressed this issue by changing the unmark value to ~0.97.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

