---
# Core Classification
protocol: TON Locker Contract
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60486
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ton-locker-contract/6872997f-1110-45cc-b70f-2a4cd639da1f/index.html
source_link: https://certificate.quantstamp.com/full/ton-locker-contract/6872997f-1110-45cc-b70f-2a4cd639da1f/index.html
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
finders_count: 2
finders:
  - Andy Lin
  - Valerian Callens
---

## Vulnerability Title

Missing Validation for `vesting_total_duration`

### Overview

See description below for full details.

### Original Finding Content

**Update**
The team has acknowledged and decided to keep the minor issue as it is.

**File(s) affected:**`locker.fc`

**Description:** As stated in the file `README.md`, the `locker` contract should include a check for `vesting_total_duration > 0`. However, the `locker.load_data()` function currently includes validations for `deposit_end_time < vesting_start_time` and `mod( vesting_total_duration, unlock_period) == 0`, but it does not include the validation for `vesting_total_duration`.

**Recommendation:** Consider checking that `vesting_total_duration > 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | TON Locker Contract |
| Report Date | N/A |
| Finders | Andy Lin, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ton-locker-contract/6872997f-1110-45cc-b70f-2a4cd639da1f/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ton-locker-contract/6872997f-1110-45cc-b70f-2a4cd639da1f/index.html

### Keywords for Search

`vulnerability`

