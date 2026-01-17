---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40209
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Calculating liquidationReward without considering collateral decimals 

### Overview


The liquidationReward() function in the LiquidationLib.sol file is not properly calculating the liquidator's reward. This is because it does not take into account the decimals of the collateral and TCAP, resulting in a larger reward for liquidators when the collateral is a low decimals token. To fix this, the function should be changed to include the assetDecimals parameter and adjust the calculation accordingly. This bug has been fixed in the Cryptex and Cantina Managed repositories.

### Original Finding Content

## LiquidationLib.sol: Lines 17-19

**Description:**  
In liquidation, the `liquidationReward()` function is used to calculate the liquidator's reward. It computes the rewarded collateral amount based on the TCAP amount burned by the liquidator.

```solidity
function liquidationReward(uint256 burnAmount, uint256 tcapPrice, uint256 collateralPrice, uint64 liquidationPenalty) internal pure returns (uint256) {
    return burnAmount * tcapPrice * (1e18 + liquidationPenalty) / collateralPrice / 1e18;
}
```

**Problem:**  
The issue here is that `liquidationReward()` doesn't take into account the decimals of the collateral and TCAP, resulting in the calculated `liquidationReward` being quite large when the collateral is a low-decimals token (such as USDC/USDT), thereby giving the liquidator a larger reward.

**Recommendation:**  
Change to:
```solidity
- liquidationReward = LiquidationLib.liquidationReward(burnAmount, tcapPrice, collateralPrice, liquidation.penalty);
+ liquidationReward = LiquidationLib.liquidationReward(burnAmount, tcapPrice, collateralPrice, liquidation.penalty, assetDecimals);
```

Modify the function as follows:
```solidity
- function liquidationReward(uint256 burnAmount, uint256 tcapPrice, uint256 collateralPrice, uint64 liquidationPenalty) internal pure returns (uint256) {
-     return burnAmount * tcapPrice * (1e18 + liquidationPenalty) / collateralPrice / 1e18;
+ function liquidationReward(uint256 burnAmount, uint256 tcapPrice, uint256 collateralPrice, uint64 liquidationPenalty, uint8 collateralDecimals) internal pure returns (uint256) {
+     return burnAmount * tcapPrice * (1e18 + liquidationPenalty) * 10 ** collateralDecimals / collateralPrice / 1e18 / 10 ** 18;
}
```

**Cryptex:** Fixed in PR 9.  
**Cantina Managed:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

