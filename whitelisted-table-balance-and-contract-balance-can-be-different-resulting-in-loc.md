---
# Core Classification
protocol: Global Interlink
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44579
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global Interlink.md
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

Whitelisted table balance and contract balance can be different resulting in locked funds for users

### Overview


This bug report describes a problem with a contract that allows users to add funds to a pool and also whitelist certain addresses. The issue is that the contract admin can add tokens to the whitelist table that do not match the actual token balance in the contract. This could cause problems for users who have vested funds as they may not be able to access them. The recommendation is to implement a check to prevent this from happening or to transfer vested funds directly when adding a user to the whitelist. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

At this moment, the whitelisted address are added through the add_to_whitelist method and the funds of the pool are added through the deposit functionality, however these 2 steps pattern can become problematic for the contract integrity and the vested users, as the contract admin can add in the whitelist table tokens amount that do not reflect the true token balances in the contract, and users could be stuck with uncorrelated/hypothetical funds because there would be nothing for them to release from vesting.

**Recommendation**: 

Implement a check to never being able to add more hypothetical total funds in the table then the ones in contract balance or every time admin add a new user to the whitelist also transfer the necessary vested funds for that user directly in the same function logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Global Interlink |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global Interlink.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

