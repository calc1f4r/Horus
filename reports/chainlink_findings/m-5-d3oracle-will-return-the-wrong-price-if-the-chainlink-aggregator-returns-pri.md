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
solodit_id: 20852
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/89
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/129

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
finders_count: 7
finders:
  - Proxy
  - kutugu
  - BugHunter101
  - 0xdice91
  - PRAISE
---

## Vulnerability Title

M-5: D3Oracle will return the wrong price if the Chainlink aggregator returns price outside min/max range

### Overview


This bug report is about the issue M-5, where the Chainlink oracle will return the wrong price if the price is outside the min/max range. The bug was found by 0xdice91, BugHunter101, MohammedRizwan, PRAISE, Proxy, dirk_y, and kutugu. The issue is with the `getPrice()` and `getOriginalPrice()` functions in the D3Oracle.sol file, as they only check if the price is greater than 0, and not if it is within the correct range. If the price goes below the minimum price the oracle will not return the correct price but only the min price. The same goes for the other extremity. This wrong price may be returned in the event of a market crash, and the functions with the issue are used in the D3VaultFunding.sol, D3VaultLiquidation.sol, and D3UserQuota.sol files. The bug was manually reviewed, and the recommendation is to check the latest answer against reasonable limits and/or revert in case you get a bad price. An example code is provided to do this. The discussion thread contains a question about how to get the minPrice and maxPrice from the oracle contract, with an answer providing a link to the documentation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/129 

## Found by 
0xdice91, BugHunter101, MohammedRizwan, PRAISE, Proxy, dirk\_y, kutugu
## Summary

Chainlink oracles have a min and max price that they return. If the price goes below the minimum price the oracle will not return the correct price but only the min price. Same goes for the other extremity.

## Vulnerability Detail

Both [`getPrice()`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L48-L56) and [`getOriginalPrice()`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L58-L67) only check `price > 0` not are they within the correct range

```solidity
(uint80 roundID, int256 price,, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData();
require(price > 0, "Chainlink: Incorrect Price");
require(block.timestamp - updatedAt < priceSources[token].heartBeat, "Chainlink: Stale Price");
require(answeredInRound >= roundID, "Chainlink: Stale Price");
```

## Impact

The wrong price may be returned in the event of a market crash.
The functions with the issue are used in [`D3VaultFunding.sol`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultFunding.sol), [`D3VaultLiquidation.sol`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/D3VaultLiquidation.sol) and [`D3UserQuota.sol`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/D3Vault/periphery/D3UserQuota.sol)

## Code Snippet

- D3Oracle.sol functions:
  - [`getPrice()`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L48-L56)
  - [`getOriginalPrice()`](https://github.com/sherlock-audit/2023-06-dodo/blob/main/new-dodo-v3/contracts/DODOV3MM/periphery/D3Oracle.sol#L58-L67)

## Tool used

Manual Review

## Recommendation

[Check the latest answer against reasonable limits](https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits) and/or revert in case you get a bad price

```solidity
 require(price >= minAnswer && price <= maxAnswer, "invalid price");
```




## Discussion

**Attens1423**

How can we get minPrice and maxPrice from oracle contract? Could you give us a more detailed procession?

**0xffff11**

https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits @Attens1423 


**Attens1423**

We understand this doc. If you could offer a code example, including how to get minPrice and maxPrice from code, we would appreciate it

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | DODO V3 |
| Report Date | N/A |
| Finders | Proxy, kutugu, BugHunter101, 0xdice91, PRAISE, MohammedRizwan, dirk\_y |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-dodo-judging/issues/129
- **Contest**: https://app.sherlock.xyz/audits/contests/89

### Keywords for Search

`vulnerability`

