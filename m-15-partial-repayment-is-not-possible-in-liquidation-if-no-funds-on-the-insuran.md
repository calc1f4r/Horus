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
solodit_id: 36495
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

[M-15] Partial repayment is not possible in liquidation if no funds on the insurance pool

### Overview


This bug report discusses a problem with the liquidation process in a financial protocol. When an account's debt is being cleared, if there are not enough funds in the insurance pool to cover the full debt, the transaction fails and none of the debt is repaid. This is because the collateral for the account is locked in the contract and there is no incentive for the account owner to partially repay the debt. The report suggests two options to address this issue - allowing partial repayment and skipping the clearing of debt for the liquidity pool where the full debt cannot be repaid. The report also includes code changes that can be made to implement these options.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

At the end of the liquidation process, all debts of the account being liquidated are cleared. This is done by repaying the debt in each liquidity pool with the account's funds. If the account is underwater, the remaining funds required to repay the debt are taken from the insurance pool.

If the insurance pool does not have enough funds to cover the debt, none of the debt is repaid, and the account collateral can only be used to repay the debt partially if the account's owner calls the `repay` function. However, there is no incentive for the account owner to do so, as the collateral is locked in the contract.

**Proof of concept**

- Account owes 100 WETH (worth 300,000 USDC) and 10 WBTC (worth 800,000 USDC).
- Account has 500,000 USDC in her account.
- When account is tried to be liquidated, debt is cleared from each of the liquidity pools.
- In the first iteration 300,000 USDC are taken from the account to repay the WETH debt.
- In the second iteration, 200,000 USDC are taken from the account to repay the WBTC debt. That covers 2.5 WBTC, so the remaining 7.5 WBTC have to be transferred from the insurance pool.
- The insurance pool only has 5 WBTC, so the transaction reverts and none of the debt is repaid.

**Recommendations**

One option allowing partial repayment of debts if there are not enough funds in the insurance pool to cover the full debt. In this case, bad debt will be absorbed by the protocol.

```diff
    if (amountInUSDC > userUSDCbalance) {
        uint amountOut = modularSwapRouter.swapInput(baseToken, availableTokenToLiquidityPool[i], userUSDCbalance, 0);
        erc20ByContract[marginAccountID][baseToken] -= userUSDCbalance;
+       uint256 insurancePoolBalance = IERC20(availableTokenToLiquidityPool[i]).balanceOf(insurancePool);
+       if (insurancePoolBalance < poolDebt - amountOut) {
+           poolDebt = insurancePoolBalance + amountOut;
+       }
        IERC20(availableTokenToLiquidityPool[i]).transferFrom(insurancePool, address(this), poolDebt-amountOut);
    } else {
        uint amountIn = modularSwapRouter.swapOutput(baseToken, availableTokenToLiquidityPool[i], poolDebt);
        erc20ByContract[marginAccountID][baseToken] -= amountIn;
    }
    ILiquidityPool(liquidityPoolAddress).repay(marginAccountID, poolDebt);
```

Another option is to skip the clearing of the debt just for the liquidity pool where the full debt cannot be repaid.

```diff
    if (amountInUSDC > userUSDCbalance) {
+       uint amountOut = calculateAmountOutERC20(baseToken, availableTokenToLiquidityPool[i], userUSDCbalance);
+       uint256 insurancePoolBalance = IERC20(availableTokenToLiquidityPool[i]).balanceOf(insurancePool);
+       if (insurancePoolBalance < poolDebt - amountOut) {
+           continue;
+       }
        modularSwapRouter.swapInput(baseToken, availableTokenToLiquidityPool[i], userUSDCbalance, 0);
```

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

