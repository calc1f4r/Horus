---
# Core Classification
protocol: Stader Labs
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 20187
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-stader
source_link: https://code4rena.com/reports/2023-06-stader
github_link: https://github.com/code-423n4/2022-06-stader-findings/issues/15

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
  - stale_price
  - chainlink

# Audit Details
report_date: unknown
finders_count: 25
finders:
  - peanuts
  - Breeje
  - piyushshukla
  - tallo
  - dwward3n
---

## Vulnerability Title

[M-14] Chainlink's `latestRoundData` may return a stale or incorrect result

### Overview


This bug report is about the StaderOracle.sol smart contract. It is used to retrieve price feed data from Chainlink's `latestRoundData` but there is insufficient protection against price staleness. This can lead to inaccurate price data that can cause functions not working as expected and/or loss of funds. To mitigate this, a check for the `updatedAt` returned value from `latestRoundData` should be added. This is an Oracle bug and has been acknowledged and commented on by manoj9april (Stader).

### Original Finding Content


<https://github.com/code-423n4/2023-06-stader/blob/main/contracts/StaderOracle.sol#L646> <br><https://github.com/code-423n4/2023-06-stader/blob/main/contracts/StaderOracle.sol#L648>

Chainlink's `latestRoundData` is used here to retrieve price feed data; however, there is insufficient protection against price staleness.

Return arguments other than `int256 answer` are necessary to determine the validity of the returned price, as it is possible for an outdated price to be received. See [here](https://ethereum.stackexchange.com/questions/133242/how-future-resilient-is-a-chainlink-price-feed/133843#133843) for reasons why a price feed might stop updating.

The return value `updatedAt` contains the timestamp at which the received price was last updated, and can be used to ensure that the price is not outdated. See more information about `latestRoundID` in the [Chainlink docs](https://docs.chain.link/data-feeds/api-reference#latestrounddata). Inaccurate price data can lead to functions not working as expected and/or loss of funds.

### Proof of Concept

```solidity
    function getPORFeedData()
        internal
        view
        returns (
            uint256,
            uint256,
            uint256
        )
    {
        (, int256 totalETHBalanceInInt, , , ) = AggregatorV3Interface(staderConfig.getETHBalancePORFeedProxy())
            .latestRoundData();
        (, int256 totalETHXSupplyInInt, , , ) = AggregatorV3Interface(staderConfig.getETHXSupplyPORFeedProxy())
            .latestRoundData();
        return (uint256(totalETHBalanceInInt), uint256(totalETHXSupplyInInt), block.number);
    }
```

### Recommended Mitigation Steps

Add a check for the `updatedAt` returned value from `latestRoundData`.

```diff
    function getPORFeedData()
        internal
        view
        returns (
            uint256,
            uint256,
            uint256
        )
    {
-       (, int256 totalETHBalanceInInt, , , ) = AggregatorV3Interface(staderConfig.getETHBalancePORFeedProxy())
+       (, int256 totalETHBalanceInInt, , uint256 balanceUpdatedAt, ) = AggregatorV3Interface(staderConfig.getETHBalancePORFeedProxy())
            .latestRoundData();
+       require(block.timestamp - balanceUpdatedAt <= MAX_DELAY, "stale price");

-       (, int256 totalETHXSupplyInInt, , , ) = AggregatorV3Interface(staderConfig.getETHXSupplyPORFeedProxy())
+       (, int256 totalETHXSupplyInInt, , uint256 supplyUpdatedAt, ) = AggregatorV3Interface(staderConfig.getETHXSupplyPORFeedProxy())
            .latestRoundData();
+       require(block.timestamp - supplyUpdatedAt <= MAX_DELAY, "stale price");

        return (uint256(totalETHBalanceInInt), uint256(totalETHXSupplyInInt), block.number);
    }
```

### Assessed type

Oracle

**[manoj9april (Stader) acknowledged and commented](https://github.com/code-423n4/2022-06-stader-findings/issues/15#issuecomment-1596573683):**
 > Solution with chainlink is not finalized.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | peanuts, Breeje, piyushshukla, tallo, dwward3n, saneryee, MohammedRizwan, whimints, erictee, etherhood, Aymen0909, Madalad, Hama, Bauchibred, kutugu, bin2chen, DadeKuma, LaScaloneta, turvy\_fuzz, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-stader
- **GitHub**: https://github.com/code-423n4/2022-06-stader-findings/issues/15
- **Contest**: https://code4rena.com/reports/2023-06-stader

### Keywords for Search

`Stale Price, Chainlink`

