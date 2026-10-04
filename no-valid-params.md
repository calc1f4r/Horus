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
solodit_id: 28366
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#1-no-valid-params
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

No valid params

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is some admin methods which don't check values:
* `setMotionDuration` - `_motionDuration` may be too large https://github.com/lidofinance/easy-track/blob/ec694adb872877db814da960d96ce767ccbdf462/contracts/MotionSettings.sol#L23
* `setMotionsCountLimit` — `_motionsCountLimit` may be zero https://github.com/lidofinance/easy-track/blob/ec694adb872877db814da960d96ce767ccbdf462/contracts/MotionSettings.sol#L40
This allows admin to make an incorrect configuration.
##### Recommendation
If necessary, we recommend to insert additional checks.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Easy%20Track/README.md#1-no-valid-params
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

