---
# Core Classification
protocol: Ellipsis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48356
audit_firm: OtterSec
contest_link: https://ellipsislabs.xyz/
source_link: https://ellipsislabs.xyz/
github_link: Repos in notes

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
finders_count: 4
finders:
  - Robert Chen
  - William Wang
  - OtterSec
  - Nicola Vella
---

## Vulnerability Title

Account Creation DOS

### Overview


The Phoenix account creation feature has a bug where it will produce an error if the account already has some lamports. This could potentially be used by attackers to prevent the creation of seats. The code that is affected by this bug is located in the "manageseat.rs" file, written in the RUST programming language. To fix this issue, users should use the "transfer" and "allocate" functions instead of "create_account", which is similar to what the Anchor program does. This bug has been resolved in the latest update, version #1.

### Original Finding Content

## Account Creation Primitives in Phoenix

Account creation primitives in Phoenix will error if the account already has lamports. This could, for example, allow an attacker to deny seat creation.

## Code Snippet

```rust
// processor/manageseat.rs
let space = size_of::<Seat>();
invoke_signed(
    &system_instruction::create_account(
        payer.key,
        seat.key,
        Rent::get()?.minimum_balance(space),
        space.try_into().unwrap(),
        &crate::ID,
    ),
    &[payer.clone(), seat.clone(), system_program.clone()],
    &[&[b"seat", market_key.as_ref(), trader.as_ref(), &[bump]]],
);
```

## Remediation

Use `transfer` and `allocate` instead of `create_account`, similar to what Anchor does.

### Code Snippet

```rust
// Fund the account for rent exemption.
// ...
// Allocate space.
// ...
// Assign to the SPL token program.
```

## Patch

Resolved in #1.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ellipsis |
| Report Date | N/A |
| Finders | Robert Chen, William Wang, OtterSec, Nicola Vella |

### Source Links

- **Source**: https://ellipsislabs.xyz/
- **GitHub**: Repos in notes
- **Contest**: https://ellipsislabs.xyz/

### Keywords for Search

`vulnerability`

