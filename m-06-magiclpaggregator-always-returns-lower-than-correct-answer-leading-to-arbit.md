---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32062
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-abracadabra-money
source_link: https://code4rena.com/reports/2024-03-abracadabra-money
github_link: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/223

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
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-06] MagicLpAggregator always returns lower than correct answer, leading to arbitrage loss

### Overview


The MagicLpAggregator is a tool used to determine the value of LP tokens for related underlying tokens. However, there is a bug in the code that allows for easy arbitrage opportunities. This means that an attacker can buy LP tokens at a lower price, withdraw the underlying tokens, and sell them for a higher price, resulting in a profit. This causes a loss of value for LP holders. To fix this issue, it is recommended to calculate the value based on the real underlying token value multiplied by the amount. It is also suggested to create two separate oracles for lower and upper bound results to prevent this type of arbitrage. Some users have also reported potential rounding errors in the code. 

### Original Finding Content


MagicLpAggregator is used to price LP tokens for "closely-tied" underlying tokens. It calculates the price below:

    function latestAnswer() public view override returns (int256) {
        uint256 baseAnswerNomalized = uint256(baseOracle.latestAnswer()) * (10 ** (WAD - baseOracle.decimals()));
        uint256 quoteAnswerNormalized = uint256(quoteOracle.latestAnswer()) * (10 ** (WAD - quoteOracle.decimals()));
        uint256 minAnswer = baseAnswerNomalized < quoteAnswerNormalized ? baseAnswerNomalized : quoteAnswerNormalized;
        (uint256 baseReserve, uint256 quoteReserve) = _getReserves();
        baseReserve = baseReserve * (10 ** (WAD - baseDecimals));
        quoteReserve = quoteReserve * (10 ** (WAD - quoteDecimals));
        return int256(minAnswer * (baseReserve + quoteReserve) / pair.totalSupply());
    }

The code takes the minimal answer between the underlying oracles and considers all reserves to be worth that amount:
`return int256(minAnswer * (baseReserve + quoteReserve) / pair.totalSupply());`

The issue is that any difference in price between the assets represents an easy arbitrage opportunity. Suppose we have tokens (A,B), where real oracle shows:

*   A = $0.99
*   B = $1

The Pool has 1000000 LP tokens and contains:

*   1000000 A
*   1000000 B

The LP value would calculate as:
`0.99 * 2000000 / 1000000 = $1.98`
The actual value is:
`(0.99 * 1000000 + 1 * 1000000) / 1000000 = $1.99`

Suppose a platform trades LPs using the aggregator pricing. An attacker could:

*   Buy 100,000 LP tokens at $198000
*   Withdraw from the pool the underlying shares
*   Sell 100,000 A, 100,000 B at $199000
*   Profit $1000 from the exchange, when the difference is just $0.01 (this is very common fluctuation even with pegged assets).

The delta comes at the expense of LP holders whose position gets minimized.

### Impact

Loss of value due to arbitrage of any platform using MagicLpAggregator pricing.

### Recommended Mitigation Steps

Always calculate the value based on the real underlying token value multiplied by amount.

Consider creating two separate oracles for lower-bound and upper-bound results. Then a lending protocol could indeed use the lower-bound for determining collateral value.

**[0xm3rlin (Abracadabra) disputed and commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/223#issuecomment-1998696507):**
 > Intended behavior.

**[141345 (Lookout) commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/223#issuecomment-1999800615):**
 > Rounding error could accumulate in MagicLpAggregator.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-abracadabra-money
- **GitHub**: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/223
- **Contest**: https://code4rena.com/reports/2024-03-abracadabra-money

### Keywords for Search

`vulnerability`

