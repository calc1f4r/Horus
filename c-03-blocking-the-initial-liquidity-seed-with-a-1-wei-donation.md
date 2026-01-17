---
# Core Classification
protocol: Moarcandy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36508
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/MoarCandy-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-03] Blocking the initial liquidity seed with a 1 wei donation

### Overview


This bug report describes a scenario where an attacker can create an empty token pair on Uniswap and manipulate the reserve values, causing a failure in the protocol when trying to create a pair after the initial sale phase. The report suggests a solution to directly interact with the Uniswap pair instead of relying on a router to prevent this issue.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

Consider the following scenario:

1. While the bonding token (TOK) is still in the initial sale phase, the attacker creates an empty TOK/WETH pair on the Uniswap
2. He then donates 1 wei of WETH to the pair and calls the `sync` function:

```solidity
/// https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L198
    function sync() external lock {
        _update(IERC20(token0).balanceOf(address(this)), IERC20(token1).balanceOf(address(this)), reserve0, reserve1);
    }
```

As a result, one of the reserves will be non-zero. 3. When the sale is over, the protocol will attempt to create a pair via the Uniswap router, but the call will fail:

```solidity
    function _addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin
    ) internal virtual returns (uint amountA, uint amountB) {
        // create the pair if it doesn't exist yet
        if (IUniswapV2Factory(factory).getPair(tokenA, tokenB) == address(0)) {
            IUniswapV2Factory(factory).createPair(tokenA, tokenB);
        }
>>      (uint reserveA, uint reserveB) = UniswapV2Library.getReserves(factory, tokenA, tokenB);
        if (reserveA == 0 && reserveB == 0) {
            (amountA, amountB) = (amountADesired, amountBDesired);
        } else {
>>          uint amountBOptimal = UniswapV2Library.quote(amountADesired, reserveA, reserveB);
            if (amountBOptimal <= amountBDesired) {
                require(amountBOptimal >= amountBMin, 'UniswapV2Router: INSUFFICIENT_B_AMOUNT');
                (amountA, amountB) = (amountADesired, amountBOptimal);
            } else {
>>              uint amountAOptimal = UniswapV2Library.quote(amountBDesired, reserveB, reserveA);
                assert(amountAOptimal <= amountADesired);
                require(amountAOptimal >= amountAMin, 'UniswapV2Router: INSUFFICIENT_A_AMOUNT');
                (amountA, amountB) = (amountAOptimal, amountBDesired);
            }
        }
    }
```

Because one of the reserves has a non-zero value the `quote` function will be invoked:

```solidity
    function quote(uint amountA, uint reserveA, uint reserveB) internal pure returns (uint amountB) {
        require(amountA > 0, 'UniswapV2Library: INSUFFICIENT_AMOUNT');
>>      require(reserveA > 0 && reserveB > 0, 'UniswapV2Library: INSUFFICIENT_LIQUIDITY');
        amountB = amountA.mul(reserveB) / reserveA;
    }
```

And since one of the reserves is empty, `addLiquidity` will fail to trap bonding tokens and collected ETH in the contract.

**Recommendations**

To address this issue, it is suggested to interact directly with the Uniswap pair instead of relying on a router:

```diff
        if (poolType == LP_POOL.Uniswap) {
            wNative = IUniswapV2Router02(router).WETH();
+           IFactory factory = IFactory(IUniswapV2Router02(router).factory());
+           address pair = factory.getPair(address(this), wNative);
+           if(pair == address(0)) pair = factory.createPair(address(this), wNative));
+           IWETH(wNative).deposit{value: currentEth}();
+           IWETH(wNative).transfer(pair, currentEth);
+           _transfer(address(this), pair, currentTokenBalance);
+           uint256 liquidity = IPair(pair).mint(address(this));
        } else if (poolType == LP_POOL.TraderJoe) {
            wNative = IJoeRouter02(router).WAVAX();
+           IFactory factory = IFactory(IJoeRouter02(router).factory());
+           address pair = factory.getPair(address(this), wNative);
+           if(pair == address(0)) pair = factory.createPair(address(this), wNative));
+           IWETH(wNative).deposit{value: currentEth}();
+           IWETH(wNative).transfer(pair, currentEth);
+           _transfer(address(this), pair, currentTokenBalance);
+           uint256 liquidity = IPair(pair).mint(address(this));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Moarcandy |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/MoarCandy-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

