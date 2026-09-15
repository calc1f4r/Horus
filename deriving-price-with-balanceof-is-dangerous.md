---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7216
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - wrong_math
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Deriving price with balanceOf is dangerous

### Overview


This bug report is related to the ConnextPriceOracle.sol file, specifically lines 109 to 135. It has been given a high risk severity rating. The function getPriceFromDex is used to derive the price of a token and it does this by querying the balance of an AMM's pools. However, this is dangerous as balanceOf can be gamed. An example of this is the univ2 protocol, which allows exploiters to send tokens into a pool and pump the price, then absorb the tokens that were previously donated.

The recommendation is to query the DEX's state through function calls such as Univ2's getReserves(), which returns the correct state of the pool. This issue has been solved in PR 1649 and has been verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
`ConnextPriceOracle.sol#L109-L135`

## Description
The function `getPriceFromDex` derives the price by querying the balance of AMM’s pools.

```solidity
function getPriceFromDex(address _tokenAddress) public view returns (uint256) {
    PriceInfo storage priceInfo = priceRecords[_tokenAddress];
    ...
    uint256 rawTokenAmount = IERC20Extended(priceInfo.token).balanceOf(priceInfo.lpToken);
    ...
    uint256 rawBaseTokenAmount = IERC20Extended(priceInfo.baseToken).balanceOf(priceInfo.lpToken);
    ...
}
```

Deriving the price with `balanceOf` is dangerous as `balanceOf` may be gamed. Consider Uniswap V2 as an example; exploiters can first send tokens into the pool and pump the price, then absorb the tokens that were previously donated by calling `mint`.

## Recommendation
Consider querying DEX’s state through function calls such as Uniswap V2’s `getReserves()` which returns the correct state of the pool.

## References
- **Connext**: Solved in PR 1649.
- **Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math, Business Logic`

