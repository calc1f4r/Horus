---
# Core Classification
protocol: Wallek
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35369
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
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

Reward amount of 'stakeToken might be taken from users' stakes when unstaking stakeToken2`.

### Overview


The bug report is about an issue in the TestStake::unStakeAndBurn()#2095 function. When a user unstakes and burns their 'stakeToken2', they should receive an equivalent amount of 'stakeToken'. However, this amount is not currently being provided by the protocol and instead is taken from users' deposits. This can lead to a lack of tokens on the contract's balance, preventing other users from withdrawing their staked 'stakeToken'. The severity of this issue is marked as medium, as it depends on the owner's action to provide the necessary 'stakeToken'. The recommendation is to validate the current flow and ensure that the contract has enough balance of 'stakeToken' to avoid taking tokens from users' deposits. After an audit, it was confirmed that the contract now has enough balance to provide rewards from users' deposits. 

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**


TestStake::unStakeAndBurn()#2095.
When 'stakeToken2' is unstaked and burnt, a user receives a corresponding amount of 'stakeToken'. This amount is equal to the total amount of 'stakeToken2', that a user unstakes; thus, it is not connected to the user's stakes of 'stakeToken. Hence, this amount of 'stakeToken must be provided as additional rewards allocated by the protocol to the smart contract balance in advance. Otherwise, the amount of 'stakeToken' will be taken from users' deposits, leading to the lack of tokens on the contract's balance and preventing later users from withdrawing their staked 'stakeToken'.
The issue is marked as a medium since it depends on the owner's action to provide the necessary 'stakeToken. However, if tokens are not provided, users may lose their staked 'stakeToken'.

**Recommendation:**

Validate the correctness of the current flow. Ensure that the contract has enough balance of `stakeToken' to ensure tokens sent to users during the burning of 'stakeToken2 are not taken from deposits of 'stakeToken.
**Post audit**. It is now validated that 'stakeToken.balanceOf(address(this)) - total TokenLocked - totalFeeCollected' is greater than withdrawnAmount'. Thus, rewards can be paid out from users' deposits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Wallek |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-04-Wallek.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

