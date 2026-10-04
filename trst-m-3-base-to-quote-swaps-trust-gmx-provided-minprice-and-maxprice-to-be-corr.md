---
# Core Classification
protocol: Lyra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18898
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-3 base to quote swaps trust GMX-provided minPrice and maxPrice to be correct, which may be manipulated

### Overview


The bug report describes an issue with the exchangeFromExactBase() function in GMXAdapter, which converts an amount of base to quote. It implements slippage protection by using the GMX vault’s getMinPrice() and getMaxPrice() utilities, however this is insufficient because GMX prices may be manipulated. A possible attack would be to drive up the base token (e.g. ETH) price, sell a large ETH amount to the GMXAdapter, and repay the flashloan used for manipulation.

The recommended mitigation is to verify getMinPrice() and getMinPrice() outputs are close to Chainlink-provided prices as done in getSpotPriceForMarket(). The team has fixed this for exchangeFromExactBase() by using Chainlink price instead of gmxMinPrice of baseAsset. This way, if the price is favorable for the LPs (given they rely on CL) it will not revert.

### Original Finding Content

**Description:**
exchangeFromExactBase() in GMXAdapter converts an amount of base to quote. It 
implements slippage protection by using the GMX vault’s getMinPrice() and getMaxPrice() 
utilities. However, such protection is insufficient because GMX prices may be manipulated. 
Indeed, GMX supports “AMM pricing” mode where quotes are calculated from Uniswap 
reserves. A possible attack would be to drive up the base token (e.g. ETH) price, sell a large 
ETH amount to the GMXAdapter, and repay the flashloan used for manipulation. 
exchangeFromExactBase() is attacker-reachable from LiquidityPool’s exchangeBase().
```solidity
    uint tokenInPrice = _getMinPrice(address(baseAsset));
        uint tokenOutPrice = _getMaxPrice(address(quoteAsset));
    ...
    uint minOut = tokenInPrice
      .multiplyDecimal(marketPricingParams[_optionMarket].minReturnPercent)
        .multiplyDecimal(_amountBase)
          .divideDecimal(tokenOutPrice);
```

**Recommended Mitigation:**
Verify `getMinPrice()`, `getMinPrice()` outputs are close to Chainlink-provided prices as done in 
`getSpotPriceForMarket()`.

**Team Response:**
Fixed for `exchangeFromExactBase()` here, by using Chainlink price instead of **gmxMinPrice** of 
**baseAsset**. This way if the price is favorable for the LPs (given they rely on CL) it will not revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Lyra Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-01-19-Lyra Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

