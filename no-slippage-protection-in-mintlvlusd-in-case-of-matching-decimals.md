---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46588
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
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
finders_count: 3
finders:
  - Mario Poneder
  - Delvir0
  - Om Parikh
---

## Vulnerability Title

No slippage protection in mintlvlUSD in case of matching decimals 

### Overview


This bug report is about a potential issue with the mintlvlUSD method in the LevelBaseReserveManager contract. If the decimals of the collateral token and the lvlUSD token are the same, the minimum lvlUSDAmount will remain 0, which could result in losses for the receiver or collateral provider. This is because the minimum lvlUSDAmount serves as a protection against slippage. The report recommends adding a condition to cover this case and states that the bug has been fixed in a recent pull request. The risk of this bug is considered low. 

### Original Finding Content

## Vulnerability Report

## Context
**File**: LevelBaseReserveManager.sol  
**Lines**: 203-213

## Description
In the `mintlvlUSD` method, if `collateralDecimals == lvlUsdDecimals`, the minimum `lvlUSDAmount` (slippage protection) will remain 0, leading to potential losses for the receiver/collateral provider.

The `mintlvlUSD` method of the `LevelBaseReserveManager` contract is responsible for creating and submitting a MINT order to the `LevelMinting` contract to mint the appropriate amount of `lvlUSD` for the given amount of collateral. This order includes a minimum `lvlUSDAmount`, which serves as a slippage parameter, ensuring that the receiver/collateral provider is not at a loss due to an unexpectedly low amount of minted `lvlUSD`.

Assuming the collateral is also a USD stablecoin, the minimum `lvlUSDAmount` only needs to be scaled according to the collateral token's decimals:

```solidity
uint256 lvlUSDAmount;
if (collateralDecimals < lvlUsdDecimals) {
    lvlUSDAmount = collateralAmount * (10 ** (lvlUsdDecimals - collateralDecimals));
} else if (collateralDecimals > lvlUsdDecimals) {
    lvlUSDAmount = collateralAmount / (10 ** (collateralDecimals - lvlUsdDecimals));
}
```

However, in the case where `collateralDecimals == lvlUsdDecimals`, the `lvlUSDAmount` remains 0.

## Impact
Having a minimum `lvlUSDAmount` of 0 exposes the receiver/collateral provider to a maximum slippage risk in terms of minted `lvlUSD` vs. provided collateral, which can result in a severe loss.

## Likelihood
The `lvlUSD` token has 18 decimals, which is most common for ERC20 tokens. Despite USDC/USDT having only 6 decimals on Ethereum, it is not unlikely that another stablecoin with 18 decimals will be used as collateral.

## Recommendation
It is recommended to cover the case where `collateralDecimals == lvlUsdDecimals`:

```solidity
uint256 lvlUSDAmount;
if (collateralDecimals < lvlUsdDecimals) {
    lvlUSDAmount = collateralAmount * (10 ** (lvlUsdDecimals - collateralDecimals));
} else if (collateralDecimals > lvlUsdDecimals) {
    lvlUSDAmount = collateralAmount / (10 ** (collateralDecimals - lvlUsdDecimals));
} else {
    lvlUSDAmount = collateralAmount;
}
```

## Level
Fixed in PR 25.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Mario Poneder, Delvir0, Om Parikh |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022

### Keywords for Search

`vulnerability`

