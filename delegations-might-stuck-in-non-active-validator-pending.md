---
# Core Classification
protocol: Skale Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13832
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/01/skale-token/
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
  - Sergii Kravchenko
  - Shayan Eskandari
---

## Vulnerability Title

Delegations might stuck in non-active validator  Pending

### Overview


This bug report is about the issue that when a validator does not get enough funds to run a node (Minimum Staking Requirement, MSR), all token holders that delegated tokens to the validator cannot switch to a different validator, and might result in funds getting stuck with the nonfunctioning validator for up to 12 months. This is because of the code/contracts/delegation/ValidatorService.sol:L166, which requires that the validator has to meet Minimum Staking Requirement. The Skale team acknowledged this issue and will address this in future versions. The recommendation is to allow token holders to withdraw delegation earlier if the validator didn’t get enough funds for running nodes.

### Original Finding Content

#### Resolution



Skale team acknowledged this issue and will address this in future versions.


#### Description


If a validator does not get enough funds to run a node (`MSR - Minimum staking requirement`), all token holders that delegated tokens to the validator cannot switch to a different validator, and might result in funds getting stuck with the nonfunctioning validator for up to 12 months.


#### Example


**code/contracts/delegation/ValidatorService.sol:L166**



```
require((validatorNodes.length + 1) \* msr <= delegationsTotal, "Validator has to meet Minimum Staking Requirement");

```
#### Recommendation


Allow token holders to withdraw delegation earlier if the validator didn’t get enough funds for running nodes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Skale Token |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/01/skale-token/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

