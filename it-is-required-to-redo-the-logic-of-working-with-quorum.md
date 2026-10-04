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
solodit_id: 28141
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#1-it-is-required-to-redo-the-logic-of-working-with-quorum
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

It is required to redo the logic of working with quorum

### Overview


This bug report is about the quorum value not being associated with the number of guardians in the Lido DAO project. Currently, it is possible for the `depositBufferedEther()` function to work with the signature of only one guardian, which contradicts the documentation. To fix this issue, the bug report recommends removing the ability to change the quorum variable when changing the number of guardians, using the percentage of the number of elements in the `guardians` array, and adding a lower bound for the percentage of quorum members and the minimum number of guardians.

### Original Finding Content

##### Description
At the following lines there is the value of the `quorum` variable changed:
- https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L265  when adding one guardian
- https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L278  when adding multiple guardians
- https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L265  when removing one guardian

There may even be such a situation that the next such action will set the quorum value equal to `1`.
In this case, it is possible for the `depositBufferedEther()` function to work with the signature of only one guardian.
This disagrees with the documentation https://github.com/lidofinance/lido-improvement-proposals/blob/develop/LIPS/lip-5.md:
"To make a deposit, we propose to collect a quorum of 2/3 of the signatures of the committee members".
Currently, the value of the `quorum` variable is not associated with the value of the `guardians` variable.
We recommend doing the following:
- remove the ability to change the variable that affects the quorum when changing the number of guardians
- instead of the `quorum` variable, use the percentage of the number of elements in the `guardians` array
- add a lower bound for the percentage of quorum members and the minimum number of guardians
##### Recommendation
It is necessary to redo the logic of work with quorum counting.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#1-it-is-required-to-redo-the-logic-of-working-with-quorum
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

