---
# Core Classification
protocol: Octopus Network Anchor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52711
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
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

LACK OF UPPER LIMIT CHECKS ALLOWS BLOCKING WITHDRAWALS

### Overview


This bug report is about two functions in the "appchain-anchor/src/user_actions/settings_manager.rs" file that do not have a limit on the values they can accept. These functions allow the owner to set the number of days before validators and delegators can withdraw their rewards. This means that the owner can set very large numbers, which could result in years before the balances can be withdrawn. The code for these functions can be found in the same file. The impact of this bug is rated as 4 out of 5 and the likelihood is 2 out of 5. The recommendation is that the risk has been accepted by the Octopus Network team.

### Original Finding Content

##### Description

The `change_unlock_period_of_delegator_deposit()` and `change_unlock_period_of_validator_deposit()` functions in \"appchain-anchor/src/user\_actions/settings\_manager.rs\" do not check for an upper bound for the values passed to them. These functions allow the owner to set the number of days before validators/delegators can withdraw their rewards.

By not checking for an upper bound, the owner can set the values to big numbers that would correspond to years before validators/delegators can actually withdraw their balances.

Code Location
-------------

#### appchain-anchor/src/user\_actions/settings\_manager.rs

```
fn change_unlock_period_of_delegator_deposit(&mut self, value: U64) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value.0 != protocol_settings.unlock_period_of_delegator_deposit.0,
        "The value is not changed."
    );
    protocol_settings.unlock_period_of_delegator_deposit = value;
    self.protocol_settings.set(&protocol_settings);
}

```

#### appchain-anchor/src/user\_actions/settings\_manager.rs

```
fn change_unlock_period_of_validator_deposit(&mut self, value: U64) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value.0 != protocol_settings.unlock_period_of_validator_deposit.0,
        "The value is not changed."
    );
    protocol_settings.unlock_period_of_validator_deposit = value;
    self.protocol_settings.set(&protocol_settings);
}

```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

**RISK ACCEPTED**: The `Octopus Network team` accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Octopus Network Anchor |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

