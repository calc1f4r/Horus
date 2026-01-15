---
# Core Classification
protocol: OpalProtocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40767
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007
source_link: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
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
finders_count: 9
finders:
  - 8olidity
  - bronzepickaxe
  - 0xhashiman
  - AuditorPraise
  - Chad0
---

## Vulnerability Title

Chainlink 's latestrounddata might return stale or incorrect results 

### Overview


The BPTOracle.sol file has a bug in line 242 where the latestRoundData() function does not check if the data returned is outdated. This could result in incorrect values being returned from the oracle, which could compromise the security of the protocol. According to Chainlink documentation, this could lead to prices being stale. To fix this issue, checks need to be added to verify the accuracy of the data. This can be done by adding the following code: (uint80 roundID, int256 answer, uint256 timestamp, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData(); if (updatedAt + tokenHeartbeat[token] < block.timestamp) revert StalePrice(); require(timestamp != 0, "Round not complete"); require(answeredInRound >= roundID, "Stale Price"); require(answer > 0, "Invalid Price"). This will ensure that the data is up-to-date and accurate.

### Original Finding Content

## BPTOracle.sol#L242

## Description
In `BPTOracle.sol`, we are using the `latestRoundData()` function, but there is no check if the return value indicates stale data. This could lead to potentially incorrect values being returned from the oracle, which would compromise the security of the protocol. This could lead to stale prices according to the Chainlink documentation.

## Recommendation
The issue can be mitigated by adding checks that will verify the correctness of the data:

```solidity
(uint80 roundID, int256 answer, uint256 timestamp, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData();
if (updatedAt + tokenHeartbeat[token] < block.timestamp) revert StalePrice();
require(timestamp != 0, "Round not complete");
require(answeredInRound >= roundID, "Stale Price");
require(answer > 0, "Invalid Price");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | OpalProtocol |
| Report Date | N/A |
| Finders | 8olidity, bronzepickaxe, 0xhashiman, AuditorPraise, Chad0, J4X98, z, erbyte, Naveen Kumar Naik J - 1nc0gn170 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_opal_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0c9f46ff-e5b4-412c-b928-ecb135f44007

### Keywords for Search

`vulnerability`

