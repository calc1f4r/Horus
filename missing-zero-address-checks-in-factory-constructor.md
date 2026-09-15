---
# Core Classification
protocol: Yield Basis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61929
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yield%20Basis/DAO/README.md#2-missing-zero-address-checks-in-factory-constructor
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

Missing Zero-Address Checks in `Factory` Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description

Only `price_oracle_impl` is validated; `amm_impl` and `lt_impl` are not. If either is zero, `create_from_blueprint` will revert, bricking the factory.

https://github.com/yield-basis/yb-core/blob/3352c612fc33e48f1a106da41f63810f31bc38be/contracts/Factory.vy#L110
<br/>
##### Recommendation

We recommend asserting `amm_impl` and `lt_impl` are not zero.



---


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yield Basis |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yield%20Basis/DAO/README.md#2-missing-zero-address-checks-in-factory-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

