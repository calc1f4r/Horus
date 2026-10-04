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
solodit_id: 58762
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

Tokens Can Be Redeemed From Any Sale

### Overview


This bug report is about a vulnerability in a program that allows an attacker to create fake receipts and use them to redeem legitimate tokens from a sale. The client has marked it as "fixed" and provided an explanation on how they addressed the issue. They also recommend adding a new feature to prevent this type of exploit in the future.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `e57b33c4e7604080c2824c07dba116d77c5d02b5`. The client provided the following explanation:

> The sale key was added to the receipt PDA seeds and new unit tests were created to test this edge case

**File(s) affected:**`programs/early-purchase/src/state/sale.rs`, `programs/early-purchase/src/instructions/purchase_tokens.rs`, `programs/early-purchase/src/instructions/redeem_receipt.rs`

**Description:** Sale accounts can be created by any user and they are assigned as their admins. Additionally, receipt PDAs are derived with the following seeds at the buyer's first token purchase:

```
seeds = [
    Receipt::PREFIX.as_bytes(),
    &buyer.key.to_bytes()
]
```

This implies that `Receipt` accounts are initialized in a 1:1 relation to buyer accounts, allowing an attacker to create a receipt and purchase an amount of a worthless token and redeem the receipt against a sale that holds actual, legitimate tokens.

**Exploit Scenario:**

1.   An attacker creates a new "mock" token.
2.   The attacker creates a sale and sells the "mock" tokens for a very cheap price.
3.   The attacker buys 1000000 "mock" tokens. Their receipt now records the amount of tokens they purchased, but not the sale address.
4.   A legitimate sale ends, and users can start redeeming their receipts.
5.   The attacker uses the receipt from the "mock" tokens to redeem 1000000 tokens from the legit sale.

**Recommendation:** Consider adding the `sale` pubkey to the seeds used to derive the `receipt` PDA and only allow one `receipt` account per token, much like how ATAs work.

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

