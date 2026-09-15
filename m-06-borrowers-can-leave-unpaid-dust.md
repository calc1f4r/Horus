---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36486
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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

[M-06] Borrowers can leave unpaid dust

### Overview


This bug report describes an issue with the `withdrawERC20`, `withdrawERC721`, `borrow` and `liquidate` functions in the `MarginTrading` contract. These functions calculate the portfolio ratio to determine if an account is undercollateralized by dividing the value of assets held by the account by the value of the debt. However, the value of the debt is calculated by converting the due amount to the base token, which can sometimes round down to zero for small amounts of debt. This allows users to withdraw their collateral without repaying the remaining debt, resulting in a loss for the platform. The report suggests checking the pending debt in the debt token before allowing users to withdraw all their collateral as a possible solution. 

### Original Finding Content

**Severity**

**Impact:** Low

**Likelihood:** High

**Description**

`withdrawERC20`, `withdrawERC721`, `borrow` and `liquidate` functions in `MarginTrading` contract calculate the portfolio ratio to check if the account is undercollateralized. This ratio is calculated by dividing the value of the assets held by the account by the value of the debt, both denominated in the base currency (USDC).

```solidity
File: MarginTrading.sol

196:     function _calculatePortfolioRatio(uint marginAccountValue, uint debtWithAccruedInterest) private pure returns (uint marginAccountRatio) {
197:         if (debtWithAccruedInterest == 0) {
198:             return 0;
199:         }
200:         require(marginAccountValue*COEFFICIENT_DECUMALS > debtWithAccruedInterest, "Margin Account value should be greater than debt with accrued interest");
201:         marginAccountRatio = marginAccountValue*COEFFICIENT_DECUMALS/debtWithAccruedInterest;
202:     }
```

For its part, `debtWithAccruedInterest` is calculated by iterating over the different tokens that the account has borrowed, converting the due amount to the base token and summing the resulting values.

```solidity
File: ModularSwapRouter.sol

82:     function calculateTotalPositionValue(ERC20PositionInfo[] memory erc20Params, ERC721PositionInfo[] memory erc721Params)
83:         external
84:         onlyRole(MARGIN_TRADING_ROLE)
85:         returns (uint totalValue)
86:     {
87:         address marginTradingBaseToken = marginTrading.BASE_TOKEN();
88:         for (uint i; i < erc20Params.length; i++) {
89:             address moduleAddress = tokenInToTokenOutToExchange[erc20Params[i].tokenIn][erc20Params[i].tokenOut];
90:             if (
91:                 erc20Params[i].tokenIn == marginTradingBaseToken &&
92:                 erc20Params[i].tokenOut == marginTradingBaseToken
93:             ) {
94:                 totalValue += erc20Params[i].value;
95:             } else if (moduleAddress != address(0)) {
96:   @>            totalValue += IPositionManagerERC20(moduleAddress).getInputPositionValue(erc20Params[i].value);
97:             }
98:         }
```

`getInputPositionValue` returns the value of the debt for a given token, expressed in the base token. For small amounts of debt tokens, this conversion can round down to zero, effectively valuing the debt at zero, so the user can withdraw the collateral without repaying the remaining debt.

While this amount is small, it can keep accruing over time by different users and tokens.

**Proof of concept**

```solidity
function test_borrowerLeavesUnpaidDust() public {
    uint256 collateralAmount = 10_000e6;
    uint256 borrowAmount = 1e18;
    uint256 dustAmount = 249_999_999;

    provideInitialLiquidity();

    vm.startPrank(alice);
    marginTrading.provideERC20(marginAccountID[alice], address(USDC), collateralAmount);

    // Alice borrows 1 WETH
    marginTrading.borrow(marginAccountID[alice], address(WETH), borrowAmount);

    // Alice repays debt and interest
    marginTrading.repay(marginAccountID[alice], address(WETH), borrowAmount - dustAmount);

    // Alice withdraws collateral and dust
    marginTrading.withdrawERC20(marginAccountID[alice], address(USDC), collateralAmount);
    marginTrading.withdrawERC20(marginAccountID[alice], address(WETH), dustAmount);
}
```

**Recommendations**

A possible solution is checking that the pending debt valued in the debt token is also zero before allowing the user to withdraw all the collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

