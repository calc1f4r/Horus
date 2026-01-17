---
# Core Classification
protocol: Rysk Uniswapv3Rangeorderreactor
chain: everychain
category: uncategorized
vulnerability_type: uniswap

# Attack Vector Details
attack_type: uniswap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18846
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2022-12-23-rysk UniswapV3RangeOrderReactor.md
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
  - uniswap
  - overflow/underflow
  - decimals

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-1 multiplication overflow in getPoolPrice() likely

### Overview


This bug report is regarding the `getPoolPrice()` function used in hedgeDelta. The issue is that calculation of p is likely to overflow, as sqrtPriceX96 has 96 bits for decimals, and 10** `token0.decimals()` will have 60 bits when decimals is 18, leaving only 2 bits for non-decimal part of sqrtPriceX96. 

The recommended mitigation was to consider converting the sqrtPrice to a 60x18 format and performing arithmetic operations using the PRBMathUD60x18 library. The team response was that the issue was fixed and calculations are now performed safely using the standard FullMath library.

### Original Finding Content

**Description:**
`getPoolPrice()` is used in hedgeDelta to get the price directly from Uniswap v3 pool:
```solidity 
    function getPoolPrice() public view returns (uint256 price, uint256 
         inversed){
            (uint160 sqrtPriceX96, , , , , , ) = pool.slot0();
        uint256 p = uint256(sqrtPriceX96) * uint256(sqrtPriceX96) * (10 
        ** token0.decimals());
     // token0/token1 in 1e18 format
          price = p / (2 ** 192);
              inversed = 1e36 / price;
         }

```
The issue is that calculation of p is likely to overflow. sqrtPriceX96 has 96 bits for decimals, 
10** `token0.decimals()` will have 60 bits when decimals is 18, therefore there is only 
(256 – 2 * 96 – 60) / 2 = 2 bits for non-decimal part of sqrtPriceX96. 

**Recommended Mitigation:**
Consider converting the sqrtPrice to a 60x18 format and performing arithmetic operations 
using the PRBMathUD60x18 library.

**Team Response:**
Fixed

**Mitigation Review**
Calculations are now performed safely using the standard FullMath library

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Rysk Uniswapv3Rangeorderreactor |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2022-12-23-rysk UniswapV3RangeOrderReactor.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Uniswap, Overflow/Underflow, Decimals`

