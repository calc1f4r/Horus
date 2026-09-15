---
# Core Classification
protocol: Coinflip_2025-02-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55491
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
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

[M-05] Game completion can be front-run by stakers

### Overview


The report discusses a problem with the protocol where stakers can profit from players losing their bets and potentially lose money when players win. This is due to a loophole where stakers can front-run the completion of a lost game by staking tokens, resulting in an unrealized profit. This process can be repeated multiple times, making it statistically profitable for the staker. Similarly, stakers can also avoid losses by tracking and unstaking before a winning game is completed. The report recommends implementing a delay for staking and unstaking to mitigate this issue, but it may also lead to denial of service for stakers.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

Stakers in the protocol profit from players losing their bets and incur losses when players win.

Users can front-run the completion of a lost game by staking tokens, achieving an unrealized profit. While the staker will have to wait for the cooldown period to unstake, and in that period, the unrealized profits can be lost, the repetition of this process in the long term is statistically profitable.

Consider the following scenario:

- `Staking` contract has 100 tokens deposited

- Alice bets 50 tokens on a coin flip

- In the following block, Bob sees in the mempool the transaction where `PythRandomnessProvider.entropyCallback` is called and verifies that the random number will make Alice lose

- Bob front-runs the transaction and stakes 10,000 tokens

- The game is completed and Alice’s bet amount is transferred to `Staking` contract

- Bob’s stake is now worth 10,049 tokens

- Bob repeats the process every time he detects a losing game

In the same way, a staker who’s cooldown period has elapsed, can track the mempool and unstake before a game is completed with a win for the player, and avoid the loss.

## Recommendations

There is no straightforward solution to this issue. A possible mitigation would pass for accounting for the new amount staked is added to `info.totalStaked` and `stakedBalances[token][msg.sender]` only after `n` blocks have passed since the user staked the tokens. For unstaking, it would be required to add a delay between the request and the actual unstaking process. However, such an implementation would require taking special care to avoid a denial of service for the stakers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

