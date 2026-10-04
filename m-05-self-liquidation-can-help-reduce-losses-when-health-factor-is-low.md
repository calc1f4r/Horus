---
# Core Classification
protocol: Hyperstable_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57796
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] Self-liquidation can help reduce losses when health factor is low

### Overview


This bug report discusses a problem with insufficient collateral in a system that handles liquidation rewards. The severity of this issue is high, meaning it can have a significant impact on the system. However, the likelihood of it occurring is low. 

When a user's collateral is not enough to cover the liquidation reward, the system will withdraw tokens from the LiquidationBuffer to pay the liquidator. However, if the LiquidationBuffer also does not have enough tokens, the system will withdraw from the Vault to cover the reward. 

In cases where the user's collateral is still not enough to pay the liquidation reward, they have the option to self-liquidate. This means the system will absorb part of their loss instead of the user having to repay the entire amount. 

To prevent potential issues, it is recommended to either disable self-liquidation or limit the liquidation of debts to privileged addresses only. This will ensure that the system is not at risk of absorbing too much loss. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When the user's collateral is insufficient to cover the liquidation reward, tokens will be withdrawn from the LiquidationBuffer to pay the liquidator. If the LiquidationBuffer also lacks sufficient tokens to cover the liquidation reward, tokens will be withdrawn from the Vault to pay the liquidator.

If the user's collateral is insufficient to pay the liquidation reward, they can opt for self-liquidation, which allows the protocol to absorb part of their loss, as compared to the normal repayment method.

For example, if the current value of the user's collateral is 100, and the liquidation of the entire debt requires collateral worth 110 (to reward the liquidator), the user can choose to self-liquidate to reduce their loss due to the decline in the value of the collateral,.

## Recommendations

It is recommended to prevent self-liquidation or restrict liquidation of debts in the redistribution state to privileged addresses only.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

