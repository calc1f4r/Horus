---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48094
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Rounding Errors Result In Lost Accrued Rewards

### Overview


The staking_pool.move function has a bug where the request_withdraw_stake function does not accurately calculate the number of tokens to withdraw. This can result in users receiving zero tokens when attempting to withdraw a small number, allowing attackers to exploit the error. A proof of concept shows how this can happen and suggests disallowing the generation of StakedSui objects with less than one SUI as a solution. This bug has been fixed in a recent patch.

### Original Finding Content

## Staking Pool Withdrawal Issue

In `staking_pool.move`, `request_withdraw_stake` is responsible for withdrawing staked tokens and accrued rewards from a staking pool. However, the function utilizes `get_token_amount` to calculate the number of tokens to withdraw, which rounds down the token calculation.

When a user attempts to withdraw a small number of tokens, such as one SUI, the calculation will result in a withdrawal of zero tokens. An attacker may exploit this rounding error to prevent regular users of the staking pool from receiving their rewards accurately.

## Proof of Concept

Consider the following scenario:

1. User A stakes 1000 SUI at an exchange rate of 1 SUI : 1 token to a staking pool that currently has 2000 SUI and 1000 tokens (1000 SUI from rewards).
2. User B stakes 2000 SUI at an exchange rate of 2000 SUI : 1000 tokens to the same staking pool, which changes the current pool state to 4000 SUI and 2000 tokens.
3. User B begins withdrawing their SUI one by one using `split` on `StakedSui`. On each withdrawal, the conversion to tokens results in `floor(1 * 1000 / 2000) = 0`. Therefore, User B does not end up withdrawing any tokens every time they withdraw 1 SUI. This process repeats until User B withdraws all of their funds.
4. At this point, the pool state is User A: 1000 staked SUI at an exchange rate of 1 SUI : 1 token, with the pool having 2000 SUI and 2000 tokens.
5. User A attempts to withdraw their 1000 SUI, which gets converted to 1000 tokens using the original exchange rate.
6. `withdraw_rewards` ends up calculating the `total_sui_withdraw_amount` as 1000 SUI, and as a result, the rewards end up being zero.
7. User A ends up with 1000 SUI instead of 2000 SUI, losing all their accrued rewards.

## Remediation

Disallow the generation of `StakedSui` objects with a principal less than one SUI.

## Patch

Fixed in `cdc7dad`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

