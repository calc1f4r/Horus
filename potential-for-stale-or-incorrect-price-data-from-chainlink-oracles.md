---
# Core Classification
protocol: Sakazuki
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35618
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-27-Sakazuki.md
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

Potential for Stale or Incorrect Price Data from Chainlink Oracles

### Overview


This bug report is about a problem in the `SakazukiSilver` smart contract that uses Chainlink oracles to get real-time exchange rates for ETH/USD and JPY/USD. The issue is that sometimes the data received from Chainlink can be old or incorrect, which can affect the prices of NFTs being minted. This could lead to overvaluing or undervaluing NFTs, which can impact the financial integrity and user confidence in the platform. The recommendation is to add validation checks in the smart contract to ensure that the data received from Chainlink is accurate and up-to-date.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**:

The `SakazukiSilver` smart contract utilizes Chainlink oracles to obtain real-time exchange rates for ETH/USD and JPY/USD, which are crucial for calculating the dynamic minting prices of NFTs. However, there is a significant risk associated with the potential of receiving stale or incorrect data from Chainlink oracles. This can happen due to delays in starting new rounds, consensus issues among Chainlink nodes, network congestion, or vulnerabilities/attacks on the Chainlink system. Using outdated or incorrect data for price calculation could lead to improper NFT pricing, either overvaluing or undervaluing the minted NFTs, which impacts the financial integrity and user confidence in the platform.

**Recommendation**

Implement immediate validation checks within the smart contract when fetching the latest round data from Chainlink oracles. Example checks include:
```solidity
(uint80 roundID, int price, , uint256 updateTime, uint80 answeredInRound) = AggregatorV3Interface(oracleAddress).latestRoundData();
require(price > 0, "Chainlink price <= 0");
require(updateTime != 0, "Incomplete round");
require(answeredInRound >= roundID, "Stale price");
```
These checks ensure that the price is positive, the round of data is complete, and the data is not stale.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Sakazuki |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-27-Sakazuki.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

