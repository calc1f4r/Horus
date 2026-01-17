---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21411
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Xiaoming90
  - 0xNazgul
  - Jonatas Martins
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Calculation error of getAmountOut leads to revert of Router

### Overview

See description below for full details.

### Original Finding Content

## Analysis Report

## Severity
**Low Risk**

## Context
**File:** Pair.sol  
**Lines:** 450-476

## Description
The function `getAmountOut` in `Pair` calculates the correct swap amount and token price.

### Code Snippet
```solidity
// Pair.sol#L442-L444
function _f(uint256 x0, uint256 y) internal pure returns (uint256) {
    return (x0 * ((((y * y) / 1e18) * y) / 1e18)) / 1e18 + (((((x0 * x0) / 1e18) * x0) / 1e18) * y) / 1e18; , !
}
```

```solidity
// Pair.sol#L450-L476
function _get_y(
    uint256 x0,
    uint256 xy,
    uint256 y
) internal pure returns (uint256) {
    for (uint256 i = 0; i < 255; i++) {
        uint256 y_prev = y;
        uint256 k = _f(x0, y);
        if (k < xy) {
            uint256 dy = ((xy - k) * 1e18) / _d(x0, y);
            y = y + dy;
        } else {
            uint256 dy = ((k - xy) * 1e18) / _d(x0, y);
            y = y - dy;
        }
        if (y > y_prev) {
            if (y - y_prev <= 1) {
                return y;
            }
        } else {
            if (y_prev - y <= 1) {
                return y;
            }
        }
    }
    return y;
}
```

The `getAmountOut` function is not always correct. This results in the router unexpectedly reverting a regular and correct transaction. We can find one parameter that the router will fail to swap within 5 seconds of fuzzing.

### Test Function
```solidity
function testAmountOut(uint swapAmount) public {
    vm.assume(swapAmount < 1_000_000_000 ether);
    vm.assume(swapAmount > 1_000_000);
    uint256 reserve0 = 100 ether;
    uint256 reserve1 = 100 ether;
    uint amountIn = swapAmount - swapAmount * 2 / 10000;
    uint256 amountOut = _getAmountOut(amountIn, token0, reserve0, reserve1);
    uint initialK = _k(reserve0, reserve1);
    reserve0 += amountIn;
    reserve1 -= amountOut;
    console.log("initial k:", initialK);
    console.log("curent k:", _k(reserve0, reserve1));
    console.log("curent smaller k:", _k(reserve0, reserve1 - 1));
    require(initialK < _k(reserve0, reserve1), "K");
    require(initialK > _k(reserve0, reserve1-1), "K");
}
```

After the fuzzer has a counter example of `swapAmount = 1413611527073436`, we can test that the Router will revert if given the fuzzed parameters.

### Pair Test Contract
```solidity
contract PairTest is BaseTest {
    function testRouterSwapFail() public {
        Pair pair = Pair(factory.createPair(address(DAI), address(FRAX), true));
        DAI.approve(address(router), 100 ether);
        FRAX.approve(address(router), 100 ether);
        _addLiquidityToPool(
            address(this),
            address(router),
            address(DAI),
            address(FRAX),
            true,
            100 ether,
            100 ether
        );
        uint swapAmount = 1413611527073436;
        DAI.approve(address(router), swapAmount);
        // vm.expectRevert();
        console.log("fee:", factory.getFee(address(pair), true));
        IRouter.Route[] memory routes = new IRouter.Route[](1);
        routes[0] = IRouter.Route(address(DAI), address(FRAX), true, address(0));
        uint daiAmount = DAI.balanceOf(address(pair));
        uint FRAXAmount = FRAX.balanceOf(address(pair));
        console.log("daiAmount: ", daiAmount, "FRAXAmount: ", FRAXAmount);
        vm.expectRevert("Pair: K");
        router.swapExactTokensForTokens(swapAmount, 0, routes, address(owner), block.timestamp);
    }
}
```

## Recommendation
There are two causes of the miscalculation:

1. The function `_f` gets a different value from `_k` because of the rounding error.

    ```solidity
    + uint256 _a = (x0 * y) / 1e18;
    + uint256 _b = ((x0 * x0) / 1e18 + (y * y) / 1e18);
    + return (_a * _b) / 1e18;
    - return (x0 * ((((y * y) / 1e18) * y) / 1e18)) / 1e18 + (((((x0 * x0) / 1e18) * x0) / 1e18) * y) / 1e18; , !
    ```

2. The value of `y` at `Pair.sol#L459` will be impacted by the rounding error.
   
    ```solidity
    function _get_y(
        uint256 x0, // @audit (amountIn + reserveA) post reserveA
        uint256 xy, // k
        uint256 y // reserveB
    ) internal view returns (uint256) {
        for (uint256 i = 0; i < 255; i++) {
            uint256 y_prev = y;
            //@audit _f have a different rounding to _k
            uint256 k = _f(x0, y);
            if (k < xy) {
                //@audit: there are two cases where dy == 0
                // case 1: The y is converged and we find the correct answer
                // case 2: _d(x0, y) is too large compare to (xy - k) and the rounding error
                // screwed us.
                // In this case, we need to increase y by 1
                uint256 dy = ((xy - k) * 1e18) / _d(x0, y);
                if (dy == 0) {
                    if (k == xy ) {
                        // We found the correct answer. Return y
                        return y;
                    }
                    if (_k(x0, y + 1) > xy) {
                        // If _k(x0, y + 1) > xy, then we are close to the correct answer.
                        // There's no closer answer than y + 1
                        return y + 1;
                    }
                    dy = 1;
                }
                y = y + dy;
            } else {
                uint256 dy = ((k - xy) * 1e18) / _d(x0, y);
                if (dy == 0) {
                    if (k == xy || _f(x0, y - 1) < xy) {
                        // Likewise, if k == xy, we found the correct answer.
                        // If _f(x0, y - 1) < xy, then we are close to the correct answer.
                        // There’s no closer answer than "y"
                        return y;
                    }
                    dy = 1;
                }
                y = y - dy;
            }
        }
        // @audit - should never happen. If it does, it means it doesn't converge for 255 iterations
        // @audit - should assign a custom error to save gas.
        revert("y not found");
    }
    ```

## Acknowledgements
**Velodrome:** I have reviewed this and I agree with the finding. We can fix it for the new Pair contracts but note that like the "current value of a Pair is not always returning a 30-minute TWAP and can be manipulated" issue, it will only be fixed for new Pair contracts, while old Pair contracts will continue to have the faulty code in them. Fixed in commit 9ca981.

**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | Xiaoming90, 0xNazgul, Jonatas Martins, 0xLeastwood, Jonah1005, Alex the Entreprenerd |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Velodrome-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

