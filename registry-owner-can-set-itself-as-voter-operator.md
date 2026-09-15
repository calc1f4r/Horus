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
solodit_id: 52725
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

REGISTRY OWNER CAN SET ITSELF AS VOTER OPERATOR

### Overview


A bug was found in the `Octopus Network` code where the `owner` could set itself as a `voter_operator`, which goes against the principle of least privilege. This means that the `owner` has additional privileges that it should not have. The bug can be found in the `appchain-registry/src/registry_settings_actions.rs` file. The impact of this bug is rated as a 4 out of 5 and the likelihood of it occurring is a 3 out of 5. The recommendation for fixing this bug is to add a relevant check in the code to prevent the `owner` from setting itself as a `voter_operator`. The `Octopus Network` team has already solved this issue by adding the necessary check in the code. The fixed code can be found in the same file mentioned above.

### Original Finding Content

##### Description

It was observed that the `owner` could set itself as a `voter_operator`. This functionality violates the principle of least privilege giving the `owner` additional privileges.

Code Location
-------------

#### appchain-registry/src/registry\_settings\_actions.rs

```
   fn change_operator_of_counting_voting_score(&mut self, operator_account: AccountId) {
        self.assert_owner();
        let mut registry_settings = self.registry_settings.get().unwrap();
        registry_settings.operator_of_counting_voting_score.clear();
        registry_settings
            .operator_of_counting_voting_score
            .push_str(&operator_account);
        self.registry_settings.set(&registry_settings);
    }


```

##### Score

Impact: 4  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Octopus Network` team solved the issue by adding relevant check.

Fixed Code:

#### appchain-registry/src/registry\_settings\_actions.rs

```
    fn change_operator_of_counting_voting_score(&mut self, operator_account: AccountId) {
        self.assert_owner();
        assert_ne!(
            operator_account, self.owner,
            "The account should NOT be the owner."
        );
        let mut registry_settings = self.registry_settings.get().unwrap();
        assert_ne!(
            operator_account, registry_settings.operator_of_counting_voting_score,
            "The account is not changed."
        );
        registry_settings.operator_of_counting_voting_score = operator_account;
        self.registry_settings.set(&registry_settings);
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

