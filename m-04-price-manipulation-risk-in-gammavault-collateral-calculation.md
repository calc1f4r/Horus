---
# Core Classification
protocol: GammaSwap_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45535
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GammaSwap-security-review_2024-12-30.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] Price manipulation risk in GammaVault collateral calculation

### Overview


The report states that there is a bug in the GammaVault contract that calculates external collateral for GammaPool positions using the current spot price from Uniswap V3. This makes it vulnerable to potential attacks where an attacker can manipulate the spot price and force unfair liquidations. The recommended solution is to use TWAP price instead of spot price to calculate the external collateral.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The GammaVault contract calculates external collateral for GammaPool positions using the current spot price from Uniswap V3, rather than a more manipulation-resistant price source. This creates a potential vulnerability where an attacker could manipulate the spot price to affect collateral calculations and force unfair liquidations.

```solidity
    function _getCollateral(address _gammaPool, uint256 _tokenId) internal override virtual view returns(uint256 collateral) {
        uint160 sqrtPriceX96 = getCurrentPrice(); // @audit collateral is depent on spot price
        uint160 sqrtPriceAX96 = RangedPoolMath.calcSqrtRatioAtTick(s.tickLower);
        uint160 sqrtPriceBX96 = RangedPoolMath.calcSqrtRatioAtTick(s.tickUpper);

        uint128[] memory tokensHeld = new uint128[](2);
        {
            (uint256 amount0, uint256 amount1) = RangedPoolMath.getAmountsForLiquidity(sqrtPriceX96, sqrtPriceAX96,
            sqrtPriceBX96, uint128(s.totalLiquidity));
            tokensHeld[0] = uint128(amount0);
            tokensHeld[1] = uint128(amount1);
        }

        collateral = GSHedgeMath.convertAmountsToLiquidity(cfmm, tokensHeld, numOfDecimals0, numOfDecimals1, mathLib);
    }
```

Let's see an attack scenario:

- Attacker identifies a GammaVault position with: - Tight tick range in UniswapV3 (high concentration of liquidity) - High hedge ratio - Collateral value close to liquidation threshold
- Attacker executes a large swap to manipulate the UniswapV3 spot price
- This manipulation temporarily reduces the calculated collateral value via `_getCollateral`
- Attacker triggers liquidation of the hedge position
- Attacker profits by claiming the internal collateral (tokensHeld) at a discount

## Recommendations

The collateral should use TWAP price instead of spot price to calculate the external collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GammaSwap_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GammaSwap-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

