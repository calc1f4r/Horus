---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6210
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-papr-contest
source_link: https://code4rena.com/reports/2022-12-backed
github_link: https://github.com/code-423n4/2022-12-backed-findings/issues/187

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - evan
  - HollaDieWaldfee
  - bin2chen
  - 0x52
---

## Vulnerability Title

[M-05] PaprController.buyAndReduceDebt: msg.sender can lose paper by paying the debt twice

### Overview


This bug report is about the `PaprController.buyAndReduceDebt` function in the codebase of the project "with-backed/papr". This function should allow a user to swap some amount of the underlying token for papr token and use this amount of papr token to repay debt for the address in the `account` parameter. However, due to a mistake in the code, the swapped papr token are sent to the `account` address instead of the `msg.sender` address and the papr token are burnt from `msg.sender`. This leads to the `msg.sender` paying double the amount he wants to, once by swapping his underlying tokens for papr and the second time because his papr token are burnt. 

The vulnerability is demonstrated by calling the `UniswapHelpers.swap` function within the `PaprController.buyAndReduceDebt` function, which has the second parameter `account` as the recipient of the swap and the last parameter `msg.sender` as the address paying the input amount for the swap. 

To mitigate this issue, the swapped papr token should be sent to the `msg.sender` instead of `account` such that they can then be burnt from `msg.sender`. This requires a single line change in the code, from `account` to `msg.sender`.

### Original Finding Content


<https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L208-L232>

<https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/libraries/UniswapHelpers.sol#L31-L61>

### Impact

The `PaprController.buyAndReduceDebt` function (<https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L208-L232>) should work like this:

1.  `msg.sender` swaps some amount of the underlying token for papr token
2.  This amount of papr token is used to repay debt for the address in the `account` parameter

`msg.sender` and `account` can be different addresses such that one can repay anyone's debt.

However there is a mistake in the function which leads to this behavior:

1.  `msg.sender` swaps some amount of the underlying token for papr token
2.  The papr token is sent to the `account` address
3.  The papr token is burnt from the `msg.sender`
4.  The amount of papr token burnt from the `msg.sender` is used to pay back the debt of the `account` address

The issue is that the swapped papr token are sent to `account` but the papr token are burnt from `msg.sender`.

In the best scenario when calling this function, the msg.sender does not have enough papr token to burn so the function call reverts.

In the scenario that is worse, the `msg.sender` has enough papr token to be burnt.

So the `account` address receives the swapped papr token and the debt of `account` is paid as well by the `msg.sender`.

Thereby the `msg.sender` pays double the amount he wants to.

Once by swapping his underlying tokens for papr.

The second time because his papr token are burnt.

### Proof of Concept

The `PaprController.buyAndReduceDebt` function (<https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L208-L232>) calls `UniswapHelpers.swap` (<https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/libraries/UniswapHelpers.sol#L31-L61>):

```solidity
(uint256 amountOut, uint256 amountIn) = UniswapHelpers.swap(
    pool,
    account,
    token0IsUnderlying,
    params.amount,
    params.minOut,
    params.sqrtPriceLimitX96,
    abi.encode(msg.sender)
);
```

The second parameter which has the value `account` is the recipient of the swap.

The last parameter which is `msg.sender` is the address paying the input amount for the swap.

So the `msg.sender` pays some amount of underlying and the papr that the underlying is swapped for is sent to the `account`.

But then the debt of `account` is reduced by burning papr token from `msg.sender`:

```solidity
_reduceDebt({account: account, asset: collateralAsset, burnFrom: msg.sender, amount: amountOut});
```

However the papr token from the swap were received by `account`. So the `msg.sender` pays twice and `account` receives twice.

### Tools Used

VS Code

### Recommended Mitigation Steps

The swapped papr token should be sent to the `msg.sender` instead of `account` such that they can then be burnt from `msg.sender`.

In order to achieve this, a single line in `PaprController.buyAndReduceDebt` must be changed:

```solidity
         (uint256 amountOut, uint256 amountIn) = UniswapHelpers.swap(
             pool,
-            account,
+            msg.sender,
             token0IsUnderlying,
             params.amount,
             params.minOut,
             params.sqrtPriceLimitX96,
            abi.encode(msg.sender)
        );
```
**[wilsoncusack (Backed) confirmed](https://github.com/code-423n4/2022-12-backed-findings/issues/187)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | evan, HollaDieWaldfee, bin2chen, 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-backed
- **GitHub**: https://github.com/code-423n4/2022-12-backed-findings/issues/187
- **Contest**: https://code4rena.com/contests/2022-12-papr-contest

### Keywords for Search

`Business Logic`

