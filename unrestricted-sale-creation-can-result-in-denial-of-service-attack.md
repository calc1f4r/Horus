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
solodit_id: 58775
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

Unrestricted Sale Creation Can Result in Denial of Service Attack

### Overview


The client has marked a bug as "Fixed" in the file `programs/early-purchase/src/instructions/initialize_sale.rs`. The bug allows any user to create a new sale without any fees or restrictions, which can be exploited by malicious actors to spam the platform or create sales with harmful properties. The recommendation is to add a fee or permission restriction to the initialization instruction and to add the creator's key to the Sale PDA seed to prevent global ID exhaustion.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `8dc2fd528da16911410d19d9b3545a5fb9bd2254`

**File(s) affected:**`programs/early-purchase/src/instructions/initialize_sale.rs`

**Description:** The `early_purchase::initialize_sale::handler()` function allows any user to create a new `Sale`. However, it does not implement any fee or significant disincentive beyond standard Solana transaction costs and account rent. This open and low-cost sale creation mechanism that can be exploited by malicious actors to spam the platform by creating a large number of sales or create sales with malicious properties.

**Recommendation:** Consider adding a sale creation fee or refundable deposit to the initialization instruction, or restrict the sale creation to permissioned users. Consider also adding the creator's key to the seed of the Sale PDA, preventing global ID exhaustion.

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

