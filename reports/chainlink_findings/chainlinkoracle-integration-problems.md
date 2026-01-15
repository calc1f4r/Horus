---
# Core Classification
protocol: Conic Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29921
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#11-chainlinkoracle-integration-problems
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
  - MixBytes
---

## Vulnerability Title

ChainlinkOracle integration problems

### Overview


The report discusses issues with the current implementation of the interaction with Chainlink. There are four main problems identified: 

1. `ChainlinkOracle.isTokenSupported()` does not consider the case when a Chainlink feed has been abandoned and returns true even in this situation. 
2. `ChainlinkOracle._getPrice()` uses a deprecated function, `answeredInRound`, which can cause errors. 
3. `ChainlinkOracle._getPrice()` does not check for stale prices, which can lead to incorrect information being retrieved. 
4. `ChainlinkOracle.getUSDPrice()` has a check for `price_ != 0` which should be `price_ > 0` to account for potential negative values. 

To address these issues, the report recommends the following: 

1. Adding a check for abandoned pools in `isTokenSupported()`. 
2. Removing the deprecated `answeredInRound` check. 
3. Implementing checks for stale prices. 
4. Ensuring that `price_ > 0`.

### Original Finding Content

##### Description

There are several shortcomings in the current implementation of the interaction with Chainlink.

1. `ChainlinkOracle.isTokenSupported()` returns true if a Chainlink feed exists, but it does not consider the case when it has been abandoned (not updated for a long time):
```
function isTokenSupported(...) external view override returns (bool) {
   ...
   try _feedRegistry.getFeed(...) returns (IAggregatorV2V3) {
      return true;
   } catch Error(string memory) {
      try _feedRegistry.getFeed(...) returns (IAggregatorV2V3) {
         return true;
```
https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/oracles/ChainlinkOracle.sol#L52-L56

2. `ChainlinkOracle._getPrice()` uses the deprecated `answeredInRound`, see https://docs.chain.link/data-feeds/api-reference#latestrounddata
```
function _getPrice(
    ...
    require(answeredInRound_ >= roundID_, "stale price");
```
https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/oracles/ChainlinkOracle.sol#L83

3. `ChainlinkOracle._getPrice()` doesn't check for stale prices.

Each feed has a `heartbeat`, and for each call to [`latestRoundData()`](https://docs.chain.link/data-feeds/feed-registry/feed-registry-functions#latestrounddata) the equation `updatedAt < block.timestamp - heartbeat` must be checked, see https://ethereum.stackexchange.com/questions/133890/chainlink-latestrounddata-security-fresh-data-check-usage.

4. `ChainlinkOracle.getUSDPrice()` has a check for `price_ != 0` which should actually be `price_ > 0` since it is `int256` and could hypothetically be negative:
```
function _getPrice
    ...
    require(price_ != 0, "negative price");
```
https://github.com/ConicFinance/protocol/blob/7a66d26ef84f93059a811a189655e17c11d95f5c/contracts/oracles/ChainlinkOracle.sol#L82

##### Recommendation

Recommendations are as follows:
1. Add a check for abandoned pools in `isTokenSupported()`.
2. Remove the deprecated `answeredInRound` check.
3. Implement checks for stale prices.
4. Ensure the `price_ > 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Conic Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Conic%20Finance/Conic%20Finance%20v2/README.md#11-chainlinkoracle-integration-problems
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

