---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42344
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-vader
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/212

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

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-24] Wrong design/implementation of `addLiquidity()` allows attacker to steal funds from the liquidity pool

### Overview


The current design of Vader pool allows users to add liquidity using any amount, instead of a fixed ratio like Uni v2. This can be exploited by attackers to manipulate the pool's price and create an opportunity for arbitrage. The code snippet provided shows how this can be done. The proof of concept shows how an attacker can profit by adding liquidity, swapping BTC for USDV, and then removing the liquidity. The Vader team has disputed this issue, stating that it is the intended design of the Thorchain CLP model. The judge has acknowledged the issue, but the Vader team does not acknowledge it and claims it is inherent to the model.

### Original Finding Content

_Submitted by WatchPug_

The current design/implementation of Vader pool allows users to `addLiquidity` using arbitrary amounts instead of a fixed ratio of amounts in comparison to Uni v2.

We believe this design is flawed and it essentially allows anyone to manipulate the price of the pool easily and create an arbitrage opportunity at the cost of all other liquidity providers.

An attacker can exploit this by adding liquidity in extreme amounts and drain the funds from the pool.

<https://github.com/code-423n4/2021-11-vader/blob/429970427b4dc65e37808d7116b9de27e395ce0c/contracts/dex-v2/pool/VaderPoolV2.sol#L284-L335>

```solidity
function mintFungible(
    IERC20 foreignAsset,
    uint256 nativeDeposit,
    uint256 foreignDeposit,
    address from,
    address to
) external override nonReentrant returns (uint256 liquidity) {
    IERC20Extended lp = wrapper.tokens(foreignAsset);

    require(
        lp != IERC20Extended(_ZERO_ADDRESS),
        "VaderPoolV2::mintFungible: Unsupported Token"
    );

    (uint112 reserveNative, uint112 reserveForeign, ) = getReserves(
        foreignAsset
    ); // gas savings

    nativeAsset.safeTransferFrom(from, address(this), nativeDeposit);
    foreignAsset.safeTransferFrom(from, address(this), foreignDeposit);

    PairInfo storage pair = pairInfo[foreignAsset];
    uint256 totalLiquidityUnits = pair.totalSupply;
    if (totalLiquidityUnits == 0) liquidity = nativeDeposit;
    else
        liquidity = VaderMath.calculateLiquidityUnits(
            nativeDeposit,
            reserveNative,
            foreignDeposit,
            reserveForeign,
            totalLiquidityUnits
        );

    require(
        liquidity > 0,
        "VaderPoolV2::mintFungible: Insufficient Liquidity Provided"
    );

    pair.totalSupply = totalLiquidityUnits + liquidity;

    _update(
        foreignAsset,
        reserveNative + nativeDeposit,
        reserveForeign + foreignDeposit,
        reserveNative,
        reserveForeign
    );

    lp.mint(to, liquidity);

    emit Mint(from, to, nativeDeposit, foreignDeposit);
}
```

##### Proof of Concept

Given:

*   A Vader pool with `100,000 USDV` and `1 BTC`;
*   The `totalPoolUnits` is `100`.

The attacker can do the following in one transaction:

1.  Add liquidity with `100,000 USDV` and 0 BTC, get `50 liquidityUnits`, representing 1/3 shares of the pool;
2.  Swap `0.1 BTC` to USDV, repeat for 5 times; spent`0.5 BTC` and got `62163.36 USDV`;
3.  Remove liquidity, get back `45945.54 USDV` and `0.5 BTC`; profit for: 62163.36 + 45945.54 - 100000 = 8108.9 USDV.

**[SamSteinGG (Vader) disputed](https://github.com/code-423n4/2021-11-vader-findings/issues/212#issuecomment-979177570):**
 > This is the intended design of the Thorchain CLP model. Can the warden provide a tangible attack vector in the form of a test?

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/212#issuecomment-991472853):**
 > Sponsor is acknowledging the issue.

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/212#issuecomment-995712459):**
 > @alcueca We do not acknowledge the issue. This is the intended design of the CLP model and the amount supplied for a trade is meant to be safeguarded off-chain. It is an inherent trait of the model.
>





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/212
- **Contest**: https://code4rena.com/reports/2021-11-vader

### Keywords for Search

`vulnerability`

