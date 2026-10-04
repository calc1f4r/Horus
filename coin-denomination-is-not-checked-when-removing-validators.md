---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51168
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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

COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS

### Overview


This bug report states that there is a problem with the `remove_validator` function in the `krp-staking-contracts/basset_sei_validators_registry` contract. The issue is that when using this function to remove a validator, there is no check to ensure that the delegated amount of coins matches the target denomination. This could lead to unexpected situations in the protocol, such as removing a validator with delegated coins that are different from the target denomination. The code location of this issue is in the `contract.rs` file, and the BVSS score for this bug is 5.0. The Kryptonite team has accepted the risk of this finding.

### Original Finding Content

##### Description

When removing a validator using the `remove_validator` function in the **krp-staking-contracts/basset\_sei\_validators\_registry** contract, there is no check about coin denomination in the delegated amount (i.e.: coin to be redelegated). As a consequence, some unexpected situations could arise in the protocol, e.g.: removing a validator with delegated native coins different from the target one.

Code Location
-------------

There is no check about coin denomination in the `remove_validator` function:

#### krp-staking-contracts/contracts/basset\_sei\_validators\_registry/src/contract.rs

```
for i in 0..delegations.len() {
 if delegations[i].is_zero() {
  continue;
 }
 redelegations.push((
  validators[i].address.clone(),
  Coin::new(delegations[i].u128(), delegation.amount.denom.as_str()),
 ));
}

```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

**RISK ACCEPTED**: The `Kryptonite team` accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

