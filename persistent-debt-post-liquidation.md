---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53695
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Persistent Debt Post Liquidation

### Overview


The bug report describes an issue where the liquidation process in the SDUtilityPool is not properly handling pending and total interests. This can lead to incorrect debt calculations and potential reverts in other functions. The issue can be exploited by utilizing SD, allowing fees to accrue, and then attempting to repay a zero amount before initiating a liquidation call. The recommended solution is to update the liquidation logic to call `_repay()` instead of updating the utilizer's `utilizeIndex`. This issue has been resolved in a recent commit.

### Original Finding Content

## Description

Pending and total interests are not correctly addressed in the liquidation logic. In `SDUtilityPool.liquidationCall()`, the liquidator pays off all of the utilizer’s interest. To reset the utilizer’s tracked total interest back to 0, their `utilizeIndex` is updated to the global `utilizeIndex` value.

```plaintext
utilizerData[account].utilizeIndex = utilizeIndex
```

However, if the utilizer has updated their `UtilizerStruct` by calling `_utilize()` or `_repay()` after their initial utilization, then updating the utilizer’s `utilizeIndex` does not reset the utilizer’s tracked total interest back to 0. This is because `_utilize()` and `_repay()` compound the utilizer’s interest by adding any pending interest back to their tracked principal amount and updating their `utilizeIndex`.

### In `_utilize()`:

```plaintext
uint256 accountUtilizedPrev = _utilizerBalanceStoredInternal(utilizer);
utilizerData[utilizer].principal = accountUtilizedPrev + utilizeAmount;
utilizerData[utilizer].utilizeIndex = utilizeIndex;
totalUtilizedSD += utilizeAmount;
```

### In `_repay()`:

```plaintext
uint256 feeAccrued = accountUtilizedPrev - ISDCollateral(staderConfig.getSDCollateral()).operatorUtilizedSDBalance(utilizer);
if (!staderConfig.onlyStaderContract(msg.sender, staderConfig.SD_COLLATERAL())) {
    if (repayAmountFinal > feeAccrued) {
        ISDCollateral(staderConfig.getSDCollateral()).reduceUtilizedSDPosition(utilizer, repayAmountFinal - feeAccrued);
    }
}
feePaid = Math.min(repayAmountFinal, feeAccrued);
utilizerData[utilizer].principal = accountUtilizedPrev - repayAmountFinal;
utilizerData[utilizer].utilizeIndex = utilizeIndex;
```

### This can cause several issues:

1. During liquidation call, the liquidator pays for the utilizer’s entire `totalInterestSD`, but not all or even none of the utilizer’s debt is cleared.
2. Since the liquidation process does not adequately address the total interest due, the `OperatorRewardsCollector.claimFor()` function can potentially revert if:
   - (a) the utilizer has no remaining active keys and needs to withdraw their utilized SD balance. The utilizer will not have enough SD balance and revert on line [132] of `SDCollateral.withdrawOnBehalf()`.
   - (b) the operator’s health factor falls below `1e18`. An underflow issue on line [71] of `OperatorRewardsCollector.withdrawableInEth()` will cause the call to revert.

### The issue can be exploited as follows:

1. **Set Up**: Initialize variables and deposit amounts for the liquidation scenario.
2. **Operator Action**: The operator (Bob) utilizes SD from the SDUtilityPool, leading to the accrual of fees.
3. **Interest Accrual**: Allow significant fees to accrue over time, simulating long-term use of the pool.
4. **Repay Zero Amount**: Bob attempts to repay a zero amount, which updates his `utilizeIndex` but does not affect his total interest due.
5. **Liquidation Call**: Alice initiates a liquidation call against Bob.
6. **Post-Liquidation Check**: Despite the liquidation process, Bob’s total interest remains unchanged, demonstrating that the liquidation did not clear Bob’s debt.

## Recommendations

Ensure that both pending and total interests are fully addressed in the liquidation logic of `SDUtilityPool` by calling `_repay()` to handle the clearing of debt instead of updating the utilizer’s `utilizeIndex`. This change will ensure the operator’s financial obligations are completely resolved post-liquidation, thereby restoring the health of their position.

## Resolution

`liquidationCall()` was modified to call `repay()`. `OperatorRewardsCollector.withdrawableInEth()` now returns 0 if there isn’t enough collateral to cover total SD interest and open liquidations. This issue has been addressed in commit `21ba418`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/stader/sd-pool/review.pdf

### Keywords for Search

`vulnerability`

