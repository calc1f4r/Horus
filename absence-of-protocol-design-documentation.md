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
solodit_id: 63389
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

Absence of Protocol Design Documentation

### Overview

See description below for full details.

### Original Finding Content

**Update**
The client added a design documentation explaining intentions. This could be extended with graphics and diagrams. Addressed in: `75886a65030e81687b58c743e394668a16508d3f`.

**Description:** The protocol lacks documentation explaining its design decisions, making it difficult to evaluate whether the chosen mechanisms will maintain peg stability. We found no rationale for critical choices like using instant liquidations instead of auctions, allowing users to select oracle subsets, implementing PSM price tolerance thresholds, or excluding liquidation penalties entirely. Without understanding the team's intentions and trade-offs, we cannot properly assess whether our recommendations align with the protocol's goals or if certain "issues" are actually deliberate design choices.

This gap is particularly concerning for a CDP protocol where seemingly minor parameter choices can trigger cascading failures during market stress. The absence of economic modeling documentation or stress test scenarios leaves both auditors and future operators guessing about expected behavior under extreme conditions.

**Recommendation:** Document the reasoning behind key design decisions, including why certain industry-standard mechanisms were excluded and what alternatives were considered. This should cover oracle architecture choices, liquidation mechanism selection, PSM parameters, and the economic models used to validate these decisions. Clear documentation helps distinguish bugs from features and ensures the protocol operates as intended.

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

