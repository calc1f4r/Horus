---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37097
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Attacker Can Grief `mintWithSignature` And `mintWithAutomation` Calls

### Overview


A high severity bug was found and has been resolved in the DebtorNFT.sol contract. The bug allowed a debtor to accept a creditor's loan position by using two additional functions: mintWithDebtorSignature and mintWithAutomation. These functions call the _validateLoan internal function which checks that the balance of the vault is equal to the debt amount set during loan initialization. However, an attacker can exploit this by sending the minimum amount of debt token directly to the vault contract, causing the _validateLoan function to always revert. The recommendation is to either have an internal accounting system or change the condition to a less than comparison instead of relying on the balanceOf() function.

### Original Finding Content

**Severity** - High

**Status** - Resolved

**Description**

A debtor can accept a creditor’s loan position from the DebtorNFT.sol contract . Aside from the usual mint function (which accepts a loan offer an mints a debtor NFT) there are two more options , one is mintWithDebtorSignature which uses offchain signature and the other is mintWithAutomation which interacts with the DefaultCreditorAutomation.sol.
These 2 functions calls the _validateLoan internal function at L70 and L109 (DebtorNFT.sol)

Inside the _validateLoan at L202 it checks that the balance of the vault should be exactly the debtAmount which was set during the initialization of the loan. 
An attacker can send the minimum amount of debt token directly to the vault contract and make this line revert, and because of this the _validateLoan would always revert since the balance of the vault would never equal debtAmount now.

**Recommendation**:

Instead of relying on balanceOf() have an internal accounting system or change the condition from a strict equality to less than comparison.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

