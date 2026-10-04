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
solodit_id: 41240
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#18-missing-validation-for-withdrawal-queue-limits
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

Missing Validation for Withdrawal Queue Limits

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the function [\_claimUnstETH](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/abstract/CSBondCore.sol#L187-L190) of the contract `CSBondCore`. The current implementation does not validate the minimum and maximum limits imposed by the withdrawal queue when processing withdrawal requests. This omission can lead to unexpected behavior, as withdrawal requests that fall outside these limits will be rejected.

The issue is classified as **Low** severity because it can disrupt the withdrawal process, leading to unexpected reverts for users.

##### Recommendation
We recommend implementing checks to ensure that the requested withdrawal amounts adhere to the withdrawal queue's minimum and maximum limits.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#18-missing-validation-for-withdrawal-queue-limits
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

