---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57595
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-09-16-Umami .md
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
  - zokyo
---

## Vulnerability Title

Excessive authority for `setVault` function in `VaultOwned` contract.

### Overview


The report discusses a bug in the contract called VaultOwned. The bug is related to the amount of authority given to one executor, which could potentially lead to funds being embezzled if the executor is not trustworthy. The recommendation given is to use multisig, which allows for multiple parties to have control over the contract. The bug has been resolved based on the response from the partner, who states that the Umami DAO Multisig wallet is currently set as the vault for the Umami token. This means that all token operations are controlled through the DAO and governance voting, and no changes need to be made.

### Original Finding Content

**Description**

contract VaultOwned - in body of setVault( address vault_) external returns (bool) onlyOwner

Too much authority for one executor that might lead to funds embezzled if not trusted

**Recommendation**

Use multisig

**Re-audit comment**

Resolved.

Fix-1: according to partner's response, The Umami DAO Multisig wallet is the address currently set as the vault for the Umami token. All token operations are controlled through the DAO and through governance voting

Therefore, there's no change needs to be made

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-09-16-Umami .md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

