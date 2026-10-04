---
# Core Classification
protocol: Wormhole Shims
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53195
audit_firm: OtterSec
contest_link: https://wormholelabs.com/
source_link: https://wormholelabs.com/
github_link: https://github.com/wormholelabs-xyz/wormhole

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
finders_count: 4
finders:
  - Kevin Chow
  - Robert Chen
  - Gabriel Ottoboni
  - Xiang Yin
---

## Vulnerability Title

Missing Ownership Validation

### Overview

See description below for full details.

### Original Finding Content

## Current Issue

Currently, `process_verify_hash` does not check whether `guardian_signatures` account is owned by the expected program (`VERIFY_VAA_SHIM_PROGRAM_ID`). This implies that any account that can be deserialized into `GuardianSignatures` may be utilized in the verification process.

## Remediation

Modify the function to add an ownership check for the `guardian_signatures` account.

## Patch

Resolved in `a0ffda4`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Wormhole Shims |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, Gabriel Ottoboni, Xiang Yin |

### Source Links

- **Source**: https://wormholelabs.com/
- **GitHub**: https://github.com/wormholelabs-xyz/wormhole
- **Contest**: https://wormholelabs.com/

### Keywords for Search

`vulnerability`

