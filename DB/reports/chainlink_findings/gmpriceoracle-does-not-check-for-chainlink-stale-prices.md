---
# Core Classification
protocol: GMI and Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51842
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
source_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
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

GMPriceOracle does not check for Chainlink stale prices

### Overview


Chainlink feeds are used to get the latest price for assets on the Gloop Finance platform. However, the `GMPriceOracle` code does not check if the returned price data is stale, which can result in incorrect prices being used and potentially causing losses for users and the platform. The recommended solution is to compare the returned timestamp against a staleness factor and revert the transaction if the price data is too old. The Gloop Finance team has solved this issue by implementing this solution.

### Original Finding Content

##### Description

Chainlink feeds return the time where the price feed was updated with the latest price. This is done to make it possible for developers to choose to either use a price or not if it is considered too old. However, the `GMPriceOracle` does not check this. If the returned pricing data is stale, the code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for the user and/or the protocol, even liquidating users unfairly. It can be seen in the implementation of the `getPriceFromChainlink`:

<https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/GMPriceOracle.sol#L59C1-L69C6>

```
    function getPriceFromChainlink(address feedId) internal view returns (uint256) {
        AggregatorV3Interface dataFeed = AggregatorV3Interface(feedId);
        (
            ,
            /* uint80 roundID */ int answer /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/,
            ,
            ,

        ) = dataFeed.latestRoundData();
        return uint256(answer);
    }
```

that it does not check anything and returns `answer` without further validation of whether it is a stale price or not.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U)

##### Recommendation

Compare the returned `timeStamp` against a staleness factor to revert the transaction if the price data is too old. Moreover, as it is a generic implementation for all assets being used by the system, take into account that different feeds have different heartbeats so you would need to have a mapping of assets to staleness factors. You can check [Chainlink’s list of Ethereum mainnet price feeds](https://docs.chain.link/data-feeds/price-feeds/addresses/?network=ethereum), selecting the “Show More Details” box, which will show the “Heartbeat” column for each feed, and use those values in your implementation.

### Remediation Plan

**SOLVED:** The **Gloop Finance team** solved this issue as recommended above.

##### Remediation Hash

<https://github.com/GloopFinance/gm-lending-protocol/commit/9f79538287d22ed076b95760483203dfe37ac0f2#diff-dfbed02222b608a1b2e2157b7482a24afffe2c989483c72fe6750d1849532e44>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | GMI and Lending |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending

### Keywords for Search

`vulnerability`

