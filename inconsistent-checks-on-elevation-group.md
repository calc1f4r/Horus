---
# Core Classification
protocol: Hubble Kamino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47874
audit_firm: OtterSec
contest_link: https://kamino.finance/
source_link: https://kamino.finance/
github_link: https://github.com/hubbleprotocol/kamino-lending

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
  - Akash Gurugunti
  - Robert Chen
  - Thibault Marboud
  - OtterSec
---

## Vulnerability Title

Inconsistent Checks On Elevation Group

### Overview

See description below for full details.

### Original Finding Content

## Potential Inconsistencies in Protocol Verification

The issue relates to potential inconsistencies in the protocol’s verification of elevation groups, loan-to-value (LTV) ratios, and liquidation threshold values. Elevation groups categorize assets based on their risk profiles, where each elevation group has specific loan-to-value ratios and liquidation thresholds. Loan-to-value ratios determine how much collateral a borrower must maintain relative to their borrowed amount, while liquidation thresholds represent the point at which a borrower’s collateral-to-debt ratio triggers liquidation. Assets or elevation groups with higher risk may have lower liquidation thresholds.

## Code Example

```rust
lending_operations.rs RUST
pub fn validate_reserve_config(config: &ReserveConfig, market: &LendingMarket) -> Result<()> {
    for elevation_group_id in config.elevation_groups {
        let elevation_group = get_elevation_group(elevation_group_id, market)?;
        if elevation_group_id == ELEVATION_GROUP_NONE {
            // The reserve is removed from an elevation group id
        } else {
            [...]
            if elevation_group.liquidation_threshold_pct < config.liquidation_threshold {
                msg!("Invalid liquidation threshold, elevation id liquidation threshold must be greater than the config's");
                return err!(LendingError::InvalidConfig);
            }
            if elevation_group.ltv_ratio_pct < config.loan_to_value_ratio {
                msg!("Invalid LTV ratio, cannot be bigger than the LTV ratio");
                return err!(LendingError::InvalidConfig);
            }
        }
    }
}
```

While assigning elevation group IDs to the reserves configuration, the values in the elevation group are checked with the loan-to-value and liquidation threshold values on the reserves configuration, as shown in the code above.

However, the lending market owner has the authority to change the loan-to-value ratios and liquidation thresholds for elevation groups. This introduces a potential inconsistency because, during the modification of these values by the owner, there is no mechanism to ensure that existing reserves and obligations comply with the new values, as seen in the code snippet below. This may result in situations where reserves and borrowers are no longer adequately collateralized or are at risk of liquidation.

## Additional Code Example

```rust
Kamino Finance Audit 04 | Vulnerabilities
handler_update_lending_market.rs RUST
pub fn process(
    ctx: Context<UpdateLendingMarket>,
    mode: u64,
    value: [u8; VALUE_BYTE_ARRAY_LEN_MARKET],
) -> Result<()> {
    UpdateLendingMarketMode::UpdateElevationGroup => {
        let elevation_group: ElevationGroup = BorshDeserialize::deserialize(&mut &value[..]).unwrap();
        msg!("Value is {:?}", elevation_group);
        [...]
        if elevation_group.liquidation_threshold_pct >= 100
            || elevation_group.ltv_ratio_pct >= 100
            || elevation_group.ltv_ratio_pct > elevation_group.liquidation_threshold_pct
            || elevation_group.max_liquidation_bonus_bps > FULL_BPS as u16
        {
            return err!(LendingError::InvalidElevationGroupConfig);
        }
        [...]
    }
}
```

## Remediation

Implement a validation mechanism that verifies the validity of the new loan-to-value ratios and liquidation thresholds set by the lending market owner for elevation groups.

## Patch

The Kamino Finance team acknowledged the issue and decided to create a tool in the CLI to validate these values.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Kamino |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Thibault Marboud, OtterSec |

### Source Links

- **Source**: https://kamino.finance/
- **GitHub**: https://github.com/hubbleprotocol/kamino-lending
- **Contest**: https://kamino.finance/

### Keywords for Search

`vulnerability`

