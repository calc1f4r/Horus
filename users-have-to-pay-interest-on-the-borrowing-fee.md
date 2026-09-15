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
solodit_id: 60127
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

Users Have to Pay Interest on the Borrowing Fee

### Overview

The client has acknowledged the issue with the proportion of borrowing fees being negligible. This issue affects the `BorrowerOperations.sol` file and results in users being charged a borrowing fee that is added to their total USDE Debt. However, the fee is immediately minted to the treasury and not received by the borrower, causing it to accumulate interest. The recommendation is to track the borrowing fee separately to prevent it from accumulating interest.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The proportion of borrow fees is negligible.

**File(s) affected:**`BorrowerOperations.sol`

**Description:** Users are charged a borrowing fee that is added to their total USDE Debt, which accumulates interest. However, the borrowing fee is minted immediately to the treasury and is never received by the borrower. The borrowing fee should not accumulate interest as it is not loaned to the borrower.

**Recommendation:** Track the borrowing fee separately from the debt such that it does not accumulate interest.

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

