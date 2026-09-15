---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37099
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
  - Zokyo
---

## Vulnerability Title

No Price Staleness Check

### Overview


The function latestRoundData() is not properly checking for outdated prices of an asset. This means that the reported price may not be accurate. The client has recommended implementing checks for the roundId and timestamp to ensure the price is up-to-date. This will help prevent any issues with loans.

### Original Finding Content

**Severity** - Medium

**Status** - Acknowledged

**Description**

The function latestRoundData() has been used to fetch the price of an asset, but there are no price staleness checks.
Instances:
L24 -> AggregatedChainnlinkOracle.sol
L25 -> WBTCOracle.sol


There should be checks for the roundId and timestamp , i.e.
```solidity
(uint80 roundID, int256 answer, , uint256 timestamp, uint80 answeredInRound) = _btcUsdFeed.latestRoundData();
require(answeredInRound >= roundID, "Stale price");
require(timestamp != 0,"Round not complete");
```

**Recommendation**:

Introduce price staleness checks.
**Comment**: The client has suggested they can monitor their oracles for the StalePrice event and replace the oracles asap without disrupting the loans

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

