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
solodit_id: 51150
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

NO ACCESS CONTROL IN WITHDRAW FUNCTION

### Overview


The `WithdrawCollateral` function in the **krp-market-contracts/custody\_base** and **krp-market-contracts/custody\_bsei** contracts allows anyone to withdraw collateral from another user's account without proper access control. This means that an attacker could steal collateral from other users. The code location and BVSS (Bug Vulnerability Severity Score) are provided, and the Kryptonite team has solved this issue in a recent commit.

### Original Finding Content

##### Description

The `WithdrawCollateral` entry point of the **krp-market-contracts/custody\_base** and **krp-market-contracts/custody\_bsei** contracts allows a borrower to withdraw any amount of previously deposited collateral.

This entry point is designed to be called by the **krp-market-contracts/overseer** contract; however, there is no access control in the `withdraw_collateral` function to verify that.

As a consequence, any attacker could withdraw any amount of collateral from any other user, since the `borrower` and `amount` values are taken from the entry point input.

Code Location
-------------

Code fragment of the `withdraw_collateral` function of the **krp-market-contracts/custody\_bsei** contract:

#### krp-market-contracts/contracts/custody\_bsei/src/collateral.rs

```
pub fn withdraw_collateral(
    deps: DepsMut,
    borrower: String,
    amount: Option<Uint256>,
) -> Result<Response, ContractError> {
    let config: Config = read_config(deps.storage)?;

    let borrower_raw = deps.api.addr_canonicalize(borrower.as_str())?;
    let mut borrower_info: BorrowerInfo = read_borrower_info(deps.storage, &borrower_raw);

    // Check spendable balance
    let amount = amount.unwrap_or(borrower_info.spendable);
    if borrower_info.spendable < amount {
        return Err(ContractError::WithdrawAmountExceedsSpendable(
            borrower_info.spendable.into(),
        ));
    }

    // decrease borrower collateral
    borrower_info.balance = borrower_info.balance - amount;
    borrower_info.spendable = borrower_info.spendable - amount;

    if borrower_info.balance == Uint256::zero() {
        remove_borrower_info(deps.storage, &borrower_raw);
    } else {
        store_borrower_info(deps.storage, &borrower_raw, &borrower_info)?;
    }

    Ok(Response::new()
        .add_message(CosmosMsg::Wasm(WasmMsg::Execute {
            contract_addr: deps
                .api
                .addr_humanize(&config.collateral_token)?
                .to_string(),
            funds: vec![],
            msg: to_binary(&Cw20ExecuteMsg::Transfer {
                recipient: borrower.to_string(),
                amount: amount.into(),
            })?,
        }))

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [717dbe0](https://github.com/KryptoniteDAO/krp-market-contracts/pull/11/commits/717dbe019707eaa0699ac816cccccb6e16c616a8).

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

