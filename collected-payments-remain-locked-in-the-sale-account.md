---
# Core Classification
protocol: Exceed Finance Liquid Staking & Early Purchase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58763
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
finders_count: 3
finders:
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Collected Payments Remain Locked in the Sale Account

### Overview


The report states that a bug was fixed by the client in a program called `early-purchase`. The bug was related to transferring payments from buyers to the sale organizer during the token purchase phase. The program did not have a way to transfer these payments to the designated recipient address. The report suggests implementing a mechanism to allow the sale organizer or admin to withdraw the payments and SOL to a designated address.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `de2c6f30136f9ff9cfd6fef5ed6a920024ab7675`. The client provided the following explanation:

> The purchase instruction, sale struct and unit tests were changed and a new 'withdraw_funds' instruction was added.

**File(s) affected:**`programs/early-purchase/src/instructions/deposit_tokens.rs`

**Description:** During the token purchase phase in the `early-purchase` program, buyers transfer their payments (either SPL tokens to the `sale_payment_ata` or SOL directly to the Sale PDA). The sale organizer (acting through a Guardian) deposits the `sale.purchase_mint` tokens for distribution after the sale ends. However, the program lacks a mechanism to transfer the collected buyer payments from the `Sale` PDA and ATA accounts to the sale organizer or a designated treasury.

It is also noted that the address of the user initiating the sale is not saved in the `Sale` PDA, and only guardians with `deposit_tokens` permission can deposit the `sale.purchase_mint` tokens.

**Recommendation:** Consider implementing a mechanism to allow the designated sale organizer or admin to withdraw the collected payment tokens and SOL to a designated recipient address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Exceed Finance Liquid Staking & Early Purchase |
| Report Date | N/A |
| Finders | István Böhm, Mustafa Hasan, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html

### Keywords for Search

`vulnerability`

