---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49451
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#11-missing-validation-on-_hooks-in-settlement-contract
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
  - MixBytes
---

## Vulnerability Title

Missing validation on `_hooks` in settlement contract

### Overview


The report points out a vulnerability in the `settle` function of the `LiquoriceSettlement.sol` contract. This function calls `validateOrder()` to perform necessary checks on the `_interactions` variable, which ensures secure interactions with the `LendingPool`. However, the `_hooks` parameter is not subjected to the same validation process, allowing an attacker to bypass the checks and potentially exploit the contract. The recommendation is to add validation checks for the `_hooks` parameter within the `settle` function, similar to those applied to `_interactions`. 

### Original Finding Content

##### Description

- https://github.com/Liquorice-HQ/contracts/blob/a5b4c6a56df589b8ea4f6c7b8cb028b1723ad479/src/contracts/settlement/LiquoriceSettlement.sol#L65

In the `LiquoriceSettlement.sol` contract, the `settle` function calls `validateOrder()`, which performs necessary checks on the `_interactions` variable. These checks include validations that ensure secure interactions with the `LendingPool`, as seen in the [`validateOrder` function](https://github.com/Liquorice-HQ/contracts/blob/a5b4c6a56df589b8ea4f6c7b8cb028b1723ad479/src/contracts/settlement/Signing.sol#L100).

However, the `_hooks` parameter in `settle()` is not subjected to the same validation process. This omission allows an attacker to bypass the `_interactions` checks by leveraging the `_hooks` parameter. As a result, the attacker can circumvent critical validations intended to secure the contract's operations, potentially leading to unauthorized actions or exploitation of the `LendingPool`.

##### Recommendation
We recommend to add validation checks for the `_hooks` parameter within the `settle` method, analogous to those applied to `_interactions`.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#11-missing-validation-on-_hooks-in-settlement-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

