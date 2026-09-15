---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6647
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/20

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - uniswap
  - stale_price

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - cergyk
  - 0x52
  - psy4n0n
  - bitx0x
  - obront
---

## Vulnerability Title

H-10: IchiLpOracle is extemely easy to manipulate due to how IchiVault calculates underlying token balances

### Overview


This bug report is about the issue H-10 concerning the IchiLpOracle, an Ethereum-based protocol. It was found by seven people: carrot, obront, ctf_sec, cergyk, banditx0x, psy4n0n, and 0x52. The issue is that the IchiVault#getTotalAmounts uses the UniV3Pool.slot0 to determine the number of tokens it has in its position, which is the most recent data point and is extremely easy to manipulate. This manipulation would compound to make malicious uses even easier. This manipulation can cause loss of funds for the protocol and other users. 

To fix this issue, it is recommended that token balances should be calculated inside the oracle instead of getting them from the IchiVault. To determine the liquidity, use a TWAP instead of slot0. The tool used for finding this issue was manual review.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/20 

## Found by 
carrot, obront, ctf\_sec, cergyk, banditx0x, psy4n0n, 0x52

## Summary

`IchiVault#getTotalAmounts` uses the `UniV3Pool.slot0` to determine the number of tokens it has in it's position. `slot0` is the most recent data point and is therefore extremely easy to manipulate. Given that the protocol specializes in leverage, the effects of this manipulation would compound to make malicious uses even easier.

## Vulnerability Detail

[ICHIVault.sol](https://etherscan.io/token/0x683f081dbc729dbd34abac708fa0b390d49f1c39#code#L3098)

    function _amountsForLiquidity(
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity
    ) internal view returns (uint256, uint256) {
        (uint160 sqrtRatioX96, , , , , , ) = IUniswapV3Pool(pool).slot0();
        return
            UV3Math.getAmountsForLiquidity(
                sqrtRatioX96,
                UV3Math.getSqrtRatioAtTick(tickLower),
                UV3Math.getSqrtRatioAtTick(tickUpper),
                liquidity
            );
    }

`IchiVault#getTotalAmounts` uses the `UniV3Pool.slot0` to determine the number of tokens it has in it's position. [slot0](https://docs.uniswap.org/contracts/v3/reference/core/interfaces/pool/IUniswapV3PoolState#slot0) is the most recent data point and can easily be manipulated.

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/oracle/IchiLpOracle.sol#L27-L36

`IchiLPOracle` directly uses the token values returned by `vault#getTotalAmounts`. This allows a malicious user to manipulate the valuation of the LP. An example of this kind of manipulation would be to use large buys/sells to alter the composition of the LP to make it worth less or more. 

## Impact

Ichi LP value can be manipulated to cause loss of funds for the protocol and other users

## Code Snippet

## Tool used

Manual Review

## Recommendation

Token balances should be calculated inside the oracle instead of getting them from the `IchiVault`. To determine the liquidity, use a TWAP instead of `slot0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | cergyk, 0x52, psy4n0n, bitx0x, obront, carrot, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/20
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`Uniswap, Stale Price`

