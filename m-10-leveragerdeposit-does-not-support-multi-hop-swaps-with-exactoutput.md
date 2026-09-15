---
# Core Classification
protocol: Yieldoor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55048
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/791
source_link: none
github_link: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/577

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
finders_count: 13
finders:
  - elolpuer
  - JohnTPark24
  - bladeee
  - yotov721
  - 0x73696d616f
---

## Vulnerability Title

M-10: `Leverager::deposit`, does not support multi-hop swaps with `exactOutput`

### Overview


This bug report is about an issue with the `Leverager::deposit` function in the Yieldoor smart contract. The function is supposed to support multi-hop swaps with `exactOutput`, but it does not work as intended. This means that when a user tries to deposit into the leverager, if the borrowed token is not `token0` or `token1`, the function cannot perform the necessary swaps to receive the borrowed token. This is due to an infinite loop in the code that is supposed to validate the `denomination` token. This bug only affects users who are trying to do multi-hop swaps. The impact of this bug is that the `Leverager::deposit` function does not work as intended. A possible solution to this issue is to overwrite the path when calling `skipToken` in order to fix the infinite loop.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/577 

## Found by 
000000, 0x73696d616f, AlexCzm, Foundation, JohnTPark24, Pelz, Uddercover, bladeee, elolpuer, future2\_22, iamnmt, roccomania, yotov721

### Summary

When depositing into the leverager, if the borrowed token is not `token0` or `token1`, the function has to perform an `exactOutput` swap, to receive the borrowed `token0`/`token1`.

```solidity
function openLeveragedPosition(LeverageParams calldata lp) external nonReentrant returns (uint256 _id) {
        ...
        {
            // we first borrow the maximum amount the user is willing to borrow. Any unused within the swaps is later repaid.
            ILendingPool(lendingPool).borrow(lp.denomination, lp.maxBorrowAmount);

            IMainnetRouter.ExactOutputParams memory swapParams;

            if (a0 > lp.amount0In && up.token0 != lp.denomination) {
                swapParams = abi.decode(lp.swapParams1, (IMainnetRouter.ExactOutputParams));

                address tokenIn = _getTokenIn(swapParams.path);
                require(tokenIn == lp.denomination, "token should be denomination");

                IERC20(tokenIn).forceApprove(swapRouter, swapParams.amountInMaximum);

                swapParams.amountOut = a0 - lp.amount0In;
                IMainnetRouter(swapRouter).exactOutput(swapParams);
                IERC20(tokenIn).forceApprove(swapRouter, 0);
            }

            if (a1 > lp.amount1In && up.token1 != lp.denomination) {
                swapParams = abi.decode(lp.swapParams2, (IMainnetRouter.ExactOutputParams));
                address tokenIn = _getTokenIn(swapParams.path);
                require(tokenIn == lp.denomination, "token should be denomination 2 ");
                IERC20(tokenIn).forceApprove(swapRouter, swapParams.amountInMaximum);

                swapParams.amountOut = a1 - lp.amount1In;
                IMainnetRouter(swapRouter).exactOutput(swapParams);
                IERC20(tokenIn).forceApprove(swapRouter, 0);
            }
        }

        if (delta0 > 0) ILendingPool(lendingPool).pushFunds(up.token0, delta0);
        if (delta1 > 0) ILendingPool(lendingPool).pushFunds(up.token1, delta1);
        ...
    }
```


In order to validate that the `denomination` token  is the `tokenIn`, we call the internal `_getTokenIn`.

```solidity
    function _getTokenIn(bytes memory path) internal pure returns (address) {
        while (path.hasMultiplePools()) {
            path.skipToken();
        }

        (, address tokenIn,) = path.decodeFirstPool();
        return tokenIn;
    }
```

The function intends to skip, the pools until only the initial one is available, to get the tokenIn.

However, `path` is never changed which causes an infinite loop when the user is trying to do a multi-hop swaps.



### Root Cause

When, [skipping tokens](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Leverager.sol#L568), path is never changed, causing an infinite loop, for users trying to do multihop swaps.

### Internal Pre-conditions

None

### External Pre-conditions

1. User tries to do a multi-hop swaps

### Attack Path

None

### Impact

The `Leverager::deposit` function fails to support multi-hop swaps as intended

### PoC

_No response_

### Mitigation

Consider overwriting the path when calling `skipToken`

```diff
 while (path.hasMultiplePools()) {
-          path.skipToken();
+         path  = path.skipToken();
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Yieldoor |
| Report Date | N/A |
| Finders | elolpuer, JohnTPark24, bladeee, yotov721, 0x73696d616f, 000000, Foundation, Pelz, roccomania, AlexCzm, future2\_22, Uddercover, iamnmt |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/577
- **Contest**: https://app.sherlock.xyz/audits/contests/791

### Keywords for Search

`vulnerability`

