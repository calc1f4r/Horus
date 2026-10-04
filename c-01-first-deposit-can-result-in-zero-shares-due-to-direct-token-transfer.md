---
# Core Classification
protocol: ManifestFinance-security-review_2025-08-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62715
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/ManifestFinance-security-review_2025-08-26.md
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
  - Kann
---

## Vulnerability Title

[C-01] First Deposit Can Result in Zero Shares Due to Direct Token Transfer

### Overview


The StakedUSH vault has a critical bug that allows for zero share deposits when USH tokens are sent directly to the contract. This is because the vault calculates shares based on totalSupply and totalAssets, which can be manipulated when tokens are sent directly to the contract. This can result in legitimate depositors receiving 0 shares and potentially losing their funds. The root cause of this bug is the way the vault calculates shares using a formula that does not account for direct token transfers. The team has fixed this bug.

### Original Finding Content


## Severity

Critical

## Description

The StakedUSH vault is vulnerable to zero share deposits when USH tokens are sent directly to the contract.
Because the vault calculates shares based on totalSupply and totalAssets, a direct token transfer increases totalAssets without increasing totalSupply.
As a result, legitimate depositor will receive 0 shares for a positive deposit, breaking fair share distribution and potentially locking user funds.

Root Cause:
The sUSH vault calculates shares using the formula:

shares = (assets * (totalSupply + decimalsOffset)) / (totalAssets + 1)

If a user directly transfers USH to the vault contract (bypassing deposit()), the vault’s totalAssets increases while totalSupply remains 0.

When the next user calls deposit(), the formula becomes:

(assets * (0 + 0)) / (totalAssets + 1) = 0

Thus, the user receives 0 shares (REVERTS), even though they tried depositing a positive amount of assets.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | ManifestFinance-security-review_2025-08-26 |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/ManifestFinance-security-review_2025-08-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

