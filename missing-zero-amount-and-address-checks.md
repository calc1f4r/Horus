---
# Core Classification
protocol: Tradable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44932
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missing zero amount and address checks

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

In the TradableBalanceVault contract, there is a missing non-zero check for the amount parameter in the marginAccountWithdrawal() function. This could accidentally lead to the withdrawal of 0 amount being processed, which could lead to unnecessary transactions and gas wastage.
Also, there is a missing zero address check for the receiver. This could lead to a loss of funds for users if a zero address is accidentally used by users for the receiver parameter.
In Contract TradableSideVault, the sendMessage(...) method has a `destination` parameter which is not checked for address(0). It is advised to check if the `destination` parameter is address(0) and revert if it is.

In Contract TradableSettings.sol, the constructor sets the `adminUser` which is used all across the protocol contracts and does not validate if the given parameter _adminUser is address(0) or not. In case, the admin user is set address(0), the contract may be needed to be deployed again. 


**Recommendation**: 

It is advised to add a missing zero amount check as well as a zero address check for the mentioned methods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tradable |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

