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
solodit_id: 37033
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

Unfair liquidation mechanism adopted

### Overview


The bug report is about a lack of incentive for liquidators to close losing positions in the VodkaVaultV2.sol program. This is because liquidators only receive a reward if the position has enough funds to cover its debt, which means they may not bother closing positions that are too far in debt. The recommendation is to still give a reward to liquidators even if the position cannot fully cover its debt, in order to prevent further losses. The client has acknowledged the issue and plans to address it by prioritizing rewards for users of the program.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

VodkaVaultV2.sol - No incentive to liquidate a losing position if it is overwhelmed by debt. It is shown in function fulfillLiquidation() that liquidator receives reward only if wr.returnedUSDC >= debtPortion as when debt is higher (i.e. worse position), the liquidator takes no rewards because the protocol receives whatever it can get in order to compensate for the debt. But that in turn deincentivizes liquidators to get to liquidate such a position leaving the protocol to deal with severe losses.

**Recommendation** 

Give some portion to liquidator even if the position does not have sufficient return to pay for the whole debt. This in order to stop positions from losing even more.

**Fix** -  Client pledges to deal with that as being part of the project is to have liquidator bots called by owners of project as according to client, they prioritizing the rewards for water users first.

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

