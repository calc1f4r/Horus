---
# Core Classification
protocol: The Standard Smart Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38349
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - Giovanni Di Siena
---

## Vulnerability Title

Comment incorrectly refers to `€` when it should be `$`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The following comment is [present](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L91) when summing the stablecoin collateral in `SmartVaultV4::yieldVaultCollateral`:

```solidity
// both USDs and its vault pair are € stablecoins, but can be equivalent to €1 in collateral
```

Here, the `€` symbol is used for USD instead of `$`.

**Recommended Mitigation:** Update the comment to use the `$` symbol.

**The Standard DAO:** No longer applicable. Comment removed in commit [`5862d8e`](https://github.com/the-standard/smart-vault/commit/5862d8e10ac8648b89a7e3a78498ff20dc31e42e).

**Cyfrin:** Verified, comment has been removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Smart Vault |
| Report Date | N/A |
| Finders | Immeas, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

