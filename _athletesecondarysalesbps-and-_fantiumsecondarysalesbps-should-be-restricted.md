---
# Core Classification
protocol: Fantium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27914
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#5-_athletesecondarysalesbps-and-_fantiumsecondarysalesbps-should-be-restricted
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

`_athleteSecondarySalesBPS` and `_fantiumSecondarySalesBPS` should be restricted

### Overview


This bug report is related to two variables, `_athleteSecondarySalesBPS` and `_fantiumSecondarySalesBPS`, which are used in other contracts to calculate royalties. If the combined value of these two variables is greater than 10,000, the royalty payment will exceed 100%, which will cause the transaction to be reverted. Therefore, it is recommended to add a check to ensure that the combined value of the two variables does not exceed 10,000.

### Original Finding Content

##### Description
`_athleteSecondarySalesBPS` and `_fantiumSecondarySalesBPS` should be restricted because they will be used in other contracts to calculate royalties with base point = 1 / 10_000, so if `_athleteSecondarySalesBPS + _fantiumSecondarySalesBPS > 10_000`, the royalty will be > 100%. Due to this all transactions with royalty payments will revert.
https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L526-L527
https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L544-L545
https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L658-L659
https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L752-L753

##### Recommendation
We recommend adding the following check: `_athleteSecondarySalesBPS + _fantiumSecondarySalesBPS <= 10_000`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Fantium |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#5-_athletesecondarysalesbps-and-_fantiumsecondarysalesbps-should-be-restricted
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

