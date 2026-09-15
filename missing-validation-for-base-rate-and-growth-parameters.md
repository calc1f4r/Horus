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
solodit_id: 50441
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

MISSING VALIDATION FOR BASE RATE AND GROWTH PARAMETERS

### Overview

See description below for full details.

### Original Finding Content

##### Description

`instantiate` and `update_config` functions in **staking-v1** contract do not validate that values of `base_rate`, `linear_growth` or `exponential_growth` are less or equal than a **threshold** (e.g.: 0.1) predefined in the contract.

The aforementioned values are used to calculate premium bBRO rewards. If those values are not correctly set, the premium bBRO rewards for users could be much higher than expected.

Code Location
-------------

`instantiate` function does not validate that `base_rate`, `linear_growth` or `exponential_growth` are less or equal than a predefined **threshold**:

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

\color{black}\color{white}`update_config` function does not validate that `base_rate`, `linear_growth` or `exponential_growth` are less or equal than a predefined **threshold**:

#### contracts/staking-v1/src/commands.rs

```
if let Some(base_rate) = base_rate {
    config.lockup_config.base_rate = base_rate;
}

if let Some(linear_growth) = linear_growth {
    config.lockup_config.linear_growth = linear_growth;
}

if let Some(exponential_growth) = exponential_growth {
    config.lockup_config.exponential_growth = exponential_growth;
}

```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED:** The issue was fixed in commit [032d729b4cddd49c990fdb5d9e78c608d21f0d25](https://github.com/block42-blockchain-company/brotocol-token-contracts/commit/032d729b4cddd49c990fdb5d9e78c608d21f0d25).

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

