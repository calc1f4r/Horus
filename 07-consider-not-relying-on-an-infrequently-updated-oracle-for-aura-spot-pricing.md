---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49083
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
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
finders_count: 0
finders:
---

## Vulnerability Title

[07] Consider not relying on an infrequently updated oracle for AURA spot pricing

### Overview

See description below for full details.

### Original Finding Content


The `AuraVault` contract relies on an oracle for calculating the AURA spot price, which is not updated frequently, potentially leading to inaccurate price reflections and impacting various operations within the vault.

The `_getAuraSpot` function in the `AuraVault` contract calculates the AURA spot price by fetching the time-weighted average price from a custom oracle. This oracle is not updated frequently, which leads to discrepancies between the calculated price and the actual market value of AURA.

Here we have an infrequent updates, because for Balancer/Aura oracles, the update to the price is only done whenever a transaction (e.g., `swap`) within the pool is triggered (see [here](https://etherscan.io/address/0x32296969Ef14EB0c6d29669C550D4a0449130230), for example). Due to the lack of updates, the price provided by the Oracle might not reflect the true value of the assets. Attached in the linked oracle, we can see how even for days no updates were made to the price if tx were not processed.

```solidity
function _getAuraSpot() internal view returns (uint256 price) {
  uint256 ethPrice;
  (, int256 answer, , , ) = AggregatorV3Interface(ETH_CHAINLINK_FEED).latestRoundData();
  ethPrice = wdiv(uint256(answer), ETH_CHAINLINK_DECIMALS);

  IPriceOracle.OracleAverageQuery[] memory queries = new IPriceOracle.OracleAverageQuery[](1);
  queries[0] = IPriceOracle.OracleAverageQuery(IPriceOracle.Variable.PAIR_PRICE, 1800, 0);
  uint256[] memory results = IPriceOracle(auraPriceOracle).getTimeWeightedAverage(queries);

  price = wmul(results[0], ethPrice);
}
```

### Impact

The infrequent updates to the oracle used for AURA spot price calculation can result in the price not accurately reflecting the true market value of AURA. This can affect:

- **Vault Settlement**: Inaccurate asset valuation can lead to incorrect settlement values, impacting the distribution of rewards and potentially causing losses.
- **Deleverage/Liquidation of Accounts**: Users close to the liquidation threshold might face premature deleveraging or liquidation due to undervalued assets.
- **Borrowing**: Overvaluation could allow users to borrow more than they should, based on inaccurate asset prices.

### Recommended Mitigation Steps

Consider using more frequently updated oracles, such as Chainlink/Pyth, as the primary source for price information. If a secondary oracle is needed, ensure it provides timely updates to reflect market conditions accurately.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

