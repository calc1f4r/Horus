---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45988
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Flawed risk allocation mechanism in Metavault

### Overview


The Metavault (LendingAssetVault) has a flaw in its max allocation mechanism, which can result in a compromised lending vault stealing all of the funds in the metavault. This is due to the fact that `vaultUtilization[_vault]` can be affected by the share/asset ratio of the vault, causing it to decrease and allowing the vault to pull more funds from the metavault. To fix this, it is recommended to update `vaultUtilization[_vault]` based on the number of tokens provided to the vault instead of the value of the lending vault's shares. This bug has a high impact and medium likelihood.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The Metavault (LendingAssetVault) implements a max allocation mechanism for each lending vault that it supplies to. This is to ensure that in a situation where a lending vault is compromised, the maximum loss is well-defined and limited.

However, due to a flaw in this mechanism, a compromised lending vault can steal ALL of the funds in the metavault, exceeding the maximum allocation that was set.

The max risk allocation mechanism works by ensuring that `vaultUtilization[_vault]` cannot exceed `vaultMaxAllocation[_vault]`

However, `vaultUtilization[_vault]` varies depending on the share/asset ratio of the vault. This means that if a large amount of bad debt occurs in a pool (which lowers the value of the lending pair's shares), then the `vaultUtilization[_vault]` decreases, allowing the vault to pull more funds from the Metavault.

This allows the total funds pulled from the vault to exceed `vaultMaxAllocation[_vault]`, even though this is not reflected in `vaultUtilization[_vault]`.

## Recommendations

It is recommended to update `vaultUtilization[_vault]` based on the number of tokens provided to the vault, instead of varying it by the value of the lending vault's shares.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

