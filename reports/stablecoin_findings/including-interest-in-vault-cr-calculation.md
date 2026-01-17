---
# Core Classification
protocol: Thala
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48058
audit_firm: OtterSec
contest_link: https://www.thalalabs.xyz/
source_link: https://www.thalalabs.xyz/
github_link: https://github.com/ThalaLabs/thala-modules

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Including Interest In Vault CR Calculation

### Overview


The functions redeem_collateral and liquidate are used to calculate the collateral ratio (CR) for a vault, but they do not take into account the updated interest of the vault. This results in an incorrect CR value being used in other calculations. To fix this, the functions should be updated to consider the updated interest of the vault when calculating the CR. This can be done by using the function accrue_vault_interest before calculating the CR in redeem_collateral. The updated interest should also be taken into account when calculating the CR for a vault in both redeem_collateral and liquidate. This issue has been fixed in version 108cd74 by using the function vault_liability_amount, which returns the total liability of the vault (vault.debt + vault.interest).

### Original Finding Content

## Collateral Ratio Calculation Issue

## Overview

The `redeem_collateral` and `liquidate` functions calculate the collateral ratio (CR) for a vault, which is used in redemption and liquidation calculations. However, these functions do not account for the updated interest of the vault when calculating the CR. As a result, the CR is calculated without considering `vault.interest`, leading to the use of an incorrect CR value in other calculations.

## Remediation

The `redeem_collateral` and `liquidate` functions should be updated to consider the updated interest of the vault when calculating the collateral ratio (CR). Specifically, `vault.interest` should be updated using `accrue_vault_interest` just before calculating the CR in `redeem_collateral`. In addition, the updated `vault.interest` should be taken into account when calculating the CR for a vault in both `redeem_collateral` and `liquidate`.

## Patch

This issue has been fixed in commit `108cd74` by using `vault_liability_amount`, which returns the total liability of the vault, i.e., `vault.debt + vault.interest`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://www.thalalabs.xyz/
- **GitHub**: https://github.com/ThalaLabs/thala-modules
- **Contest**: https://www.thalalabs.xyz/

### Keywords for Search

`vulnerability`

