---
# Core Classification
protocol: Metalabel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20409
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Metalabel.md
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

[M-02] Using the `transfer` function of `address payable` is discouraged

### Overview


This bug report is about a problem with the `mint` function in the `DropEngine` code. When the recipient of the funds is a smart contract or a multi-sig wallet, the `transfer` method used by the `mint` function can take up more than the 2300 gas limit, meaning the sequence won't be usable as mints will revert. The likelihood of this happening is medium.

The recommended solution is to use a `call` with value instead of `transfer`. Additionally, the `payable` keyword can be removed from the `revenueRecipient` variable as the `mint` method has a check for the caller to be an EOA, meaning there is no risk from reentrancy.

### Original Finding Content

**Impact:**
Medium, as sequence won't be usable as mints will revert

**Likelihood:**
Medium, as it happens any time the recipient is a smart contract or a multisig wallet that has a receive function taking up more than 2300 gas

**Description**

The `mint` function in `DropEngine` uses the `transfer` method of `address payable` to transfer native asset funds to an address. This address is set by a node owner and is possible to be a smart contract that has a `receive` or `fallback` function that takes up more than the 2300 gas which is the limit of `transfer`. Examples are some smart contract wallets or multi-sig wallets, so usage of `transfer` is discouraged.

**Recommendations**

Use a `call` with value instead of `transfer`. There is no risk from reentrancy in the `mint` method as it has a check for the caller to be an EOA. When this is done you can remove the `payable` keyword from the `revenueRecipient` variable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Metalabel |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Metalabel.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

