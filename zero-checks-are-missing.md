---
# Core Classification
protocol: Algebra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27905
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Farmings/README.md#17-zero-checks-are-missing
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

Zero checks are missing

### Overview

See description below for full details.

### Original Finding Content

##### Description
The protocol allows to transfer 0 amount of tokens to the 0 address.
https://github.com/cryptoalgebra/Algebra/blob/7290fad656bfa89db3743c52af631154f6a8a2d5/src/tokenomics/contracts/farmings/AlgebraEternalFarming.sol#L410

##### Recommendation
We recommend adding a check that tokens cannot be transferred to the 0 address and farming doesn't try to send 0 tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Algebra Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Farmings/README.md#17-zero-checks-are-missing
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

