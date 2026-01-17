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
solodit_id: 48765
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

Improperly Validated Lender Account

### Overview


The bug report discusses an issue with the AcceptBorrowRequest instruction, where if the lender closes their external token account after accepting the borrow request, the borrower is unable to repay the loan and is forced to default. This can be exploited by a malicious lender, causing the borrower to lose their collateral. To fix this, a PDA should be used to collect the repaid loan amount and a new instruction should be implemented for the lender to collect their loan amount from the PDA. This issue has been addressed in a recent patch.

### Original Finding Content

## AcceptBorrowRequest Instruction Vulnerability

In the **AcceptBorrowRequest** instruction, the lender passes in an external token account which the borrower pays into. If the lender closes said account after accepting the borrow request, the borrower will become unable to repay the loan, and thus is forced to default.

## Proof of Concept

Consider the following scenario:

1. A borrower creates a borrow request using the **InitializeBorrowRequest** instruction.
2. The borrower adds one or more collateral tokens to the borrow request using the **AddCollateral** instruction.
3. A malicious lender accepts the borrow request using the **AcceptBorrowRequest** instruction.
4. After accepting the borrow request, the lender closes their `repay_recipient_token_account`.
5. When the borrower tries to repay their loan using the **RepayLoan** instruction, the transaction fails, since the destination address of the transfer is closed.
6. After the duration of the borrow request is over, the lender seizes the collateral using the **SeizeCollateral** instruction.

## Remediation

To remediate this vulnerability, use a **PDA** (Program Derived Address) that collects the repaid loan amount and implement another instruction for the lender to collect their loan amount from the PDA.

## Patch

Now using a PDA to receive the repaid loan amount. Fixed in #2.

© 2022 OtterSec LLC. All Rights Reserved. 8 / 25

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

