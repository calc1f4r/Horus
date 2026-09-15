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
solodit_id: 45432
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Stardusts-security-review_2024-12-19.md
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

[M-02] An error in the `minOrderSize` check

### Overview


This bug report discusses a medium severity issue in a code function used for buying tokens. The function does not properly check the minimum order size, which can result in a user's transaction being frontrun and not providing the intended slippage protection. The report recommends moving the check for the minimum order size to the end of the function to ensure it is applied after all other conditions.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

```javascript
function _validateBondingCurveBuy(uint256 minOrderSize)
        internal
        returns (uint256 totalCost, uint256 trueOrderSize, uint256 fee, uint256 refund, bool shouldGraduate)
    {
        // Set the total cost to the amount of ETH sent
        totalCost = msg.value;

        // Calculate the fee
        fee = (totalCost * feeBps) / 10000;

        // Calculate the amount of ETH remaining for the order
        uint256 remainingEth = totalCost - fee;

        // Get quote for the number of tokens that can be bought with the amount of ETH remaining
        trueOrderSize = getOutTokenAmount(remainingEth);

        // Ensure the order size is greater than the minimum order size
@>        if (trueOrderSize < minOrderSize) revert SlippageTooHigh();

        // Calculate the maximum number of tokens that can be bought on the bonding curve
        uint256 maxRemainingTokens = (X0 - X1) - totalSupply();

        // Start the market if the order size equals the number of remaining tokens
        if (trueOrderSize == maxRemainingTokens) {
            shouldGraduate = true;
        }

        // If the order size is greater than the maximum number of remaining tokens:
        if (trueOrderSize > maxRemainingTokens) {
            // Reset the order size to the number of remaining tokens
@>            trueOrderSize = maxRemainingTokens;

            // Calculate the amount of ETH needed to buy the true order
            uint256 ethNeeded = Y1 - virtualEthLiquidity;

            // Recalculate the fee with the updated order size
            fee = (ethNeeded * feeBps) / 10000;

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

It can be observed that under the condition trueOrderSize > maxRemainingTokens, trueOrderSize is reassigned, but there is no check on minOrderSize.
This can lead to situations where a transaction is frontrun, causing the user’s minOrderSize to not provide the intended slippage protection.

## Recommendations

Moving the check if (trueOrderSize < minOrderSize) revert SlippageTooHigh(); to the end of the \_validateBondingCurveBuy() function to ensure that the minOrderSize check is applied after all other conditions

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

