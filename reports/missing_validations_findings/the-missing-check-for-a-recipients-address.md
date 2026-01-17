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
solodit_id: 27875
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Periphery/README.md#7-the-missing-check-for-a-recipients-address
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

The missing check for a recipient's address

### Overview

See description below for full details.

### Original Finding Content

##### Description
There are two functions - https://github.com/cryptoalgebra/Algebra/blob/bddd6487c86e0d6afef39638159dc403a91ba433/src/periphery/contracts/base/PeripheryPayments.sol#L21 and https://github.com/cryptoalgebra/Algebra/blob/bddd6487c86e0d6afef39638159dc403a91ba433/src/periphery/contracts/base/PeripheryPayments.sol#L32 which accept the `recipient` address as a parameter. As the `recipient` parameter value is not checked, it is possible to transfer tokens to zero address.
##### Recommendation
We recommend adding checks that the `recipient` is not a zero address in both functions.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Periphery/README.md#7-the-missing-check-for-a-recipients-address
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

