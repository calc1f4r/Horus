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
solodit_id: 41237
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#15-unnecessary-modifier-whenpaused
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

Unnecessary modifier `whenPaused`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [resume](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSFeeOracle.sol#L139) function of the `CSFeeOracle` contract. There is an unnecessary `whenPaused` modifier used because there is a `_checkPaused` check inside the `_resume` function at the [following line](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/lib/utils/PausableUntil.sol#L54).

The issue is classified as **Low** severity because it doesn't affect the protocol functionality, but the unnecessary modifier removal can improve its efficiency.

##### Recommendation
We recommend removing the mentioned unnecessary modifier from the `resume` function.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#15-unnecessary-modifier-whenpaused
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

