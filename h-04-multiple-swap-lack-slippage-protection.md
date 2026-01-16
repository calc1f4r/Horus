---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33663
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-bakerfi
source_link: https://code4rena.com/reports/2024-05-bakerfi
github_link: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/32

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
finders_count: 5
finders:
  - 0xStalin
  - rvierdiiev
  - bin2chen
  - t0x1c
---

## Vulnerability Title

[H-04] Multiple swap lack slippage protection

### Overview



This bug report discusses a problem with the current protocol, which involves swapping tokens in multiple places. The `_swap()` method is used for these swaps, but it does not set the `amountOutMinimum` parameter. This can lead to front running sandwich attacks or other types of price manipulation. It is recommended to set `amountOutMinimum` to `params.amountOut` and accurately calculate the allowed slippage value when calling `_swap()`. This has been confirmed by the BakerFi team and has been fixed in a recent update.

### Original Finding Content


The current protocol requires swapping tokens in multiple places, such as `weth -> ierc20A` or `ierc20A -> weth`.

Primarily, these swaps are executed using the `_swap()` method.

```solidity
    function _swap(
        ISwapHandler.SwapParams memory params
    ) internal override returns (uint256 amountOut) {
        if (params.underlyingIn == address(0)) revert InvalidInputToken();
        if (params.underlyingOut == address(0)) revert InvalidOutputToken();
        uint24 fee = params.feeTier;
        if (fee == 0) revert InvalidFeeTier();

        // Exact Input
        if (params.mode == ISwapHandler.SwapType.EXACT_INPUT) {
            amountOut = _uniRouter.exactInputSingle(
                IV3SwapRouter.ExactInputSingleParams({
                    tokenIn: params.underlyingIn,
                    tokenOut: params.underlyingOut,
                    amountIn: params.amountIn,
@>                  amountOutMinimum: 0,   //@audit miss set params.amountOut
                    fee: fee,
                    recipient: address(this),
                    sqrtPriceLimitX96: 0
                })
            );
            if (amountOut == 0) {
                revert SwapFailed();
            }
            emit Swap(params.underlyingIn, params.underlyingOut, params.amountIn, amountOut);
            // Exact Output
        } else if (params.mode == ISwapHandler.SwapType.EXACT_OUTPUT) {
            uint256 amountIn = _uniRouter.exactOutputSingle(
                IV3SwapRouter.ExactOutputSingleParams({
                    tokenIn: params.underlyingIn,
                    tokenOut: params.underlyingOut,
                    fee: fee,
                    recipient: address(this),
                    amountOut: params.amountOut,
                    amountInMaximum: params.amountIn,
                    sqrtPriceLimitX96: 0
                })
            );
            if (amountIn < params.amountIn) {
                IERC20(params.underlyingIn).safeTransfer(address(this), params.amountIn - amountIn);
            }
            emit Swap(params.underlyingIn, params.underlyingOut, amountIn, params.amountOut);
            amountOut = params.amountOut;
        }
    }
```

This method does not set `amountOutMinimum`.

And when call same miss set `Amount Out`.

```solidity
abstract contract StrategyLeverage is
    function _convertFromWETH(uint256 amount) internal virtual returns (uint256) {
        // 1. Swap WETH -> cbETH/wstETH/rETH
        return
            _swap(
                ISwapHandler.SwapParams(
                    wETHA(), // Asset In
                    ierc20A(), // Asset Out
                    ISwapHandler.SwapType.EXACT_INPUT, // Swap Mode
                    amount, // Amount In
                    //@audit miss slippage protection
@>                  0, // Amount Out 
                    _swapFeeTier, // Fee Pair Tier
                    bytes("") // User Payload
                )
            );
    }
```

These methods do not have slippage protection.

<https://docs.uniswap.org/contracts/v3/guides/swaps/single-swaps>

> amountOutMinimum: we are setting to zero, but this is a significant risk in production. For a real deployment, this value should be calculated using our SDK or an onchain price oracle - this helps protect against getting an unusually bad price for a trade due to a front running sandwich or another type of price manipulation

Include：`UseSwapper._swap()`/ `_convertFromWETH()`/`_convertToWETH()`/`_payDebt()`

### Impact

Front running sandwich or another type of price manipulation.

### Recommended Mitigation

1.  `_swap()` need set `amountOutMinimum = params.amountOut`

```diff
    function _swap(
        ISwapHandler.SwapParams memory params
    ) internal override returns (uint256 amountOut) {
        if (params.underlyingIn == address(0)) revert InvalidInputToken();
        if (params.underlyingOut == address(0)) revert InvalidOutputToken();
        uint24 fee = params.feeTier;
        if (fee == 0) revert InvalidFeeTier();

        // Exact Input
        if (params.mode == ISwapHandler.SwapType.EXACT_INPUT) {
            amountOut = _uniRouter.exactInputSingle(
                IV3SwapRouter.ExactInputSingleParams({
                    tokenIn: params.underlyingIn,
                    tokenOut: params.underlyingOut,
                    amountIn: params.amountIn,
-                   amountOutMinimum: 0,
+                  amountOutMinimum: params.amountOut
                    fee: fee,
                    recipient: address(this),
                    sqrtPriceLimitX96: 0
                })
            );
            if (amountOut == 0) {
                revert SwapFailed();
            }
```

2.  Call `_swap()` need set `params.amountOut` calculating the allowed slippage value accurately.

**[hvasconcelos (BakerFi) confirmed](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/32#event-13082084164)**

**[ickas (BakerFi) commented](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/32#issuecomment-2167742316):**
 > Fixed → https://github.com/baker-fi/bakerfi-contracts/pull/41



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | 0xStalin, rvierdiiev, bin2chen, t0x1c |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-bakerfi
- **GitHub**: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/32
- **Contest**: https://code4rena.com/reports/2024-05-bakerfi

### Keywords for Search

`vulnerability`

