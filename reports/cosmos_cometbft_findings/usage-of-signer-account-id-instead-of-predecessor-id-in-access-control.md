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
solodit_id: 52730
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

USAGE OF SIGNER ACCOUNT ID INSTEAD OF PREDECESSOR ID IN ACCESS CONTROL

### Overview


The bug report is about a risky usage of a function called `env::signer_account_id()` in a project called `Octopus Network`. The function is used to check if the caller is the owner of the appchain. However, this can be risky because it can be manipulated by a malicious contract to execute functions under the owner's role. The team behind `Octopus Network` has solved the issue by changing the function to `env::predecessor_account_id()`. This ensures that the caller is the previous contract in the chain of cross-contract calls, making it more secure.

### Original Finding Content

##### Description

It was observed that the `env::signer_account_id()` was used in the `assert_appchain_owner` to assert whether the caller is the appchain\_owner.

* `env::signer_account_id()`: The id of the account that either signed the original transaction or issued the initial cross-contract call.
* `env::predecessor_account_id()`: The id of the account that was the previous contract in the chain of cross-contract calls. If this is the first contract, it is equal to `signer_account_id`.

From their definitions above, we can derive that the usage of `env::signer_account_id()` is risky in access control scenarios. There is a risk that the appchain owner can be phished to sign the cross contract call and hence unknowingly let the malicious contract execute functions in the project's contract under that owner's role.

Code Location
-------------

#### appchain-registry/src/lib.rs

```
fn assert_appchain_owner(&self, appchain_id: &AppchainId) {
        let appchain_basedata = self.get_appchain_basedata(appchain_id);
        assert_eq!(
            env::signer_account_id(),
            appchain_basedata.owner().clone(),
            "Function can only be called by appchain owner."
        );
    }

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Octopus Network` team solved the issue by changing `env::signer_account_id()` to `env::predecessor_account_id()`.

Fixed Code:

#### appchain-registry/src/lib.rs

```
fn assert_appchain_owner(&self, appchain_id: &AppchainId) {
        let appchain_basedata = self.get_appchain_basedata(appchain_id);
        assert_eq!(
            env::predecessor_account_id(),
            appchain_basedata.owner().clone(),
            "Function can only be called by appchain owner."
        );
    }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

