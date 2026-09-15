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
solodit_id: 52708
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

OWNER ACCOUNTID CAN BE SET TO AN INVALID VALUE

### Overview


The `set_owner()` method implemented in the AppchainAnchor Struct does not validate the AccountId value passed to it, which can result in a loss of control over the contract. This can happen when an owner tries to pass ownership to another user and provides an invalid NEAR account ID. The bug is located in "appchain-anchor/src/lib.rs" and has been solved by the Octopus Network team.

### Original Finding Content

##### Description

The `set_owner()` method implemented in the AppchainAnchor Struct, which can be found in “appchain-anchor/src/lib.rs”, does not validate that the AccountId value passed to it actually contains a valid AccountId following the NEAR’s account ID rules. As a result, an owner who wishes to update pass ownership to another user can erroneously call the function with a string pointing to an invalid NEAR account ID, resulting in complete and irreversible loss of control over the contract from that point forward.

Code Location
-------------

#### appchain-anchor/src/lib.rs

```
fn set_owner(&mut self, owner: AccountId) {
    self.assert_owner();
    self.owner = owner;
}

```

The following is a test case developed as a PoC, notice that the test prints `Owner is: th!$1$!nv@|!d` when finished:

```
fn test_set_invalid_owner(){
    let total_supply = common::to_oct_amount(TOTAL_SUPPLY);
    let (root, _, _registry, anchor, _) = common::init(total_supply, false);
    anchor.contract.set_owner("test".to_string());
    let result1 = call!(root, anchor.set_owner("th!$_1$_!nv@|!d".to_string()));
    result1.assert_success();
    let result = view!(anchor.get_owner());
    println!("New owner is: {}", result.unwrap_json::<String>());
}

```

##### Score

Impact: 5  
Likelihood: 1

##### Recommendation

**SOLVED**: The `Octopus Network team` solved the issue in [commit ef2219a37c5be402cec720d9db03501981c2ca80](https://github.com/octopus-network/octopus-appchain-anchor/commit/ef2219a37c5be402cec720d9db03501981c2ca80)

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

