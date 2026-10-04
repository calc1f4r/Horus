---
# Core Classification
protocol: DesciLaunchpad_2025-02-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55464
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/DesciLaunchpad-security-review_2025-02-07.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-08] Missing validation for `start_time` and `end_time`

### Overview

See description below for full details.

### Original Finding Content

The `create_token_handler` function does not validate whether the `start_time` and `end_time` provided in the `CreateTokenArgs` are in the future relative to the current time.

This can lead to the following issue:

**Invalid Launchpad Timing**: If `start_time` or `end_time` is in the past, the token sale may start or end immediately.

**Code Location :** [create_token.rs](https://github.com/merklelabshq/desci-launchpad/blob/master/contract/programs/desci-launchpad/src/instructions/create_token.rs)

```rust
    token_stats.token_id = ctx.accounts.stats.tokens_created;
    token_stats.name = args.name.clone();
    token_stats.symbol = args.symbol.clone();
    token_stats.uri = args.uri.clone();
    token_stats.decimals = args.decimals;
    token_stats.payment_token = args.payment_token.key();
    token_stats.total_supply = args.total_supply;
    token_stats.sale_supply = args.sale_supply;
    token_stats.limit_per_wallet = args.limit_per_wallet;
    token_stats.price_per_token = args.price_per_token;
    token_stats.start_time = args.start_time;
    token_stats.end_time = args.end_time;
    token_stats.cooldown_duration = args.cooldown_duration;
    token_stats.min_threshold = args.min_threshold;
    token_stats.max_threshold = args.max_threshold;
    token_stats.bump = ctx.bumps.token_stats;
```

Add validation to ensure that both `start_time` and `end_time` are in the future relative to the current time. Use the `Clock::get()?` function to retrieve the current timestamp and compare it with `start_time` and `end_time`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | DesciLaunchpad_2025-02-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/DesciLaunchpad-security-review_2025-02-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

