---
# Core Classification
protocol: Hanji
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55162
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Hanji/Liquidity%20Vault/README.md#4-unnecessary-state-storage-of-pyth-address
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

Unnecessary State Storage of `pyth` Address

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `pyth` address is stored as a regular state variable. If this address is never intended to change, making it effectively immutable could save gas on repeated reads.

The issue is classified as **low** severity because it focuses on optimization rather than a security flaw.

##### Recommendation
We recommend defining `pyth` as an `immutable` variable within the constructor if updates are unnecessary post-deployment.

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Hanji |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Hanji/Liquidity%20Vault/README.md#4-unnecessary-state-storage-of-pyth-address
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

