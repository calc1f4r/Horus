---
# Core Classification
protocol: Akita
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48768
audit_firm: OtterSec
contest_link: https://akt.finance/
source_link: https://akt.finance/
github_link: https://github.com/otter-sec/akita/tree/master/ programs/akita.

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Unsound collateral design

### Overview


The bug report describes a vulnerability in the AddCollateral instruction, where a malicious user can add collateral with their own collateral_mint and freeze_authority, preventing the borrower and lender from accessing previously added collateral. This can be exploited by freezing the token supply account. To fix this, the WithdrawCollateral and SeizeCollateral instructions need to be modified to be independent of their order. The bug has been fixed in the latest update.

### Original Finding Content

## Collateral Management Vulnerability

Using the **AddCollateral** instruction, any user can add collateral to any borrow request. A malicious user can add collateral with a `collateral_mint` of their own and a `freeze_authority` set to their own account.

The user can then freeze the `collateral_token_account` using their freeze authority. Then neither the borrower nor the lender will be able to withdraw or seize the collateral that is added prior to the malicious collateral, since the token transfer instruction in **WithdrawCollateral** and the **SeizeCollateral** instruction will fail.

## Proof of Concept

Consider the following scenario:

1. A borrower creates a borrow request using the **InitializeBorrowRequest** instruction.
2. The borrower adds one or more collateral tokens to the borrow request using the **AddCollateral** instruction.
3. A malicious user then adds collateral using the **AddCollateral** instruction with a `collateral_mint` of their own and a source token account. The tokens are transferred from the source token account to the token supply (PDA).
4. The malicious user now freezes the token supply PDA account.
5. This prevents both the borrower and the lender from taking the collateral that is added prior to the malicious collateral.

## Remediation

To remediate this vulnerability, implement the **WithdrawCollateral** and **SeizeCollateral** instructions such that they are independent of their order. For example, one could take the index of the collateral and use it to generate the `collateral_token_account` PDA in the **WithdrawCollateral** and **SeizeCollateral** instructions.

## Patch

Changed so that only the borrower can add collateral. Fixed in #3.

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Akita |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://akt.finance/
- **GitHub**: https://github.com/otter-sec/akita/tree/master/ programs/akita.
- **Contest**: https://akt.finance/

### Keywords for Search

`vulnerability`

