---
# Core Classification
protocol: Devve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37628
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
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
  - Zokyo
---

## Vulnerability Title

Usage of native `transfer()`

### Overview


This bug report discusses a medium severity issue that has been resolved. The report identifies that certain contracts, specifically Treasury.sol, Vesting.sol, and Staking.sol, use a function called `transfer()` to transfer ETH. However, this function only provides a limited amount of gas, which can cause the transfer to fail in certain situations. This can happen if the contract's callback spends more than the allotted gas, if the contract is called through a proxy that also uses up the gas, or if there are complex operations or external calls involved. This means that users may not be able to receive funds from the contract. The recommendation is to use a different function called `.call()` instead of `transfer()`.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

it was identified that the Treasury.sol, Vesting.sol and Staking.sol contracts uses the native `transfer()` function to transfer ETH, which could result in reverts. The `transfer()` only provides 2300 gas for its operation. This means the following cases can cause the transfer to fail: 

- The contract's callback spends more than 2300 gas (which is only enough to emit something) 

- The contract is called through a proxy which itself uses up the 2300 gas 

- complex operations or external calls

If a user falls into one of the above categories, they'll be unable to receive funds from the contract.

**Recommendation**: 

Consider using the low-level `.call()` instead of `transfer()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Devve |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

