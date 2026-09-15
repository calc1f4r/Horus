---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32067
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-abracadabra-money
source_link: https://code4rena.com/reports/2024-03-abracadabra-money
github_link: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/93

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
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - DarkTower
---

## Vulnerability Title

[M-11] `MagicLpAggregator` can be incompatible with potential integrators due to incorrect `latestRoundData` function

### Overview


The `MagicLpAggregator` has a bug where it does not update certain values correctly. This can cause issues for integrators who use the oracle because the values returned are always incorrect. This means that any integrator who uses the `latestRoundData()` function will not be able to integrate `MagicLpAggregator` correctly. The recommended solution is to use the values from the `baseOracle` or `quoteOracle` instead.

### Original Finding Content


`MagicLpAggregator` does not update the `roundId`, `startAt`, `updatedAt` and `answeredInRound` to correct values.

[MagicLpAggregator.sol#L48-L50](https://github.com/code-423n4/2024-03-abracadabra-money/blob/main/src/oracles/aggregators/MagicLpAggregator.sol#L48-L50)

```solidity
    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        return (0, latestAnswer(), 0, 0, 0);
    }
```

A common code is to check `updatedAt` for staleness issue (although it isn't required to do so anymore.

```solidity
(, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();

if (updatedAt < block.timestamp - 60 * 60 /* 1 hour */) {
   revert("stale price feed");
}
```

Therefore any integrator that uses the above code will not be able to integrate
`MagicLpAggregator` oracles as it will always revert due to the incorrect `updatedAt` being provided.

### Recommended Mitigation Steps

Use the values `roundId`, `startAt`, `updatedAt` and `answeredInRound` from whichever oracle, `baseOracle` or `quoteOracle` was used.

**[rexjoseph (Warden) commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/93#issuecomment-2034370525):**
> I think we should reiterate the issue here as the submission has tried its best to point out:
> 
> 1. The `MagicLpAggregator` gets the price from Chainlink's Feed
> 2. Integrators (for example protocol A) query the `MagicLPAggregator` Oracle for price specifically the `latestRoundData()` function it exposes in their implementation
> 3. They make sure the prices returned are fresh and so do well to check the time specifically `updatedAt` so they can be sure the feed is fresh to proceed with utilizing the returned data
> 4. Since the `updatedAt` as well as other returned data are hardcoded to 0 in `MagicLpAggregator` oracle implementation, the call reverts. 0 will always be less than `block.timestamp - 60 * 60`
> 
> 
> The step by step description of the issue above I believe is sufficient but here's a provided POC to elaborate on this in code:
> 
> Test file in the abracadabra codebase is:  MagicLPAggregator.t.sol
> 
> ```js
> function testProtocolAIntegrationOfMagicLPAggReverts() public {
> 
>         // return values of `MagicLpAggregator` latestRoundData()
>         (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) = aggregator.latestRoundData();
> 
>         // protocol A tries to make sure the prices returned is fresh by checking the time
> 
>         // keep in mind the time aka updatedAt is hardcoded to 0. So 0 will always be less than `block.timestamp - 60 * 60` hence a revert
> 
>         if (updatedAt < block.timestamp - 60 * 60 /* 1 hour */) {
>          revert("stale price feed");
>         }
>     }
> ```
> 
> ```js
> Ran 1 test for test/MagicLpAggregator.t.sol:MagicLpAggregatorTest
> [FAIL. Reason: revert: stale price feed] testProtocolAIntegrationOfMagicLPAggReverts() (gas: 57187)
> Suite result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 2.56s (2.88ms CPU time)
> ```

**[cccz (Judge) commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/93#issuecomment-2037525115):**
 > latestRoundData() is different from the standard and may cause integration issues. 
> Will consider it a valid M.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | DarkTower |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-abracadabra-money
- **GitHub**: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/93
- **Contest**: https://code4rena.com/reports/2024-03-abracadabra-money

### Keywords for Search

`vulnerability`

