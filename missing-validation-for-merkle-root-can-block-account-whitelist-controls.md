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
solodit_id: 58790
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

Missing Validation for Merkle Root Can Block Account Whitelist Controls

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> This is not really a bug, in general, it is always possible to set the root hash to some invalid hash, there is no real way to verify the legitimate hash without passing in the whole tree, which we should avoid doing due to memory constraints.

**File(s) affected:**`programs/liquid-staking/src/instructions/update_whitelist.rs`

**Description:** In `liquid_staking::update_whitelist.handler()`function, an `access_authority` can update the `access_control.merkle_root` value. However, the function lacks validation to prevent setting the `merkle_root` to an array of all zeros. This oversight creates a potential issue which may block any whitelist verification logic (especially if `is_whitelist_enabled` remains enabled). Additionally, since this function modifies critical program state, an event should be emitted for auditability.

**Recommendation:** Consider implementing validation to reject `merkle_root` values containing all zeros and emit an event when the whitelist is updated.

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

