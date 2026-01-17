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
solodit_id: 41231
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#9-inflexibility-in-contract-pause-duration-extension
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

Inflexibility in Contract Pause Duration Extension

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [\_pauseFor](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/utils/PausableUntil.sol#L59-L70) function of the `PausableUntil` contract. Currently, the function does not allow for the prolongation of an existing pause duration. Once set, the pause duration is fixed until it expires. This lack of flexibility could lead to poor user experience, especially in scenarios where extending a pause without resuming the contract would be beneficial.

The issue is classified as **Low** severity because it pertains to the user experience and administrative flexibility rather than the core functionality or security of the contract.

##### Recommendation
We recommend enhancing the `_pauseFor` function to allow for the extension of the current pause duration.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#9-inflexibility-in-contract-pause-duration-extension
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

