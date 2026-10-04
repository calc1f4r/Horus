---
# Core Classification
protocol: FOMO Game
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47602
audit_firm: OtterSec
contest_link: https://play.fomosolana.com/
source_link: https://play.fomosolana.com/
github_link: https://github.com/Doge-Capital/FOMO-GAME

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Tamta Topuria
  - OtterSec
---

## Vulnerability Title

Disparity In Rewards Update

### Overview


There is a bug in the program where the user's total rewards (total_amount) are not being updated correctly when they win the sidepot money. This leads to a difference between the total rewards and the withdrawable rewards (balance_amount). This can cause problems with fairness and accuracy in reward distribution. To fix this, the total rewards should always be updated along with the withdrawable rewards whenever there are changes to rewards, including when winning the sidepot. This issue has been resolved in the latest patch.

### Original Finding Content

## Issue with `buy_ticket` Function

The `buy_ticket` function fails to update `user_acc.total_amount`, when the user wins the sidepot money, resulting in an inconsistency between `user_acc.total_amount` and `user_acc.balance_amount`, which is correctly updated with the sidepot reward. Throughout the program, `user_acc.total_amount` and `user_acc.balance_amount` variables are increased together as `total_amount` represents the total accumulated rewards by the user (including historical rewards), while `balance_amount` tracks accumulated rewards which haven’t been withdrawn yet by the user.

## Code Snippet (src/lib.rs)

```rust
pub fn buy_ticket(ctx: Context<BuyTicket>, team: String, quantity: u64) -> Result<()> {
    [...]
    if curr_time > game_acc.start_time + INITIAL_PHASE_DURATION {
        vault_acc.sidepot_amount += total_amount / 100;
        vault_acc.sidepot_probability += quantity;
        if random_num_acc.is_used {
            msg!("Random number not generated");
        } else {
            msg!("Random number used : {}", random_num_acc.random_num);
            if random_num_acc.random_num < vault_acc.sidepot_probability {
                let amount = vault_acc.sidepot_amount;
                user_acc.balance_amount += amount;
                user_acc.sidepot_amount += amount;
                user_acc.sidepot_wins += 1;
                [...]
            }
        }
    }
}
```

Thus, if these two values do not increase in tandem, `total_amount` may fall below `balance_amount`, resulting in a disparity between the presented total rewards and the withdrawable rewards. Any computations or conditions dependent on `user_acc.total_amount` will yield inaccurate outcomes, influencing the fairness and precision of reward distribution.

## Remediation

Ensure that `user_acc.total_amount` is consistently updated alongside `user_acc.balance_amount` whenever rewards are accrued or modified, including when winning the sidepot.

## FOMOSolana Audit 04 | Vulnerabilities

### Patch

Resolved in `ff0d967`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | FOMO Game |
| Report Date | N/A |
| Finders | Akash Gurugunti, Tamta Topuria, OtterSec |

### Source Links

- **Source**: https://play.fomosolana.com/
- **GitHub**: https://github.com/Doge-Capital/FOMO-GAME
- **Contest**: https://play.fomosolana.com/

### Keywords for Search

`vulnerability`

