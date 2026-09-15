---
# Core Classification
protocol: Liquistake
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58498
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
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
  - zokyo
---

## Vulnerability Title

Updating of WSX, Staking Proxy or Validator may lead to the loss of funds.

### Overview


This bug report is about a potential issue in a code for a cryptocurrency called StWSX. The problem is related to a function called Claim Rewards, which is used to distribute rewards to users who have staked their funds. The code also has functions for setting parameters related to WSX, staking proxy, and validator. If any of these parameters are updated, users who have not unstaked their funds may lose them. The recommendation is to add a mechanism for migrating staked funds when these parameters are updated. This issue has been resolved by removing the ability to update these parameters and implementing a migration process through a new contract.

### Original Finding Content

**Description**

StWSX.sol: oracle Claim Rewards(), line 332.
StWSX.sol: setWSXToken(), setStaking Proxy(), setValidatorAddress().
Updating WSX, Staking Proxy, or Validator may cause users whose funds were not unstaked before the update to lose them. Thus, when updating these parameters, users' staked funds may get stuck.

**Recommendation**

Implement a migration mechanism for staked WSX when updating the core parameters.

**Re-audit comment**

Resolved.

Post-audit. Setters were removed so that WSX, Staking Proxy, and Validator parameters can only be set during deployment. The migration will be performed via redemption and deposit to a new contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Liquistake |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-08-LiquiStake.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

