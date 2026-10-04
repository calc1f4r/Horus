---
# Core Classification
protocol: Otim Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57055
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
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
finders_count: 2
finders:
  - Quan Nguyen
  - Omar Inuwa Trail of Bits PUBLIC
---

## Vulnerability Title

Lack of validation of latestRoundData return value

### Overview


The report is about a vulnerability in the `weiToToken` function of the `FeeTokenRegistry` contract. This function uses the `latestRoundData` function without checking if the returned data is outdated, which could lead to incorrect prices and potential loss of gas payments. The function also does not check for an invalid `roundId`. This could result in users paying more or less money than necessary for transactions. The report recommends adding checks to the `weiToToken` function to prevent these issues and implementing fallback mechanisms and monitoring for all third-party price feeds in the long term.

### Original Finding Content

## Vulnerability Report

## Difficulty: Low

## Type: Denial of Service

## Description
The `weiToToken` function in the `FeeTokenRegistry` contract uses the `latestRoundData` function without validating whether the returned data is stale, potentially leading to the usage of outdated prices. Specifically, the function does not check the value of `updatedAt`, creating a vulnerability to stale prices, which might jeopardize gas payments. 

According to Chainlink’s documentation, a timestamp of 0 means the round is not complete and should not be used. Without this check, the `weiToToken` function could receive incorrect price data. Furthermore, the function does not check for an invalid `roundId`, which is 0.

```solidity
// slither-disable-next-line unused-return
(, int256 latestPrice,,,) = AggregatorV3Interface(data.priceFeed).latestRoundData();

// if the latest price is zero or negative, revert
if (latestPrice <= 0) {
    revert InvalidPrice();
}
```

**Figure 3.1**: Lack of checks when receiving price data in `FeeTokenRegistry.sol`

## Exploit Scenario
A user has to unduly pay more gas for a transaction because the price feed returns a stale price above the current market value. Alternatively, a user unduly pays less money to the transaction executor because the price feed returns a stale price below the current market value.

## Recommendations
- **Short term**: Add checks to `weiToToken` to ensure that `updatedAt != 0`, that the feed data is still within an acceptable threshold (i.e., not stale), and that the current `roundId` is not 0.
- **Long term**: Implement for all third-party price feeds fallback mechanisms, robust monitoring, and graceful handling of failures and returned stale data.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Otim Smart Wallet |
| Report Date | N/A |
| Finders | Quan Nguyen, Omar Inuwa Trail of Bits PUBLIC |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-03-otim-smart-wallet-securityreview.pdf

### Keywords for Search

`vulnerability`

