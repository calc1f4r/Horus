---
# Core Classification
protocol: Altr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60247
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
source_link: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
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
  - Roman Rohleder
  - Ruben Koch
  - Mostafa Yassin
---

## Vulnerability Title

NFT Valuations Indifferent to Borrow Token Decimals

### Overview


The client has marked a bug as "Fixed" in the `Lending.sol` file. The issue is related to the protocol allowing for multiple borrow tokens, but the `PriceIndex` valuation contract is not considering the target borrow token and its decimals when requesting a new loan. This can lead to incorrect borrow restrictions or exceeding the actual collateral value. The recommendation is to take the borrow token decimals into account when checking the target borrow amount.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `6f5b551c82312187a5e26a970ac23ed47027574d`.

**File(s) affected:**`Lending.sol`

**Description:** While the protocol allows for multiple different borrow tokens to be used, as defined with `setTokens()`, the value returned by the `PriceIndex` valuation contract when requesting a new loan is indifferent to the target borrow token and its decimals, always returning the same nomination.

Given an NFT valuation, the following check would be indifferent to the target borrow token decimals, potentially grossly mistreating an allowed borrow amount:

```
require(_amount <= (valuation.price * valuation.ltv) / 100, "Lending: amount greater than max borrow");
```

For example, while the valuation could be designed for tokens with 6 decimals, requesting a loan for a token with more decimals would lead to unnecessary borrow restrictions as a potentially only much lower amount would pass the check. Similarly, a token with less than 6 decimals may allow for borrow amounts exceeding the actual collateral value.

**Recommendation:** We recommend taking the borrow token decimals into account when checking the target borrow amount to be within a certain price valuation bound.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Altr |
| Report Date | N/A |
| Finders | Roman Rohleder, Ruben Koch, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/altr/b6241933-b256-42d2-bb46-acb54a26e560/index.html

### Keywords for Search

`vulnerability`

