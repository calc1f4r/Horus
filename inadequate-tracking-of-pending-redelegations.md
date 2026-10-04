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
solodit_id: 51164
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

INADEQUATE TRACKING OF PENDING REDELEGATIONS

### Overview


The report describes a bug in the `krp-staking-contracts/basset_sei_validators_registry` contract. When the `remove_validator` function is executed and the redelegation is not possible, the validator is removed from storage but there is no proper tracking of pending redelegations. This can cause problems later when trying to redelegate. The code location of the bug is in the `contract.rs` file. The BVSS score for this bug is 6.3, which is considered a medium severity. The recommendation is to solve the issue, which has been done by the Kryptonite team in commit ab8ef52.

### Original Finding Content

##### Description

When executing the `remove_validator` function in the **krp-staking-contracts/basset\_sei\_validators\_registry** contract and the redelegation was not possible (e.g.: because of `can_redelegate.amount`), the validator is removed from the storage, but there is not an adequate tracking of pending redelegations to be done later.

Code Location
-------------

#### krp-staking-contracts/contracts/basset\_sei\_validators\_registry/src/contract.rs

```
if let Some(delegation) = delegated_amount {
 // Terra core returns zero if there is another active redelegation
 // That means we cannot start a new redelegation, so we only remove a validator from
 // the registry.
 // We'll do a redelegation manually later by sending RedelegateProxy to the hub
 if delegation.can_redelegate.amount < delegation.amount.amount {
  return StdResult::Ok(Response::new());
 }

 let (_, delegations) =
  calculate_delegations(delegation.amount.amount, validators.as_slice())?;

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:U (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:M/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [ab8ef52](https://github.com/KryptoniteDAO/krp-staking-contracts/pull/21/commits/ab8ef528d2a43672c26ba1015ede1bafaa0cb372).

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

