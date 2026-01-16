---
# Core Classification
protocol: Thetanuts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56504
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-16-Thetanuts.md
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
  - Zokyo
---

## Vulnerability Title

Incorrect amount of LP tokens might be stored.

### Overview


The bug report is about a function called "rebalance()" in a contract called IndexVaultV1.sol. The function is supposed to deposit collateral tokens into a target vault, but instead of adding the correct amount of LP tokens, it adds the collateral amount. This could cause problems because the ratio between LP and collateral may not be 1:1, leading to incorrect tracking and operation of the vault. The recommendation is to add the actual amount of received LP tokens instead of the collateral amount.

### Original Finding Content

**Description**

IndexVaultV1.sol, function rebalance().
After depositing collateral tokens to target vault, an amount of collateral is added to vault’s
amount instead of received LP tokens(line 145). It is possible, that the ratio between target
vault LP and collateral isn’t 1:1, thus an incorrect amount of vault’s LP tokens will be tracked,
which might lead to incorrect operation of the vault.

**Recommendation**:

Add actual amount of received LP tokens instead of received collateral amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Thetanuts |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-16-Thetanuts.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

