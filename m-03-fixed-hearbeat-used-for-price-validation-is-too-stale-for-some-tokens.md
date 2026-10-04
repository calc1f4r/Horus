---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33498
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/563

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Maroutis
  - ZanyBonzy
  - ilchovski
  - NentoR
---

## Vulnerability Title

[M-03] Fixed hearbeat used for price validation is too stale for some tokens

### Overview


The bug report discusses an issue with the stale period, or the time period after which data becomes outdated, used for an oracle price validation in the Renzo protocol. The current stale period of 24 hours and 60 seconds may be too short for certain tokens on different chains, leading to the protocol consuming outdated prices. It is recommended to store a mapping of the stale period for each token and chain to mitigate this issue. This bug falls under the category of an Oracle bug and has been acknowledged by the Renzo team.

### Original Finding Content


<https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Bridge/L2/Oracle/RenzoOracleL2.sol#L13>

<https://github.com/code-423n4/2024-04-renzo/blob/519e518f2d8dec9acf6482b84a181e403070d22d/contracts/Bridge/L2/Oracle/RenzoOracleL2.sol#L52>

### Impact

The stale period `86400 + 60 seconds` used for the oracle price validation is too short for some tokens like `ezETH` for example on Arbitrum. This could lead to the protocol consuming stale prices on Arbitrum.

### Proof of Concept

In both `RenzoOracle` and `RenzoOracleL2`, the hearbeat period `MAX_TIME_WINDOW` is set to `86400 + 60; // 24 hours + 60 seconds`. In the functions `RenzoOracleL2::getMintRate` and `RenzoOracle::lookupTokenValue`, a validation checks sees if the price data fed by Chainlink's price feed aggregators is stale depending if the period of `24 hours + 60 seconds` has passed. Example :

```js
    function getMintRate() public view returns (uint256, uint256) {
        (, int256 price, , uint256 timestamp, ) = oracle.latestRoundData();
        if (timestamp < block.timestamp - MAX_TIME_WINDOW) revert OraclePriceExpired();
```

The problem is that depending on the token and the chain, the same period can be considered too small or too stale.

Let's consider the ezETH/ETH oracles on different chains:

- On Ethereum, the oracle will update the price data every [`~24 hours`](https://data.chain.link/feeds/ethereum/mainnet/ezeth-eth).
- On Arbitrum, the oracle will update the price data every [`~6 hours`](https://data.chain.link/feeds/arbitrum/mainnet/ezeth-eth-exchange-rate).
- On Linea, the oracle will update the price data every [`24 hours`](https://data.chain.link/feeds/linea/mainnet/ezeth-eth).

This means that on Arbitrum, `24 hours` can be considered too large for the stale period which will cause the function `RenzoOracleL2::getMintRate` to return stale data.

### Recommended Mitigation Steps

It is recommended to store a mapping that would record the hearbeat parameter for the stale period of each token and for every different chain.

### Assessed type

Oracle

**[jatinj615 (Renzo) acknowledged](https://github.com/code-423n4/2024-04-renzo-findings/issues/563#event-13001051441)**

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-04-renzo-findings/issues/563).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | Maroutis, ZanyBonzy, ilchovski, NentoR |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/563
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

