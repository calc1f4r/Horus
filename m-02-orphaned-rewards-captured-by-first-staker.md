---
# Core Classification
protocol: Elixir_2025-08-17
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62324
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elixir-security-review_2025-08-17.md
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

[M-02] Orphaned rewards captured by first staker

### Overview


The report describes a bug in a contract called `sdeusd.move`. This bug occurs when rewards are distributed while there are no `sdeUSD` holders. The bug allows the first subsequent staker to capture all orphaned rewards at a 1:1 conversion rate, which means they get all the rewards without having to share with other stakers. This happens because the contract does not check if there are active stakers before distributing rewards. This bug can be exploited by timing the staking process to become the first staker after a period of no active stakers. The report recommends preventing reward distribution when there are no active stakers to fix this bug.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

In contract `sdeusd.move` func `transfer_in_rewards()` and `convert_to_shares()` when rewards are distributed while no sdeUSD holders exist, the first subsequent staker captures all orphaned rewards at 1:1 conversion rate.

If you check the **vulnerable logic** it doesn't check if there are active stakers.
```move
// transfer_in_rewards() - No check for active stakers
public fun transfer_in_rewards(...) {
    // Missing: assert!(total_supply(management) > 0, ENoActiveStakers);
    update_vesting_amount(management, amount, clock);
}

// convert_to_shares() - 1:1 ratio when no existing stakers
if (total_supply == 0 || total_assets == 0) {
    assets  // First staker gets 1:1 regardless of unvested rewards
}
```

Let's take an example **how it occurs**
1. Protocol has zero sdeUSD holders (total_supply = 0).
2. 100 deUSD rewards distributed via `transfer_in_rewards()`.
3. Alice stakes 1000 deUSD during the vesting period → gets 1000 shares (1:1 ratio).
4. Vesting completes → Alice's 1000 shares now represent 1100 deUSD total assets.
5. Alice redeems for 100 deUSD profit (orphaned community rewards).

No validation prevents reward distribution to an empty staker pool, combined with 1:1 conversion, ignoring unvested assets.

### Impact

**First staker after empty periods captures all orphaned community rewards** through timing manipulation.

## Recommendation

Prevent reward distribution when no active stakers exist.

```move
public fun transfer_in_rewards(...) {
    assert!(total_supply(management) > 0, ENoActiveStakers);
    update_vesting_amount(management, amount, clock);
    // ... rest of function
}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elixir_2025-08-17 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elixir-security-review_2025-08-17.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

