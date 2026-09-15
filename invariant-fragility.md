---
# Core Classification
protocol: Exponent Jito Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46727
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core/tree/fix-kysol-market-calc

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
  - Akash Gurugunti
---

## Vulnerability Title

Invariant Fragility

### Overview


The bug report discusses an issue with the MintSy and RedeemSy instructions in the jito_restaking_standard software. The invariant, which is used to ensure that the amount of base tokens in the token_vrt_escrow account matches the supply of synthetic yield (SY) tokens in the mint_sy account, is causing problems when a single SY token is burned. This causes the check in the invariant to fail and prevents any further mints or redemptions, leading to a denial of service situation. The recommended solution is to replace strict equality with an acceptable range or margin of error. This issue has been fixed in the latest version of the software. 

### Original Finding Content

## MintSy and RedeemSy Instructions

In the MintSy and RedeemSy instructions, the invariant is utilized to validate that the amount of base tokens in the `token_vrt_escrow` account equals the supply of synthetic yield (SY) tokens in the `mint_sy` account to ensure that SY is backed by enough VRT. 

However, in the case that even a single SY token is burned, the `mint_sy.supply` decreases, and consequently, the check in the invariant would fail. The invariant failure prevents any subsequent mints or redemptions, effectively creating a denial of service scenario.

```rust
> _ jito_restaking_standard/src/instructions/redeem_sy.rs
fn invariant(&mut self) -> Result<()> {
    invariant(&self.token_vrt_escrow.amount, &self.mint_sy.supply)
}
```

## Remediation

Replace strict equality with an acceptable range or a margin of error.

## Patch

Fixed in commit `bbca170`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Jito Restaking |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core/tree/fix-kysol-market-calc
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

