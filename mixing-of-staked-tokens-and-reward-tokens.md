---
# Core Classification
protocol: Zero Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59360
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/zero-staking/40ffa176-7b8d-43ec-a7e2-29732c12f21e/index.html
source_link: https://certificate.quantstamp.com/full/zero-staking/40ffa176-7b8d-43ec-a7e2-29732c12f21e/index.html
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
finders_count: 3
finders:
  - Jennifer Wu
  - Julio Aguilar
  - Jeffrey Kam
---

## Vulnerability Title

Mixing of Staked Tokens and Reward Tokens

### Overview


A client reported a bug in the `StakingERC20.sol` file where staked tokens and reward tokens are not properly separated. This can result in staked tokens being used to pay out rewards to other users, leading to a depletion of users' staked tokens. Additionally, if the staked token and reward token are the same, a function called `withdrawLeftoverRewards()` can be used to withdraw staked funds. The recommendation is to implement internal accounting mechanisms to clearly separate staked tokens and reward tokens to prevent this issue. The bug has been marked as fixed by the client.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `78885e6851aa2c8f2a6892ef80937d7f53c1949c`. The client added a separate variable to track staked and unstaked funds accordingly through `totalStake`.

**File(s) affected:**`StakingERC20.sol`

**Description:** If the staked token and reward token are identical, the staked tokens may be incorrectly used to pay out rewards to other users. This occurs because there is no separation between the funds that are staked by users and the tokens that are sent to the contract to distribute as rewards. This lack of separation can lead to a situation where users' staked tokens are depleted to fulfill reward claims.

Furthermore, if the staked token and reward tokens are identical, the function `withdrawLeftoverRewards()` can be used to withdraw staked funds.

**Recommendation:** Implement internal accounting mechanisms to ensure a clear separation between staked tokens and reward tokens. This will prevent the unintended use of staked tokens for reward distribution.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Zero Staking |
| Report Date | N/A |
| Finders | Jennifer Wu, Julio Aguilar, Jeffrey Kam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/zero-staking/40ffa176-7b8d-43ec-a7e2-29732c12f21e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/zero-staking/40ffa176-7b8d-43ec-a7e2-29732c12f21e/index.html

### Keywords for Search

`vulnerability`

