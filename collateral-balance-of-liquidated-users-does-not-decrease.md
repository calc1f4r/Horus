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
solodit_id: 51153
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

COLLATERAL BALANCE OF LIQUIDATED USERS DOES NOT DECREASE

### Overview


The `liquidate_collateral` function in the `krp-cdp-contracts/central_control` contract has a bug where the `DecreaseBalance` message is not being called. This means that when collateral is liquidated, the user's balance will not decrease and they will continue to earn rewards. The bug has been solved by the Kryptonite team in commit [4a00da9](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/34/commits/4a00da9807a0567f0f99fb43324e9ea2278f3583).

### Original Finding Content

##### Description

In the `liquidate_collateral` function from the **krp-cdp-contracts/central\_control** contract, when each collateral in the `liquidation_amount` vector is liquidated, the `DecreaseBalance` message is not called.

As a consequence, the collateral balance of the liquidated user won't decrease and will continue accruing rewards.

Code Location
-------------

The `DecreaseBalance` message is not called in the `liquidate_collateral` function:

#### krp-cdp-contracts/contracts/central\_control/src/contract.rs

```
for collateral in liquidation_amount {
 if collateral.1 > Uint256::zero() {
  let whitelist_elem = read_whitelist_elem(deps.storage, &collateral.0)?;
  liquidation_messages.push(CosmosMsg::Wasm(WasmMsg::Execute {
   contract_addr: deps
    .api
    .addr_humanize(&whitelist_elem.custody_contract)?
    .to_string(),
   funds: vec![],
   msg: to_binary(&CustodyExecuteMsg::LiquidateCollateral {
    liquidator: info.sender.to_string(),
    amount: collateral.1.into(),
   })?,
  }))
 }
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:C/R:N/S:U (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:C/R:N/S:U)

##### Recommendation

**SOLVED**:The `Kryptonite team` solved this issue in commit [4a00da9](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/34/commits/4a00da9807a0567f0f99fb43324e9ea2278f3583).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

