---
# Core Classification
protocol: Thala Swap + Math V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46717
audit_firm: OtterSec
contest_link: https://www.thalalabs.xyz/
source_link: https://www.thalalabs.xyz/
github_link: https://github.com/ThalaLabs/thala-modules/thalaswap_v2

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
  - Bartłomiej Wierzbiński
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Bypassing Funds Repayment via Double Upscaling

### Overview


This bug report discusses a vulnerability in the ThalaSwap V2 code related to the repayment process for meta-stable pools. The issue arises from double upscaling, which causes the post-repayment invariant to be calculated incorrectly. This means that the code may accept a repayment that is less than the borrowed amount, resulting in loss of funds. To fix this issue, the double upscaling needs to be eliminated. This has already been addressed in a recent patch.

### Original Finding Content

## Vulnerability Report: Double Upscaling in pay_flashloan

## Description

The vulnerability arises from double upscaling during the repayment process in `pay_flashloan` when handling meta-stable pools. Specifically, `pay_flashloan` upscales `balance_after_flashloan` twice. When handling meta-stable pools, the funds are multiplied by their value derived from an oracle. As a result, the post-repayment invariant computation utilizes an incorrectly scaled value.

## Code Snippet

> _ thalaswap_v2/sources/pool.move rust

```rust
public fun pay_flashloan(assets: vector<FungibleAsset>, loan: Flashloan) acquires PauseFlag,
,→ Pool, MetaStablePool, StablePool, ThalaSwap, WeightedPool {
    [...]
    if (pool_is_metastable(pool_obj)) {
        borrow_amounts = upscale_metastable_amounts(pool_obj, borrow_amounts);
        balances = upscale_metastable_amounts(pool_obj, pool_balances(pool_obj));
    };
    [...]
    while (i < len) {
        let repay_sub_fees = *vector::borrow(&repay_amounts, i) - *vector::borrow(&fee_amounts,
        ,→ i);
        let balance_after_flashloan = *vector::borrow(&balances, i) + repay_sub_fees;
        vector::push_back(&mut balances_after_flashloan, balance_after_flashloan);
        i = i + 1;
    };
    [...]
    if (pool_is_metastable(pool_obj)) {
        balances_after_flashloan = upscale_metastable_amounts(pool_obj,
        ,→ balances_after_flashloan);
    };
    [...]
}
```

Consequently, this creates a discrepancy where the post-repayment invariant (`curr_invariant`) appears larger than the pre-repayment invariant (`prev_invariant`), even if no real repayment has occurred. This incorrect invariant validation allows the flashloan repayment to proceed without properly verifying the adequacy of the repayment. Thus, the pool may accept a repayment that is less than the borrowed amount, resulting in a loss of funds.

## Remediation

Eliminate the double upscaling to prevent inflation of the `curr_invariant`.

## Patch

Fixed in commit `19dc5f1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala Swap + Math V2 |
| Report Date | N/A |
| Finders | Bartłomiej Wierzbiński, Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://www.thalalabs.xyz/
- **GitHub**: https://github.com/ThalaLabs/thala-modules/thalaswap_v2
- **Contest**: https://www.thalalabs.xyz/

### Keywords for Search

`vulnerability`

