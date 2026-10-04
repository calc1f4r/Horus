---
# Core Classification
protocol: LMCV part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50696
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
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

DATA RETURNED FROM CHAINLINK IS NOT VALIDATED

### Overview


This bug report is about a function called `getLatestPrice` in the `ChainlinkClient.sol` contract. This function gets the latest asset price from a Chainlink aggregator. However, there are no checks on the `roundID` or `timeStamp`, which could lead to outdated prices being used. This could happen if there are problems with Chainlink starting a new round and finding consensus on the new value for the oracle. The impact of this bug is rated as 4 out of 10 and the likelihood is 2 out of 10. The recommendation is to add validation for the data returned from Chainlink. This bug has been solved by adding validation in the code.

### Original Finding Content

##### Description

The `getLatestPrice` function in the contract `ChainlinkClient.sol` fetches the asset price from a Chainlink aggregator using the latestRoundData function. However, there are no checks on `roundID` nor `timeStamp`, which may result in stale prices.

If there is a problem with Chainlink starting a new round and finding consensus on the new value for the oracle (e.g., Chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the Chainlink system), consumers of this contract may continue using outdated stale data (if oracles are unable to submit no new round is started).

Code Location
-------------

#### contracts/lmcv/ChainlinkClient.sol

```
function getLatestPrice() public view returns (int256) {
    (
        /*uint80 roundID*/,
        int256 price,
        /*uint startedAt*/,
        /*uint timeStamp*/,
        /*uint80 answeredInRound*/
    ) = priceFeed.latestRoundData();
    return price;
}

```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

**SOLVED**: Validation of data returned from Chainlink was added.

Reference: [ChainlinkClient.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/ChainlinkClient.sol#L29)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

