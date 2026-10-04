---
# Core Classification
protocol: GooseFX SSL
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48651
audit_firm: OtterSec
contest_link: https://goosefx.io/
source_link: https://goosefx.io/
github_link: github.com/GooseFX1/gfx-ssl.

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
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Incorrect rounding in unstake

### Overview


The bug report discusses an issue in the gfx-controller program's Unstake instruction where a user can withdraw a percentage of their share from the pool and receive tokens without sacrificing any shares. This is due to the program using floor division in all three computations, which can result in a scenario where delta_share is floored to zero but delta_balance is non-zero. The report suggests a solution to calculate delta_balance based on delta_share instead of unstake_percent, which has been fixed in a recent patch.

### Original Finding Content

## gfx-controller Program's Unstake Instruction

In the `gfx-controller` program’s Unstake instruction, a user withdraws a percentage of their share from the pool. There are three quantities the program computes with this percentage:

- **delta_share**: The number of shares to remove.
- **delta_balance**: The number of tokens, including staking rewards, to transfer.
- **delta_staked_amount**: The number of tokens, excluding staking rewards, to transfer.

## Code Snippet

```rust
let delta_share = 
    U128::from(staking_account.share) * unstake_percent /
    10u64.pow(BP_DECIMAL);
let delta_balance = 
    U128::from(controller.staking_balance) * staking_account.share *
    unstake_percent /
    controller.total_staking_share /
    10u64.pow(BP_DECIMAL);
let delta_staked_amount = 
    U128::from(staking_account.amount_staked) * unstake_percent /
    10u64.pow(BP_DECIMAL);
```

The issue is that all three computations use a floor division. In particular, consider a scenario where `unstake_percent` is tuned such that `delta_share` is floored to zero and `delta_balance` is non-zero. In this case, the user receives tokens without sacrificing any shares.

## Remediation

Calculate `delta_balance` based on `delta_share`, instead of `unstake_percent` directly. With this change, a floor division will always work in favor of the pool.

## Revised Code Snippet

```rust
let delta_balance = 
    U128::from(controller.staking_balance) * delta_share /
    controller.total_staking_share;
```

## Patch

Fixed in commit **c858099**.

© TODO OtterSec LLC. All Rights Reserved. 8 / 21

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX SSL |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://goosefx.io/
- **GitHub**: github.com/GooseFX1/gfx-ssl.
- **Contest**: https://goosefx.io/

### Keywords for Search

`vulnerability`

