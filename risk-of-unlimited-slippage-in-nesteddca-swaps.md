---
# Core Classification
protocol: Mass
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29680
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
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
finders_count: 5
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Tarun Bansal
  - Kurt Willis
  - Richie Humphrey
---

## Vulnerability Title

Risk of unlimited slippage in NestedDca swaps

### Overview


The NestedDca contract from Uniswap V3 has a bug that allows unlimited slippage when executing swaps. This is because the slippage protection is assigned to a memory variable that is not passed on to the next function executing the swap. This means that an attacker can front-run or sandwich the swap transaction and benefit from the unprotected swap. The bug can be fixed by passing the value of the memory variable to the next function. In the long term, the code should be carefully reviewed and unit tests should be added to catch similar issues.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Description

The swaps executed by the `NestedDca` contract from Uniswap V3 allow unlimited slippage because the slippage protection is assigned to a memory variable that is not passed on to the next function executing the swap.

When executing swaps on Uniswap, a slippage check parameter is required to protect users from paying an unexpectedly higher amount for the token being bought. The `NestedDca` contract executes the DCA by swapping user-conﬁgured tokens in a loop, as shown below:

```solidity
for (uint256 i; i < swapsAmount;) {
    ISwapRouter.ExactInputSingleParams memory swapParams = dcas[dcaId].swapsParams[i];
    address uniswapPool = uniswapFactory.getPool(swapParams.tokenIn, swapParams.tokenOut, swapParams.fee);
    
    if (pools[uniswapPool] == 0) revert UnauthorizedUniswapPool(uniswapPool);
    
    // Compute the minimum acceptable output amount
    swapParams.amountOutMinimum = ExchangeHelpers.estimateDcaSwapAmountOut(
        uniswapPool, swapParams, uint32(pools[uniswapPool]), dcas[dcaId].swapSlippage
    );

    IERC20(swapParams.tokenIn).safeTransferFrom(ownerOf[dcaId], address(this), swapParams.amountIn);
    
    // Perform the DCA programmed swap
    amountsOut[i] = _performDcaSwap(dcaId, i);
    
    unchecked {
        ++i;
    }
}
```

*Figure 22.1: The performDca function in NestedDca.sol*

The swap parameters are assigned from contract storage to a local memory variable named `swapParams`. The slippage value is computed and set to the memory variable `swapParams.amountOutMinimum`. This value is not set to the storage variable; therefore, it is visible only in the scope of this function, not in other functions that read swap parameters from storage.

The `performDca` function then calls the `_performDcaSwap` function, which again assigns swap parameters from contract storage to a local memory variable named `swapParams`, as shown below:

```solidity
function _performDcaSwap(bytes32 dcaId, uint256 swapParamsIndex)
private
returns (uint256 amountOut)
{
    ISwapRouter.ExactInputSingleParams memory swapParams = dcas[dcaId].swapsParams[swapParamsIndex];
    amountOut = uniswapRouter.exactInputSingle(swapParams);
}
```

*Figure 22.2: The _performDcaSwap function in NestedDca.sol*

So the value of `swapParams.amountOutMinimum` is not correct in the scope of the `_performDcaSwap` function—it is `0`, indicating no slippage protection. This incorrect value is then sent as an argument to the Uniswap V3 router, which executes the swap without slippage protection. An attacker can front-run or sandwich the swap transaction to benefit from this unprotected swap transaction.

## Exploit Scenario

Alice uses a DCA strategy to buy $50,000 worth of MyToken every day. The DCA is executed every day at 9 a.m. ET by the Gelato operators. Eve front-runs the transaction, buys $10,000 worth of MyToken, and sells them directly after Alice's transaction. As a result, Alice bought MyToken at an unfair price, and Eve profited from it.

## Recommendations

- **Short term**: Have the code pass the value of the memory variable `swapParams` from the `performDca` function to the `_performDcaSwap` function as an argument.
- **Long term**: Carefully review the code to check for the correct use of values set to memory variables. Add unit test cases that mimic front-running to capture such issues.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Mass |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Tarun Bansal, Kurt Willis, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

