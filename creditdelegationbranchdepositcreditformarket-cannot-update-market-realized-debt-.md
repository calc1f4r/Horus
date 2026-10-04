---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49979
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
  - i_atiq
---

## Vulnerability Title

CreditDelegationBranch::depositCreditForMarket cannot update market realized debt properly

### Overview


The function `CreditDelegationBranch::depositCreditForMarket` is not properly updating the market's realized debt. This happens when the function `market.settleCreditDeposit` is called, which changes the `realizedDebtUsdPerVaultShare` value. However, if the function `CreditDelegationBranch::updateMarketCreditDelegations` is called right after, it resets the `realizedDebtUsdPerVaultShare` to its previous value, undoing the changes made by `settleCreditDeposit`. This can result in markets showing higher realized debt than they should. To fix this, the function `getRealizedDebtUsd` needs to be updated to properly reflect the changes made by `settleCreditDeposit`.

### Original Finding Content

## Summary
The function `CreditDelegationBranch::depositCreditForMarket` calls `market.settleCreditDeposit`, which modifies `realizedDebtUsdPerVaultShare`. However, if `CreditDelegationBranch::updateMarketCreditDelegations` is called immediately after, it **resets `realizedDebtUsdPerVaultShare` to its previous value**, effectively undoing the changes made by `settleCreditDeposit`.

---

## Vulnerability Details

When engine calls `depositCreditForMarket` to deposit USDC, `settleCreditDeposit` is called with address zero. So no asset from `creditDeposits` is removed in market storage. The `settleCreditDeposit` just updates the usdc amount and realized debt per vault share. But if immediately someone calls `updateMarketCreditDelegations`, it will update the `realizedDebtUsdPerVaultShare` to previous value.

call stack:
`updateMarketCreditDelegations` -> `Vault::recalculateVaultsCreditCapacity` -> `_recalculateConnectedMarketsState`

The `_recalculateConnectedMarketsState` calls `Market::getRealizedDebtUsd` to get all realized debt. This function returns all the added value of credit deposits in USD. `_recalculateConnectedMarketsState` will then call `distributeDebtToVaults` to update the `realizedDebtUsdPerVaultShare`.

Since when calling `settleCreditDeposit`, address zero is passed, no credit address is removed. So `getRealizedDebtUsd` will return the same value even after credit is settled. As a result `realizedDebtUsdPerVaultShare` will go back to previous value.

---

## Impact
- Markets will continue showing higher realized debt than they should.
- If `updateMarketCreditDelegations()` is called immediately, the **debt settlement is erased**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | i_atiq |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

