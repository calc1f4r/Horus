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
solodit_id: 37446
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
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

The vault contract is not compliant with the ERC4626

### Overview


This bug report is about a contract called GlmVault that is not functioning correctly. The contract is inheriting from another contract called ERC4626 and has overridden some methods, but not others. This is causing confusion and misleading information when certain functions are called. The report recommends that the contract be updated to fix these issues.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

Contract GlmVault is inheriting from the ERC4626 implementation and overriding several methods. 

GlmVault has overridden the method `deposit()` and `mint()` method but `maxDeposit()` and `maxMint()` are not overridden.

This implies that when `mint()` is called it reverts but `maxMint()` returns `uint(256).max` which is misleading.

Similarly, the deposit method can be paused but `maxDeposit()` still returns `uint(256).max` which is misleading.

Adding to that, `withdraw()` is overridden as well, and any call to `withdraw()` reverts but `maxWithdraw()` returns an uint256 value.

In case these values are read internally or externally will provide incorrect information especially if they are integrated with other smart contracts.

**Recommendations**: 

Update the contract to override the suggested methods to return appropriate values as per the contract state to not return any misleading values.

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

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

