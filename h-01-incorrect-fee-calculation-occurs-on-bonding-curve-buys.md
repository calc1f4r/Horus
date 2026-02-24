---
# Core Classification
protocol: Stardusts_2024-12-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45430
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Stardusts-security-review_2024-12-19.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Incorrect fee calculation occurs on bonding curve buys

### Overview


This bug report is about a medium severity issue that has a high likelihood of occurring. The problem occurs when users try to buy using a bonding curve and the amount they want to buy is more than the maximum remaining tokens. In this case, the fee is calculated based on the total cost instead of the ETH needed to make the purchase. This results in an underestimation of the fee. The recommendation is to change the fee calculation to be more accurate in this scenario.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When users perform bonding curve buy and the `trueOrderSize` is greater than `maxRemainingTokens`, it will calculate `fee` based on `ethNeeded`.

```solidity
    function _validateBondingCurveBuy(uint256 minOrderSize)
        internal
        returns (uint256 totalCost, uint256 trueOrderSize, uint256 fee, uint256 refund, bool shouldGraduate)
    {
        // Set the total cost to the amount of ETH sent
        totalCost = msg.value;

        // Calculate the fee
>>>     fee = (totalCost * feeBps) / 10000;

        // Calculate the amount of ETH remaining for the order
        uint256 remainingEth = totalCost - fee;

        // ...

        // If the order size is greater than the maximum number of remaining tokens:
        if (trueOrderSize > maxRemainingTokens) {
            // Reset the order size to the number of remaining tokens
            trueOrderSize = maxRemainingTokens;

            // Calculate the amount of ETH needed to buy the true order
            uint256 ethNeeded = Y1 - virtualEthLiquidity;

            // Recalculate the fee with the updated order size
>>>         fee = (ethNeeded * feeBps) / 10000;

            // Recalculate the total cost with the updated order size and fee
            totalCost = ethNeeded + fee;

            // Refund any excess ETH
            if (msg.value > totalCost) {
                refund = msg.value - totalCost;
            }

            shouldGraduate = true;
        }

    }
```

It can be observed that when `trueOrderSize` is greater than `maxRemainingTokens`, the `fee` is based on `totalCost`, not the ETH needed to buy. This leads to an underestimation of the fee when `trueOrderSize` exceeds `maxRemainingTokens`.

## Recommendations

Change the fee calculation as follows :

```diff
        if (trueOrderSize > maxRemainingTokens) {
            // Reset the order size to the number of remaining tokens
            trueOrderSize = maxRemainingTokens;

            // Calculate the amount of ETH needed to buy the true order
            uint256 ethNeeded = Y1 - virtualEthLiquidity;

            // Recalculate the fee with the updated order size
+            totalCost = (10000 * ethNeeded ) / (10000 - feeBps);
-            fee = (ethNeeded * feeBps) / 10000;
+            fee = totalCost - ethNeeded;

            // Recalculate the total cost with the updated order size and fee
-            totalCost = ethNeeded + fee;

            // Refund any excess ETH
            if (msg.value > totalCost) {
                refund = msg.value - totalCost;
            }

            shouldGraduate = true;
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Stardusts_2024-12-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Stardusts-security-review_2024-12-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

