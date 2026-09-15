---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4060
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-fairside-contest
source_link: https://code4rena.com/reports/2021-05-fairside
github_link: https://github.com/code-423n4/2021-05-fairside-findings/issues/70

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
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-09] Should check return data from Chainlink aggregators

### Overview


This bug report is about the `getEtherPrice` function in the contract `FSDNetwork`, which fetches the ETH price from a Chainlink aggregator using the `latestRoundData` function. However, there are no checks on `roundID` nor `timeStamp`, resulting in stale prices. This could lead to incorrect pricing, and thus, incorrect calculations in the contract.

The proof of concept can be seen in the referenced code, which is FSDNetwork.sol#L376-L381. The recommended mitigation steps are to add checks on the return data with proper revert messages if the price is stale or the round is uncomplete. This would ensure that the data is up to date and correct.

### Original Finding Content


The `getEtherPrice` function in the contract `FSDNetwork` fetches the ETH price from a Chainlink aggregator using the `latestRoundData` function. However, there are no checks on `roundID` nor `timeStamp`, resulting in stale prices.

Recommend adding checks on the return data with proper revert messages if the price is stale or the round is incomplete, for example:
```Solidity
(uint80 roundID, int256 price, , uint256 timeStamp, uint80 answeredInRound) = ETH_CHAINLINK.latestRoundData();
require(answeredInRound >= roundID, "...");
require(timeStamp != 0, "...");
```

**[fairside-core (FairSide) confirmed](https://github.com/code-423n4/2021-05-fairside-findings/issues/70#issuecomment-851051273):**
 > Fixed in [PR#7](https://github.com/fairside-core/2021-05-fairside/pull/7).

**[cemozerr (Judge) commented](https://github.com/code-423n4/2021-05-fairside-findings/issues/70#issuecomment-857059051):**
 > Labeling this as medium risk as stale ether price could put funds at risk.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-fairside
- **GitHub**: https://github.com/code-423n4/2021-05-fairside-findings/issues/70
- **Contest**: https://code4rena.com/contests/2021-05-fairside-contest

### Keywords for Search

`vulnerability`

