---
# Core Classification
protocol: Isomorph
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 5699
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/22
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/200

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - oracle
  - stale_price

protocol_categories:
  - liquid_staking
  - yield
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 8olidity
  - yixxas
  - \_\_141345\_\_
  - caventa
  - HonorLt
---

## Vulnerability Title

M-7: `latestRoundData()` has no check for round completeness

### Overview


This bug report is about an issue found in the oracle wrapper `getOraclePrice()` of the Velo-Deposit-Tokens contract. This function calls out to an oracle with `latestRoundData()` to get the price of some token, however, there is no check for round completeness. As a result, the returned data might be outdated, leading to stale prices and wrong price return value. This could cause the functions relying on accurate price feed to not work as expected, and sometimes can lead to fund loss.

The impact of this issue varies depending on the situation, such as incorrect liquidation, wrong price feed, and inappropriate loan being taken. A code snippet and a reference to Chainlink's documentation are provided for further understanding.

The issue was found by \_\_141345\_\_, 8olidity, yixxas, caventa, HonorLt, and was fixed by kree-dotcom. The recommendation is to validate data feed for round completeness by adding a check for `answeredInRound >= roundID`.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/200 

## Found by 
\_\_141345\_\_, 8olidity, yixxas, caventa, HonorLt

## Summary

No check for round completeness could lead to stale prices and wrong price return value, or outdated price. The functions rely on accurate price feed might not work as expected, sometimes can lead to fund loss. 


## Vulnerability Detail

The oracle wrapper `getOraclePrice()` call out to an oracle with `latestRoundData()` to get the price of some token. Although the returned timestamp is checked, there is no check for round completeness.

According to Chainlink's documentation, this function does not error if no answer has been reached but returns 0 or outdated round data. The external Chainlink oracle, which provides index price information to the system, introduces risk inherent to any dependency on third-party data sources. For example, the oracle could fall behind or otherwise fail to be maintained, resulting in outdated data being fed to the index price calculations. Oracle reliance has historically resulted in crippled on-chain systems, and complications that lead to these outcomes can arise from things as simple as network congestion.

## Reference
Chainlink documentation:
https://docs.chain.link/docs/historical-price-data/#historical-rounds

## Impact

If there is a problem with chainlink starting a new round and finding consensus on the new value for the oracle (e.g. chainlink nodes abandon the oracle, chain congestion, vulnerability/attacks on the chainlink system) consumers of this contract may continue using outdated stale data (if oracles are unable to submit no new round is started).

This could lead to stale prices and wrong price return value, or outdated price.

As a result, the functions rely on accurate price feed might not work as expected, sometimes can lead to fund loss. The impacts vary and depends on the specific situation like the following:
- incorrect liquidation
    - some users could be liquidated when they should not
    - no liquidation is performed when there should be
- wrong price feed 
    - causing inappropriate loan being taken, beyond the current collateral factor
    - too low price feed affect normal bor


## Code Snippet

https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Velo-Deposit-Tokens/contracts/DepositReceipt_Base.sol#L164-L181


## Tool used

Manual Review


## Recommendation

Validate data feed for round completeness:
```solidity
    function getOraclePrice(IAggregatorV3 _priceFeed, int192 _maxPrice, int192 _minPrice) public view returns (uint256 ) {
        (
            uint80 roundID,
            int signedPrice,
            /*uint startedAt*/,
            uint timeStamp,
            uint80 answeredInRound
        ) = _priceFeed.latestRoundData();
        //check for Chainlink oracle deviancies, force a revert if any are present. Helps prevent a LUNA like issue
        require(signedPrice > 0, "Negative Oracle Price");
        require(timeStamp >= block.timestamp - HEARTBEAT_TIME , "Stale pricefeed");
        require(signedPrice < _maxPrice, "Upper price bound breached");
        require(signedPrice > _minPrice, "Lower price bound breached");
        require(answeredInRound >= roundID, "round not complete");

        uint256 price = uint256(signedPrice);
        return price;
    }
```

## Discussion

**kree-dotcom**

Sponsor confirmed, will fix. 

**kree-dotcom**

Fixed https://github.com/kree-dotcom/Velo-Deposit-Tokens/commit/5c656e791e70ecdfe26f9807438498384d7f6108

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Isomorph |
| Report Date | N/A |
| Finders | 8olidity, yixxas, \_\_141345\_\_, caventa, HonorLt |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/200
- **Contest**: https://app.sherlock.xyz/audits/contests/22

### Keywords for Search

`Oracle, Stale Price`

