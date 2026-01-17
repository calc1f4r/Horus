---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34822
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
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
  - Dacian
---

## Vulnerability Title

`TradingAccount::withdrawMarginUsd` transfers an incorrectly larger amount of margin collateral for tokens with less than 18 decimals

### Overview


This bug report discusses an issue with the `withdrawMarginUsd` function in the `TradingAccount` contract. The function does not properly scale down the transferred amount of collateral tokens with less than 18 decimal places, leading to a potential loss of funds for users. The recommended solution is to scale down the amount before transferring it. The bug has been fixed in the Zaros codebase and verified by Cyfrin.

### Original Finding Content

**Description:** The `UD60x18` values are [scaled up to 18 decimal places](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/MarginCollateralConfiguration.sol#L46-L50) for collateral tokens with less than 18 decimals places. But when `TradingAccount::withdrawMarginUsd` transfers tokens to the recipient it doesn't scale the transferred amount back down to the collateral token's native decimal value:

```solidity
function withdrawMarginUsd(
    Data storage self,
    address collateralType,
    UD60x18 marginCollateralPriceUsdX18,
    UD60x18 amountUsdX18,
    address recipient
)
    internal
    returns (UD60x18 withdrawnMarginUsdX18, bool isMissingMargin)
{
    UD60x18 marginCollateralBalanceX18 = getMarginCollateralBalance(self, collateralType);
    UD60x18 requiredMarginInCollateralX18 = amountUsdX18.div(marginCollateralPriceUsdX18);
    if (marginCollateralBalanceX18.gte(requiredMarginInCollateralX18)) {
        withdraw(self, collateralType, requiredMarginInCollateralX18);

        withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(amountUsdX18);

        // @audit wrong amount for collateral tokens with less than 18 decimals
        // needs to be scaled down to collateral token's native precision
        IERC20(collateralType).safeTransfer(recipient, requiredMarginInCollateralX18.intoUint256());

        isMissingMargin = false;
        return (withdrawnMarginUsdX18, isMissingMargin);
    } else {
        UD60x18 marginToWithdrawUsdX18 = marginCollateralPriceUsdX18.mul(marginCollateralBalanceX18);
        withdraw(self, collateralType, marginCollateralBalanceX18);
        withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(marginToWithdrawUsdX18);

        // @audit wrong amount for collateral tokens with less than 18 decimals
        // needs to be scaled down to collateral token's native precision
        IERC20(collateralType).safeTransfer(recipient, marginCollateralBalanceX18.intoUint256());

        isMissingMargin = true;
        return (withdrawnMarginUsdX18, isMissingMargin);
    }
}
```

Here is a possible scenario.
- A user deposits 10K USDC(has 6 decimals) to his trading account. Then his margin collateral balance will be `10000 * 10^(18 - 6) = 10^16`.
- During a liquidation/settlement, `withdrawMarginUsd` is called with `requiredMarginInCollateralX18 = 1e4` which means `10^-8 USDC`.
- But due to the incorrect decimal conversion logic, the function transfers the whole collateral(10K USDC) but still has `10^16 - 10^4` collateral balance.

**Impact:** Margin collateral balances become corrupt allowing users to withdraw more collateral than they should leading to loss of funds for other users since they won't be able to withdraw.

**Recommended Mitigation:** `withdrawMarginUsd` should scale the amount down to the collateral token's native precision before calling `safeTransfer`.

**Zaros:** Fixed in commit [1ac2acc](https://github.com/zaros-labs/zaros-core/commit/1ac2acc179830c08069b3e5856b9439867a06d50#diff-f09472a5f9e6d5545d840c0760cb5606febbfe8a60fa8b7fc6e7cda8735ce357R378-R396).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

