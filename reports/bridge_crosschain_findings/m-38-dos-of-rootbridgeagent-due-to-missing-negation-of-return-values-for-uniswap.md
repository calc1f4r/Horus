---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: dos
vulnerability_type: signed/unsigned

# Attack Vector Details
attack_type: signed/unsigned
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26107
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/262

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - signed/unsigned
  - dos

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - peakbolt
---

## Vulnerability Title

[M-38] DoS of `RootBridgeAgent` due to missing negation of return values for `UniswapV3Pool.swap()`

### Overview


A bug has been identified in the Ulysses Omnichain's RootBridgeAgent.sol code, which can cause a Denial of Service (DoS) of the Ulysses Omnichain. This bug occurs when the return value of the UniswapV3Pool.swap() function is not negated before casting to uint256 in the RootBridgeAgent._gasSwapIn() and RootBridgeAgent._gasSwapOut() functions. This causes the parent functions anyExecute() and _manageGasOut() to revert on overflow when casting return values of _gasSwapIn() and _gasSwapOut() with SafeCastLib.toUint128(). 

Several external functions in RootBridgeAgent are affected by this issue, including anyExecute(), callOut(), callOutAndBridge(), callOutAndBridgeMultiple(), etc. This means RootBridgeAgent will not function properly at all, resulting in a DoS of the Ulysses Omnichain.

The issue can be simulated by adding a line of code to MockPool.swap() in RootTest.t.sol#L1916. Running RootTest.testCallOutWithDeposit() will demonstrate that swap() will cause an overflow to revert CoreRootRouter.addBranchToBridgeAgent(), preventing RootTest.setUp() from completing.

The recommended mitigation steps for this issue are to negate the return values of UniswapV3Pool.swap() in RootBridgeAgent._gasSwapIn() and RootBridgeAgent._gasSwapOut() before casting to uint256. However, this bug will not be rectified due to the upcoming migration of this section to LayerZero.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L684><br><https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L728>

### Vulnerability details

Both `RootBridgeAgent._gasSwapIn()` and `RootBridgeAgent._gasSwapOut()` do not negate the negative returned value of `UniswapV3Pool.swap()` before casting to `uint256`. That will cause the parent functions `anyExecute()` and `_manageGasOut()` to revert on overflow when casting return values of `_gasSwapIn()` and `_gasSwapOut()` with `SafeCastLib.toUint128()`.

### Impact

Several external functions in `RootBridgeAgent` (such as `anyExecute()`,  `callOut()`, `callOutAndBridge()`, `callOutAndBridgeMultiple()`, etc) are affected by this issue. That means `RootBridgeAgent` will not function properly at all, causing a DoS of the Ulysses Omnichain.

### Detailed Explanation

`UniSwapV3Pool.swap()` returns a negative value for exact input swap (see [documentation](<https://docs.uniswap.org/contracts/v3/reference/core/UniswapV3Pool#swap>)).

This is evident in UniswapV3's `SwapRouter.sol`, which shows that the returned value is negated before casting to `uint256`.

<https://github.com/Uniswap/v3-periphery/blob/main/contracts/SwapRouter.sol#L111>

```Solidity
    function exactInputInternal(
        uint256 amountIn,
        address recipient,
        uint160 sqrtPriceLimitX96,
        SwapCallbackData memory data
    ) private returns (uint256 amountOut) { 
        ...

        (int256 amount0, int256 amount1) =
            getPool(tokenIn, tokenOut, fee).swap(
                recipient,
                zeroForOne,
                amountIn.toInt256(),
                sqrtPriceLimitX96 == 0
                    ? (zeroForOne ? TickMath.MIN_SQRT_RATIO + 1 : TickMath.MAX_SQRT_RATIO - 1)
                    : sqrtPriceLimitX96,
                abi.encode(data)
            );

        //@audit return values amount0 and amount1 are negated before casting to uint256
        return uint256(-(zeroForOne ? amount1 : amount0));
    }
```

However, both `RootBridgeAgent._gasSwapIn()` and `RootBridgeAgent._gasSwapOut()` do not negate the returned value before casting to `uint256`.

```Solidity
    function _gasSwapIn(uint256 _amount, uint24 _fromChain) internal returns (uint256) {
        ...

        try IUniswapV3Pool(poolAddress).swap(
            address(this),
            zeroForOneOnInflow,
            int256(_amount),
            sqrtPriceLimitX96,
            abi.encode(SwapCallbackData({tokenIn: gasTokenGlobalAddress}))
        ) returns (int256 amount0, int256 amount1) {
            //@audit missing negation of amount0/amount1 before casting to uint256
            return uint256(zeroForOneOnInflow ? amount1 : amount0);
        } catch (bytes memory) {
            _forceRevert();
            return 0;
        }
    }

     function _gasSwapOut(uint256 _amount, uint24 _toChain) internal returns (uint256, address) {
        ...

        //Swap imbalanced token as long as we haven't used the entire amountSpecified and haven't reached the price limit
        (int256 amount0, int256 amount1) = IUniswapV3Pool(poolAddress).swap(
            address(this),
            !zeroForOneOnInflow,
            int256(_amount),
            sqrtPriceLimitX96,
            abi.encode(SwapCallbackData({tokenIn: address(wrappedNativeToken)}))
        );

        //@audit missing negation of amount0/amount1 before casting to uint256
        return (uint256(!zeroForOneOnInflow ? amount1 : amount0), gasTokenGlobalAddress);
    }
```

In `anyExecute()` and `_manageGasOut()` , both return value of `_gasSwapIn()` and `_gasSwapOut()` are converted using `SafeCastLib.toUint128()`. That means, these calls will revert due to overflow, as casting a negative `uint256` value to `uint256` will result in a large value exceeding `uint128`.

<https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L884-L886>

```Solidity
    function anyExecute(bytes calldata data)
        external
        virtual
        requiresExecutor
        returns (bool success, bytes memory result)
    {
        ...
            //@audit SafeCastLib.toUint128() will revert due to large return value from _gasSwapIn()
            //Swap in all deposited Gas
            _userFeeInfo.depositedGas = _gasSwapIn(
                uint256(uint128(bytes16(data[data.length - PARAMS_GAS_IN:data.length - PARAMS_GAS_OUT]))), fromChainId
            ).toUint128();
    }
```

<https://github.com/code-423n4/2023-05-maia/blob/main/src/ulysses-omnichain/RootBridgeAgent.sol#L757-L767>

```Solidity
    function _manageGasOut(uint24 _toChain) internal returns (uint128) {
        ...

        if (_initialGas > 0) {
            if (userFeeInfo.gasToBridgeOut <= MIN_FALLBACK_RESERVE * tx.gasprice) revert InsufficientGasForFees();
            (amountOut, gasToken) = _gasSwapOut(userFeeInfo.gasToBridgeOut, _toChain);
        } else {
            if (msg.value <= MIN_FALLBACK_RESERVE * tx.gasprice) revert InsufficientGasForFees();
            wrappedNativeToken.deposit{value: msg.value}();
            (amountOut, gasToken) = _gasSwapOut(msg.value, _toChain);
        }

        IPort(localPortAddress).burn(address(this), gasToken, amountOut, _toChain);

        //@audit SafeCastLib.toUint128() will revert due to large return value from _gasSwapOut()
        return amountOut.toUint128();
    }
```

### Proof of Concept

First, simulate a negative return value by adding the following line to `MockPool.swap()` in [RootTest.t.sol#L1916](https://github.com/code-423n4/2023-05-maia/blob/main/test/ulysses-omnichain/RootTest.t.sol#L1916):

```Solidity
        //@audit simulate UniSwapV3Pool negative return value
        return (-amount0, -amount1);
```

Then, run `RootTest.testCallOutWithDeposit()`, which will demonstrate that `swap()` will cause an overflow to revert `CoreRootRouter.addBranchToBridgeAgent()`, preventing `RootTest.setUp()` from completing.

### Recommended Mitigation Steps

Negate the return values of `UniswapV3Pool.swap()` in `RootBridgeAgent._gasSwapIn()` and `RootBridgeAgent._gasSwapOut()` before casting to `uint256`.

### Assessed type

DoS

**[0xBugsy (Maia) confirmed and commented](https://github.com/code-423n4/2023-05-maia-findings/issues/262#issuecomment-1655931922):**
 > We recognize the audit's findings on Anycall Gas Management. These will not be rectified due to the upcoming migration of this section to LayerZero.
> 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | peakbolt |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/262
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`Signed/Unsigned, DOS`

