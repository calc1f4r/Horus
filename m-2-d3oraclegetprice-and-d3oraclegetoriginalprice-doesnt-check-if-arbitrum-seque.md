---
# Core Classification
protocol: DODO V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20849
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/89
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/62

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
finders_count: 16
finders:
  - Avci
  - jprod15
  - qckhp
  - kutugu
  - bitsurfer
---

## Vulnerability Title

M-2: D3Oracle.getPrice() and D3Oracle.getOriginalPrice() doesn't check If Arbitrum sequencer is down for Chainlink feeds

### Overview


This bug report is about the vulnerability in the D3Oracle smart contract, which is used in L2 chains like Arbitrum. The vulnerability is that the D3Oracle.getPrice() and D3Oracle.getOriginalPrice() functions do not check if the Arbitrum sequencer is down for Chainlink feeds. This means that malicious actors could potentially exploit this vulnerability to gain an unfair advantage. The code snippets of the two functions have been provided in the report. The bug was found by 0xHati, 0xNoodleDon, 0xdice91, Avci, MohammedRizwan, PNS, PRAISE, bitsurfer, jprod15, kutugu, qckhp, seeques, shogoki, shtesesamoubiq, skyge, and tsvetanovv, and the tool used to find the bug was Manual Review. A code example of Chainlink has been provided as a recommendation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/62 

## Found by 
0xHati, 0xNoodleDon, 0xdice91, Avci, MohammedRizwan, PNS, PRAISE, bitsurfer, jprod15, kutugu, qckhp, seeques, shogoki, shtesesamoubiq, skyge, tsvetanovv
## Summary
When utilizing Chainlink in L2 chains like Arbitrum, it's important to ensure that the prices provided are not falsely perceived as fresh, even when the sequencer is down. This vulnerability could potentially be exploited by malicious actors to gain an unfair advantage.

## Vulnerability Detail
There is no check in D3Oracle.getPrice()
```solidity
 function getPrice(address token) public view override returns (uint256) {
        require(priceSources[token].isWhitelisted, "INVALID_TOKEN");
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceSources[token].oracle);
        (uint80 roundID, int256 price,, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData();
        require(price > 0, "Chainlink: Incorrect Price");
        require(block.timestamp - updatedAt < priceSources[token].heartBeat, "Chainlink: Stale Price");
        require(answeredInRound >= roundID, "Chainlink: Stale Price");
        return uint256(price) * 10 ** (36 - priceSources[token].priceDecimal - priceSources[token].tokenDecimal);
    }
```

no check in D3Oracle.getOriginalPrice() too
```solidity
 function getOriginalPrice(address token) public view override returns (uint256, uint8) {
        require(priceSources[token].isWhitelisted, "INVALID_TOKEN");
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceSources[token].oracle);
        (uint80 roundID, int256 price,, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData();
        require(price > 0, "Chainlink: Incorrect Price");
        require(block.timestamp - updatedAt < priceSources[token].heartBeat, "Chainlink: Stale Price");
        require(answeredInRound >= roundID, "Chainlink: Stale Price");
        uint8 priceDecimal = priceSources[token].priceDecimal;
        return (uint256(price), priceDecimal);
    }
```

## Impact
could potentially be exploited by malicious actors to gain an unfair advantage.

## Code Snippet
https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L48

https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L58
## Tool used

Manual Review

## Recommendation
code example of Chainlink:
https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO V3 |
| Report Date | N/A |
| Finders | Avci, jprod15, qckhp, kutugu, bitsurfer, 0xdice91, skyge, PRAISE, 0xNoodleDon, seeques, MohammedRizwan, tsvetanovv, shogoki, 0xHati, PNS, shtesesamoubiq |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/62
- **Contest**: https://app.sherlock.xyz/audits/contests/89

### Keywords for Search

`vulnerability`

