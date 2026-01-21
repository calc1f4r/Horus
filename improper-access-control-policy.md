---
# Core Classification
protocol: Ocean Protocol H2O System and Action
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50384
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
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

IMPROPER ACCESS CONTROL POLICY

### Overview


This bug report discusses the importance of implementing Access Control policies in smart contracts to maintain security and decentralize permissions. It highlights the risk of having only one authorized account that controls all privileged functions, as it can be compromised and give an attacker full control over the contract. The report recommends implementing Role-based access control and authorizing only trusted contracts or proxy contracts to improve security. The team plans to fix this issue in a future release.

### Original Finding Content

##### Description

Implementing a valid Access Control policy in smart contracts is essential to maintain security and decentralize permissions on a token. Moreover, access Control gives the features to mint/burn tokens and pause contracts. For instance, Ownership is the most common form of Access Control. In other words, the owner of a contract (the account that deployed it by default) can do some administrative tasks on it. Nevertheless, different authorization levels are required to keep the principle of least privilege, also known as least authority. Briefly, any process, user, or program can only access the necessary resources or information. Otherwise, the ownership role is beneficial in simple systems, but more complex projects require more roles using Role-based access control.

In most scope contracts, The `authorizedAccounts` of the contract are the accounts that control all privileged functions. Everything is managed and controlled by the `Authorized` accounts, with no other access control. If this account is compromised, then all functionalities would be controlled by an attacker, such as removing all other authorized accounts, changing price source to a malicious address, restarting feed and setting it to 0, starting and stopping the DSM OSM, etc.

Code Location
-------------

#### In-Scope Contracts

```
    constructor (address priceSource_) public {
        authorizedAccounts[msg.sender] = 1;

```

#### In-Scope Contracts

```
    constructor (address priceSource_, uint256 deviation) public {
        require(deviation > 0 && deviation < WAD, "DSM/invalid-deviation");

        authorizedAccounts[msg.sender] = 1;

```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

**PENDING**: The team will fix the issue in a future release adding the below points.

* In case externally owned accounts (EOAs) are the authorized accounts, the team will implement RBAC according to the software engineering principle of separation of concerns by authorizing only a single proxy contract and implementing RBAC in the proxy contract configuration. For example, the [DSRoles proxy contract](https://github.com/reflexer-labs/ds-roles/blob/c8cf2406aa4dbb5f751d36ed4e9a428ce61a687c/src/roles.sol#L89) implements permissions at an address method signature level.
* In other cases, if a smart contract is the authorized account; the team will only authorize smart contracts for which the code is known and trusted in advance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ocean Protocol H2O System and Action |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

