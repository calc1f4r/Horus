---
# Core Classification
protocol: Bucket Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63383
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
source_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
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
  - Hamed Mohammadi
  - Adrian Koegl
  - Rabib Islam
---

## Vulnerability Title

Protocol only Supports Hard Liquidations

### Overview

See description below for full details.

### Original Finding Content

**Update**
"Acknowledged" by the client. The client provided the following explanation:

> On purpose. Will upgrade to soft liquidation if needed using the LiquidationRule witness.

**File(s) affected:**`bucket_cdp/sources/vault.move`

**Description:** The liquidation mechanism forces complete position closure regardless of how slightly a position breaches the minimum collateralization ratio. For example, a position at 149% collateralization faces total liquidation despite needing only minimal deleveraging to restore a 150% threshold. This all-or-nothing approach causes unnecessarily severe user losses and discourages efficient capital utilization near the collateralization boundaries.

The implementation allows liquidators to specify repayment amounts but always liquidates proportionally across the entire position rather than targeting a healthy collateralization ratio. This design may hold back users who are looking for optimized capital efficiency, since their position would be extremely risky.

**Recommendation:** Implement partial liquidation logic that calculates and liquidates only the minimum collateral needed to restore a position to a safe collateralization level.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bucket Protocol V2 |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html

### Keywords for Search

`vulnerability`

