---
# Core Classification
protocol: Anchor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46860
audit_firm: OtterSec
contest_link: https://github.com/coral-xyz
source_link: https://github.com/coral-xyz
github_link: https://github.com/coral-xyz/anchor

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Single-Byte Discriminator Conflict

### Overview


The bug report discusses a vulnerability in the Anchor framework when using single-byte custom discriminators. This can lead to an accidental match with other account types that have default 8-byte discriminators if their first byte is also zero. This can result in account data being overwritten. To fix this issue, the zero constraint needs to be modified to check at least 8 bytes, regardless of the discriminator size. This has been addressed in a recent pull request.

### Original Finding Content

## Vulnerability Overview

This vulnerability arises when utilizing single-byte custom discriminators in the Anchor framework. Normally, an account type’s discriminator is utilized to ensure account data is associated with the correct program. However, if an account with only a single-byte discriminator (such as `[account(discriminator = [89])]`) is initialized with the zero constraint, it checks only that the first byte of the account’s data is zero. This may result in an accidental match with other account types that generate default 8-byte discriminators if their discriminator’s first byte is also zero.

## Proof of Concept

```rust
#[account(zero)]
Foo: Account<'info, Foo>,
[...]
#[account(discriminator = [89])]
pub struct Foo {
    [...]
}
```

In the example provided above, suppose the Ab account type has a default 8-byte discriminator, where its first byte is zero. This creates a 1-in-256 chance that the Ab account type will have the same starting byte as Foo (the single-byte `[89]` discriminator) and thus be erroneously interpreted as Foo. Consequently, the account data of Ab will be overwritten if it is passed in.

## Remediation

Ensure that the zero constraint is modified to check at least 8 bytes, regardless of the discriminator size, to reduce the likelihood of accidental matches.

## Patch

Fixed in PR#3365

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Anchor |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://github.com/coral-xyz
- **GitHub**: https://github.com/coral-xyz/anchor
- **Contest**: https://github.com/coral-xyz

### Keywords for Search

`vulnerability`

