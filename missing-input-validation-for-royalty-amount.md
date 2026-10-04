---
# Core Classification
protocol: Petaverse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60627
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/petaverse/194b7ad8-a1b4-43f9-9e3e-f8655173fffc/index.html
source_link: https://certificate.quantstamp.com/full/petaverse/194b7ad8-a1b4-43f9-9e3e-f8655173fffc/index.html
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
finders_count: 4
finders:
  - Danny Aksenov
  - Hytham Farah
  - Mostafa Yassin
  - Jonathan Mevs
---

## Vulnerability Title

Missing Input Validation for Royalty Amount

### Overview


The bug report discusses an issue with the `setRoyaltyInfo()` function in the `Pet.sol` and `Voucher.sol` files. The function does not check for the `0x0` address in the `royaltyReceiver` and does not set an upper bound for the `royaltyNumerator`. This can result in the royalty being higher than the sale price. The recommendation is to fix these issues by adding checks for the `royaltyReceiver` and setting an upper bound for the `royaltyNumerator`. This has been fixed in the `acfbdd3` update, where the Openzeppelin ERC2981 standard has been implemented.

### Original Finding Content

**Update**
**Fixed** in `acfbdd3`. Switched to using Openzeppelin ERC2981 standard.

**File(s) affected:**`Pet.sol`, `Voucher.sol`

**Description:** The function `setRoyaltyInfo()` does not verify the `royaltyReceiver` to not be the `0x0 address`, and the `royaltyNumerator` to be within a defined bound.

If the royaltyNumerator is the same as the `ROYALTY_DENOMINATOR`, then the royalty will be the entire sale price.

If it is greater than the `ROYALTY_DENOMINATOR` then the royalty will be more than the sale price itself.

**Recommendation:** Check the `royaltyReceiver` to not be the 0x0 address. Also, set an upper bound for the `royaltyNumerator`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Petaverse |
| Report Date | N/A |
| Finders | Danny Aksenov, Hytham Farah, Mostafa Yassin, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/petaverse/194b7ad8-a1b4-43f9-9e3e-f8655173fffc/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/petaverse/194b7ad8-a1b4-43f9-9e3e-f8655173fffc/index.html

### Keywords for Search

`vulnerability`

