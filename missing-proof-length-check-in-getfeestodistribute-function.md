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
solodit_id: 41251
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#29-missing-proof-length-check-in-getfeestodistribute-function
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

Missing Proof Length Check in `getFeesToDistribute` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [getFeesToDistribute](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSFeeDistributor.sol#L175-L179) function of the contract `CSFeeDistributor`. The function currently does not validate the length of the Merkle proof provided in the `proof` parameter. As a result, there is a possibility that an empty or malformed proof could be passed, potentially allowing a user to craft a situation where they extract stETH shares without proper verification. This could lead to an unauthorized distribution of funds.

The issue is classified as **Low** severity because it requires to find shares amount that will generate a valid Merkle root. However, ensuring that the proof length is checked adds an extra layer of security to prevent potential exploits.

##### Recommendation
We recommend adding a check to validate the length of the Merkle proof before verifying it.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#29-missing-proof-length-check-in-getfeestodistribute-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

