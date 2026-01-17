---
# Core Classification
protocol: Finance Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51951
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bonzo/finance-contracts
source_link: https://www.halborn.com/audits/bonzo/finance-contracts
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
  - Halborn
---

## Vulnerability Title

Unsafe Modification of Decimals in LendingPoolConfigurator

### Overview


This bug report discusses an issue in the `LendingPoolConfigurator` contract, specifically with the `setDecimals` function. This function allows changing the number of decimals for a reserve asset, but if the new decimals do not match the underlying asset's actual decimals, it can cause critical issues. These issues include under or overestimation of collateral value, discrepancies in borrowing calculations, and potential liquidation or over-leverage scenarios for users. The report recommends either removing the `setDecimals` functionality or restricting changes to only when there are no supplies or borrows in the pool. The bug has been solved by removing the `setDecimals` function.

### Original Finding Content

##### Description

In the `LendingPoolConfigurator` contract, the `setDecimals` function allows changing the number of decimals for a reserve asset. This can lead to critical issues if the new decimals do not match the underlying asset's actual decimals. The core functions `getAmountInEth` and `_executeBorrow` assume the decimals correspond to the underlying asset, which impacts calculations involving collateral and borrowing.

Assume:

* Original decimals of the underlying asset: `D1`
* New decimals set via `setDecimals`: `D2`
* Amount of asset held by a user: `A`
* Price of the asset in ETH: `P`

Value in ETH with original decimals:

`V1 = (A*P)/10^{D1}`

Value in ETH with new decimals:

`V2 = (A*P)/10^{D2}`

**Impact:**

* If `D2 > D1`, `V2 < V1`: The collateral value in ETH is underestimated, leading to potential under-collateralization and allowing excessive borrowing.
* If `D2 < D1`, `V2 > V1`: The collateral value in ETH is overestimated, restricting borrowing more than necessary.

Changing the decimals without ensuring they match the underlying asset's decimals can cause:

* Underestimation or overestimation of collateral value.
* Discrepancies in borrowing calculations.
* Potential liquidation or over-leverage scenarios for users.

This demonstrates the critical issues that arise from mismatched decimals, emphasizing the need for consistent handling of asset decimals across the smart contract system.

##### BVSS

[AO:S/AC:L/AX:L/C:M/I:C/A:C/D:C/Y:C/R:N/S:C (4.7)](/bvss?q=AO:S/AC:L/AX:L/C:M/I:C/A:C/D:C/Y:C/R:N/S:C)

##### Recommendation

1. **Remove the** `setDecimals` **Functionality**: Consider removing the ability to change the decimals of a reserve asset to maintain consistency and avoid critical issues related to collateral and borrowing calculations.

2. **Restrict Decimals Change:** If retaining the functionality, restrict changes to only when there are no supplies or borrows in the pool. Ensure that the new decimals match the underlying asset's actual decimals by performing a validation check before applying the change.

These measures will help maintain the integrity of the system and prevent discrepancies in collateral and borrowing values.

###

##### Remediation

**SOLVED:** The `setDecimals` function was removed.

##### Remediation Hash

9f29c6812e7f962b5f06513c91d7d17123e0650d

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Finance Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bonzo/finance-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bonzo/finance-contracts

### Keywords for Search

`vulnerability`

