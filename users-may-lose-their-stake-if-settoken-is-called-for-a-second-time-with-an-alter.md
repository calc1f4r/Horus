---
# Core Classification
protocol: Devve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37622
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
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

Users May Lose Their Stake If `setToken` Is Called For A Second Time With An Alternative Address

### Overview


This bug report discusses an issue with the `setToken` function in the Staking contract. This function is used to set the token for staking, but there is a problem where the owner can accidentally reset the staking token, causing a temporary loss of funds for users. This happens when the owner changes the token to a different address, which locks the previously staked tokens and prevents users from unstaking them. The report recommends adding a check to ensure that the token is already set before resetting it, and the client has already made this change. 

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

The `setToken` function is used to initially set the token used for staking within the Staking contract however, there is a lack of checks which allow owners to accidentally reset the staking token to cause a temporary loss of funds before resetting it back. 

Consider the following scenario:

- `Token` is set to address(A)
- User stakes X amount of tokens address(A)
- Owner changes `token` to address(B)
- User now can not unstake the previously staked tokens address(A) and will remain locked.

**Recommendation**: 

It’s recommended that there is a check that the token is already set by including a check `require(token == address(0) || totalStaking == 0)` before resetting the staking token to ensure that no more users are staked into the protocol.

**Client comment**: The only change was checking if input address is `address(0)`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Devve |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Devve.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

