---
# Core Classification
protocol: GooseFX v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47693
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Missing Asset Type Validation

### Overview


The report identifies a bug in the CreateSsl function where the asset_type parameter is not properly validated. This can lead to users creating an SSL pool with an invalid or uninitialized asset_type, resulting in a denial of service. The bug can be fixed by implementing proper input validation and handling potential errors gracefully. The bug has been fixed in the latest patch.

### Original Finding Content

## Validation Issue in CreateSsl

Within `CreateSsl`, there is a lack of validation on the `asset_type` parameter. This may result in a user creating an SSL pool with an invalid or uninitialized `asset_type`. Specifically, in `PoolRegistry`, while fetching token ratios based on the `asset_type` of each pool, if `max_pool_token_ratio` encounters an `InvalidAssetType` error, the swap operations will fail, as `asset_type` is immutable, essentially locking the associated mint in the pool registry. This will result in denial of service.

## Code Snippet

```rust
// admin/create_ssl.rs 
pub fn process(
    &mut self,
    initial_pool_deposit: u64,
    oracle_type: OracleType,
    asset_type: AssetType,
    math_params: SSLMathParams,
    number_of_slots_throttle: Option<u8>,
    max_slot_price_staleness: Option<u8>,
    bump: u8,
) -> Result<()> {
    if initial_pool_deposit == 0 {
        return err!(SSLV2Error::ZeroInitialDeposit);
    }
    // Initialize the oracle price history
    {
        let mut oracle_price_history = self.oracle_price_history.load_init()?;
        #[cfg(feature = "debug-msg")]
        msg!("Oracle: {}", self.oracle_account.key());
        oracle_price_history.initialize(
            [...]
        )?;
        oracle_price_history.update_price(&self.oracle_account.data.borrow()[..])?;
    }
    [...]
}
```

## Remediation

Implement proper input validation in `CreateSsl` to ensure that only valid `asset_type` values are accepted. Additionally, when handling `asset_type` in the `PoolRegistry` operations, validate and handle potential errors gracefully to avoid a denial of service.

## Patch

Fixed in commit `4f0c2ed`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX v2 |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Thibault Marboud |

### Source Links

- **Source**: https://www.goosefx.io/
- **GitHub**: https://github.com/GooseFX1/gfx-ssl-v2
- **Contest**: https://www.goosefx.io/

### Keywords for Search

`vulnerability`

