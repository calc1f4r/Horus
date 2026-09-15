---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49596
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-benddao-invitational
source_link: https://code4rena.com/reports/2024-12-benddao-invitational
github_link: https://code4rena.com/audits/2024-12-benddao-invitational/submissions/F-10

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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - oakcobalt
---

## Vulnerability Title

[M-03] Missing price staleness check for `WEETH_AGGREGATOR`

### Overview


The bug report discusses an issue with the code in the EETHPriceAdapter.sol file, specifically in line 115. The function latestRoundData() is called by PriceOracle::getAssetPriceFromChainlink and provides the price of eETH in USD by using two chainlink oracles. However, the problem is that the flow of getAssetPriceFromChainlink -> EETHPriceAdapter::latestRoundata() only checks for price staleness in one of the oracles, leaving the other vulnerable to providing an invalid price. The report includes a proof of concept and recommends adding a staleness check for the second oracle in order to ensure a valid answer. The team responsible for the code has acknowledged the issue and a judge has deemed it a valid finding. 

### Original Finding Content



Code reference: [EETHPriceAdapter.sol# L115](https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/oracles/EETHPriceAdapter.sol# L115)

EETHPriceAdapter::latestRoundata() is called by PriceOracle::getAssetPriceFromChainlink. It provides price of eETH in baseCurrency(USD) by using two chainlink oracles - ETH/USD(`BASE_AGGREGATOR`), WETH/ETH (`WEETH_AGGREGATOR`).

The problem is the flow of getAssetPriceFromChainlink -> EETHPriceAdapter::latestRoundata() would only have price staleness check for `BASE_AGGREGATOR` oracle, but no price staleness check for `WEETH_AGGREGATOR` oracle.

Missing price staleness check for one of the two oracle could result in a invalid eETH/USD price.

### Proof of Concept

Flows: PriceOracle::getAssetPriceFromChainlink -> EETHPriceAdapter::latestRoundata

In EETHPriceAdapter::latestRoundData, only the data feed timestamp(`updatedAT_`) of `BASE_AGGREGATOR` is passed as return values. `WETH_AGGREGATOR` is invoked using a simplified method `latestAnswer` instead of `latestRoundData` and no meta data of the price feed is passed.
```

//src/oracles/EETHPriceAdapter.sol
    function latestRoundData()
        public
        view
        returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)
    {
    ...
            (
            uint80 roundId_,
            int256 basePrice,
            uint256 startedAt_,
            uint256 updatedAt_,
            uint80 answeredInRound_
        ) = BASE_AGGREGATOR.latestRoundData();

|>      int256 eETHBasePrice = _convertWEETHPrice(basePrice, weETHPrice);

        return (roundId_, eETHBasePrice, startedAt_, updatedAt_, answeredInRound_);
    }
```

[EETHPriceAdapter.sol# L115](https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/oracles/EETHPriceAdapter.sol# L115)

In PriceOracle::getAssetPriceFromChainlink, only `BASE_AGGREGATOR`’s price staleness is checked.
```

//src/PriceOracle.sol

    function getAssetPriceFromChainlink(address asset) public view returns (uint256) {
        AggregatorV2V3Interface sourceAgg = assetChainlinkAggregators[asset];
        require(address(sourceAgg) != address(0), Errors.ASSET_AGGREGATOR_NOT_EXIST);

        (uint80 roundId, int256 answer, , uint256 updatedAt, uint80 answeredInRound) = sourceAgg.latestRoundData();
          //@audit when calling EETHPriceAdapter::latestRoundData, only BASE_AGGREGATOR's staleness will be checked. WEETH_AGGREGATOR's staleness check is missing.
|>        require(answer > 0, Errors.ASSET_PRICE_IS_ZERO);
|>        require(updatedAt != 0, Errors.ORACLE_PRICE_IS_STALE);
|>        require(answeredInRound >= roundId, Errors.ORACLE_PRICE_IS_STALE);

        return uint256(answer);
    }
```

[PriceOracle.sol# L181](https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/PriceOracle.sol# L181)

Since two chainlink price feeds are used, both price feed’s staleness need to be checked to ensure a valid answer.

### Recommended mitigation steps

Consider adding staleness check for `WEETH_AGGREGATOR` in EETHPriceAdapter::latestRoundata.

**thorseldon (BendDAO) acknowledged**

**[0xTheC0der (judge) commented](https://code4rena.com/audits/2024-12-benddao-invitational/submissions/F-10?commentParent=L2F3U6yfQau):**

> Close to M-2 “Use of deprecated chainlink function: `latestAnswer()`” from the [automated findings report](https://github.com/code-423n4/2024-12-benddao/blob/main/4naly3er-report.md), but still different due to staleness consideration. Therefore, valid.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-benddao-invitational
- **GitHub**: https://code4rena.com/audits/2024-12-benddao-invitational/submissions/F-10
- **Contest**: https://code4rena.com/reports/2024-12-benddao-invitational

### Keywords for Search

`vulnerability`

