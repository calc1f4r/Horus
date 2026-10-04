---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1307
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/126

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

protocol_categories:
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - p4st13r4
---

## Vulnerability Title

[M-01] repayDebt in Vault.sol could DOS functionality for markets

### Overview


This bug report is about a vulnerability in the `Vault.sol` smart contract. The `repayDebt()` function allows any user to pay the debt for any borrower, up-to and including the `totalDebt` value. If a malicious user were to repay the debt for all the borrowers, markets functionality regarding borrowing would be DOSed. The proof of concept to demonstrate this vulnerability can be found in the given link and the recommended mitigation step is to make `repayDebt()` accept an amount up-to and including the value of the debt for the given borrower.

### Original Finding Content

_Submitted by p4st13r4_

Any user can pay the debt for any borrower in `Vault.sol`, by using `repayDebt()`. This function allows anyone to repay any amount of borrowed value, up-to and including the `totalDebt` value; it works by setting the `debts[_target]` to zero, and decreasing `totalDebt` by the given amount, up to zero. However, all debts of the other borrowers are left untouched.

If a malicious (but generous) user were to repay the debt for all the borrowers, markets functionality regarding borrowing would be DOSed: the vault would try to decrease the debt of the market, successfully, but would fail to decrease `totalDebt` as it would result in an underflow

#### Proof of Concept

<https://github.com/code-423n4/2022-01-insure/blob/main/contracts/Vault.sol#L257>


#### Recommended Mitigation Steps

Make `repayDebt()` accept an amount up-to and including the value of the debt for the given borrower

**[oishun1112 (Insure) confirmed](https://github.com/code-423n4/2022-01-insure-findings/issues/126):**
 > this needs to be specified how in more detail.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | p4st13r4 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/126
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`vulnerability`

