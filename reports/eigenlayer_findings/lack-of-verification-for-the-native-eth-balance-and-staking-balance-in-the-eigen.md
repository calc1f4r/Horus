---
# Core Classification
protocol: KelpDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30478
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#5-lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigenpod
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Lack of verification for the native `ETH` balance and staking balance in the `eigenPod`

### Overview


This bug report states that there is an issue with verifying the balance of `ETH` and staking within the `eigenPod` when using the `removeNodeDelegatorContractFromQueue` function. This could cause problems with the accuracy of the `RSETH` price. The recommendation is to check for a zero balance during this function.

### Original Finding Content

##### Description
There is a lack of verification for the native `ETH` balance and staking balance in the `eigenPod` within the `removeNodeDelegatorContractFromQueue` function, potentially leading to the discrepancies of the `RSETH` price.
##### Recommendation
We recommend checking zero balance during the `removeNodeDelegatorContractFromQueue` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#5-lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigenpod
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

