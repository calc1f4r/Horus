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
solodit_id: 50442
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

MISSING VALIDATION FOR BONDING DISCOUNTS AND REWARD RATIO

### Overview

See description below for full details.

### Original Finding Content

##### Description

`instantiate` and `update_config` functions in **bonding-v1** contract do not validate that values of `ust_bonding_reward_ratio`, `ust_bonding_discount` or `lp_bonding_discount` are less or equal than 1.

The aforementioned values are used to calculate rewards distribution and amounts of BRO tokens to claim. If those values are not correctly set, operations will throw error messages and won't allow legitimate users to claim their rewards, thus generating a denial of service (DoS) in Brokkr protocol.

Code Location
-------------

`instantiate` function does not validate that `ust_bonding_discount` or `lp_bonding_discount` are less or equal than 1:

#### contracts/bonding-v1/src/contract.rs

```
if msg.ust_bonding_reward_ratio > Decimal::from_str("1.0")?
    || msg.ust_bonding_reward_ratio <= Decimal::zero()
{
    return Err(ContractError::InvalidUstBondRatio {});
}

store_config(
    deps.storage,
    &Config {
        owner: deps.api.addr_canonicalize(&msg.owner)?,
        bro_token: deps.api.addr_canonicalize(&msg.bro_token)?,
        lp_token: deps.api.addr_canonicalize(&msg.lp_token)?,
        rewards_pool_contract: deps.api.addr_canonicalize(&msg.rewards_pool_contract)?,
        treasury_contract: deps.api.addr_canonicalize(&msg.treasury_contract)?,
        astroport_factory: deps.api.addr_canonicalize(&msg.astroport_factory)?,
        oracle_contract: deps.api.addr_canonicalize(&msg.oracle_contract)?,
        ust_bonding_reward_ratio: msg.ust_bonding_reward_ratio,
        ust_bonding_discount: msg.ust_bonding_discount,
        lp_bonding_discount: msg.lp_bonding_discount,
        min_bro_payout: msg.min_bro_payout,
        vesting_period_blocks: msg.vesting_period_blocks,
        lp_bonding_enabled: msg.lp_bonding_enabled,
    },
)?;

```

\color{black}\color{white}`update_config` function does not validate that `ust_bonding_reward_ratio`, `ust_bonding_discount` or `lp_bonding_discount` are less or equal than 1:

#### contracts/bonding-v1/src/commands.rs

```
if let Some(ust_bonding_reward_ratio) = ust_bonding_reward_ratio {
    config.ust_bonding_reward_ratio = ust_bonding_reward_ratio;
}

if let Some(ust_bonding_discount) = ust_bonding_discount {
    config.ust_bonding_discount = ust_bonding_discount;
}

if let Some(lp_bonding_discount) = lp_bonding_discount {
    config.lp_bonding_discount = lp_bonding_discount;
}

```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED:** The issue was fixed in commit [e80b7dc97ff20b683cd27d7a4cdaa6d7d60c1076](https://github.com/block42-blockchain-company/brotocol-token-contracts/commit/e80b7dc97ff20b683cd27d7a4cdaa6d7d60c1076).

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

