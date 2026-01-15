---
# Core Classification
protocol: EVM Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50168
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
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

USE OF DEPRECATED CHAINLINK API

### Overview


The `ChainlinkOracle` contract uses an outdated method called `latestAnswer()` from Chainlink's API. This method may suddenly stop working if Chainlink stops supporting outdated APIs. This can cause issues with retrieving the latest value. The code location of this issue is in the `ChainlinkOracle.sol` file. The impact and likelihood of this issue are both rated as 3 out of 5. The recommended solution is to use a better Chainlink Oracle API call, specifically `latestRoundData()`. The issue has been solved with the implementation of this new API call in the code, which can be found in the `Commit ID` e23657c5fbeb12c7393fa49da6f350dc0bd5114e and 762cdc4cd9a8d09f29765f9e143b25af0ebe9720.

### Original Finding Content

##### Description

The `ChainlinkOracle` contract uses Chainlink’s deprecated API `latestAnswer()`. Such functions might suddenly stop working if Chainlink stopped supporting deprecated APIs. This method will return the last value, but it is possible to check if the data is fresh.

Code Location
-------------

#### ChainlinkOracle.sol

```
function getChainlinkPrice(AggregatorV2V3Interface feed) internal view returns (uint) {
        // Chainlink USD-denominated feeds store answers at 8 decimals
        uint decimalDelta = uint(18).sub(feed.decimals());
        // Ensure that we don't multiply the result by 0
        if (decimalDelta > 0) {
            return uint(feed.latestAnswer()).mul(10**decimalDelta);
        } else {
            return uint(feed.latestAnswer());
        }
    }

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED:** This issue was solved by implementing better ChainLink Oracle API call (`latestRoundData()`).

`Commit ID:` **e23657c5fbeb12c7393fa49da6f350dc0bd5114e** && **762cdc4cd9a8d09f29765f9e143b25af0ebe9720**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

