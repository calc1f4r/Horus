---
# Core Classification
protocol: Port Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48868
audit_firm: OtterSec
contest_link: https://www.port.finance/
source_link: https://www.port.finance/
github_link: https://github.com/port-finance/sundial.

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
  - Parth Shastri
  - Robert Chen
  - OtterSec
  - David Chen
---

## Vulnerability Title

Excess Collateral Liquidations

### Overview

The bug report describes an issue with the program instruction "liquidate_sundial_profile" which rounds up the amount of collateral received by the liquidator. This allows an attacker to repeatedly repay a low-value token and receive a much higher valued collateral token, eventually causing the value of the collateral to be lower than the obligation. This results in a loss of funds for the lending protocol. The report suggests a fix to ensure that the health of the account increases during liquidation and to properly handle small obligations. 

### Original Finding Content

## Liquidate Sundial Profile Vulnerability

The program instruction `liquidate_sundial_profile` rounds up the amount of collateral received by the liquidator. This results in the liquidators being able to create an undercollateralized account by repaying much less than the value of the collateral received repeatedly.

### Code Snippet

```rust
instructions/borrow_instructions/liquidate_sundial_profile.rs
let withdraw_value = log_then_prop_err!(collateral_to_withdraw
    .config
    .liquidation_config
    .get_liquidation_value(loan_to_repay.asset.get_value(repay_amount)?));
let withdraw_amount = log_then_prop_err!(collateral_to_withdraw
    .asset
    .get_amount(withdraw_value)
    .and_then(|d| d.try_ceil_u64()));
```

Notice how the `withdraw_amount` is ceilinged in the calculation. The minimum amount received by the liquidator is one collateral token as long as the repay token has a non-zero liquidation value. If the value of the repaid token is lower than the collateral token, a liquidator can then repeatedly repay with a low-valued repay token and receive a much higher-valued collateral token.

While each repayment only causes a small discrepancy between the collateral and obligation amount, eventually an attacker will be able to push the value of the collateral lower than the obligation. Note that each of these operations is still profitable to the attacker, similar to the previous spl-token-lending rounding bug.

Because the attacker is profiting from such a transaction, the lending protocol must be losing money. This leads to a loss of funds scenario for the Sundial program.

## Proof of Concept

More concretely, consider the following scenario:
1. Attacker deposits some token A, which has a high value per minimum token unit (BTC for example).
2. Attacker borrows some token B, which has a low value per minimum token unit (SOL for example).
3. The price of SOL goes up, which makes the attacker liquidatable.
4. The attacker liquidates themselves, repaying a single lamport and receiving 1 satoshi.
5. Because such a liquidation lowers the health of the account, the user is able to do this repeatedly, and the account remains liquidatable throughout.
6. The loan is never repaid fully and the collateral is drained by the liquidator. The lending protocol ends up with an undercollateralized account.
7. The attacker keeps both the collateral and the borrowed asset, in essence stealing the obligation from the lending protocol.

We constructed a proof of concept which creates an undercollateralized account by repeatedly repaying a low-value token while receiving a high-value collateral token. In our proof of concept for demonstration purposes, we used two fake tokens with a large value difference. A real-world example of this with less extreme value differentials could be found between USDC and BTC. 

After a series of malicious liquidation operations, we are able to entirely drain the lower value collateral, leaving behind a severely undercollateralized account.

### Values Before and After Liquidation

- Total collateral value before: `100000283919052573356860`
- Total loan value before: `90200000000000000000000`
- Total collateral value after: `100000000000000000`
- Total loan value: `90180000000000000000000`

This leads to a loss of funds scenario for the lending protocol. If an attacker maliciously creates an undercollateralized account, they could simply keep the loan, never repaying the obligation. Because the value of the loan is higher than the collateral, the lending protocol would be forced to make up the difference.

## Remediation

The lending protocol should ensure that in the general case, the health of the account increases. A liquidation should generally never result in bringing the user closer to becoming undercollateralized. 

At the same time, it will be necessary to ensure that small obligations can be properly liquidated in a profitable manner for the liquidator, even if that liquidation might decrease the health of the account. 

This could be done similar to spl-token-lending’s `reserve.calculate_liquidation` function which considers such small amounts as an edge case.

```rust
// Close out obligations that are too small to liquidate normally
if liquidity.borrowed_amount_wads < LIQUIDATION_CLOSE_AMOUNT.into() {
    // settle_amount is fixed, calculate withdraw_amount and repay_amount
    settle_amount = liquidity.borrowed_amount_wads;
    let liquidation_value = liquidity.market_value.try_mul(bonus_rate)?;
    match liquidation_value.cmp(&collateral.market_value) {
        Ordering::Greater => {
            // Additional logic...
        }
    }
}
```

### Patch

Ensure risk factor decreases during liquidation, fixed in #77.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Port Finance |
| Report Date | N/A |
| Finders | Parth Shastri, Robert Chen, OtterSec, David Chen |

### Source Links

- **Source**: https://www.port.finance/
- **GitHub**: https://github.com/port-finance/sundial.
- **Contest**: https://www.port.finance/

### Keywords for Search

`vulnerability`

