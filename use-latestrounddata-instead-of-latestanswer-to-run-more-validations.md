---
# Core Classification
protocol: Ocean Protocol H2O System and Action
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50385
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
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

USE LATESTROUNDDATA INSTEAD OF LATESTANSWER TO RUN MORE VALIDATIONS

### Overview


This bug report discusses an issue with the Chainlink contract. The contract uses a method called latestAnswer to get asset prices, but this method is now deprecated. This can cause problems because the prices may not be up-to-date, which can affect an account's health and lead to incorrect liquidation prices. The report recommends using the latestRoundData method instead, which allows for extra validations and reduces the risk of using stale prices. The report also includes a code location and a score for the impact and likelihood of the bug. However, the issue has been solved by the H2O team through a series of commits, which added additional validation and now uses the latestRoundData method.

### Original Finding Content

##### Description

Chainlink contract are calling latestAnswer to get the asset prices. The latestAnswer is deprecated. Freshness of the returned price should be checked, since it affects an account's health (and therefore liquidations). Stale prices that do not reflect the current market price anymore could be used, which would influence the liquidation pricing. This method will return the last value, but you won’t be able to check if the data is fresh. On the other hand, calling the method latestRoundData allow you to run some extra validations. Stale prices can put funds in a risk. According to Chainlink's documentation, This function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the Price oracle. (https://docs.chain.link/docs/historical-price-data/#solidity). Furthermore, latestAnswer is deprecated. (https://docs.chain.link/docs/price-feeds-api-reference/))

Code Location
-------------

[Chainlink Integration](https://github.com/reflexer-labs/geb-chainlink-median/blob/master/src/ChainlinkRelayer.sol#L114)

#### Chainlink Integration

```
    function read() external view returns (uint256) {
        // The relayer must not be null
        require(address(chainlinkAggregator) != address(0), "ChainlinkRelayer/null-aggregator");

        // Fetch values from Chainlink
        uint256 medianPrice         = multiply(uint(chainlinkAggregator.latestAnswer()), 10 ** uint(multiplier));
        uint256 aggregatorTimestamp = chainlinkAggregator.latestTimestamp();

        require(both(medianPrice > 0, subtract(now, aggregatorTimestamp) <= staleThreshold), "ChainlinkRelayer/invalid-price-feed");
        return medianPrice;
    }

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: The `H2O team` solved the above issue in the following commits

* [b6cc5edc266b78a48a1f1f09bd9d229a73619c50](https://github.com/stablecoin-research/h2o-chainlink-median/commit/b6cc5edc266b78a48a1f1f09bd9d229a73619c50)
* [3a3ed51516b53d8ed16b703e07452f8edfb5019b](https://github.com/stablecoin-research/h2o-chainlink-median/commit/3a3ed51516b53d8ed16b703e07452f8edfb5019b)
* [eafcca39e12a33db609bc2a371275fd809e68815](https://github.com/stablecoin-research/h2o-chainlink-median/commit/eafcca39e12a33db609bc2a371275fd809e68815)

As a result, the team added the additional validation and now uses `latestRoundData`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ocean Protocol H2O System and Action |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

