---
# Core Classification
protocol: Mysten Republic Security Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46853
audit_firm: OtterSec
contest_link: https://www.mystenlabs.com/
source_link: https://www.mystenlabs.com/
github_link: https://github.com/MystenLabs/security-token

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
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Possible Overflow Due to Exceeding the Type Limit

### Overview


This bug report discusses a potential issue with the calculation of dividends and unlocked amounts in the code. This issue may occur when dealing with large values, causing an overflow in the u64 data type. To fix this issue, the values involved in the calculation should be converted to u128 before performing any arithmetic operations. This bug has been resolved in the code update a393844.

### Original Finding Content

## Potential Overflow Risk in `dividends::calculate_available_dividends`

There is a potential overflow risk in `dividends::calculate_available_dividends` during the calculation of dividends for a particular address. Specifically, when multiplying two large `u64` values, such as `self.total_funds` and `snapshot.address_balance(addr)`, the result may exceed the maximum value for `u64`, resulting in an overflow.

## Code Snippet
```rust
public fun calculate_available_dividends<T, U>(
    self: &Dividends<U>,
    snapshot: &Snapshot<T>,
    addr: address,
): u64 {
    [...]
    // prettier-ignore
    let addr_total_dividends =
        (self.total_funds * snapshot.address_balance(addr)) / unlocked_supply_t;
    addr_total_dividends - already_claimed
}
```

Similarly, `schedule_config::calculate_unlocked` contains multiple multiplications and divisions involving `u64` values, which may result in an overflow when handling large amounts or time periods. For example, while calculating `unlocked`, `full_amount`, and `initial_release_portion_in_bps` may be large values, and multiplying them in `u64` space may exceed the `u64` limit.

## Remediation
Ensure the values involved in the multiplication and division are converted to `u128` before performing the arithmetic operations. Moving to `u128` will provide a much larger range, removing the risk of overflow.

## Patch
Resolved in `a393844`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Republic Security Token |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://www.mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/security-token
- **Contest**: https://www.mystenlabs.com/

### Keywords for Search

`vulnerability`

