---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43853
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#2-potential-blockage-of-funds-if-terminated-before-vesting-start
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Potential Blockage of Funds if Terminated Before Vesting Start

### Overview


A critical bug has been found in the `getVestedTokenAmount` function of the RestrictedTokenAward contract. If the restricted token allocation is terminated before the vesting start time, the funds will be locked in the contract and cannot be accessed by the grantee or authority. To fix this, a check should be added to transfer all funds to the authority if termination occurs before the vesting start time. This will prevent the locking of funds in the contract and potential loss to the protocol.

### Original Finding Content

##### Description
This issue has been identified in the `getVestedTokenAmount` function of the [RestrictedTokenAward](https://github.com/MetaLex-Tech/MetaVesT/blob/b614405e60bce8b852e46d06c03fd47b04d86dde/src/RestrictedTokenAllocation.sol#L201) contract.
If the restricted token allocation is terminated prior to the vesting start time, the current implementation will lock the funds in the contract without providing a way to claim them. This can lead to a situation where vested tokens remain inaccessible to the grantee and authority, causing a potential loss to the protocol.
The issue is classified as **Critical** severity because it directly affects the protocol's ability to access its funds in case of early termination of the vesting schedule.
##### Recommendation
We recommend adding a check to ensure that if the termination occurs before the vesting start time, all the funds are immediately transferred to the authority. This will prevent the locking of funds in the contract in such scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/MetaVesT/README.md#2-potential-blockage-of-funds-if-terminated-before-vesting-start
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

