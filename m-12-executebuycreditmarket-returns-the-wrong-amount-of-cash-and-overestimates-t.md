---
# Core Classification
protocol: Size
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38051
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-06-size
source_link: https://code4rena.com/reports/2024-06-size
github_link: https://github.com/code-423n4/2024-06-size-findings/issues/15

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
finders_count: 10
finders:
  - samuraii77
  - said
  - inzinko
  - zhaojohnson
  - KupiaSec
---

## Vulnerability Title

[M-12] `executeBuyCreditMarket` returns the wrong amount of cash and overestimates the amount that needs to be checked in the variable pool

### Overview


This bug report discusses an issue with the `executeBuyCreditMarket` function in the `BuyCreditMarket.sol` contract. When this function is called, it will return the cash amount without deducting the fee, resulting in an overestimation of the value that needs to be validated by `validateVariablePoolHasEnoughLiquidity`. This means that the function could unnecessarily revert and cause issues. The recommended mitigation is to update the returned `cashAmountIn` to `cashAmountIn - fees` at the end of the function. This is considered a medium-severity issue, as while the likelihood of it causing problems is low, it could still potentially cause issues. The bug has been confirmed and fixed by the developers.

### Original Finding Content


When `executeBuyCreditMarket` is called and returns the cash amount, it will return the cash amount without deducting the fee. This results in overestimating the value that needs to be validated by `validateVariablePoolHasEnoughLiquidity`.

### Proof of Concept

When `executeBuyCreditMarket` is called, it will transfer `cashAmountIn - fees` to the borrower. This means the amount that needs to be available for withdrawal in the variable pool is `cashAmountIn - fees`.

<https://github.com/code-423n4/2024-06-size/blob/main/src/libraries/actions/BuyCreditMarket.sol#L195>

```solidity
    function executeBuyCreditMarket(State storage state, BuyCreditMarketParams memory params)
        external
>>>     returns (uint256 cashAmountIn)
    {
        // ...

        uint256 creditAmountOut;
        uint256 fees;

        if (params.exactAmountIn) {
            cashAmountIn = params.amount;
            (creditAmountOut, fees) = state.getCreditAmountOut({
                cashAmountIn: cashAmountIn,
                maxCashAmountIn: params.creditPositionId == RESERVED_ID
                    ? cashAmountIn
                    : Math.mulDivUp(creditPosition.credit, PERCENT, PERCENT + ratePerTenor),
                maxCredit: params.creditPositionId == RESERVED_ID
                    ? Math.mulDivDown(cashAmountIn, PERCENT + ratePerTenor, PERCENT)
                    : creditPosition.credit,
                ratePerTenor: ratePerTenor,
                tenor: tenor
            });
        } else {
            creditAmountOut = params.amount;
            (cashAmountIn, fees) = state.getCashAmountIn({
                creditAmountOut: creditAmountOut,
                maxCredit: params.creditPositionId == RESERVED_ID ? creditAmountOut : creditPosition.credit,
                ratePerTenor: ratePerTenor,
                tenor: tenor
            });
        }

       // ...

>>>     state.data.borrowAToken.transferFrom(msg.sender, borrower, cashAmountIn - fees);
        state.data.borrowAToken.transferFrom(msg.sender, state.feeConfig.feeRecipient, fees);
    }
```

However, `executeBuyCreditMarket` will return `cashAmountIn`, and provide it to `validateVariablePoolHasEnoughLiquidity` and check if the variable pool have `cashAmountIn` amount of token.

<https://github.com/code-423n4/2024-06-size/blob/main/src/Size.sol#L178-L185>

```solidity
    function buyCreditMarket(BuyCreditMarketParams calldata params) external payable override(ISize) whenNotPaused {
        state.validateBuyCreditMarket(params);
>>>     uint256 amount = state.executeBuyCreditMarket(params);
        if (params.creditPositionId == RESERVED_ID) {
            state.validateUserIsNotBelowOpeningLimitBorrowCR(params.borrower);
        }
>>>     state.validateVariablePoolHasEnoughLiquidity(amount);
    }
```

<https://github.com/code-423n4/2024-06-size/blob/main/src/libraries/CapsLibrary.sol#L67-L72>

```solidity
    function validateVariablePoolHasEnoughLiquidity(State storage state, uint256 amount) public view {
        uint256 liquidity = state.data.underlyingBorrowToken.balanceOf(address(state.data.variablePool));
        if (liquidity < amount) {
            revert Errors.NOT_ENOUGH_BORROW_ATOKEN_LIQUIDITY(liquidity, amount);
        }
    }
```

This will overestimate the amount of liquidity that needs to be available in the variable pool and could cause the call to unnecessarily revert.

### Recommended Mitigation Steps

Update the returned `cashAmountIn` to `cashAmountIn - fees` at the end of `executeBuyCreditMarket`.

```diff
    function executeBuyCreditMarket(State storage state, BuyCreditMarketParams memory params)
        external
>>>     returns (uint256 cashAmountIn)
    {
        // ...

        uint256 creditAmountOut;
        uint256 fees;

        if (params.exactAmountIn) {
            cashAmountIn = params.amount;
            (creditAmountOut, fees) = state.getCreditAmountOut({
                cashAmountIn: cashAmountIn,
                maxCashAmountIn: params.creditPositionId == RESERVED_ID
                    ? cashAmountIn
                    : Math.mulDivUp(creditPosition.credit, PERCENT, PERCENT + ratePerTenor),
                maxCredit: params.creditPositionId == RESERVED_ID
                    ? Math.mulDivDown(cashAmountIn, PERCENT + ratePerTenor, PERCENT)
                    : creditPosition.credit,
                ratePerTenor: ratePerTenor,
                tenor: tenor
            });
        } else {
            creditAmountOut = params.amount;
            (cashAmountIn, fees) = state.getCashAmountIn({
                creditAmountOut: creditAmountOut,
                maxCredit: params.creditPositionId == RESERVED_ID ? creditAmountOut : creditPosition.credit,
                ratePerTenor: ratePerTenor,
                tenor: tenor
            });
        }

       // ...

        state.data.borrowAToken.transferFrom(msg.sender, borrower, cashAmountIn - fees);
        state.data.borrowAToken.transferFrom(msg.sender, state.feeConfig.feeRecipient, fees);
+       cashAmountIn = cashAmountIn - fees;     
    }
```

### Assessed type

Invalid Validation

**[aviggiano (Size) confirmed and commented](https://github.com/code-423n4/2024-06-size-findings/issues/15#issuecomment-2209109217):**
 > Fixed in https://github.com/SizeCredit/size-solidity/pull/133.
>
 > This is arguably a `Low`-severity issue since the likelihood is Low
> 
> - Aave being illiquid.
> - Order reverting by a fee amount, which is of the order of a percentage point on the dollar.
> 
> Impact is Low (order reverting), but maybe a smaller order could succeed.

**[hansfriese (judge) commented](https://github.com/code-423n4/2024-06-size-findings/issues/15#issuecomment-2223061997):**
 > After consideration, keeping it as a valid Medium to remain consistent with [#152](https://github.com/code-423n4/2024-06-size-findings/issues/152).

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-06-size-findings/issues/15).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Size |
| Report Date | N/A |
| Finders | samuraii77, said, inzinko, zhaojohnson, KupiaSec, trachev, alix40, ether\_sky, Honour, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2024-06-size
- **GitHub**: https://github.com/code-423n4/2024-06-size-findings/issues/15
- **Contest**: https://code4rena.com/reports/2024-06-size

### Keywords for Search

`vulnerability`

