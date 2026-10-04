---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51102
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
source_link: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
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

LATESTANSWER CALL MAY RETURN STALE RESULTS

### Overview


The `ChainlinkOracle` contract has a function called `getChainlinkPrice()` which is used to retrieve prices from different Chainlink aggregators. However, this function is deprecated and should not be used according to Chainlink's documentation. Additionally, using `latestAnswer()` in this function could result in returning invalid or old prices. The BVSS rating for this issue is 6.3, which is moderate. The Irrigation Protocol team has solved this issue by implementing the recommended solution and the commit ID for this fix is 57d3945089a52425b91cdc8005b62b73d5648c68.

### Original Finding Content

##### Description

In the `ChainlinkOracle` contract, the function `getChainlinkPrice()` is used to retrieve prices from different Chainlink aggregators:

#### ChainlinkOracle.sol

```
/// @dev returns price with decimals 18
function getChainlinkPrice(AggregatorV2V3Interface feed) internal view returns (uint256) {
    // Chainlink USD-denominated feeds store answers at 8 decimals
    uint256 decimalDelta = uint256(18) - feed.decimals();
    // Ensure that we don't multiply the result by 0
    if (decimalDelta > 0) {
        return uint256(feed.latestAnswer()) * 10 ** decimalDelta;
    } else {
        return uint256(feed.latestAnswer());
    }
}

```

According to the [Chainlink's documentation](https://docs.chain.link/data-feeds/api-reference#latestanswer) this function is deprecated and should not be used. Moreover, using `latestAnswer()` could lead to return invalid/stale prices.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:C (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

**SOLVED:** The `Irrigation Protocol team` solved the issue by implementing the recommended solution.

`Commit ID :` [57d3945089a52425b91cdc8005b62b73d5648c68](https://github.com/IrrigationProtocol/irrigation-contracts-diamond/commit/57d3945089a52425b91cdc8005b62b73d5648c68).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/irrigation/protocol-smart-contract-security-assessment-2

### Keywords for Search

`vulnerability`

