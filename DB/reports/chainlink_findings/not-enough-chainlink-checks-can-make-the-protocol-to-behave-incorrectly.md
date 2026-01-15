---
# Core Classification
protocol: Beyond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45753
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Not enough Chainlink checks can make the protocol to behave incorrectly

### Overview


Severity: Critical

Status: Resolved

Description:

The `TokenBridge.Base.sol` smart contract has a function called `getChainlinkDataFeedLatestAnswer()` which is used to retrieve asset prices using Chainlink Price Feeds. However, there are several checks that need to be implemented in order for the function to work properly. These include using a try-catch block to handle multisig accounts blocking access to price feeds, checking if the sequencer is down, and ensuring that the staleFeedThreshold is unique for each data feed.

Recommendation:

Implement the necessary checks to ensure the correct behavior of price feeds. For more detailed instructions on how to implement these fixes, refer to the thread at https://x.com/saxenism/status/1656632735291588609.

### Original Finding Content

**Severity**: Critical	

**Status**: Resolved

**Description**

The `TokenBridge.Base.sol` smart contract implements a `getChainlinkDataFeedLatestAnswer()` function which uses Chainlink Price Feeds to retrieve asset’s prices:
```solidity
/**
    * Returns the latest answer
    * @param dataFeed Chainlink data feed
    * @return answer The latest answer
    */
   function getChainlinkDataFeedLatestAnswer( 
       AggregatorV3Interface dataFeed
   ) internal view returns (int) {
       // prettier-ignore
       (
           /* uint80 roundId */,
           int answer,
           /* uint startedAt */,
           /* uint updatedAt */,
           /* uint80 answeredInRound */
       ) = dataFeed.latestRoundData();
       return answer;
   }
```

However, retrieving asset’s prices using Chainlink Price Feeds requires several checks that must be implemented to ensure its correct behaviour:

The `latestRoundData()` call should be wrapped by a try-catch block because multisig accounts can block the access to price feeds, leading the execution to revert.

It is needed to check if the sequencer is down: Optimistic rollup protocols move all execution off the layer 1 (L1) Ethereum chain, complete execution on a layer 2 (L2) chain, and return the results of the L2 execution back to the L1. These protocols have a sequencer that executes and rolls up the L2 transactions by batching multiple transactions into a single transaction. If a sequencer becomes unavailable, it is impossible to access read/write APIs that consumers are using and applications on the L2 network will be down for most users without interacting directly through the L1 optimistic rollup contracts. The L2 has not stopped, but it would be unfair to continue providing service on your applications when only a few users can use them. Check the official documentation: https://docs.chain.link/data-feeds/l2-sequencer-feeds
The staleFeedThreshold should be unique for each data feed because their heartbeats varies.

**Recommendation**:

Implement the necessary mentioned checks to ensure the correct behavior of price feeds. You can consult this thread for a more in detail explanation on how to implement each fix: https://x.com/saxenism/status/1656632735291588609

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Beyond |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-24-Beyond.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

