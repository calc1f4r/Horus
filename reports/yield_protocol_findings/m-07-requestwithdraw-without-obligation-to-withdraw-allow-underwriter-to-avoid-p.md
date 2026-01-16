---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42440
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-insure
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/295

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
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] `requestWithdraw` without obligation to withdraw allow underwriter to avoid payout

### Overview


This bug report is about a problem with the withdrawal process in the Insure contract. The contract has a lockup period between withdrawal requests and actual withdrawals, but there is no obligation for users to actually withdraw their funds after the lockup period. This allows underwriters to continuously request withdrawals every lockup period, keeping their average lockup time at half the set lockup period. This means they can continue to earn interest on their funds while only having to pay the extra gas cost for the withdrawal request. To fix this issue, it is recommended to either extend the lockup period or force underwriters to withdraw after the lockup period. The team has acknowledged the issue and plans to have a longer lockup period in the production version of the contract.

### Original Finding Content

_Submitted by gzeon_

To prevent withdrawal front-running, a lockup period is set between withdrawal request and withdrawal. However, there are no obligation to withdraw after the lockup period and the capital will keep earning premium during lockup. A strategy for underwriter is to keep requesting withdrawal every `lockup period` to keep their average lockup to `lockup period/2`.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-insure/blob/19d1a7819fe7ce795e6d4814e7ddf8b8e1323df3/contracts/PoolTemplate.sol#L279>

Assuming

1.  Reporting DAO vote last for 24 hours (according to docs) plus there will be delay between the hack and vote creation
2.  the `lockup period` is set to 86400 (24 hours) in the supplied test cases

It is very likely an underwriter can avoid payout by such strategy since their effective lockup would be 12 hours only. They will continue to earn yield in the pool and only require some extra gas cost for the `requestWithdraw` every 24 hours.

#### Recommended Mitigation Steps

Extend the lockup period at least by a factor of 2 or force underwriter to withdraw after lockup period.


**[oishun1112 (Insure) acknowledged](https://github.com/code-423n4/2022-01-insure-findings/issues/295):**
 > Yes, lock up period is going to be like a week~2week in production.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/295
- **Contest**: https://code4rena.com/reports/2022-01-insure

### Keywords for Search

`vulnerability`

