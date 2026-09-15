---
# Core Classification
protocol: Foundry DeFi Stablecoin CodeHawks Audit Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34423
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0
source_link: none
github_link: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin

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
finders_count: 49
finders:
  - RugpullDetector
  - 0xdeadbeef
  - ni8mare
  - chainNue
  - 0xRizwan
---

## Vulnerability Title

staleCheckLatestRoundData() does not check the status of the Arbitrum sequencer in Chainlink feeds.

### Overview


This bug report discusses an issue with a function called staleCheckLatestRoundData() in a contract that uses Chainlink in L2 chains like Arbitrum. This function does not check the status of the Arbitrum sequencer, which can lead to outdated data being used in the event of an outage. This can impact the accuracy of prices and affect operations. The report recommends adding a verification step to check the active status of the sequencer before trusting the data. A code example is provided for reference.

### Original Finding Content

## Summary

Given that the contract will be deployed on any EVM chain, when utilizing Chainlink in L2 chains like Arbitrum, it's important to ensure that the prices provided are not falsely perceived as fresh particularly in scenarios where the sequencer might be non-operational. Hence, a critical step involves confirming the active status of the sequencer before trusting the data returned by the oracle.


## Vulnerability Details

In the event of an Arbitrum Sequencer outage, the oracle data may become outdated, potentially leading to staleness. While the function  staleCheckLatestRoundData() provides checks if a price is stale, it does not check if Arbirtrum Sequencer is active. Since OracleLib.sol library is used to check the Chainlink Oracle for stale data, it is important to add this verification. You can review Chainlink docs on L2 Sequencer Uptime Feeds for more details on this. https://docs.chain.link/data-feeds/l2-sequencer-feeds 


## Impact

In the scenario where the Arbitrum sequencer experiences an outage, the protocol will enable users to maintain their operations based on the previous (stale) rates.


## Tools Used

Manual Review

## Recommendations


There is a code example on Chainlink docs for this scenario: https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code. 
For illustrative purposes this can be:

```
function isSequencerAlive() internal view returns (bool) {
    (, int256 answer, uint256 startedAt,,) = sequencer.latestRoundData();
    if (block.timestamp - startedAt <= GRACE_PERIOD_TIME || answer == 1)
        return false;
    return true;
}


function staleCheckLatestRoundData(AggregatorV3Interface priceFeed)
        public
        view
        returns (uint80, int256, uint256, uint256, uint80)
    {
require(isSequencerAlive(), "Sequencer is down");
       ....//remaining parts of the function
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | RugpullDetector, 0xdeadbeef, ni8mare, chainNue, 0xRizwan, sm4rty, CircleLooper, JMTT, tsvetanovv, Phantasmagoria, zaevlad, Polaristow, Avci, Juntao, serialcoder, mau, pks27, 0x9527, T1MOH, 0xMosh, twcctop, aviggiano, ss3434, Bauer, natzuu, crippie, nicobevi, Niki, Madalad, 0x3b, Flint14si2o, Bauchibred, 33audits, Crunch, owade, StErMi, ABA, paspe, darkart, pep7siup, pengun, tsar, MrjoryStewartBaxter, siguint, AlexCzm, BenRai, honeymewn, Shogoki |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`

