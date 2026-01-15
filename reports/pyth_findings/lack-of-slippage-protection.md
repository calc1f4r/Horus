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
solodit_id: 58773
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Lack of Slippage Protection

### Overview


The client has marked a bug as "Fixed" in the `early-purchase` program. The bug was related to purchasing tokens using SOL, where the current price was determined dynamically using a Pyth Network oracle price feed. However, users were not able to specify a maximum amount of SOL they were willing to pay for their desired quantity of tokens, which could lead to issues with recent price volatility. The recommendation is to implement a slippage protection mechanism to prevent this issue in the future. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `67b78deafaafd3c855c080d32eef8fbabc667537`. The client provided the following explanation:

> A u64 field max_lamports_to_spend has been added to PurchaseTokenParams. If SOL is being used as the input token, this field will be checked against the calculated price from the oracle, erroring if its value is exceeded

**File(s) affected:**`programs/early-purchase/src/instructions/purchase_tokens.rs`

**Description:** When users purchase tokens in the `early-purchase` program using SOL, the current SOL price is determined dynamically at the time of transaction execution using a Pyth Network oracle price feed. However, the current token purchase implementation does not allow users to specify a maximum amount of SOL they are willing to pay for their desired quantity of purchase tokens, only the number of tokens to buy.

While the `sale.max_price_feed_age` check ensures the oracle price is not excessively stale, it does not protect against legitimate, recent price volatility that occurs before transaction confirmation. The `sale.purchase_mint` token price (`sale.payment_amount`) may also change without the buyer's knowledge.

**Recommendation:** Consider implementing a slippage protection mechanism to protect users from slippage. For example, allow users to specify the maximum amount of SOL or `sale.payment_mint` tokens they are willing to pay for the requested number (`amount_to_purchase`) of `sale.purchase_mint` tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

