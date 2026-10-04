---
# Core Classification
protocol: Gamma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13287
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/02/gamma/
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
finders_count: 2
finders:
  - Sergii Kravchenko
  -  David Oz Kashi

---

## Vulnerability Title

Hypervisor - Multiple “sandwiching” front running vectors ✓ Fixed

### Overview


This bug report is about a potential manipulation of the amount of tokens received from UniswapV3Pool functions. This is due to the decentralized nature of AMMs, where the order of transactions can not be pre-determined. A potential “sandwicher” may insert a buying order before the user’s call to Hypervisor.rebalance and a sell order after.

The bug was fixed in GammaStrategies/hypervisor/commit/9a7a3dd88e8e8b106bf5d0e4c56e879442a72181 by removing the call to pool.swap and adopting the auditor recommendation for pool.mint, pool.burn with slippage of 10%.

The auditor also recommended adding an amountMin parameter to ensure that at least the amountMin of tokens was received. This would help prevent manipulation of the amount of tokens received.

### Original Finding Content

#### Resolution



Fixed in [GammaStrategies/[email protected]`9a7a3dd`](https://github.com/GammaStrategies/hypervisor/commit/9a7a3dd88e8e8b106bf5d0e4c56e879442a72181) by removing the call to `pool.swap`, and adopting the auditor recommendation for `pool.mint`, `pool.burn` with `slippage = 10%`


#### Description


The amount of tokens received from `UniswapV3Pool` functions might be manipulated by front-runners due to the decentralized nature of AMMs, where the order of transactions can not be pre-determined.
A potential “sandwicher” may insert a buying order before the user’s call to `Hypervisor.rebalance` for instance, and a sell order after.


More specifically, calls to `pool.swap`, `pool.mint`, `pool.burn` are susceptible to “sandwiching” vectors.


#### Examples


`Hypervisor.rebalance`


**code/contracts/Hypervisor.sol:L278-L286**



```
if (swapQuantity != 0) {
    pool.swap(
        address(this),
        swapQuantity > 0,
        swapQuantity > 0 ? swapQuantity : -swapQuantity,
        swapQuantity > 0 ? TickMath.MIN\_SQRT\_RATIO + 1 : TickMath.MAX\_SQRT\_RATIO - 1,
        abi.encode(address(this))
    );
}

```
**code/contracts/Hypervisor.sol:L348-L363**



```
function \_mintLiquidity(
    int24 tickLower,
    int24 tickUpper,
    uint128 liquidity,
    address payer
) internal returns (uint256 amount0, uint256 amount1) {
    if (liquidity > 0) {
        (amount0, amount1) = pool.mint(
            address(this),
            tickLower,
            tickUpper,
            liquidity,
            abi.encode(payer)
        );
    }
}

```
**code/contracts/Hypervisor.sol:L365-L383**



```
function \_burnLiquidity(
    int24 tickLower,
    int24 tickUpper,
    uint128 liquidity,
    address to,
    bool collectAll
) internal returns (uint256 amount0, uint256 amount1) {
    if (liquidity > 0) {
        // Burn liquidity
        (uint256 owed0, uint256 owed1) = pool.burn(tickLower, tickUpper, liquidity);

        // Collect amount owed
        uint128 collect0 = collectAll ? type(uint128).max : \_uint128Safe(owed0);
        uint128 collect1 = collectAll ? type(uint128).max : \_uint128Safe(owed1);
        if (collect0 > 0 || collect1 > 0) {
            (amount0, amount1) = pool.collect(to, tickLower, tickUpper, collect0, collect1);
        }
    }
}

```
#### Recommendation


Consider adding an `amountMin` parameter(s) to ensure that at least the `amountMin` of tokens was received.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Gamma |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  David Oz Kashi
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/02/gamma/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

