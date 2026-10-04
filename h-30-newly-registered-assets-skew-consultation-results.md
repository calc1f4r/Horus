---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 1015
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/249

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
  - oracle

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
  - leastwood
---

## Vulnerability Title

[H-30] Newly Registered Assets Skew Consultation Results

### Overview


This bug report is about a vulnerability in the `TwapOracle.consult()` function of the VADER and USDV protocols. This function iterates over all token pairs which belong to either `VADER` or USDV` and then calculates the price of the respective asset by using both UniswapV2 and Chainlink price data. If a new asset is added by first registering the token pair and aggregator, the consultation result for that token pair will remain skewed until the next update interval. This is due to the fact that the native asset amount will return `0` due to the default `price1Average` value being used. As a result, the query will be skewed in favour of `sumUSD` resulting in incorrect consultations. This can lead to issues in other areas of the protocol that use this data in performing sensitive actions, making it a high risk issue.

The recommended mitigation steps for this vulnerability include performing proper checks to ensure that if `pairData.price1Average._x == 0`, then the Chainlink aggregator is not queried and not added to `sumUSD`, as well as fixing the current check to assert that the `pairData.price1Average.mul(1).decode144()` result is not `0`.

### Original Finding Content

_Submitted by leastwood_

#### Impact

The `TwapOracle.consult()` function iterates over all token pairs which belong to either `VADER` or USDV\` and then calculates the price of the respective asset by using both UniswapV2 and Chainlink price data. This helps to further protect against price manipulation attacks as the price is averaged out over the various registered token pairs.

If a new asset is added by first registering the token pair and aggregator, the consultation result for that token pair will remain skewed until the next update interval. This is due to the fact that the native asset amount will return `0` due to the default `price1Average` value being used. However, the Chainlink oracle will return a valid result. As a result, the query will be skewed in favour of `sumUSD` resulting in incorrect consultations.

I'd classify this issue as high risk as the oracle returns false results upon being consulted. This can lead to issues in other areas of the protocol that use this data in performing sensitive actions.

#### Proof of Concept

- <https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L115-L157>
- <https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L314>
- <https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L322-L369>

#### Tools Used

Manual code review.

#### Recommended Mitigation Steps

Consider performing proper checks to ensure that if `pairData.price1Average._x == 0`, then the Chainlink aggregator is not queried and not added to `sumUSD`. Additionally, it may be useful to fix the current check to assert that the `pairData.price1Average.mul(1).decode144()` result is not `0`, found [here](https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L129-L132). `require(sumNative != 0)` is used to assert this, however, this should be `require(pairData.price1Average.mul(1).decode144() != 0)` instead.

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/249)**
>The TWAP oracle module has been completely removed and redesigned from scratch as LBTwap that is subject of the new audit.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/249
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`Oracle`

