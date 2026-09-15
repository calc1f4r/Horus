---
# Core Classification
protocol: Meso Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47134
audit_firm: OtterSec
contest_link: https://meso.finance/
source_link: https://meso.finance/
github_link: https://github.com/MesoLendingFi/meso-smartcontract

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Inconsistency In Debt Repaid And Collateral Seized

### Overview


The report discusses a bug in a liquidation process where the amount of debt repaid by the liquidator may be less than the original amount provided. This can result in the liquidatee losing funds and remaining vulnerable to further exploitation. The bug has been fixed in the latest update.

### Original Finding Content

## Liquidation Process in Lending Pools

During liquidation, the liquidator specifies the repayment amount to be repaid on behalf of the liquidatee, and a fungible asset of that amount is provided as an argument to `repay`. 

`repay` utilizes `calculate_shares` to determine the exact number of shares to repay, rounding down in cases of non-perfect division. As a result, the liquidatee’s debt reduction may be less than the original fungible asset amount (`repaid_amount`). However, all subsequent calculations rely on the `repaid_amount` variable to determine the number of shares transferred from the liquidatee to the liquidator.

>_ lending_pool.move rust  
> 
> **public(friend) fun liquidate(**  
>     liquidator: &signer,  
>     borrow_pool: Object<LendingPool>,  
>     supply_pool: Object<LendingPool>,  
>     borrower: address,  
>     repayment: FungibleAsset,  
>     min_amount_received: u128,  
> **) acquires Fees, InterestRate, LendingPool, Liquidation, Ltv, State, UserPosition {**  
> 
>     [...]  
>     let amount_repaid = (fungible_asset::amount(&repayment) as u128);  
>     [...]  
>     repay(borrower, borrow_pool, repayment);  
>     // Calculate how many shares of supply tokens should be transferred to the liquidator.  
>     // This includes both the amount the liquidator repaid for the borrower plus a fee.  
>     let borrow_lending_pool = borrow_global<LendingPool>(borrow_pool_addr);  
>     let supply_pool_addr = object::object_address(&supply_pool);  
>     let supply_lending_pool = borrow_global<LendingPool>(supply_pool_addr);  
>     let amount_repaid_with_fees = math128::mul_div(  
>         amount_repaid,  
>         MAX_BPS_U128 + liquidation_config.liquidation_fee_bps,  
>         MAX_BPS_U128,  
>     );  
>     [...]  
> }  

This discrepancy may decrease the liquidatee’s health factor, resulting in the liquidatee losing funds. Because the health factor decreases, the liquidatee remains liquidatable even after the liquidation. The caller may exploit this repeatedly, resulting in further financial loss to the liquidatee with each cycle.

## Remediation

Recalculate the `amount_repaid` based on the correct number of shares repaid.

### Patch

Fixed in `1549b59`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Meso Lending |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://meso.finance/
- **GitHub**: https://github.com/MesoLendingFi/meso-smartcontract
- **Contest**: https://meso.finance/

### Keywords for Search

`vulnerability`

