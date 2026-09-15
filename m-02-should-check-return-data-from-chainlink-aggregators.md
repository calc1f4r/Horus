---
# Core Classification
protocol: Yeti Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1206
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-yeti-finance-contest
source_link: https://code4rena.com/reports/2021-12-yetifinance
github_link: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/91

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
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh  WatchPug
  - defsec
---

## Vulnerability Title

[M-02] Should check return data from Chainlink aggregators

### Overview


This bug report concerns the latestRoundData function in the contract PriceFeed.sol which fetches the asset price from a Chainlink aggregator. The function does not check the roundID, resulting in the possibility of stale prices which could put funds at risk. This is because the function does not error if no answer has been reached and returns 0, causing an incorrect price fed to the PriceOracle. The external Chainlink oracle, which provides index price information to the system, introduces risk inherent to any dependency on third-party data sources. 

The proof of concept involves navigating to the contract and checking the implemented checks. The recommended mitigation steps are to add checks on the return data with proper revert messages if the price is stale or the round is incomplete. This can be done by adding code such as "require(price > 0, "Chainlink price <= 0"); require(answeredInRound >= roundID, "..."); require(timeStamp != 0, "...");". 

Overall, this bug report explains that the latestRoundData function in the contract PriceFeed.sol does not check the roundID, resulting in the possibility of stale prices which could put funds at risk. The proof of concept and recommended mitigation steps are also provided.

### Original Finding Content

_Submitted by defsec, also found by hyh and WatchPug_

#### Impact

The latestRoundData function in the contract PriceFeed.sol fetches the asset price from a Chainlink aggregator using the latestRoundData function. However, there are no checks on roundID.

Stale prices could put funds at risk. According to Chainlink's documentation, This function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the PriceOracle. The external Chainlink oracle, which provides index price information to the system, introduces risk inherent to any dependency on third-party data sources. For example, the oracle could fall behind or otherwise fail to be maintained, resulting in outdated data being fed to the index price calculations of the liquidity.

Example Medium Issue : <https://github.com/code-423n4/2021-08-notional-findings/issues/18>

#### Proof of Concept

1.  Navigate to the following contract.

<https://github.com/code-423n4/2021-12-yetifinance/blob/1da782328ce4067f9654c3594a34014b0329130a/packages/contracts/contracts/PriceFeed.sol#L578>

2.  Only the following checks are implemented.

```js
    if (!_response.success) {return true;}
    // Check for an invalid roundId that is 0
    if (_response.roundId == 0) {return true;}
    // Check for an invalid timeStamp that is 0, or in the future
    if (_response.timestamp == 0 || _response.timestamp > block.timestamp) {return true;}
    // Check for non-positive price
    if (_response.answer <= 0) {return true;}
```

#### Recommended Mitigation Steps

Consider to add checks on the return data with proper revert messages if the price is stale or the round is incomplete, for example:
```solidity
(uint80 roundID, int256 price, , uint256 timeStamp, uint80 answeredInRound) = ETH_CHAINLINK.latestRoundData();
require(price > 0, "Chainlink price <= 0"); 
require(answeredInRound >= roundID, "...");
require(timeStamp != 0, "...");
```

**[kingyetifinance (Yeti finance) confirmed](https://github.com/code-423n4/2021-12-yetifinance-findings/issues/91#issuecomment-1005398691):**
 > @LilYeti: 
> 
> https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round
> 
> https://github.com/code-423n4/2021-08-notional-findings/issues/92




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yeti Finance |
| Report Date | N/A |
| Finders | hyh  WatchPug, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-yetifinance
- **GitHub**: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/91
- **Contest**: https://code4rena.com/contests/2021-12-yeti-finance-contest

### Keywords for Search

`vulnerability`

