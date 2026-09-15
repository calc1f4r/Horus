---
# Core Classification
protocol: Aries Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48488
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: github.com/Aries-Markets/aries-markets.

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
  - Shiva Shankar Genji
---

## Vulnerability Title

Improper Calculation in Liquidation

### Overview


The bug report describes an issue with the profile.move function, specifically in the calculation of the amount of shares that need to be settled. The problem occurs in the liquidation function, where the settle_share_amount is not being calculated correctly. This is because the repay_amount is being directly returned as the settle share amount, instead of using the get_share_amount_from_borrow_amount function. This results in the overall value of a borrowed share being decreased, which can negatively impact the health of the protocol. The report includes a proof of concept scenario and suggests a possible solution to fix the issue. The bug has been resolved in the latest patch.

### Original Finding Content

## Incorrect Share Settlement Calculation in `profile.move`

In `profile.move`, the amount of shares that need to be settled is calculated incorrectly. In the else case of the liquidation function, the `settle_share_amount` should be calculated from the `repay_amount` using the `get_share_amount_from_borrow_amount` function. Instead, the repay amount is directly returned as the settle share amount.

Since the value of shares increases with the accumulation of borrow interest, the actual `settle_share_amount` would be less than the `repay_amount`. Directly subtracting the repay amount from borrowed shares will decrease the overall value of a borrowed share and affect the health of the protocol.

## Proof of Concept

Consider the following scenario:

1. A user borrows **X** amount from the protocol. This is recorded as **X** number of borrowed shares.
2. After some time, borrow interest accumulates and the total borrowed amount on the reserve increases, thus increasing the borrow share value.
3. Now, if the user’s account loses health and the liquidator liquidates **X** amount of the loan amount, only **X** amount of shares are subtracted from the user’s borrowed shares in spite of the increased borrowed share value.

## Remediation

A possible remediation is converting `repay_amount` to shares using the `get_share_amount_from_borrow_amount` function in the else case of the `liquidate_profile` function.

### Aries/Sources/profile.move DIFF

```plaintext
773 if (decimal::gte(bonus_liquidation_value, collateral_value)) {
774 let repay_percentage = decimal::div(collateral_value, bonus_liquidation_value);
775 let settle_amount = decimal::mul(max_liquidation_amount, repay_percentage);
776 let repay_amount = decimal::ceil_u64(settle_amount);
777 let withdraw_amount = withdraw_reserve.collateral_amount;
778 - (repay_amount, withdraw_amount, settle_amount)
© 2022 OtterSec LLC. All Rights Reserved. 7 / 19
Aries Markets Audit 04 | Vulnerabilities
779 + (repay_amount, withdraw_amount, reserve::get_share_amount_from_borrow_amount_dec(settle_amount))
780 } else {
781 let withdraw_percentage = decimal::div(bonus_liquidation_value, collateral_value);
782 let settle_amount = max_liquidation_amount;
783 let repay_amount = decimal::ceil_u64(settle_amount);
784 let withdraw_amount = decimal::floor_u64(
785 decimal::mul_u64(withdraw_percentage, withdraw_reserve.collateral_amount)
786 );
787 - (repay_amount, withdraw_amount, settle_amount)
788 + (repay_amount, withdraw_amount, reserve::get_share_amount_from_borrow_amount_dec(settle_amount))
789 }
```

## Patch

Resolved in `ba3c164`. 

© 2022 OtterSec LLC. All Rights Reserved. 8 / 19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec, Shiva Shankar Genji |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: github.com/Aries-Markets/aries-markets.
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`

