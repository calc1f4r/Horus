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
solodit_id: 44900
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
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

Centralization Risk

### Overview


The bug report describes a problem with a system that gives too much power to the owner. For example, the owner can withdraw all the esVELA tokens to themselves and manipulate critical functions, which can harm the protocol. The report recommends adding checks and making the owner a multisig to prevent this issue.

### Original Finding Content

**Severity** : Medium

**Status** : Acknowledged 

**Description**

The whole system grants too much power to the owner, for example - inside the SakeVault.sol the owner can call `withdrawAllESVELA` to withdraw all the esVELA to the feeReceiver which can be set to the owner himself using the changeProtocolFee function. The owner has the privilege to all the critical functionalities and can be manipulated in a 
way that harms the protocol (Another example can be setting MAX_LEVERAGE and MIN_LEVERAGE to arbitrary amounts, adding weird - ERC20 tokens into the whitelist of tokens which can have unintended behavior in the ERC4626 vault if a token is said a fee on transfer).

**Recommendation** 

Ensure the owner is a multisig and add suitable checks wherever necessary, even on functions with onlyOwner.

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

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

