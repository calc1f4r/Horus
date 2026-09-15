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
solodit_id: 58780
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

Missing Validation Can Lead to Duplicate Guardians in `AccessControl` Compromising Security Redundancy

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9529211a655d1c900d3ec9830cdb2b6f1833209b`. The client provided the following explanation:

> Added a check for existing guardians in the array when adding and removing. Added a new unit test.

**File(s) affected:**`programs/liquid-staking/src/instructions/manage_guardian.rs`

**Description:** In `liquid_staking::manage_guardian::handler()`function, an `unseal_authority` can add or remove guardians from the `AccessControl` Account. While the `AccessControl` account supports adding up to five guardians for security redundancy, the implementation lacks duplicate checking for each guardian `Pubkey`. This oversight allows the same guardian `Pubkey` to be added multiple times, potentially compromising the intended redundancy if multiple or all five guardian slots contain identical keys.

**Recommendation:** Consider implementing verification logic to prevent duplicate guardian `Pubkeys` from being added to the `AccessControl` Account.

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

