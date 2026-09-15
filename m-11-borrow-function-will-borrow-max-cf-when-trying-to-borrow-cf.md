---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 945
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/45

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
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - gzeon
---

## Vulnerability Title

[M-11] borrow function will borrow max cf when trying to borrow > cf

### Overview


This bug report concerns an issue with the Borrow function in the MochiVault smart contract. The bug causes the contract to borrow to the maximum collateral factor (cf) when trying to borrow more than the maximum, instead of reverting with a “>cf” error as specified in the supplied test. This difference in behavior can cause users to borrow at dangerous collateral levels and receive less than the amount requested. A proof of concept can be found at the provided Github link. No tools were used to discover the issue. The recommended mitigation step is to revert if details[_id].debt + _amount > maxMinted with “>cf”.

### Original Finding Content

_Submitted by gzeon_

#### Impact
Borrow function in `MochiVault` will borrow to max cf when trying to borrow > cf instead of revert with ">cf" as specified in the supplied test. The difference in behavior may cause user to borrow at dangerous collateral level, and receive less than the amount requested.

#### Proof of Concept
* [`MochiVault` sol](https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol)

#### Recommended Mitigation Steps
Revert if `details\[\_id].debt` + `\_amount` > `maxMinted` with ">cf"


**[ryuheimat (Mochi) conirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/45)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/45
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

