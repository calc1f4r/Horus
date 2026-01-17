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
solodit_id: 58779
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Incorrect Minimum and Excess Deposit Checks in `LST` Swaps

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `22c750b83b4ec4febf87d195dddec9bd02325a58`. The client provided the following explanation:

> Fixed calls to exessive and minimum deposit validation methods. Added unit tests.

**File(s) affected:**`programs/liquid-staking/src/instructions/swap_lst.rs`

**Description:** The `liquid_staking::swap_lst::handler()` function enables holders of one LST to swap it for a different LST. However the function call on the `destination_pair` that checks if the deposit is too large incorrectly passes zero for the `base_token_amount` field of the function `destination_pair.check_excessive_deposit(quote_amount, base_token_amount)`. Moreover, it lacks a check to validate the the deposit meets the minimum bar via `check_minimum_deposit()`.

**Recommendation:** Consider using the correct parameters when calling `check_excessive_deposit()` and including a call to `check_minimum_deposit()` on the destination pair to ensure that the LST swap meets the maximum and minimum requirements.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

