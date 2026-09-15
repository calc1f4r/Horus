---
# Core Classification
protocol: Nayms - OnRe Offer/Redemption Program Spec
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58717
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nayms-on-re-offer-redemption-program-spec/caed5b0c-4b32-4d01-9a3a-aa2174f5485f/index.html
source_link: https://certificate.quantstamp.com/full/nayms-on-re-offer-redemption-program-spec/caed5b0c-4b32-4d01-9a3a-aa2174f5485f/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Paul Clemson
  - István Böhm
  - Mostafa Yassin
---

## Vulnerability Title

Missing Buy Token Amount Validation

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `87f0db3aa86a8749fc49afcbad13c4f6e8fa9175`.

**File(s) affected:**`take_offer.rs`

**Description:** The `instructions::take_offer::calculate_buy_amount()` function does not return an error if the calculated buy token amount is zero because of integer truncation (rounding). Not checking the return value may lead to unexpected behavior.

**Recommendation:** Consider checking if the calculated buy token amount is non-zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Nayms - OnRe Offer/Redemption Program Spec |
| Report Date | N/A |
| Finders | Paul Clemson, István Böhm, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nayms-on-re-offer-redemption-program-spec/caed5b0c-4b32-4d01-9a3a-aa2174f5485f/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nayms-on-re-offer-redemption-program-spec/caed5b0c-4b32-4d01-9a3a-aa2174f5485f/index.html

### Keywords for Search

`vulnerability`

