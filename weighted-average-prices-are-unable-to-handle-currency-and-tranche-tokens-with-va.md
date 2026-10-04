---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54411
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6
source_link: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
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
  - Liam Eastwood
  - Sujith Somraaj
---

## Vulnerability Title

Weighted average prices are unable to handle currency and tranche tokens with varying decimals 

### Overview


This report discusses an issue in the `InvestmentManager.sol` file between lines 349-403. When deposit or redeem orders are decreased, the price is not being updated correctly which leads to incorrect calculations for currency and tranche token amounts. This is due to the assumption that both amounts are of the same precision, which is not always the case. This issue affects the integration with ERC4626 and has been fixed in the latest commit. 

### Original Finding Content

## Summary of Issue in InvestmentManager.sol

## Context
File: `InvestmentManager.sol`  
Lines: 349-403

## Description
When deposit/redeem orders are decreased, the price needs to be updated to reflect a 1:1 exchange rate of currency or tranche tokens so that they can be readily redeemed. However, if the decimals of the currency and tranche token amounts differ, then the price calculation will be incorrectly stored within `state.depositPrice` and `state.redeemPrice`.

### Code Snippet: `handleExecutedDecreaseInvestOrder`

```solidity
function handleExecutedDecreaseInvestOrder(
    uint64 poolId,
    bytes16 trancheId,
    address user,
    uint128 currencyId,
    uint128 currencyPayout,
    uint128 remainingInvestOrder
) public onlyGateway {
    // ...
    // Calculating the price with both payouts as currencyPayout
    // leads to an effective redeem price of 1.0 and thus the user actually receiving
    // exactly currencyPayout on both deposit() and mint()
    state.redeemPrice = _calculatePrice(
        liquidityPool,
        state.maxWithdraw + currencyPayout,
        ((maxRedeem(liquidityPool, user)) + currencyPayout).toUint128()
    );
    // ...
}
```

As noted here, `_calculatePrice()` takes two amount arguments, `currencyAmount` and `trancheTokenAmount`. However, it assumes that both these amounts are according to their respective decimal precision. It is dangerous to assume that `((maxRedeem(liquidityPool, user)) + currencyPayout).toUint128()` will be adding two amounts of the same precision. The same can be said for when `state.depositPrice` is calculated.

### Code Snippet: `handleExecutedDecreaseRedeemOrder`

```solidity
function handleExecutedDecreaseRedeemOrder(
    uint64 poolId,
    bytes16 trancheId,
    address user,
    uint128 currencyId,
    uint128 trancheTokenPayout,
    uint128 remainingRedeemOrder
) public onlyGateway {
    // ...
    // Calculating the price with both payouts as trancheTokenPayout
    // leads to an effective redeem price of 1.0 and thus the user actually receiving
    // exactly trancheTokenPayout on both deposit() and mint()
    InvestmentState storage state = investments[liquidityPool][user];
    state.depositPrice = _calculatePrice(
        liquidityPool, 
        _maxDeposit(liquidityPool, user) + trancheTokenPayout, 
        state.maxMint + trancheTokenPayout
    );
    // ...
}
```

This breaks some integration with ERC4626 as `previewDeposit()` and `previewMint()` return inaccurate token amounts.

## Recommendation
Modify the weighted average price calculation so that it takes into account the decimals of the tokens.

## Status Updates
- **Centrifuge:** Fixed in commit `411494ce`.
- **Cantina:** Verified fix. The `handleExecutedDecreaseInvestOrder()` and `handleExecutedDecreaseRedeemOrder()` functions now perform proper conversions when calculating the new redeem and deposit prices.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Liam Eastwood, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_centrifuge_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/693b6f24-6e47-4194-97b0-356d10dc1df6

### Keywords for Search

`vulnerability`

