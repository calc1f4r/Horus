---
# Core Classification
protocol: Groupcoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41358
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Groupcoin-security-review.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Griefing the launch to UniswapV3 by creating the pool first

### Overview


This bug report discusses an issue with a function called `launchGroupCoinToUniswapV3`. The function is supposed to transition the trading of coins to a different bonding curve, but there is a problem with how it calls another function called `uniswapV3Factory.createPool`. This function is only supposed to be called once, but the bug allows a malicious user to call it multiple times, causing the `launchGroupCoinToUniswapV3` function to fail. The report suggests a potential solution to fix this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Once x amount of coins are bought and the value of the coin reaches a certain threshold, `launchGroupCoinToUniswapV3` can be called. This will transition the trading of coins to a different bonding curve.

In `launchGroupCoinToUniswapV3()`, the function will call `uniswapV3Factory.createPool` without checking the existence of the pool.

```
        address pool = uniswapV3Factory.createPool(address(token), WETH, config.fee);
        IUniswapV3Pool(pool).initialize(config.sqrtPriceX96);
```

In UniswapV3Factory.createPool, it only allows the pool to be created once:

```
 function createPool(
        address tokenA,
        address tokenB,
        uint24 fee
    ) external override noDelegateCall returns (address pool) {
        require(tokenA != tokenB);
        (address token0, address token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        require(token0 != address(0));
        int24 tickSpacing = feeAmountTickSpacing[fee];
        require(tickSpacing != 0);
 >      require(getPool[token0][token1][fee] == address(0));
        pool = deploy(address(this), token0, token1, fee, tickSpacing);
 >      getPool[token0][token1][fee] = pool;
        // populate mapping in the reverse direction, deliberate choice to avoid the cost of comparing addresses
        getPool[token1][token0][fee] = pool;
        emit PoolCreated(token0, token1, fee, tickSpacing, pool);
    }
```

A malicious user can buy some tokens and call `createPool` directly in the UniswapV3Factory, with tokenA as the coin and tokenB as WETH and the fee according to the protocol's config.

Then, when `launchGroupCoinToUniswapV3()` is called, the function will revert as the pool has already been created.

## Recommendations

There is a function from another protocol that checks whether the pool has already been created and simply calls initialize if so.

A potential solution looks something like this:

```
 function _initUniV3PoolIfNecessary(PoolAddress.PoolKey memory poolKey, uint160 sqrtPriceX96) internal returns (address pool) {
        pool = IUniswapV3Factory(UNIV3_FACTORY).getPool(poolKey.token0, poolKey.token1, poolKey.fee);
        if (pool == address(0)) {
            pool = IUniswapV3Factory(UNIV3_FACTORY).createPool(poolKey.token0, poolKey.token1, poolKey.fee);
            IUniswapV3Pool(pool).initialize(sqrtPriceX96);
        } else {
            (uint160 sqrtPriceX96Existing, , , , , , ) = IUniswapV3Pool(pool).slot0();
            if (sqrtPriceX96Existing == 0) {
                IUniswapV3Pool(pool).initialize(sqrtPriceX96);
            } else {
                require(sqrtPriceX96Existing == sqrtPriceX96, "UV3P");
            }
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Groupcoin |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Groupcoin-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

