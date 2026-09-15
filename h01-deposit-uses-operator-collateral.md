---
# Core Classification
protocol: PoolTogether – Pods Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11470
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pooltogether-pods-audit/
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

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - payments
  - farm

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Deposit uses operator collateral

### Overview


This bug report is about the `_deposit` function of the Pod contract, which is used to take collateral from the `operator` address and credit it to the `from` address. This transfer of funds from the operator to the `from` address can be successful, however, if the operator has insufficient funds or the Pod contract does not have approval, the `operatorDeposit` function will revert. The fix for this bug was to update the `transferFrom` arguments to retrieve collateral from the `from` address, which was done in Pull Request #3 and is now fixed.

### Original Finding Content

The `_deposit` function of the Pod contract [attempts to take collateral from the `operator`](https://github.com/pooltogether/pods/blob/8041b3dc72efd02b94d49fb37b9b308603af5ce/contracts/Pod.sol#L180) but [credits it to the `from` address](https://github.com/pooltogether/pods/blob/8041b3dc72efd02b94d49fb37b9b308603af5ce/contracts/Pod.sol#L185).


If successful, this effectively transfers funds from the operator to the `from` address. On the other hand, if the operator has insufficient funds or the Pod contract does not have approval, the [`operatorDeposit` function](https://github.com/pooltogether/pods/blob/8041b3dc72efd02b94d49fb37b9b308603af5ce/contracts/Pod.sol#L151) will revert. Either scenario is undesirable.


Consider updating the `transferFrom` arguments to retrieve collateral from the `from` address.


**Update:** *Fixed in [PR#3](https://github.com/pooltogether/pods/pull/3/). Collateral is correctly taken from the `from` address.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | PoolTogether – Pods Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/pooltogether-pods-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

