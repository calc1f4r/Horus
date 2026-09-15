---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36219
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#8-unobvious-durations-of-time-in-_checkclbalancedecrease
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Unobvious durations of time in `_checkCLBalanceDecrease()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
Two-time durations (`18 days` and `54 days`) are used directly in `_checkCLBalanceDecrease()` which is not obvious and explained only in the documentation. This might reduce code readability.

https://github.com/lidofinance/core/blob/efeff81c18f85451ebf98e8fd8bb78b8eb0095f6/contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol#L703-L706

##### Recommendation
We recommend using constants for `18 days` and `54 days` with brief comments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#8-unobvious-durations-of-time-in-_checkclbalancedecrease
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

