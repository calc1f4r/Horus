---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3327
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/2
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-notional-judging/issues/133

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - Waze
  - GalloDaSballo
  - Chom
  - Lambda
  - ak1
---

## Vulnerability Title

M-2: Price oracle could get a stale price

### Overview


This bug report is about an issue found in the wstETHChainlinkOracle.sol contract. The issue is that the contract does not check the round id and timestamp when it gets the baseAnswer from the Chainlink oracle, meaning it could get a stale price from the oracle. This could have an impact on the price oracle, as it could get a stale price without checking the roundId. The code snippet provided in the report shows the code that should be used to check the answer, updateAt and roundId when getting the price. The recommendation is to add the code snippet provided in the report to the contract to check the answer, updateAt and roundId when getting the price. This will ensure that the price oracle does not get a stale price.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-notional-judging/issues/133 

## Found by 
rajatbeladiya, Lambda, Chom, Waze, GimelSec, ak1, GalloDaSballo

## Summary

`_calculateAnswer()` will get `baseAnswer` from Chainlink oracle. But it doesn't check round id and timestamp, leading to it may get a stale price from Chainlink oracle.

## Vulnerability Detail

In wstETHChainlinkOracle.sol, it check `baseAnswer` > 0, but it doesn't check for the stale price by `updateAt` and `roundId`.

## Impact

Price oracle could get a stale price without checking `roundId`.

## Code Snippet

https://github.com/sherlock-audit/2022-09-notional/blob/main/leveraged-vaults/contracts/trading/oracles/wstETHChainlinkOracle.sol#L26-L44

## Tool used

Manual Review

## Recommendation

Check `answer`, `updateAt` and `roundId` when getting price:

```
        (uint80 roundId, int256 answer, , uint256 updatedAt, uint80 answeredInRound) = oracle.latestRoundData();

        require(updatedAt > 0, "Round is not complete");
        require(answer >= 0, "Malfunction");
        require(answeredInRound >= roundID, "Stale price");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional |
| Report Date | N/A |
| Finders | Waze, GalloDaSballo, Chom, Lambda, ak1, rajatbeladiya, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-notional-judging/issues/133
- **Contest**: https://app.sherlock.xyz/audits/contests/2

### Keywords for Search

`vulnerability`

