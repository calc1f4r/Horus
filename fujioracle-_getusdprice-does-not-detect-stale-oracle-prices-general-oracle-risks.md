---
# Core Classification
protocol: Fuji Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16535
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

FujiOracle - _getUSDPrice does not detect stale oracle prices; General Oracle Risks

### Overview


This bug report is about the external Chainlink oracle, which provides index price information to a system. It is possible that the oracle could become outdated or fail to be maintained, leading to incorrect data being fed into the index price calculations. This is especially a risk for lesser-known tokens with fewer ChainLink Price feeds. To reduce reliance on off-chain components and increase the resiliency of the smart contract system, the codebase needs to be updated to check the timestamp and answeredIn round of the returned price.

The code currently only relies on chainLinkOracle.latestRoundData() and does not check the timestamp or answeredIn round of the returned price. It is recommended to perform sanity checks on the price returned by the oracle, such as checking if the price is older than a configured limit, and reverting or handling it in other means if it is. Additionally, consider adding minimally invasive functionality to pause the price-feeds if the oracle becomes unreliable, and monitor the oracle data off-chain and intervene if it becomes unreliable.

On-chain, it is recommended to check both the answeredInRound and updatedAt within acceptable bounds. This should be combined with a threshold for the roundId and updatedAt, which would allow a deviation of threshold rounds and ensure that stale data is not used if there are no more rounds.

### Original Finding Content

#### Description


The external Chainlink oracle, which provides index price information to the system, introduces risk inherent to any dependency on third-party data sources. For example, the oracle could fall behind or otherwise fail to be maintained, resulting in outdated data being fed to the index price calculations. Oracle reliance has historically resulted in crippled on-chain systems, and complications that lead to these outcomes can arise from things as simple as network congestion.


This is more extreme in lesser-known tokens with fewer ChainLink Price feeds to update the price frequently.


Ensuring that unexpected oracle return values are correctly handled will reduce reliance on off-chain components and increase the resiliency of the smart contract system that depends on them.


The codebase, as is, relies on `chainLinkOracle.latestRoundData()` and does not check the `timestamp` or `answeredIn` round of the returned price.


#### Examples


* Here’s how the oracle is consumed, skipping any fields that would allow checking for stale data:


**code/contracts/FujiOracle.sol:L66-L77**



```
/\*\*
 \* @dev Calculates the USD price of asset.
 \* @param \_asset: the asset address.
 \* Returns the USD price of the given asset
 \*/
function \_getUSDPrice(address \_asset) internal view returns (uint256 price) {
 require(usdPriceFeeds[\_asset] != address(0), Errors.ORACLE\_NONE\_PRICE\_FEED);

 (, int256 latestPrice, , , ) = AggregatorV3Interface(usdPriceFeeds[\_asset]).latestRoundData();

 price = uint256(latestPrice);
}

```
* Here’s the implementation of the v0.6 FluxAggregator Chainlink feed with a note that timestamps should be checked.


**contracts/src/v0.6/FluxAggregator.sol:L489-L490**



```
\* @return updatedAt is the timestamp when the round last was updated (i.e.
\* answer was last computed)

```
#### Recommendation


Perform sanity checks on the price returned by the oracle. If the price is older, not within configured limits, revert or handle in other means.


The oracle does not provide any means to remove a potentially broken price-feed (e.g., by updating its address to `address(0)` or by pausing specific feeds or the complete oracle). The only way to pause an oracle right now is to deploy a new oracle contract. Therefore, consider adding minimally invasive functionality to pause the price-feeds if the oracle becomes unreliable.


Monitor the oracle data off-chain and intervene if it becomes unreliable.


On-chain, realistically, both `answeredInRound` and `updatedAt` must be checked within acceptable bounds.


* `answeredInRound == latestRound` - in this case, data may be assumed to be fresh while it might not be because the feed was entirely abandoned by nodes (no one starting a new round). Also, there’s a good chance that many feeds won’t always be super up-to-date (it might be acceptable to allow a threshold). A strict check might lead to transactions failing (race; e.g., round just timed out).
* `roundId + threshold >= answeredInRound` - would allow a deviation of threshold rounds. This check alone might still result in stale data to be used if there are no more rounds. Therefore, this should be combined with `updatedAt + threshold >= block.timestamp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fuji Protocol |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

