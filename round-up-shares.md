---
# Core Classification
protocol: Volo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47736
audit_firm: OtterSec
contest_link: https://www.volo.fi/
source_link: https://www.volo.fi/
github_link: https://github.com/Sui-Volo/volo-liquid-staking-contracts

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
  - Michał Bochnak
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Round Up Shares

### Overview


This report discusses a bug found in the math::to_shares function, which is used to calculate the number of shares a user will receive for staking SUI. The bug occurs when the CERT coin has a high value relative to SUI, resulting in zero shares being received for a non-zero quantity of SUI. This bug can be exploited by iteratively staking a small amount of SUI to accumulate CERT coins, which can then be unstaked for a larger amount of SUI. The report recommends modifying the limit for NativePool::min_stake to prevent this exploitation while maintaining a reasonable ratio range. The bug has been fixed in the latest patch.

### Original Finding Content

## Vulnerability Description

The vulnerability is rooted in `math::to_shares`, particularly when the CERT coin holds a significant value relative to SUI. This may result in receiving zero shares for a non-zero quantity of SUI. As a result, the function rounds up and returns one CERT.

## Function Breakdown

```rust
public fun to_shares(ratio: u256, amount: u64): u64 {
    let shares = (amount as u256) * ratio / RATIO_MAX;
    assert!(shares <= (U64_MAX as u256), E_U64_OVERFLOW);
    if (amount > 0 && shares == 0) {
        shares = 1;
    };
    (shares as u64)
}
```

This function is utilized in `native_pool::stake_non_entry` to calculate the number of shares a user will receive for staking SUI. The minimum amount of SUI that may be supplied to `native_pool::stake_non_entry` is defined by `NativePool::min_stake`, with the sole requirement being that it must be greater than zero.

```rust
public entry fun change_min_stake(self: &mut NativePool, _owner_cap: &OwnerCap, value: u64) {
    assert_version(self);
    assert!(value > 0, E_LIMIT_TOO_LOW);
    // ...
    self.min_stake = value;
}
```

Consequently, by iteratively staking a small amount of SUI (X times), users may accumulate X CERT coins. Unstaking these coins allows users to obtain more SUI than their initial stake.

## Proof Of Concept

1. **Initial State**:
   - The CERT coin holds a high value in terms of SUI, with a small ratio.
   - `NativePool::min_stake` is established at one MIST.

2. **Malicious User Actions**:
   - The malicious user stakes one MIST multiple times and receives X CERT.
   - The malicious user proceeds to stake an additional amount of SUI to acquire enough CERT coins required for the unstake process.
   - Finally, the malicious user initiates an unstake action, relinquishing all of their CERT coins.

Please find the proof-of-concept code in this section.

## Remediation

Modify the limit for `NativePool::min_stake` to prevent the exploitation process while maintaining a reasonable ratio range.

## Patch

Fixed in commit `8099e49`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Volo |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.volo.fi/
- **GitHub**: https://github.com/Sui-Volo/volo-liquid-staking-contracts
- **Contest**: https://www.volo.fi/

### Keywords for Search

`vulnerability`

