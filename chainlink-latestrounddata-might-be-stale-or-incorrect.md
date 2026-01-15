---
# Core Classification
protocol: Exchange V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51091
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

CHAINLINK LATESTROUNDDATA MIGHT BE STALE OR INCORRECT

### Overview


This bug report is about a problem with the Substance Exchange platform, specifically with the way it uses Chainlink as its price oracle. The issue is that when buying or selling a type of currency called `sUSD`, the platform is not properly checking for the most recent update of the underlying token's price. This can lead to accepting outdated data, which could cause problems in a volatile market. The code that needs to be fixed can be found in the SubstanceUSD.sol file, specifically on line 92. The report also includes a BVSS score, which rates the severity of the bug, and a recommendation for fixing the issue. It appears that the client team has already solved the problem in a recent commit. 

### Original Finding Content

##### Description

Substance Exchange uses Chainlink as its price oracle. When buying or selling `sUSD`, the `SubstanceUSD` contract queries Chainlink for the underlying token price using the `latestRoundData()` function. This function returns `uint80 roundId`, `int256 answer`, `uint256 startedAt`, `uint256 updatedAt` and `uint80 answeredInRound`. `roundId` denotes the identifier of the most recent update round, `answer` is the price of the asset, `startedAt` is the timestamp at which the round started and `updatedAt` is the timestamp at which the feed was updated. The `getPrice()` function does not check if the feed was updated at the most recent round nor does it verify the update timestamp against the current time, and this can result in accepting stale data which may threaten the stability of the exchange in a volatile market.

Code Location
-------------

[SubstanceUSD.sol#L92](https://github.com/ElijahYao/SubstanceExchangeV1/blob/d122e2c3332478f293d7759465f6739d295ca55e/contracts/core/SubstanceUSD.sol#L92)

#### SubstanceUSD.sol

```
    function getPrice(address token, bool min) public view returns (uint256 price) {
        address oracle = underlyingToken[token].oracle;
        if (oracle == address(0)) {
            revert SubstanceUSD__InvalidToken();
        }
        (, int256 oraclePrice, , , ) = AggregatorV3Interface(oracle).latestRoundData();
        if (oraclePrice <= 0) {
            revert SubstanceUSD__InvalidOraclePrice();
        }
        uint8 pDecimals = AggregatorV3Interface(oracle).decimals();
        price = (uint256(oraclePrice) * PRECISION) / (10**pDecimals);
        price = min ? Math.min(PRECISION, price) : Math.max(PRECISION, price);
    }

```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:C/D:N/Y:N/R:N/S:U (6.7)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:C/D:N/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The \client team solved this issue in commit [7717277a](https://github.com/ElijahYao/SubstanceExchangeV1/commit/https://github.com/ElijahYao/SubstanceExchangeV1/commit/7717277a15aef6b703a5cf9670509b2f0b1bd3fc).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Exchange V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

