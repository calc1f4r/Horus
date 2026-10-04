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
solodit_id: 48764
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

Missing Loan Recipient Account Check

### Overview


The report states that there is a bug in the AcceptBorrowRequest instruction which allows an attacker to transfer requested tokens to their own account without the borrower receiving them. This means that the borrower still has to repay the tokens or risk losing their collateral to the lender. The report provides steps to recreate the bug and suggests using Anchor constraints to fix it. The bug has been fixed in the latest patch.

### Original Finding Content

## Vulnerability in AcceptBorrowRequest Instruction

In the `AcceptBorrowRequest` instruction, the `loan_recipient_token_account` and `loan_token_mint` accounts are not properly checked against the borrow request state. This allows an attacker to transfer the requested tokens to their own account. Note that even though the borrower does not receive the tokens, they still are forced to repay them. Otherwise, they will lose their collateral to the lender.

## Proof of Concept

Consider the following scenario:

1. A borrower creates a borrow request using the `InitializeBorrowRequest` instruction.
2. The borrower adds one or more collateral tokens to the borrow request using the `AddCollateral` instruction.
3. A malicious lender accepts the borrow request with their own `loan_token_mint` and `loan_recipient_token_account` addresses, using the `AcceptBorrowRequest` instruction.
4. Now, the borrow request is considered to be accepted by the lender, and the loan amount is given to the borrower. However, the borrower doesn’t receive the loan in their account.
5. In addition, the borrower must now pay the requested borrow amount to the lender – or else they will lose their collateral to the lender.
6. After the duration of the loan has expired, if the borrow amount is not yet returned, the lender can seize the collateral using the `SeizeCollateral` instruction.

## Remediation

Use Anchor constraints to enforce the missing checks in the `AcceptBorrowRequest` instruction.

```rust
borrow_request.loan_recipient_token_account == loan_recipient_token_account
&& borrow_request.loan_token_mint == loan_token_mint
```

## Patch

Now using proper token account checks. Fixed in #2

© 2022 OtterSec LLC. All Rights Reserved. 7 / 25

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

