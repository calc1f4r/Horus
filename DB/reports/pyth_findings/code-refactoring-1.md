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
solodit_id: 47138
audit_firm: OtterSec
contest_link: https://meso.finance/
source_link: https://meso.finance/
github_link: https://github.com/MesoLendingFi/meso-smartcontract

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
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Code Refactoring

### Overview

See description below for full details.

### Original Finding Content

## Implementation Notes

1. **Oracle Management in Lending Pool**
   - Implement a function to unset an oracle in the lending pool to allow the system to switch from one oracle to another, ensuring flexibility and adaptability to changing market conditions. This will enhance the reliability and accuracy of price feeds, which are crucial for maintaining the integrity and security of the lending protocol.

2. **Interest Accrual Optimization**
   - In `repay` and `withdraw` in `lending_pool`, the functions accrue interest on the pool before checking if the user’s position actually exists. If the user’s position does not exist, the functions will revert after having already accrued interest. This means that the interest accrual operation is performed even though it will not result in a successful transaction. 
   - **Recommendation**: Accrue interest after asserting the position exists to optimize the code.

     ```rust
     // lending_pool.move
     public(friend) fun withdraw(
         user: address,
         pool: Object<LendingPool>,
         amount: u64,
     ): FungibleAsset acquires Fees, InterestRate, LendingPool, Ltv, State, UserPosition {
         assert_not_paused(pool);
         accrue_interest(pool);
         assert_position_exists(user);
         [...]
     }
     ```

3. **Utilization of Dispatchable Fungible Asset**
   - Utilize `dispatchable_fungible_asset::deposit` instead of `fungible_asset::deposit` in `rewards_pool::add_rewards`.

4. **Positive Exponent Handling in Oracle Price Retrieval**
   - `oracle::get_pyth_price` assumes the exponent (`expo`) retrieved from the Pyth price data is negative. It utilizes `i64::get_magnitude_if_negative(&expo)` to determine the magnitude of the negative exponent and then calculates a power of 10 (`math128::pow(10, ...)`). 
   - **Issue**: It aborts if `expo` is positive. 
   - **Recommendation**: Add a check to appropriately handle cases where `expo` is positive.

## Remediation
Implement the above-mentioned suggestions.

## Patch
1. Fixed in commit `4423500`.
2. Fixed in commit `740b3d7`.
3. Fixed in commit `d9530ba`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

