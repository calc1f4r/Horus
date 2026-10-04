---
# Core Classification
protocol: Jupiter Perps Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47713
audit_firm: OtterSec
contest_link: https://jup.ag/perps
source_link: https://jup.ag/perps
github_link: https://github.com/jup-ag/perpetuals

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - Thibault Marboud
  - OtterSec
  - Nicola Vella
---

## Vulnerability Title

Missing Validation

### Overview

See description below for full details.

### Original Finding Content

## Validate In Custody

`validateInCustody` performs validation checks on the parameters and attributes of a custody account. It returns a boolean value indicating whether the custody is valid based on specific criteria.

## Code Implementation

### custody.rs (RUST)

```rust
impl FundingRateState {
    pub fn validate(&self) -> bool {
        (self.hourly_funding_bps as u128) <= Perpetuals::BPS_POWER
    }
}

impl Custody {
    pub fn validate(&self) -> bool {
        self.token_account != Pubkey::default()
        && self.mint != Pubkey::default()
        && self.oracle.validate()
        && self.pricing.validate()
        && (self.target_ratio_bps as u128) <= Perpetuals::BPS_POWER
    }
    [...]
}
```

However, it fails to call `self.funding_rate_state.validate` internally, which checks if the funding rate is less than or equal to the defined maximum threshold (`BPS_POWER`). Thus, there is no constraint on how high the funding rate may become, which is not desirable, as extremely high funding rates disproportionately benefit one side (long or short).

## Remediation

Call `self.funding_rate_state.validate` within `validate`.

## Patch

Fixed in e7a777f.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jupiter Perps Program |
| Report Date | N/A |
| Finders | Robert Chen, Thibault Marboud, OtterSec, Nicola Vella |

### Source Links

- **Source**: https://jup.ag/perps
- **GitHub**: https://github.com/jup-ag/perpetuals
- **Contest**: https://jup.ag/perps

### Keywords for Search

`vulnerability`

