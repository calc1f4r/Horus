---
# Core Classification
protocol: Lindy Labs Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26345
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-sandclock-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-sandclock-securityreview.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Guillermo Larregay
  - Bo Henderson
---

## Vulnerability Title

Chainlink oracles could return stale price data

### Overview

See description below for full details.

### Original Finding Content

## Target
`src/steth/PriceConverter.sol`, `src/liquity/scLiquity.sol`

## Description
The `latestRoundData()` function from Chainlink oracles returns five values: `roundId`, `answer`, `startedAt`, `updatedAt`, and `answeredInRound`. The `PriceConverter` contract reads only the `answer` value and discards the rest. This can cause outdated prices to be used for token conversions, such as the ETH-to-USDC conversion shown in Figure 6.1.

```solidity
function ethToUsdc(uint256 _ethAmount) public view returns (uint256) {
    (, int256 usdcPriceInEth,,,) = usdcToEthPriceFeed.latestRoundData();
    return _ethAmount.divWadDown(uint256(usdcPriceInEth) * C.WETH_USDC_DECIMALS_DIFF);
}
```

Figure 6.1: All returned data other than the `answer` value is ignored during the call to a Chainlink feed’s `latestRoundData` method.  
(Refer to [sandclock-contracts/src/steth/PriceConverter.sol#L67–L71](https://github.com/sandclock/sandclock-contracts/blob/main/src/steth/PriceConverter.sol#L67-L71))

According to the Chainlink documentation, if the `latestRoundData()` function is used, the `updatedAt` value should be checked to ensure that the returned value is recent enough for the application.

Similarly, the LUSD/ETH price feed used by the `scLiquity` vault is an intermediate contract that calls the deprecated `latestAnswer` method on upstream Chainlink oracles.

```solidity
contract LSUDUsdToLUSDEth is IPriceFeed {
    IPriceFeed public constant LUSD_USD = IPriceFeed(0x3D7aE7E594f2f2091Ad8798313450130d0Aba3a0);
    IPriceFeed public constant ETH_USD = IPriceFeed(0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419);

    function latestAnswer() external view override returns (int256) {
        return (LUSD_USD.latestAnswer() * 1 ether) / ETH_USD.latestAnswer();
    }
}
```

Figure 6.2: The custom `latestAnswer` method in [0x60c0b047133f696334a2b7f68af0b49d2F3D4F72#code#L19](https://etherscan.io/address/0x60c0b047133f696334a2b7f68af0b49d2F3D4F72#code#L19)

The Chainlink API reference flags the `latestAnswer` method as “(Deprecated - Do not use this function.)” Note that the upstream `IPriceFeed` contracts called by the intermediate `LSUDUsdToLUSDEth` contract are upgradeable proxies. It is possible that the implementations will be updated to remove support for the deprecated `latestAnswer` method, breaking the `scLiquity` vault’s `lusd2eth` price feed.

Because the oracle price feeds are used for calculating the slippage tolerance, a difference may exist between the oracle price and the DEX pool spot price, either due to price update delays or normal price fluctuations or because the feed has become stale. This could lead to two possible adverse scenarios:

- If the oracle price is significantly higher than the pool price, the slippage tolerance could be too loose, introducing the possibility of an MEV sandwich attack that can profit on the excess.
- If the oracle price is significantly lower than the pool price, the slippage tolerance could be too tight, and the transaction will always revert. Users will perceive this as a denial of service because they would not be able to interact with the protocol until the price difference is settled.

## Exploit Scenario
Bob has assets invested in a `scWETHv2` vault and wants to withdraw part of his assets. He interacts with the contracts, and every withdrawal transaction he submits reverts due to a large difference between the oracle and pool prices, leading to failed slippage checks. This results in a waste of gas and leaves Bob confused, as there is no clear indication of where the problem lies.

## Recommendations
Short term, make sure that the oracles report up-to-date data, and replace the external LUSD/ETH oracle with one that supports verification of the latest update timestamp. In the case of stale oracle data, pause price-dependent Sandclock functionality until the oracle comes back online or the admin replaces it with a live oracle.

Long term, review the documentation for Chainlink and other oracle integrations to ensure that all of the security requirements are met to avoid potential issues, and add tests that take these possible situations into account.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Lindy Labs Sandclock |
| Report Date | N/A |
| Finders | Guillermo Larregay, Bo Henderson |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-sandclock-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-sandclock-securityreview.pdf

### Keywords for Search

`vulnerability`

