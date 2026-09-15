---
# Core Classification
protocol: Octopus Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52719
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

ANYONE CAN CHANGE OCT TOKEN ACCOUNT

### Overview


The bug report describes a problem with the `change_oct_token` function in the `AppchainRegistry` code. This function does not have a check to ensure that only the owner can change the OCT token account, allowing anyone to make changes. This could have a high impact and is likely to occur. The recommendation is that the team has already solved this issue by removing the function.

### Original Finding Content

##### Description

It was observed that the `change_oct_token` is lacking the ownership check, which allows anyone to change the OCT token account.

Code Location
-------------

#### appchain-registry/src/sudo\_actions.rs

```
impl SudoActions for AppchainRegistry {
    //
    fn change_oct_token(&mut self, oct_token: AccountId) {
        self.oct_token = oct_token;
    }


```

##### Score

Impact: 5  
Likelihood: 5

##### Recommendation

**SOLVED**: The `Octopus Network` team solved this issue by removing this function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Octopus Network |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

