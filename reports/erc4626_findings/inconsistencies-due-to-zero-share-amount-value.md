---
# Core Classification
protocol: Walrus Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53198
audit_firm: OtterSec
contest_link: https://www.mystenlabs.com/
source_link: https://www.mystenlabs.com/
github_link: https://github.com/MystenLabs/walrus

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
finders_count: 4
finders:
  - Nicholas R. Putra
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Inconsistencies Due to Zero Share Amount Value

### Overview


The staking_inner::request_withdraw_stake function does not prevent a withdrawal request with a share_amount of zero, which could allow a malicious user to manipulate the staking pool's share-to-asset ratio. Additionally, there is a possibility of a denial-of-service attack when share_amount is zero in the exchange_rate::convert_to_wal_amount function due to division by zero. This affects epoch advancement and stake withdrawals. The issue has been fixed in the latest patch.

### Original Finding Content

## Withdrawal Request Issue in Staking Pool

`staking_inner::request_withdraw_stake` does not explicitly prevent a withdrawal request with a `share_amount` of zero. This oversight may allow a malicious user to manipulate the staking pool’s share-to-asset ratio by withdrawing a small principal or leaving it.

Furthermore, there is a possibility of a denial-of-service attack when `share_amount` is zero in `exchange_rate::convert_to_wal_amount`, due to division by zero when the function performs a division by `share_amount` to compute the WAL equivalent. Specifically, this affects epoch advancement and stake withdrawals.

> ```rust
> // Source: sources/staking/exchange_rate.move
> public(package) fun convert_to_wal_amount(exchange_rate: &PoolExchangeRate, amount: u64): u64 {
>     match (exchange_rate) {
>         PoolExchangeRate::Flat => amount,
>         PoolExchangeRate::Variable { wal_amount, share_amount } => {
>             let amount = (amount as u128);
>             let res = (amount * *wal_amount) / *share_amount;
>             res as u64
>         },
>     }
> }
> ```

When calculating the pool’s active balance, `wal_balance_at_epoch` calls `convert_to_wal_amount`, affecting epoch advancements if `share_amount` is zero. Similarly, during stake withdrawal, `calculate_rewards` internally calls `convert_to_wal_amount` to compute rewards, causing the withdrawal attempt to fail if `share_amount` is zero.

## Remediation
Ensure that the minimum amount remains in the pool or `StakedWal`.

## Patch
Fixed in commit `cc4aaaa`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Walrus Contracts |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://www.mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/walrus
- **Contest**: https://www.mystenlabs.com/

### Keywords for Search

`vulnerability`

