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
solodit_id: 36216
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#5-the-value-from-storage-is-used-instead-of-memory
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

The value from `storage` is used instead of `memory`

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is a place in the code where the value from `storage` is used instead of a copy of the exact same value in the `memory`: https://github.com/lidofinance/core/blob/efeff81c18f85451ebf98e8fd8bb78b8eb0095f6/contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol#L705-L706.

##### Recommendation
We recommend using `_limitsList` instead of `_limits` in the `_checkCLBalanceDecrease` function.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#5-the-value-from-storage-is-used-instead-of-memory
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

