---
# Core Classification
protocol: Tensor Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46760
audit_firm: OtterSec
contest_link: https://tensor.foundation/
source_link: https://tensor.foundation/
github_link: https://github.com/tensor-foundation

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Absence of Royalty Enforcement

### Overview


The bug report discusses an issue with the buy_spl::process_buy_legacy_spl function where the optional_royalty_pct parameter is not being properly checked against the metadata.token_standard. This can result in incorrect amounts of royalties being paid to creators if the user-supplied percentage is not appropriate for the token standard being used. The bug is being fixed in patch #58 by ensuring that the system overrides the user-provided percentage and applies a predefined percentage if royalties are enforced for a certain token standard.

### Original Finding Content

## Overview of `process_buy_legacy_spl` Issues

In `buy_spl::process_buy_legacy_spl`, the `optional_royalty_pct` parameter is currently utilized without verifying whether the royalties are actually enforced based on the `metadata.token_standard`. 

## Explanation

- `optional_royalty_pct` is a user-provided parameter specifying the percentage of royalties to be paid to the creators.
- `metadata.token_standard` indicates the standard of the token.
- Some token standards enforce royalties at a protocol level.

By directly utilizing `optional_royalty_pct`, the token standard that requires a specific amount of royalties may receive an incorrect amount if the user-supplied amount is inappropriate.

```rust
pub fn process_buy_legacy_spl<'info, 'b>(
    ctx: Context<'_, 'b, '_, 'info, BuyLegacySpl<'info>>,
    max_amount: u64,
    optional_royalty_pct: Option<u16>,
    authorization_data: Option<AuthorizationDataLocal>,
) -> Result<()> {
    [...]
    let creator_fee = calc_creators_fee(
        metadata.seller_fee_basis_points,
        amount,
        optional_royalty_pct,
    )?;
    [...]
}
```

## Remediation

Ensure that if a royalty is enforced for a certain token standard, the system overrides any user-provided `optional_royalty_pct` and applies a predefined percentage.

## Patch

Resolved in #58.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Foundation |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://tensor.foundation/
- **GitHub**: https://github.com/tensor-foundation
- **Contest**: https://tensor.foundation/

### Keywords for Search

`vulnerability`

