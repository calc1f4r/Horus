---
# Core Classification
protocol: Secured Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59983
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
source_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
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
  - Mustafa Hasan
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Precision Loss in Itayose Process Makes `FutureValueVault` Unstable

### Overview


The bug report addresses an issue with the Future Value Vault and Lending Market Operation Logic. During the Itayose call, the total supply of Future Value is calculated using the Present Value and opening price. However, there is a precision error that occurs when calculating the total supply, leading to a mismatch between the total supply and the sum of all filled pre-orders. This results in the `isAllRemoved` condition never being fulfilled, preventing the proper cleaning of orders after maturity. The recommendation is to avoid this precision error to ensure that `isAllRemoved` can potentially be true and orders can be properly cleaned. 

### Original Finding Content

**Update**
Now the total supply of the Future Vault is split into borrowing and lending supply, and the total amount of the pending orders to be cleaned is checked before moving the residual amount to the Genesis Vault. Addressed in: `aeb7398e437b47acf7ca3e6e3538cf9d01c3fa6f`.

**File(s) affected:**`FutureValueVault.sol`, `LendingMarketOperationLogic.sol`

**Description:** During the Itayose call, we calculate the `totalSupply` of Future Value (FV) using the Present Value (PV) (total amount filled in Itayose pre-orders) and `openingPrice` calculated from them.

Following the scenario below:

If the offset pre-order has the following amount with an opening unit price of `9220`, a precision loss will happen.

```
A: 100
B: 200
```

After the Itayose process, the total supply will be `325 = (300 * 10000) / 9220`, calculated from the opening price and the total filled amount from the pre-orders.

But each PV of order becomes:

```
A: 108 = (100 * 10000) / 9220
B: 216 = (200 * 10000) / 9220
```

This total sum of orders' future value is `324`, so the precision loss is `1` (`totalSupply` was set to `325`). `isAllRemoved` will never be fulfilled in `FutureValueVault.reset()`, leading to never calling `GenesisValueVault.updateGenesisValueWithResidualAmount()`.

```
isAllRemoved =
    Storage.slot().removedLendingSupply[maturity] == Storage.slot().totalSupply[maturity] &&
    Storage.slot().removedBorrowingSupply[maturity] == Storage.slot().totalSupply[maturity];
```

**Recommendation:** Avoid precision error, so the total supply calculated in the Itayose process will match the sum of all filled pre-orders with the Itayose opening price. This way, when orders are cleaned (after maturity), `isAllRemoved` will have the possibility to be `true`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Secured Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html

### Keywords for Search

`vulnerability`

