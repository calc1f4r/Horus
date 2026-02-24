---
# Core Classification
protocol: Parcel Payroll
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20511
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Parcel Payroll.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Using the `transfer` function of `address payable` is discouraged

### Overview


This bug report is about a function called `executePayroll` which is used to transfer native asset funds to a recipient address. The address is set by the caller, but is also encoded in a Merkle Tree created off-chain. If the recipient is a smart contract or a multi-sig wallet that has a `receive` or `fallback` function that takes up more than the 2300 gas limit of `transfer`, then the payroll will revert and the Merkle Trees & approvals will have to be done again.

To fix this issue, it is recommended to use a `call` with value instead of `transfer`. The function already has a `nonReentrant` modifier so reentrancy is not a problem.

In conclusion, this bug has a medium impact and likelihood, and can be solved by using a `call` with value instead of `transfer`.

### Original Finding Content

**Impact:**
Medium, as payroll will revert and Merkle Trees & approvals would have to be done again

**Likelihood:**
Medium, as it happens any time the recipient is a smart contract or a multisig wallet that has a receive function taking up more than 2300 gas

**Description**

The `executePayroll` function uses the `transfer` method of `address payable` to transfer native asset funds to a recipient address. This address is set by the caller but is also encoded in the leaf of a Merkle Tree that is created off-chain. It is possible that this recipient is a smart contract that has a `receive` or `fallback` function that takes up more than the 2300 gas which is the limit of `transfer`. Examples are some smart contract wallets or multi-sig wallets, so usage of `transfer` is discouraged.

**Recommendations**

Use a `call` with value instead of `transfer`. The function already has a `nonReentrant` modifier so reentrancy is not a problem here.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Parcel Payroll |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-Parcel Payroll.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

