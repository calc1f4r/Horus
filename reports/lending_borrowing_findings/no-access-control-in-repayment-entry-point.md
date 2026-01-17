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
solodit_id: 51151
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

NO ACCESS CONTROL IN REPAYMENT ENTRY POINT

### Overview


This bug report describes a vulnerability in the `RepayStableFromYieldReserve` function of the `krp-market-contracts/overseer` contract. This function allows borrowers to repay their debt using the stable currency reserve in the contract. However, there is no access control in place, which means any user can use the contract's balance to repay their debt without spending any coins. This could potentially lead to loss of funds for the contract. The bug has been solved by the Kryptonite team in a recent commit.

### Original Finding Content

##### Description

The `RepayStableFromYieldReserve` entry point of the **krp-market-contracts/overseer** contract allows a borrower to repay his debt using the stable currency reserve accumulated in the contract.

This entry point has no access control, consequently, any user could repay their own debt without spending any coin, using the balance of the **Overseer** contract if it is sufficient.

Code Location
-------------

There is no access control in the `repay_stable_from_yield_reserve` function:

#### krp-market-contracts/contracts/overseer/src/collateral.rs

```
pub fn repay_stable_from_yield_reserve(
    deps: DepsMut,
    env: Env,
    _info: MessageInfo,
    borrower: Addr,
) -> Result<Response, ContractError> {
    let config: Config = read_config(deps.storage)?;
    let market = deps.api.addr_humanize(&config.market_contract)?;
    let borrow_amount_res: BorrowerInfoResponse = query_borrower_info(
        deps.as_ref(),
        market.clone(),
        borrower.clone(),
        env.block.height,
    )?;
    let borrow_amount = borrow_amount_res.loan_amount;

    let prev_balance: Uint256 = query_balance(
        deps.as_ref(),
        market.clone(),
        config.stable_denom.to_owned(),
    )?;

    let repay_messages = vec![
        CosmosMsg::Bank(BankMsg::Send {
            to_address: market.to_string(),
            amount: vec![Coin {
                denom: config.stable_denom,
                amount: borrow_amount.into(),
            }],
        }),
        CosmosMsg::Wasm(WasmMsg::Execute {
            contract_addr: market.to_string(),
            funds: vec![],
            msg: to_binary(&MarketExecuteMsg::RepayStableFromLiquidation {
                borrower: borrower.to_string(),
                prev_balance,
            })?,
        }),
    ];

    Ok(Response::new().add_messages(repay_messages))
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [e43051d](https://github.com/KryptoniteDAO/krp-market-contracts/pull/12/commits/e43051de2fecc3b28ecd777c6a42fe20601b3dc7).

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

