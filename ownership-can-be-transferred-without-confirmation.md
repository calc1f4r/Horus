---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51176
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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

OWNERSHIP CAN BE TRANSFERRED WITHOUT CONFIRMATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

An incorrect use of the `execute_update_config`, `update_config`, `change_owner`, `change_gov` or `update_staking_config` functions in some contracts can set owner to an invalid address and inadvertently lose control of them, which cannot be undone in any way.

The affected contracts are the following:

* krp-staking-contracts/basset\_sei\_hub
* krp-staking-contracts/basset\_sei\_rewards\_dispatcher
* krp-staking-contracts/basset\_sei\_validators\_registry
* krp-cdp-contracts/central\_control
* krp-cdp-contracts/custody
* krp-cdp-contracts/liquidation\_queue
* krp-cdp-contracts/reward\_book
* krp-cdp-contracts/stable\_pool
* krp-market-contracts/custody\_base
* krp-market-contracts/custody\_bsei
* krp-market-contracts/distribution\_model
* krp-market-contracts/interest\_model
* krp-market-contracts/liquidation\_queue
* krp-market-contracts/market
* krp-market-contracts/overseer
* krp-oracle/oracle\_pyth
* krp-token-contracts/boost
* krp-token-contracts/dispatcher
* krp-token-contracts/distribute
* krp-token-contracts/fund
* krp-token-contracts/keeper
* krp-token-contracts/seilor
* krp-token-contracts/staking
* krp-token-contracts/ve\_seilor
* swap-extension/swap\_sparrow

Code Location
-------------

Example - Code of the `update_config` function in the **krp-market-contracts/custody\_base** contract:

#### krp-market-contracts/contracts/custody\_base/src/contract.rs

```
pub fn update_config(
    deps: DepsMut,
    info: MessageInfo,
    owner: Option<Addr>,
    liquidation_contract: Option<Addr>,
) -> Result<Response, ContractError> {
    let mut config: Config = read_config(deps.storage)?;

    if deps.api.addr_canonicalize(info.sender.as_str())? != config.owner {
        return Err(ContractError::Unauthorized {});
    }

    if let Some(owner) = owner {
        config.owner = deps.api.addr_canonicalize(owner.as_str())?;
    }

    if let Some(liquidation_contract) = liquidation_contract {
        config.liquidation_contract = deps.api.addr_canonicalize(liquidation_contract.as_str())?;
    }

    store_config(deps.storage, &config)?;
    Ok(Response::new().add_attributes(vec![attr("action", "update_config")]))
}

```

##### BVSS

[AO:A/AC:L/AX:H/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (2.5)](/bvss?q=AO:A/AC:L/AX:H/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commits [2a7389f](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/27/commits/2a7389fb284c2470c3662f07e620f4fc06a101e7), [93247af](https://github.com/KryptoniteDAO/krp-market-contracts/pull/14/commits/93247af30c1970817f8986ab3e3c355479e8ef2e), [a1d8a9c](https://github.com/KryptoniteDAO/krp-staking-contracts/pull/23/commits/a1d8a9c7e68d823d099ddd348548ebcc84788fe0), [f3c96c8](https://github.com/KryptoniteDAO/krp-staking-contracts/pull/26/commits/f3c96c849407164f60e4e3c48b20dec8798b8906), [5ab2069](https://github.com/KryptoniteDAO/krp-token-contracts/pull/16/commits/5ab206972c1c1762e5155abec88dcb0e19592801), [2407815](https://github.com/KryptoniteDAO/swap-extension/pull/12/commits/240781527a1363f08936ea4e7838712e158aba9c) and [6dec8f1](https://github.com/KryptoniteDAO/krp-oracle/commit/6dec8f12dd1d4152cb27f747ee67073c4ce08b61).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

