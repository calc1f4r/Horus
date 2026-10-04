---
# Core Classification
protocol: Brokkr Protocol P1 Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50443
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

MISSING VALIDATION FOR MIN AND MAX VALUES OF LOCKUP PERIOD

### Overview

See description below for full details.

### Original Finding Content

##### Description

`instantiate` and `update_config` functions in **staking-v1** contract do not validate that `min_lockup_period_epochs` is less than `max_lockup_peri` `od_epochs`.

The aforementioned values are used to validate the lockup period when staking locked BRO tokens or locking a previous staked amount. If those values are not correctly set, operations will throw error messages and won't allow legitimate users to stake or lock BRO tokens, thus generating a denial of service (DoS) in Brokkr protocol.

Code Location
-------------

`instantiate` function does not validate that `min_lockup_period_epochs` is less than `max_lockup_period_epochs`:

#### contracts/staking-v1/src/contract.rs

```
store_config(
    deps.storage,
    &Config {
        owner: deps.api.addr_canonicalize(&msg.owner)?,
        paused: false,
        bro_token: deps.api.addr_canonicalize(&msg.bro_token)?,
        rewards_pool_contract: deps.api.addr_canonicalize(&msg.rewards_pool_contract)?,
        bbro_minter_contract: deps.api.addr_canonicalize(&msg.bbro_minter_contract)?,
        epoch_manager_contract: deps.api.addr_canonicalize(&msg.epoch_manager_contract)?,
        unstake_period_blocks: msg.unstake_period_blocks,
        min_staking_amount: msg.min_staking_amount,
        lockup_config: LockupConfig {
           min_lockup_period_epochs: msg.min_lockup_period_epochs,
           max_lockup_period_epochs: msg.max_lockup_period_epochs,
           base_rate: msg.base_rate,
           linear_growth: msg.linear_growth,
           exponential_growth: msg.exponential_growth,
        },
    },
)?;

```

\color{black}\color{white}`update_config` function does not validate that `min_lockup_period_epochs` is less than `max_lockup_period_epochs`:

#### contracts/staking-v1/src/commands.rs

```
if let Some(min_lockup_period_epochs) = min_lockup_period_epochs {
    config.lockup_config.min_lockup_period_epochs = min_lockup_period_epochs;
}

if let Some(max_lockup_period_epochs) = max_lockup_period_epochs {
    config.lockup_config.max_lockup_period_epochs = max_lockup_period_epochs;
}

```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED:** The issue was fixed in commit [b9c1e4ad60fa79e030737e5374a8b027c147d091](https://github.com/block42-blockchain-company/brotocol-token-contracts/commit/b9c1e4ad60fa79e030737e5374a8b027c147d091).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Brokkr Protocol P1 Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

