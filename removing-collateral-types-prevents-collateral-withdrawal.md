---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60129
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Removing Collateral Types Prevents Collateral Withdrawal

### Overview


The client has acknowledged an issue where the function `removeCollateral()` in `CollateralManager.sol` and `BorrowerOperations.sol` is causing problems for users trying to withdraw their collateral. This is because the collateral must be in a specific state before being removed, and if it is removed, users are unable to withdraw their EToken balance. Additionally, changing the EToken can also cause issues with users' ICR and TCR. The recommendation is to either create a way for users to redeem their ETokens for unsupported collaterals or disable the `removeCollateral()` and `setEToken()` functions for collateral types with a non-zero EToken supply. Another suggestion is to create a redemption method for users to redeem their ETokens for unsupported collateral.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The collateral must be in the pause state before being removed. In this state, the user can withdrawColl and closeTrove. Before removal, we will issue an announcement to users about the time to withdraw relevant collateral.

**File(s) affected:**`CollateralManager.sol`, `BorrowerOperations.sol`

**Description:** The function `CollateralManager.removeCollateral()` removes a collateral type from the list of supported collaterals. Once no longer supported, users cannot withdraw their collateral in `BorrowerOperations.withdrawCollateral()`. Any users with a non-zero EToken balance would have no way of reclaiming their collateral.

Additionally, if the EToken is changed by calling `CollateralManager.setEToken()`, the total supply of the previous EToken would map to irredeemable collateral.

Furthermore, removal of a collateral type could result in a very sudden drop of users' ICRs. To take an extreme example, if a user has deposited only stETH and it becomes unsupported, their ICR would drop to zero. This would have a corresponding effect on TCR as well.

Finally, if an EToken is transferred to an address without a trove, such users would be unable to redeem their collateral until they opened a trove.

**Recommendation:**

1.   Either create a way for users to redeem their ETokens for unsupported collaterals, or disable `removeCollateral()` and `setEToken()` for collateral types that have a non-zero total supply of their EToken. 
2.   Create a redemption method for users to redeem their ETokens for now-unsupported collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

