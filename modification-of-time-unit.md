---
# Core Classification
protocol: Hubble Farms
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47760
audit_firm: OtterSec
contest_link: https://app.kamino.finance/
source_link: https://app.kamino.finance/
github_link: https://github.com/hubbleprotocol/farms

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Modification Of Time Unit

### Overview


The update_farm_config function in the farming pool contract allows administrators to change various settings, including the time interval for reward distribution. However, changing this time interval can cause issues with historical data and inconvenience for users who are used to claiming rewards based on the previous time duration. This can lead to inaccurate reward calculations, discrepancies in claim timing, and confusion for users. To fix this issue, the contract has been updated to prevent changing the time interval mid-course. 

### Original Finding Content

## Update Farm Config

The `update_farm_config` updates the configuration of a farming pool, allowing pool administrators to modify various parameters and settings within the farm to adapt to changing market conditions. Particularly, the `UpdateFarmConfig` instruction modifies `time_unit`, which represents the time interval over which the distribution of rewards occurs and how frequently users can claim their rewards.

## Code Example

```rust
pub fn update_farm_config(
    farm_state: &mut FarmState,
    mode: FarmConfigOption,
    data: &[u8; 32],
) -> Result<()> {
    match mode {
        ...
        FarmConfigOption::UpdateFarmTimeUnit => {
            let value: u8 = BorshDeserialize::deserialize(&mut &data[..])?;
            ...
            farm_state.time_unit = value;
        }
        ...
    };
    Ok(())
}
```

The issue arises as `time_unit` correlates with multiple crucial timestamps such as `last_issuance_ts` in `reward_infos`, representing the timestamp of the last issuance of rewards to users, and `last_claim_ts` in `user_state`, responsible for recording the time when a user last claimed their rewards. 

Therefore, updating `time_unit` will modify these timestamps. Users who have previously staked their assets and claimed rewards will have done so using the earlier `time_unit`, and a sudden change in this value may result in inconsistencies, as the historical data regarding when users staked and when rewards were issued is no longer valid.

Moreover, this change will inconvenience users who have become used to claiming rewards based on the previous time duration. It may result in generating inaccurate reward calculations, discrepancies in when users may claim rewards, and confusion regarding their expected rewards and claim timing.

## Hubble Farms Audit 04 | Vulnerabilities

### Proof of Concept

1. The contract uses `time_unit` of seconds, with users earning rewards based on this unit.
2. An administrator decides to change `time_unit` to minutes, and the contract updates accordingly.
3. The change in `time_unit` renders `last_issuance_ts` in `reward_infos` incompatible with the new `time_unit`.
4. Users’ `last_claim_ts` in `user_state` is tied to the old `time_unit`, potentially resulting in timing and calculation issues when claiming rewards.

The changes described above may cause user reward discrepancies and inconsistent calculations.

## Remediation

Ensure the `time_unit` is not modified mid-course.

### Patch

Fixed in commit `6ac662e` by removing the option to change the time unit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Farms |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://app.kamino.finance/
- **GitHub**: https://github.com/hubbleprotocol/farms
- **Contest**: https://app.kamino.finance/

### Keywords for Search

`vulnerability`

