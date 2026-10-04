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
solodit_id: 38049
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-06-size
source_link: https://code4rena.com/reports/2024-06-size
github_link: https://github.com/code-423n4/2024-06-size-findings/issues/88

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
finders_count: 11
finders:
  - samuraii77
  - inzinko
  - Bob
  - ayden
  - zarkk01
---

## Vulnerability Title

[M-10] `withdraw()` users may can't withdraw `underlyingBorrowToken` properly

### Overview


The report discusses a bug in the code for withdrawing tokens in the Size protocol. The bug occurs when a user tries to withdraw their borrowed tokens, but due to a slight price fluctuation, the system fails to validate the withdrawal. This means that the user may not be able to withdraw their borrowed funds, even though they have already been borrowed and collateralized. The impact of this bug can be high, as it can result in the user not being able to access their funds. The recommended mitigation is to add a condition to the code to prevent this validation from occurring when withdrawing borrowed tokens. The severity of this bug is considered medium, as there are still ways for the user to access their funds and there is no loss of funds. 

### Original Finding Content


We can withdraw `underlyingCollateralToken` and `underlyingBorrowToken` by `withdraw()`:

```solidity
    function withdraw(WithdrawParams calldata params) external payable override(ISize) whenNotPaused {
        state.validateWithdraw(params);
        state.executeWithdraw(params);
@>      state.validateUserIsNotBelowOpeningLimitBorrowCR(msg.sender);
    }

    function executeWithdraw(State storage state, WithdrawParams calldata params) public {
        uint256 amount;
        if (params.token == address(state.data.underlyingBorrowToken)) {
            amount = Math.min(params.amount, state.data.borrowAToken.balanceOf(msg.sender));
            if (amount > 0) {
@>              state.withdrawUnderlyingTokenFromVariablePool(msg.sender, params.to, amount);
            }
        } else {
            amount = Math.min(params.amount, state.data.collateralToken.balanceOf(msg.sender));
            if (amount > 0) {
                state.withdrawUnderlyingCollateralToken(msg.sender, params.to, amount);
            }
        }

        emit Events.Withdraw(params.token, params.to, amount);
    }
```

From the code above we know that whether we take `underlyingCollateralToken` or `underlyingBorrowToken`
will check `validateUserIsNotBelowOpeningLimitBorrowCR()` `==>` `collateralRatio() > openingLimitBorrowCR`.

This makes sense for taking `underlyingCollateralToken`, but not for taking `underlyingBorrowToken`.

1. Taking the `underlyingBorrowToken` does not affect the `collateralRatio`.
2. The user has already borrowed the funds (with interest accrued and collateralized), it is the user's asset, and should be able to be withdrawn at will, even if it may be liquidated.
3. `openingLimitBorrowCR` is still far from being liquidated, and should not restrict the user from withdrawing the borrowed token.

### Impact

If the token is already borrowed, just stored in `Size` and not yet taken, but due to a slight price fluctuation, `validateUserIsNotBelowOpeningLimitBorrowCR()` fails but is still far from being liquidated, the user may not be able to take the borrowed token, resulting in the possibility that the user may not be able to withdraw the borrowed funds.

### Recommended Mitigation

```diff
    function withdraw(WithdrawParams calldata params) external payable override(ISize) whenNotPaused {
        state.validateWithdraw(params);
        state.executeWithdraw(params);
+       if (params.token != address(state.data.underlyingBorrowToken)  {
+             state.validateUserIsNotBelowOpeningLimitBorrowCR(msg.sender);
+       }
    }
```

### Assessed type

Context

**[aviggiano (Size) confirmed and commented](https://github.com/code-423n4/2024-06-size-findings/issues/88#issuecomment-2218092174):**
 > This is a valid bug and the report is good.
> 
> Fixed in https://github.com/SizeCredit/size-solidity/pull/124.

**[samuraii77 (warden) commented](https://github.com/code-423n4/2024-06-size-findings/issues/88#issuecomment-2229365151):**
 > Hi, this issue should be of high severity. The likelihood is very high, imagine a user borrows `$1000` and gives `$1500` as collateral; his collateral ratio is now `1.5e18`. If the price of ETH drops by just 1 cent (or even less), his borrowed funds will be locked. The impact is also high as well.

**[hansfriese (judge) commented](https://github.com/code-423n4/2024-06-size-findings/issues/88#issuecomment-2241487348):**
 > I still believe Medium is appropriate for the following reasons:
> 
> - The user can withdraw the borrowed funds at the time of borrowing using a multicall.
> - The user can still use the borrowed funds to repay their loan.
> - There is no fund loss; the funds are simply locked for a while.

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
| Finders | samuraii77, inzinko, Bob, ayden, zarkk01, bin2chen, elhaj, alix40, ether\_sky, 0xAlix2, 3n0ch |

### Source Links

- **Source**: https://code4rena.com/reports/2024-06-size
- **GitHub**: https://github.com/code-423n4/2024-06-size-findings/issues/88
- **Contest**: https://code4rena.com/reports/2024-06-size

### Keywords for Search

`vulnerability`

