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
solodit_id: 37040
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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

`amountOutMinimum` Hardcoded to 0

### Overview


The VaultkaV2GMXHandler's afterWithdrawalExecution function has a bug that could potentially harm users. The amountOutMinimum is hardcoded to 0, which could lead to sandwich attacks and unlimited slippage. It is recommended to set a safe value for slippage in the code to prevent this issue. The severity of this bug is medium and it has been acknowledged by the team. 

### Original Finding Content

**Severity** - Medium

**Status** - Acknowledged

**Description**

Inside VaultkaV2GMXHandler’s afterWithdrawalExecution function the ExactInputParams is populated at L553 to perform the necessary swap but the amountOutMinimum has been hardcoded to 0, this can expose users to sandwich attacks due to unlimited slippage.

**Recommendation**:

Set the slippage to a correct/safe value throughout the codebase.

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

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

