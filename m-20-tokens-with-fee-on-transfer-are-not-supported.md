---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1039
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/193

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
  - fee_on_transfer

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-20] Tokens with fee on transfer are not supported

### Overview


This bug report is about a vulnerability in the current implementation of the `BasePoolV2.sol#mint()` function. This function assumes that the received amount is the same as the transfer amount when calculating liquidity units. This is not the case with ERC20 tokens such as Vader, which charge a fee for every `transfer()` or `transferFrom()`. As a result, the function will not calculate the correct liquidity units. To fix this issue, the code should consider calling `balanceOf()` to get the actual balances.

### Original Finding Content

_Submitted by WatchPug_

There are ERC20 tokens that charge fee for every `transfer()` or `transferFrom()`, E.g `Vader` token.

In the current implementation, `BasePoolV2.sol#mint()` assumes that the received amount is the same as the transfer amount, and uses it to calculate liquidity units.

<https://github.com/code-423n4/2021-11-vader/blob/429970427b4dc65e37808d7116b9de27e395ce0c/contracts/dex-v2/pool/BasePoolV2.sol#L168-L229>

```solidity
function mint(
    IERC20 foreignAsset,
    uint256 nativeDeposit,
    uint256 foreignDeposit,
    address from,
    address to
)
    external
    override
    nonReentrant
    onlyRouter
    supportedToken(foreignAsset)
    returns (uint256 liquidity)
{
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
        "BasePoolV2::mint: Insufficient Liquidity Provided"
    );

    uint256 id = positionId++;

    pair.totalSupply = totalLiquidityUnits + liquidity;
    _mint(to, id);

    positions[id] = Position(
        foreignAsset,
        block.timestamp,
        liquidity,
        nativeDeposit,
        foreignDeposit
    );

    _update(
        foreignAsset,
        reserveNative + nativeDeposit,
        reserveForeign + foreignDeposit,
        reserveNative,
        reserveForeign
    );

    emit Mint(from, to, nativeDeposit, foreignDeposit);
    emit PositionOpened(from, to, id, liquidity);
}
```

#### Recommended

Consider calling `balanceOf()` to get the actual balances.


**[SamSteinGG (Vader) disagreed with severity](https://github.com/code-423n4/2021-11-vader-findings/issues/193#issuecomment-979174293):**
 > Tokens with a fee on transfer or rebasing tokens are not meant to be supported by the protocol, hence why the tokens supported are voted on by the DAO.

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/193#issuecomment-991508656):**
 > Not stated in the documentation, therefore the issue is valid.

**[SamSteinGG (Vader) commented](https://github.com/code-423n4/2021-11-vader-findings/issues/193#issuecomment-995715303):**
 > A medium risk issue cannot constitute lack of documentation of a trait of the system. If the inclusion of tokens to the DEX was not privileged, the issue would be valid but it is not an open function and thus the scenario described would never unfold.
>





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/193
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`Fee On Transfer`

