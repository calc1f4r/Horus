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
solodit_id: 51148
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

LOANS CAN BE REPAID WITHOUT SPENDING COINS

### Overview


This bug report is about a flaw in the `RepayStableCoin` function of the `krp-cdp-contracts/central_control` contract. This function is used to repay loans, but there is no access control in place to prevent anyone from using it. This means that anyone can call this function and repay their loans without actually spending any coins. To fix this issue, the Kryptonite team has implemented a solution in their code.

### Original Finding Content

##### Description

The `RepayStableCoin` entry point of the **krp-cdp-contracts/central\_control** contract allows users to repay their loans.

The entry point mentioned is designed to be called by the **krp-cdp-contracts/stable\_pool** contract. However, there is no access control in the `repay_stable_coin` function to verify this condition.

As a consequence, anyone can call this function to repay their loans without spending coins.

Code Location
-------------

There is no access control in the `repay_stable_coin` function:

#### krp-cdp-contracts/contracts/central\_control/src/contract.rs

```
pub fn repay_stable_coin(
 deps: DepsMut,
 _info: MessageInfo,
 sender: String,
 amount: Uint128,
) -> Result<Response, ContractError> {
 let minter_raw = deps.api.addr_canonicalize(&sender.as_str())?;
 let mut loan_info = read_minter_loan_info(deps.storage, &minter_raw)?;
 loan_info.loans = loan_info.loans - Uint256::from(amount);
 store_minter_loan_info(deps.storage, &minter_raw, &loan_info)?;

 Ok(Response::new().add_attributes(vec![
  attr("contract_name", "central_control"),
  attr("action", "repay_stable_coin"),
  attr("sender", sender.to_string()),
  attr("amount", amount.to_string()),
 ]))
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [64d3a2d](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/17/commits/64d3a2d1729e5818e91051e1ffccfaa3947e4cbf).

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

