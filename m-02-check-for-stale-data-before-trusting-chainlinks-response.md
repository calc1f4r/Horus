---
# Core Classification
protocol: Dyad
chain: everychain
category: oracle
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: oracle

# Source Information
source: solodit
solodit_id: 18768
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
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
  - validation
  - stale_price
  - oracle

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[M-02] Check for stale data before trusting Chainlink's response

### Overview


This bug report is about the math in a protocol that is based on the data provided by Chainlink's ETH-USD feed. According to Chainlink's documentation, the data needs to be checked for freshness and accuracy. To do this, the _getEthPrice() function should be updated with two checks, as seen in the code snippet included in the report. This recommendation was reviewed and confirmed in the pull request #10, which can be found in the Github repository for DyadStablecoin contracts-v3.

### Original Finding Content

Much of the math in the protocol is based on the data provided by Chainlink's ETH-USD feed.

According to [Chainlink's documentation](https://docs.chain.link/data-feeds/price-feeds/historical-data), it is important to provide additional checks that the data is fresh:

- If answeredInRound is less than roundId, the answer is being carried over.
- A timestamp with zero value means the round is not complete and should not be used.

**Recommendation**

Add the following checks to the \_getEthPrice() function to ensure the data is fresh and accurate:

```solidity
function _getEthPrice() public view returns (uint) {
(uint80 roundID, int256 price,, uint256 timeStamp, uint80 answeredInRound) = oracle.latestRoundData();
require(timeStamp != 0);
require(answeredInRound >= roundID);
return price.toUint256();
}
```

**Review**
Fix confirmed in [PR #10](https://github.com/DyadStablecoin/contracts-v3/pull/10).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Validation, Stale Price, Oracle`

