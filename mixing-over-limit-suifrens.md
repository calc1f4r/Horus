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
solodit_id: 48092
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Mixing Over Limit Suifrens

### Overview


The code in capy_labs.move is supposed to prevent users from mixing their Suifrens over a certain limit. However, there is a mistake in the code that allows users to mix their Suifrens even when they have reached the limit. This happens because the code uses the wrong value when setting the mixing limit for the second Suifren. This bug can be fixed by borrowing the correct value in the code. The issue has been resolved in the latest patch.

### Original Finding Content

## Issue with Mixing Limit in Capy Labs

In `capy_labs.move`, `mix` ensures that users are unable to mix their Suifrens over a certain limit. However, a typo in the code results in the application allowing the minting of Suifrens with an insufficient `mixing_limit`. This issue occurs in the second `else` statement where the application borrows the value of `l1` instead of `l2` while setting the `mixing_limit` of the second Suifren.

## Affected Code

```rust
sources/capy_labs.move RUST
public fun mix<T>(
    app: &mut CapyLabsApp,
    sf1: &mut SuiFren<T>,
    sf2: &mut SuiFren<T>,
    clock: &Clock,
    birth_location: vector<u8>,
    ctx: &mut TxContext
): SuiFren<T> {
    [...]
    // Deal with mixing limits;
    {
        let l1 = mixing_limit(sf1);
        let l2 = mixing_limit(sf2);
        if (option::is_none(&l1)) {
            set_limit(sf1, app.mixing_limit - 1);
        } else {
            let limit = *option::borrow(&l1);
            assert!(limit > 0, EReachedMixingLimit);
            set_limit(sf1, limit - 1);
        };
        if (option::is_none(&l2)) {
            set_limit(sf2, app.mixing_limit - 1);
        } else {
            let limit = *option::borrow(&l1);
            assert!(limit > 0, EReachedMixingLimit);
            set_limit(sf2, limit - 1);
        };
    };
    [...]
}
```

## Remediation

Borrow the value of `l2` instead of `l1` in the second `else` statement.

## Patch

Fixed in commit `b142be2`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

