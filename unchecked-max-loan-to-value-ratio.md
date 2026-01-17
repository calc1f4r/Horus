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
solodit_id: 51171
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

UNCHECKED MAX LOAN-TO-VALUE RATIO

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `whitelist_collateral` function in the **krp-cdp-contracts/central\_control** contract does not verify that `max_ltv` parameter is lower than 1. If it is mistakenly set to a value greater than 1, users will be able to redeem more coins than the value of their deposited collaterals.

This issue also applies to the `register_whitelist` and `update_whitelist` functions in the **krp-market-contracts/overseer** contract.

Code Location
-------------

The `whitelist_collateral` function in the **krp-cdp-contracts/central\_control** contract:

#### krp-cdp-contracts/contracts/central\_control/src/contract.rs

```
pub fn whitelist_collateral(
    deps: DepsMut,
    info: MessageInfo,
    name: String,
    symbol: String,
    max_ltv: Decimal256,
    custody_contract: CanonicalAddr,
    collateral_contract: CanonicalAddr,
    reward_book_contract: CanonicalAddr,
) -> Result<Response, ContractError> {
    let config = read_config(deps.storage)?;

    if deps.api.addr_canonicalize(info.sender.as_str())? != config.owner_addr {
        return Err(ContractError::Unauthorized(
            "whitelist_collateral".to_string(),
            info.sender.to_string(),
        ));
    }

    if max_ltv >= Decimal256::one() {
        return Err(ContractError::MaxLtvExceedsLimit {});
    }

    let data = WhitelistElem {
        name,
        symbol,
        max_ltv,
        custody_contract,
        collateral_contract: collateral_contract.clone(),
        reward_book_contract,
    };
    store_whitelist_elem(deps.storage, &collateral_contract, &data)?;
    Ok(Response::default())
}

```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:N/D:N/Y:M/R:N/S:U (3.4)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:N/D:N/Y:M/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commits [13e9a4f](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/28/commits/13e9a4f9009450a936c9899e194bdd97250493ea) and [8f2be6a](https://github.com/KryptoniteDAO/krp-market-contracts/pull/15/commits/8f2be6a6e461c1ddaf6f7bf5f376883d32da7247).

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

