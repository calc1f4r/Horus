---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37859
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/LeXscrow/README.md#4-missing-checks-for-zero-address
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

4 Missing checks for zero address

### Overview

See description below for full details.

### Original Finding Content

##### Description
If `openOffer = true`, the buyer's address should be zero:
https://github.com/MetaLex-Tech/LeXscrow/blob/94ca277528bb25b8421dc127941c18915144eb29/src/EthLexscrowFactory.sol#L95.

##### Recommendation
We recommend adding a check that the `buyer` address is zero if `openOffer = true`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/LeXscrow/README.md#4-missing-checks-for-zero-address
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

