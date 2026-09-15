---
# Core Classification
protocol: rICO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13743
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/04/rico/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Gonçalo Sá
  - Shayan Eskandari
---

## Vulnerability Title

Test code present in the code base ✓ Fixed

### Overview


This bug report is about a coding issue in the ReversibleICO.sol file. In the code, the variables `rescuerAddress` and `freezerAddress` are not included in the function arguments. Instead, they are being assigned to `_projectAddress`, which is only meant for testing. This issue needs to be fixed before production to ensure that the code is ready for deployment. The bug has been fixed in the commit [lukso-network/[email protected]`edb880c`](https://github.com/lukso-network/rICO-smart-contracts/commit/edb880c56e5c84fe02727f1203778a7a28323f6d). Therefore, it is recommended to make sure that all the variable assignments are ready for production before deployment.

### Original Finding Content

#### Resolution



Fixed in [lukso-network/[email protected]`edb880c`](https://github.com/lukso-network/rICO-smart-contracts/commit/edb880c56e5c84fe02727f1203778a7a28323f6d).


#### Description


Test code are present in the code base. This is mainly a reminder to fix those before production.


#### Examples


`rescuerAddress` and `freezerAddress` are not even in the function arguments.


**code/contracts/ReversibleICO.sol:L243-L247**



```
whitelistingAddress = \_whitelistingAddress;
projectAddress = \_projectAddress;
freezerAddress = \_projectAddress; // TODO change, here only for testing
rescuerAddress = \_projectAddress; // TODO change, here only for testing


```
#### Recommendation


Make sure all the variable assignments are ready for production before deployment to production.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | rICO |
| Report Date | N/A |
| Finders | Gonçalo Sá, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/04/rico/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

