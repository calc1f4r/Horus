---
# Core Classification
protocol: Meso Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47132
audit_firm: OtterSec
contest_link: https://meso.finance/
source_link: https://meso.finance/
github_link: https://github.com/MesoLendingFi/meso-smartcontract

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
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Removal Of Incorrect Debt Shares

### Overview


This bug report discusses two issues in the lending_pool function. The first issue is that in the repay function, if a user's remaining debt shares fall below a certain threshold, their debt is completely removed, resulting in a potential loss of funds for the user. The second issue is that in the withdraw function, if a user's remaining deposit shares fall below the same threshold, the function removes the shares but fails to update the pool's total supply of shares, causing inconsistencies in the pool's accounting. The report recommends modifying both functions to prevent the removal of debt and to update the total supply of shares when they fall below the threshold. The bug has been fixed in the latest patches.

### Original Finding Content

## Lending Pool Considerations

In the `lending_pool`, `DUST_THRESHOLD` is utilized to completely remove any position with remaining shares less than `DUST_THRESHOLD`. Consequently, when a user’s remaining debt shares fall below the `DUST_THRESHOLD` in `repay`, the function completely removes the user’s debt shares (as shown in the code snippet below). This removal effectively cancels any remaining debt the user has, resulting in a potential giveaway of free money, since the user no longer owes anything even though they might have an outstanding debt.

```rust
>_ lending_pool.move
public(friend) fun repay(
    user: address,
    pool: Object<LendingPool>,
    tokens: FungibleAsset,
) acquires Fees, InterestRate, LendingPool, State, UserPosition {
    [...]
    if (*current_shares <= DUST_THRESHOLD) {
        simple_map::remove(&mut user_position.debt_shares, &pool);
    };
    [...]
}
```

Furthermore, in `withdraw`, when a user’s remaining deposit shares fall below `DUST_THRESHOLD`, the function removes the user’s deposit shares but fails to update the pool’s total supply of shares. While this does not directly result in a loss of funds, there will be inconsistencies in the pool’s accounting as the value of the total supply of shares will not match the actual number.

```rust
>_ lending_pool.move
public(friend) fun withdraw(
    user: address,
    pool: Object<LendingPool>,
    amount: u64,
): FungibleAsset acquires Fees, InterestRate, LendingPool, Ltv, State, UserPosition {
    [...]
    if (*current_shares <= DUST_THRESHOLD) {
        simple_map::remove(&mut user_position.deposit_shares, &pool);
    };
    [...]
}
```

## Remediation

Modify both `repay` and `withdraw` so that the remaining debt is not removed within `repay`, and the pool’s total supply of shares is updated to reflect the removal of the user’s deposit shares when they fall below the `DUST_THRESHOLD`.

## Patch

Fixed in `ccf4541` and `7097ed8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Meso Lending |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://meso.finance/
- **GitHub**: https://github.com/MesoLendingFi/meso-smartcontract
- **Contest**: https://meso.finance/

### Keywords for Search

`vulnerability`

