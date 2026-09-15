---
# Core Classification
protocol: Scallop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47940
audit_firm: OtterSec
contest_link: https://scallop.io/
source_link: https://scallop.io/
github_link: https://github.com/scallop-io/sui-lending-protocol

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
finders_count: 5
finders:
  - Akash Gurugunti
  - Ilardi Marco
  - Sangsoo Kang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Eliminate Obsolete Constants

### Overview

See description below for full details.

### Original Finding Content

## Unutilized Constants in Codebase

Several constants in the codebase are declared without being utilized. These unutilized constants may confuse developers and make the codebase harder to maintain. The constants in question are:

1. `u64::DIVIDE_BY_ZERO`
2. `pyth_rule::rule::U8_MAX`
3. `cetus_adaptor::cetus_flash_loan::ERepayTypeIncorrect`
4. `supra_rule::rule::U8_MAX`
5. `supra_rule::rule::U64_MAX`

## Remediation

Remove the aforementioned unutilized constants.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Scallop |
| Report Date | N/A |
| Finders | Akash Gurugunti, Ilardi Marco, Sangsoo Kang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://scallop.io/
- **GitHub**: https://github.com/scallop-io/sui-lending-protocol
- **Contest**: https://scallop.io/

### Keywords for Search

`vulnerability`

