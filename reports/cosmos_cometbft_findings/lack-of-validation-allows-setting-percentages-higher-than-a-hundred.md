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
solodit_id: 52709
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

LACK OF VALIDATION ALLOWS SETTING PERCENTAGES HIGHER THAN A HUNDRED

### Overview


This bug report discusses an issue with the `change_maximum_validator_stake_percent()` method in the `settings_manager.rs` file of the `appchain-anchor` project. This method checks that a percentage value passed to it is less than 100, but other functions in the same file do not perform this check. This could cause the contract to crash and panic while rewards are being distributed if a percentage value greater than 100 is used. The impact of this bug is rated as 5 and the likelihood is rated as 1. The Octopus Network team has partially solved the issue, but some checks were removed in a subsequent commit.

### Original Finding Content

##### Description

The `change_maximum_validator_stake_percent()` method in \"appchain-anchor/src/user\textunderscore actions/settings\_manager.rs\" checks that the percentage value passed to it is less than a 100 and reverts otherwise. However, all the remaining functions allowing the owner to change other percentage values do not perform such checks, allowing percentages to exceed 100%, which would probably cause the contract to crash and panic while rewards are being distributed.

Code Location
-------------

#### appchain-anchor/src/user\_actions/settings\_manager.rs

```
fn change_maximum_market_value_percent_of_near_fungible_tokens(&mut self, value: u16) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value != protocol_settings.maximum_market_value_percent_of_near_fungible_tokens,
        "The value is not changed."
    );
    protocol_settings.maximum_market_value_percent_of_near_fungible_tokens = value;
    self.protocol_settings.set(&protocol_settings);
}

```

#### appchain-anchor/src/user\_actions/settings\_manager.rs

```
fn change_maximum_market_value_percent_of_wrapped_appchain_token(&mut self, value: u16) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value != protocol_settings.maximum_market_value_percent_of_wrapped_appchain_token,
        "The value is not changed."
    );
    protocol_settings.maximum_market_value_percent_of_wrapped_appchain_token = value;
    self.protocol_settings.set(&protocol_settings);
}

```

#### appchain-anchor/src/user\_actions/settings\_manager.rs

```
fn change_validator_commission_percent(&mut self, value: u16) {
    self.assert_owner();
    let mut protocol_settings = self.protocol_settings.get().unwrap();
    assert!(
        value != protocol_settings.maximum_market_value_percent_of_near_fungible_tokens,
        "The value is not changed."
    );
    protocol_settings.maximum_market_value_percent_of_near_fungible_tokens = value;
    self.protocol_settings.set(&protocol_settings);
}

```

##### Score

Impact: 5  
Likelihood: 1

##### Recommendation

**PARTIALLY SOLVED**: The `Octopus Network team` partially solved the issue in [commit ef2219a37c5be402cec720d9db03501981c2ca80](https://github.com/octopus-network/octopus-appchain-anchor/commit/ef2219a37c5be402cec720d9db03501981c2ca80)

Then some checks were removed in [commit eaa2a5109bca0522f6a285f53ebe1e366475bbc6](https://github.com/octopus-network/octopus-appchain-anchor/commit/eaa2a5109bca0522f6a285f53ebe1e366475bbc6)

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

