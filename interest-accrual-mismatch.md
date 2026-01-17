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
solodit_id: 47133
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

Interest Accrual Mismatch

### Overview


The report highlights an inconsistency in the accrual of interest across different pools when a user initiates and completes a flash loan. When a user starts a flash loan, the function to update the state of the lending pool to reflect accrued interest is called. However, if the user repays the loan in a different pool, the function to accrue interest is not called for that pool. This results in an inconsistent state between the borrowing pool and the repayment pool. The report recommends ensuring that interest is accrued for the repayment pool before calling the deposit function. This issue has been fixed in the latest patch.

### Original Finding Content

## Inconsistency in Flash Loan Interest Accrual

There is an inconsistency in the accrual of interest across different pools when a user initiates and completes a flash loan. When a user starts a flash loan via `start_flashloan`, `accrue_interest(pool)` is called, as shown below. This function updates the state of the lending pool to reflect the accrued interest up to the current moment. This ensures that the pool’s state accurately represents the interest accrued on all outstanding loans.

If the user repays the flash loan in the same pool from which they borrowed, `repay` is called. This function handles the repayment and updates the pool’s state accordingly.

```rust
public(friend) fun start_flashloan(
    user: &signer,
    pool: Object<LendingPool>,
    amount: u64,
): (FungibleAsset, FlashLoanReceipt) acquires InterestRate, Fees, LendingPool, Ltv, State, UserPosition {
    assert_not_paused(pool);
    accrue_interest(pool);
    create_position_if_not_exists(user);
    [...]
}
```

However, if the user deposits the repayment into a different pool via `deposit_internal`, interest is not accrued for the repayment pool before the deposit is made, as highlighted in the code below. This results in an inconsistent state because, while the borrowing pool’s state is updated to reflect the most recent accrued interest, the repayment pool’s state may not reflect the most recent accrued interest since `accrue_interest` is not called for this pool in `end_flashloan`.

```rust
public(friend) fun end_flashloan(
    repayment_pool: Object<LendingPool>,
    repayment: FungibleAsset,
    receipt: FlashLoanReceipt,
) acquires Fees, InterestRate, LendingPool, Ltv, State, UserPosition {
    [...]
    if (borrow_from == repayment_pool) {
        repay(borrower, repayment_pool, repayment);
    } else {
        deposit_internal(borrower, repayment_pool, repayment);
    };
    check_position(borrow_global<UserPosition>(borrower));
}
```

## Remediation

Ensure that interest is accrued for the repayment pool in `end_flashloan` before calling `deposit_internal`.

## Patch

Fixed in `1acebb3`.

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

