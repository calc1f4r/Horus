---
# Core Classification
protocol: Bucket Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48025
audit_firm: OtterSec
contest_link: https://bucketprotocol.io/
source_link: https://bucketprotocol.io/
github_link: https://github.com/Bucket-Protocol/v1-core

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Handle Zero Debt Case For TCR

### Overview

See description below for full details.

### Original Finding Content

## get_bucket_tcr Function in the Bucket Module

The `get_bucket_tcr` function in the bucket module retrieves the total collateral ratio of the Bucket. This function does not handle the scenario where the total minted `$BUCK` amount (debt amount) is zero, resulting in an error.

## Remediation

To resolve this issue, handle the case where the debt amount is zero by returning `constants::max_u64()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Bucket Protocol |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://bucketprotocol.io/
- **GitHub**: https://github.com/Bucket-Protocol/v1-core
- **Contest**: https://bucketprotocol.io/

### Keywords for Search

`vulnerability`

