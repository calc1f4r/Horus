---
# Core Classification
protocol: Rysk Uniswapv3Rangeorderreactor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18848
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-3 Overflow danger in _sqrtPriceX96ToUint

### Overview


This bug report describes an issue with the _sqrtPriceX96ToUint() function, which is used in the hedgeDelta() function. When the non-fractional component of sqrtPriceX96 takes up to 32 bits, it will represent a price ratio of 18446744073709551616. With different token digits, it is likely that this ratio will be crossed, causing the hedgeDelta() function to revert.

The recommended mitigation was to perform the multiplication after converting the numbers to 60x18 variables. The team fixed the issue by creating a new utility function sqrtPriceX96ToUint that correctly uses SafeMath and also multiplies in a different order depending on the price size to ensure that no overflows occur.

### Original Finding Content

**Description:**
_sqrtPriceX96ToUint will only work when the non-fractional component of sqrtPriceX96 
takes up to 32 bits. This represents a price ratio of 18446744073709551616. With different 
token digits it is not unlikely that this ratio will be crossed which will make hedgeDelta() 
revert.

    
```solidity
    function _sqrtPriceX96ToUint(uint160 sqrtPriceX96) private pure returns (uint256)
    {
        uint256 numerator1 = uint256(sqrtPriceX96) * 
         uint256(sqrtPriceX96);
    return FullMath.mulDiv(numerator1, 1, 1 << 192);
         }
```

**Recommended Mitigation:**
Perform the multiplication after converting the numbers to 60x18 variables

**Team Response:**
Fixed

**Mitigation review:**
New utility function sqrtPriceX96ToUint correctly uses SafeMath, and also multiplies in a 
different order depending on price size to ensure no overflows occur:

```solidity
        if (sqrtPrice > Q96) {
             uint256 sqrtP = FullMath.mulDiv(sqrtPrice, 10 ** token0Decimals, 
                Q96);
        return FullMath.mulDiv(sqrtP, sqrtP, 10 ** token0Decimals);
            } else {
        uint256 numerator1 = FullMath.mulDiv(sqrtPrice, sqrtPrice, 1);
        uint256 numerator2 = 10 ** token0Decimals;
             return FullMath.mulDiv(numerator1, numerator2, 1 << 192);
            }
```

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

`vulnerability`

