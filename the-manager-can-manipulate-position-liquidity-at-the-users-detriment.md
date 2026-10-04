---
# Core Classification
protocol: Teahouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45712
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
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

The Manager Can Manipulate Position Liquidity at the Users Detriment

### Overview


The report discusses a bug in a system where the manager has too much control over adding and removing liquidity positions. This could negatively impact users by adding risky positions or removing profitable ones. The recommendation is to implement policies and mechanisms to align the manager's incentives with those of the users, such as setting guidelines and implementing performance metrics. The client has acknowledged the issue but notes that a time delay may not be practical and that there is a performance fee for the manager. They also mention that a vault underperforming could result in a low TVL.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**:

The manager has full control over adding and removing liquidity positions through the addLiquidity() and removeLiquidity() functions. The manager could manipulate these positions in ways that negatively impact users, such as:
Adding liquidity to illiquid or high-risk positions that are unlikely to generate returns.
Removing profitable liquidity positions before performance fees are calculated, reducing the vault's apparent gains.
Timing the addition
or removal of liquidity to coincide with user deposits or withdrawals, affecting the share value calculations to the detriment of users.

**Recommendation**:

Implement policies and mechanisms to align the manager's incentives with those of the users, such as:
Setting guidelines or limits on the types of positions the manager can enter.
Requiring a time delay or community approval for significant changes in liquidity positions.
Implementing performance metrics that reward the manager for positive outcomes and penalize negative ones.

**Client comment**: 

Acknowledged.This vault will be used by in-house strategy team. Time delay may not be practical because the market sometimes may change very rapidly. There is a performance fee for the manager. A vault is underperforming the TVL will be very low.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Teahouse |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-09-25-Teahouse.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

