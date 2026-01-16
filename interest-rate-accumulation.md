---
# Core Classification
protocol: Etherfuse Stablebond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46995
audit_firm: OtterSec
contest_link: https://www.etherfuse.com/
source_link: https://www.etherfuse.com/
github_link: https://github.com/etherfuse/stablebond

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Interest Rate Accumulation

### Overview


The bug is related to how interest rates are handled when there is no active bond issuance. The protocol allows users to buy bonds during one issuance and redeem them in another. However, the interest rate for the bonds does not reset to zero after an issuance is completed. This means that the rate continues to accumulate even when there is no active issuance, causing bond prices to increase artificially. This results in users receiving extra rewards during periods when no issuance is active. To fix this issue, all interest rates need to be properly reset to zero after each issuance ends. This bug has been resolved in the latest patch, cf2fc93.

### Original Finding Content

## Issue with Interest Rate Accumulation

The issue revolves around the improper handling of interest rate accumulation, specifically during periods when no active issuance is taking place. The protocol allows buying bonds during one issuance and redeeming them in another. However, the rate for the interest-bearing extension does not reset to zero after an issuance is completed, resulting in the interest-bearing rate continuing to accumulate.

This creates a scenario where, even when there is no active issuance, the rate increases, artificially inflating bond prices. Thus, users receive extra rewards for the time when no issuance is active.

## Remediation

Ensure that all interest-bearing extensions are properly reset to zero after each issuance ends.

## Patch

Resolved in `cf2fc93`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Etherfuse Stablebond |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.etherfuse.com/
- **GitHub**: https://github.com/etherfuse/stablebond
- **Contest**: https://www.etherfuse.com/

### Keywords for Search

`vulnerability`

