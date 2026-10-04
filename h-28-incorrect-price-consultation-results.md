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
solodit_id: 1013
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/235

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
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[H-28] Incorrect Price Consultation Results

### Overview


This bug report is about the `TwapOracle.consult()` function in the 2021-11-vader project. This function is used to calculate the price of an asset based on UniswapV2 and Chainlink price data. The bug is that the protocol calculates the exchange rate incorrectly, resulting in false results. This can lead to issues in other parts of the protocol that rely on this data.

The bug is classified as high risk due to the false results it produces. To fix the issue, the result should be calculated as `sumUSD * token.decimals() * sumNative` instead. This would ensure the target token is denominated in USD and contains the correct number of decimals.

The bug was discovered through manual code review. Proof of concept code and similar working implementations are available in the report.

### Original Finding Content

_Submitted by leastwood_

#### Impact

The `TwapOracle.consult()` function iterates over all token pairs which belong to either `VADER` or USDV\` and then calculates the price of the respective asset by using both UniswapV2 and Chainlink price data. This helps to further protect against price manipulation attacks as the price is averaged out over the various registered token pairs.

Let's say we wanted to query the price of `USDV`, we would sum up any token pair where `USDV == pairData.token0`.

The sum consists of the following:

*   Price of `USDV` denominated in terms of `token1` (`USDV/token1`).
*   Price of token1 denominated in terms of `USD` (`token1/USD`).

Consider the following example:

*   `SUSHI` is the only registered token pair that exists alongside `USDV`.
*   Hence, calculating `sumNative` gives us an exchange rate that is denominated as `USDV/SUSHI`.
*   Similarly, `sumUSD` gives us the following denominated pair, `SUSHI/USD`.
*   I'd expect the result to equal `sumUSD * token.decimals() * sumNative` which should give us a USDV/USD denominated result.

However, the protocol calculates it as `(sumUSD * token.decimals()) / sumNative` which gives us a `SUSHI^2 / (USD*USDV)` denominated result. This seems incorrect.

I'd classify this issue as high risk as the oracle returns false results upon being consulted. This can lead to issues in other areas of the protocol that use this data in performing sensitive actions.

#### Proof of Concept

<https://github.com/code-423n4/2021-11-vader/blob/main/contracts/twap/TwapOracle.sol#L115-L157>

Similar working implementation listed below:

*   <https://github.com/gg2001/dpx-oracle/blob/master/contracts/UniswapV2Oracle.sol#L184-L211>
*   <https://github.com/gg2001/dpx-oracle/blob/master/contracts/UniswapV2Oracle.sol#L291-L304>

#### Tools Used

Manual code review.

#### Recommended Mitigation Steps

To calculate the correct consultation of a given token, the result should return `sumUSD * token.decimals() * sumNative` instead to ensure the target token to consult is denominated in `USD` and contains the correct number of decimals.

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/235#issuecomment-979182948):**
 > The description seems slightly incorrect as it uses a power where multiplication is performed but the general idea is correct.





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
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/235
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

