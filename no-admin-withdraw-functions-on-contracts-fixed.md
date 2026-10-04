---
# Core Classification
protocol: Aligned Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38370
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/08/aligned-layer/
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
finders_count: 2
finders:
  - Martin Ortner
  -  George Kobakhidze
                        
---

## Vulnerability Title

No Admin Withdraw Functions on Contracts ✓ Fixed

### Overview


This bug report discusses two contracts that are meant to handle ETH deposits, but do not have a way to withdraw the funds. This could lead to ETH getting stuck in the contracts and not being usable by anyone. The report suggests adding an admin-controlled function to retrieve the funds in case of emergencies.

### Original Finding Content

#### Resolution



 While admin withdraw functionality for stuck ETH in the contract would help to retrieve funds simply, it would also give more control over the contracts to the team. To limit admin functionality, admin withdrawals won’t be implemented, but the team acknowledges that in extreme situations a workaround may be needed, which is achievable via a proxy upgrade on the `BatcherPaymentService` contract.
On the other hand, while the `AlignedLayerServiceManager` contract also interacts with ETH deposits for individual batchers, there is no withdraw functionality for the users. In the event some batchers over\-deposit and decide to exit the system, a withdrawal may be required. This is addressed in [yetanotherco/aligned\_layer\#872](https://github.com/yetanotherco/aligned_layer/pull/872) by introducing a `withdraw(uint256 amount)` function that retrieves `amount` of ETH from `msg.sender`’s `batchersBalance`.
 

#### Description


Both contracts are intended to receive, store, and use ETH on behalf of users. The calculations for ETH subtractions and usage are for gas purposes, which are difficult to calculate accurately.


As a result, it is probable that some amount of ETH will be stuck in the contracts with nobody being able to use or claim them.


#### Recommendation


Consider adding an admin authentication\-protected `withdraw()` function that just sends a privileged address the funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aligned Layer |
| Report Date | N/A |
| Finders | Martin Ortner,  George Kobakhidze
                         |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/08/aligned-layer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

