---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37707
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-06-Vaultka.md
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

Centralized control in the program

### Overview


The report states that two programs, strategy and vault, have a centralized control issue. This means that certain accounts have too much power and can manually specify amounts or borrow assets without paying them back. The recommendation is to update the methods to decrease centralization.

### Original Finding Content

**Description**

Both programs (strategy and vault) have centralized control. In the Strategy program, an admin account can manually specify any amount within either execute_withdraw or execute_deposit, while in the Vault program, any whitelisted account can borrow assets and repay the debt without paying assets back.

**Recommendation**

update methods to decrease centralization

**Re-audit comment**

Acknowledged

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-07-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

