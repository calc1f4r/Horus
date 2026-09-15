---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45738
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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
  - Zokyo
---

## Vulnerability Title

NFT Holder Cannot Withdraw Repaid Amount Due to Loan Seller Check

### Overview


This bug report discusses an issue with the Receivable NFT in the LoanManager.sol and Receivable.sol contracts. The NFT restricts the ability to withdraw debt repayment to the original lender, but allows for the transfer of the NFT. This can lead to disputes and misrepresentations in transactions involving the NFT. The recommendation is to make the NFT non-transferrable to ensure the current owner can rightfully claim the repayment. A client has commented that the withdrawal function currently only allows for early payment from Isle's pool and does not check the seller's address.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Location** LoanManager.sol, Receivable.sol

**Description**: 

The Receivable NFT, which represents a transferable debt claim, restricts the ability to withdraw the repayment of the debt to the original lender (loan_.seller) while allowing the transfer of the NFT. In the LoanManager.sol contract, the withdrawFunds() function checks if the caller is the original lender, preventing new NFT holders from accessing repaid funds. This disallows the transfer of the debt along with its claim, leading to potential disputes and misrepresentations in transactions involving the NFT.

**Recommendation** 

Since that the debt is meant to be claimed by the original lender, it would be consistent to have non-transferrable Receivable NFT. This change will ensure that the current owner of the Receivable NFT can rightfully claim the repayment of the debt.

**Client comment#1** : The amount that can be withdrawn is not the repaid amount, it is the early payment amount from Isle’s pool. Right now we fix this issue through a removed seller address check in the withdrawalFunds(), we let the holder of NFT have the right to withdraw.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

