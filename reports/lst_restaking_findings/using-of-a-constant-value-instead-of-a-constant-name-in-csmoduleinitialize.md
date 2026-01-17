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
solodit_id: 41239
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#17-using-of-a-constant-value-instead-of-a-constant-name-in-csmoduleinitialize
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

Using of a constant value instead of a constant name in `CSModule.initialize()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
`_pauseFor(type(uint256).max);` [is used](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L206-L207) in `CSModule.initialize()` for an infinite pause. However, `PausableUntil.PAUSE_INFINITELY` is a special constant for this purpose.

##### Recommendation
We recommend changing 
`_pauseFor(type(uint256).max);`
to 
`_pauseFor(PAUSE_INFINITELY);`
in `CSModule.initialize()`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#17-using-of-a-constant-value-instead-of-a-constant-name-in-csmoduleinitialize
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

