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
solodit_id: 41243
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#21-missing-validation-of-depositcalldata-in-depositbufferedether-function
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

Missing Validation of `depositCalldata` in `depositBufferedEther` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [depositBufferedEther](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/DepositSecurityModule.sol#L500) function of the contract `DepositSecurityModule`. The `depositCalldata` parameter is not included in the guardian signatures' validation process. Although `depositCalldata` is not currently used within staking modules, this omission could lead to potential security risks or inconsistencies in future implementations where `depositCalldata` might be utilized. An unchecked `depositCalldata` could allow unintended or malicious data to be processed, compromising the integrity of the deposit process.

##### Recommendation
We recommend either verifying that `depositCalldata` is empty within the current implementation or incorporating it into the message hash that is signed by the guardians. This will ensure that any future use of `depositCalldata` is secure and validated by the guardian signatures.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#21-missing-validation-of-depositcalldata-in-depositbufferedether-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

