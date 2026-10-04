---
# Core Classification
protocol: Bucket Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48018
audit_firm: OtterSec
contest_link: https://bucketprotocol.io/
source_link: https://bucketprotocol.io/
github_link: https://github.com/Bucket-Protocol/v1-core

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Improper Tank Value Update

### Overview


The tank module has a bug where the start_s and start_g values are set to incorrect values when claiming collateral and Bucket rewards. This results in the values being one less than what was used in the calculations, causing incorrect amounts to be claimed. The bug has been fixed in the dd49e5e patch. To fix this, the start_s and start_g values should be set to the values used in the calculations, including the sec_portion.

### Original Finding Content

## Claiming Collateral in the Tank Module

The `claim_collateral` function in the tank module claims the collateral gained from liquidations. After claiming the collateral on a `ContributorToken`, `start_s` updates to indicate the claim of collateral up to that point. However, while updating the value of `start_s`, its value is set to one less than the value used for calculating the `collateral_amount` (excluding `sec_portion`).

### Code Snippet

```rust
protocol/sources/tank.move
let sec_portion = *next_s_cache / constants::scale_factor();
let collateral_amount = mul_factor(
    token.deposit_amount,
    *s_cache - token.start_s + sec_portion,
    token.start_p,
);
token.start_s = *s_cache;
```

### Claiming Bucket Rewards

Similarly, `claim_bkt` claims the Bucket rewards provided by the protocol to the Tank. After claiming `$BKT` rewards on a `ContributorToken`, the `start_g` value becomes a value less than the value used for calculating the `bkt_output_amount` (excluding `sec_portion`).

### Code Snippet

```rust
protocol/sources/tank.move
let sec_portion = *next_g_cache / constants::scale_factor();
let bkt_output_amount = mul_factor(
    token.deposit_amount,
    *g_cache - token.start_g + sec_portion,
    token.start_p,
);
token.start_g = *g_cache;
```

## Remediation

Set the `start_s` and `start_g` to values used during the amount calculations (that includes the `sec_portion`).

## Patch

Fixed in `dd49e5e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Bucket Protocol |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://bucketprotocol.io/
- **GitHub**: https://github.com/Bucket-Protocol/v1-core
- **Contest**: https://bucketprotocol.io/

### Keywords for Search

`vulnerability`

