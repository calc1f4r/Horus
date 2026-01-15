---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27482
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - nonseodion
  - toshii
---

## Vulnerability Title

LibOracle fails to check the fidelity of price data from WETH/USDC pool, which can lead to price manipulation

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/libraries/LibOracle.sol#L91-L92">https://github.com/Cyfrin/2023-09-ditto/blob/main/contracts/libraries/LibOracle.sol#L91-L92</a>


## Summary

As per the [documentation](https://dittoeth.com/technical/oracles), LibOracle should only be returning the TWAP price from the WETH/USDC pool if the amount of WETH in the pool is >= 100e18. This is to ensure the fidelity of the data, which reduces the risk of price manipulation. However, this is not properly implemented for the case in which there was an invalid fetch of chainlink data. In this case, LibOracle simply returns the TWAP price without checking if there's enough liquidity in the pool. This can lead to a lack of data fidelity for the returned price.

It's clear that reverting should be the correct action rather than returning the TWAP price without checking the liquidity, as even when there is a valid chainlink price, if the TWAP price is closer to the cached price (and there isn't enough liquidity), it will still revert.

## Vulnerability Details

LibOracle has a `baseOracleCircuitBreaker` function which handles whether to return the TWAP price or the chainlink price, when the asset is USD, and it is defined as follows:
```solidity
function baseOracleCircuitBreaker(
    uint256 protocolPrice,
    uint80 roundId,
    int256 chainlinkPrice,
    uint256 timeStamp,
    uint256 chainlinkPriceInEth
) private view returns (uint256 _protocolPrice) {
    bool invalidFetchData = roundId == 0 || timeStamp == 0
        || timeStamp > block.timestamp || chainlinkPrice <= 0
        || block.timestamp > 2 hours + timeStamp;
    ...
    if (invalidFetchData || priceDeviation) {
        uint256 twapPrice = IDiamond(payable(address(this))).estimateWETHInUSDC(
            Constants.UNISWAP_WETH_BASE_AMT, 30 minutes
        );
        uint256 twapPriceInEther = (twapPrice / Constants.DECIMAL_USDC) * 1 ether;
        uint256 twapPriceInv = twapPriceInEther.inv();
        if (twapPriceInEther == 0) {
            revert Errors.InvalidTwapPrice();
        }

        if (invalidFetchData) {
            return twapPriceInv; // @issue
        } else {
            ...
        }
    } else {
        return chainlinkPriceInEth;
    }
}
```
When `invalidFetchData` is true, meaning that the chainlink price was not properly fetched, it will always return `twapPriceInv`. However, this lacks any checks as to whether there is at least 100 WETH in the Uniswap pool, which can result in a lack of data fidelity.

## Impact

When the chainlink oracle is not functioning correctly, LibOracle will always return the TWAP price for the USD asset. However, this lacks any check as to whether there is enough liquidity in the Uniswap pool to guarantee data fidelity, meaning there is a higher likelihood of price manipulation.

## Tools Used

Manual review

## Recommendations

Before returning the TWAP price when `invalidFetchData` is true, first check whether the WETH/USDC pool has enough liquidity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | nonseodion, toshii |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`vulnerability`

