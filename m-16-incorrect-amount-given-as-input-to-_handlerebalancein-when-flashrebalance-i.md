---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27108
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/101
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/701

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
finders_count: 2
finders:
  - ck
  - Aymen0909
---

## Vulnerability Title

M-16: Incorrect amount given as input to `_handleRebalanceIn` when `flashRebalance` is called

### Overview


This bug report is about the `flashRebalance` function in the LMPDebt.sol smart contract. When the `flashRebalance` function is called, the wrong deposit amount is given to the `_handleRebalanceIn` function as the whole `tokenInBalanceAfter` amount is given as input instead of the delta value `tokenInBalanceAfter - tokenInBalanceBefore`. This can potentially lead to an incorrect rebalance operation and a denial of service (DOS) due to the insufficient amount error. 

The issue occurs in the `flashRebalance` function. The function executes a flashloan in order to receive the tokenIn amount which should be the difference between `tokenInBalanceAfter` (balance of the contract after the flashloan) and `tokenInBalanceBefore` (balance of the contract before the flashloan) : `tokenInBalanceAfter - tokenInBalanceBefore`. But when calling the `_handleRebalanceIn` function, the wrong deposit amount is given as input, as the total balance `tokenInBalanceAfter` is used instead of the received amount `tokenInBalanceAfter - tokenInBalanceBefore`.

Because the `_handleRebalanceIn` function is supposed to deposit the input amount to the destination vault, this error can result in sending a larger amount of funds to DV than what was intended or this error can cause a DOS of the `flashRebalance` function (due to the insufficient amount error when performing the transfer to DV). All of this will make the rebalance operation fail (or not done correctly) which can have a negative impact on the LMPVault.

The code snippet for this bug is available at https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/vault/libs/LMPDebt.sol#L185-L215. The bug was found manually by Aymen0909 and ck. 

The recommendation is to use the correct received tokenIn amount `tokenInBalanceAfter - tokenInBalanceBefore` as input to the `_handleRebalanceIn` function. This will ensure that the correct amount of funds is sent to the destination vault and the rebalance operation will be successful.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/701 

## Found by 
Aymen0909, ck

When `flashRebalance` is called, the wrong deposit amount is given to the `_handleRebalanceIn` function as the whole `tokenInBalanceAfter` amount is given as input instead of the delta value `tokenInBalanceAfter - tokenInBalanceBefore`, this will result in an incorrect rebalance operation and can potentialy lead to a DOS due to the insufficient amount error.

## Vulnerability Detail

The issue occurs in the `flashRebalance` function below :

```solidity
function flashRebalance(
    DestinationInfo storage destInfoOut,
    DestinationInfo storage destInfoIn,
    IERC3156FlashBorrower receiver,
    IStrategy.RebalanceParams memory params,
    FlashRebalanceParams memory flashParams,
    bytes calldata data
) external returns (uint256 idle, uint256 debt) {
    ...

    // Handle increase (shares coming "In", getting underlying from the swapper and trading for new shares)
    if (params.amountIn > 0) {
        IDestinationVault dvIn = IDestinationVault(params.destinationIn);

        // get "before" counts
        uint256 tokenInBalanceBefore = IERC20(params.tokenIn).balanceOf(address(this));

        // Give control back to the solver so they can make use of the "out" assets
        // and get our "in" asset
        bytes32 flashResult = receiver.onFlashLoan(msg.sender, params.tokenIn, params.amountIn, 0, data);

        // We assume the solver will send us the assets
        uint256 tokenInBalanceAfter = IERC20(params.tokenIn).balanceOf(address(this));

        // Make sure the call was successful and verify we have at least the assets we think
        // we were getting
        if (
            flashResult != keccak256("ERC3156FlashBorrower.onFlashLoan")
                || tokenInBalanceAfter < tokenInBalanceBefore + params.amountIn
        ) {
            revert Errors.FlashLoanFailed(params.tokenIn, params.amountIn);
        }

        if (params.tokenIn != address(flashParams.baseAsset)) {
            // @audit should be `tokenInBalanceAfter - tokenInBalanceBefore` given to `_handleRebalanceIn`
            (uint256 debtDecreaseIn, uint256 debtIncreaseIn) =
                _handleRebalanceIn(destInfoIn, dvIn, params.tokenIn, tokenInBalanceAfter);
            idleDebtChange.debtDecrease += debtDecreaseIn;
            idleDebtChange.debtIncrease += debtIncreaseIn;
        } else {
            idleDebtChange.idleIncrease += tokenInBalanceAfter - tokenInBalanceBefore;
        }
    }
    ...
}
```

As we can see from the code above, the function executes a flashloan in order to receive th tokenIn amount which should be the difference between `tokenInBalanceAfter` (balance of the contract after the flashloan) and `tokenInBalanceBefore` (balance of the contract before the flashloan) : `tokenInBalanceAfter - tokenInBalanceBefore`.

But when calling the `_handleRebalanceIn` function the wrong deposit amount is given as input, as the total balance `tokenInBalanceAfter` is used instead of the received amount `tokenInBalanceAfter - tokenInBalanceBefore`.

Because the `_handleRebalanceIn` function is supposed to deposit the input amount to the destination vault, this error can result in sending a larger amount of funds to DV then what was intended or this error can cause a DOS of the `flashRebalance` function (due to the insufficient amount error when performing the transfer to DV), all of this will make the rebalance operation fail (or not done correctely) which can have a negative impact on the LMPVault.

## Impact

See summary

## Code Snippet

https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/vault/libs/LMPDebt.sol#L185-L215

## Tool used

Manual Review

## Recommendation

Use the correct received tokenIn amount `tokenInBalanceAfter - tokenInBalanceBefore` as input to the `_handleRebalanceIn` function :

```solidity
function flashRebalance(
    DestinationInfo storage destInfoOut,
    DestinationInfo storage destInfoIn,
    IERC3156FlashBorrower receiver,
    IStrategy.RebalanceParams memory params,
    FlashRebalanceParams memory flashParams,
    bytes calldata data
) external returns (uint256 idle, uint256 debt) {
    ...

    // Handle increase (shares coming "In", getting underlying from the swapper and trading for new shares)
    if (params.amountIn > 0) {
        IDestinationVault dvIn = IDestinationVault(params.destinationIn);

        // get "before" counts
        uint256 tokenInBalanceBefore = IERC20(params.tokenIn).balanceOf(address(this));

        // Give control back to the solver so they can make use of the "out" assets
        // and get our "in" asset
        bytes32 flashResult = receiver.onFlashLoan(msg.sender, params.tokenIn, params.amountIn, 0, data);

        // We assume the solver will send us the assets
        uint256 tokenInBalanceAfter = IERC20(params.tokenIn).balanceOf(address(this));

        // Make sure the call was successful and verify we have at least the assets we think
        // we were getting
        if (
            flashResult != keccak256("ERC3156FlashBorrower.onFlashLoan")
                || tokenInBalanceAfter < tokenInBalanceBefore + params.amountIn
        ) {
            revert Errors.FlashLoanFailed(params.tokenIn, params.amountIn);
        }

        if (params.tokenIn != address(flashParams.baseAsset)) {
            // @audit Use `tokenInBalanceAfter - tokenInBalanceBefore` as input
            (uint256 debtDecreaseIn, uint256 debtIncreaseIn) =
                _handleRebalanceIn(destInfoIn, dvIn, params.tokenIn, tokenInBalanceAfter - tokenInBalanceBefore);
            idleDebtChange.debtDecrease += debtDecreaseIn;
            idleDebtChange.debtIncrease += debtIncreaseIn;
        } else {
            idleDebtChange.idleIncrease += tokenInBalanceAfter - tokenInBalanceBefore;
        }
    }
    ...
}
```



## Discussion

**sherlock-admin2**

1 comment(s) were left on this issue during the judging contest.

**Trumpero** commented:
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | ck, Aymen0909 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/701
- **Contest**: https://app.sherlock.xyz/audits/contests/101

### Keywords for Search

`vulnerability`

