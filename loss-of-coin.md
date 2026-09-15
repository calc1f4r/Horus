---
# Core Classification
protocol: Cetus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47271
audit_firm: OtterSec
contest_link: https://www.cetus.zone/
source_link: https://www.cetus.zone/
github_link: https://github.com/CetusProtocol/cetus-limitorder

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
finders_count: 3
finders:
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Loss Of Coin

### Overview


The bug in the limit_order::repay_flash_loan function allows a user to deposit target_coin into a different order than the one that initiated the limit_order::flash_loan. This can result in a financial loss for the original order. An attacker can exploit this by creating an order with the same PayCoin and TargetCoin as the victim's order, then using the victim's order to take the PayCoin and depositing the specified amount of TargetCoin into their own order instead of the victim's. To fix this, the order_id in the receipt needs to be checked to ensure it matches the ID of the limit_order. This bug has been fixed in a recent update. 

### Original Finding Content

## Limit Order Flash Loan Vulnerability

`limit_order::repay_flash_loan` lacks a check to ensure that the `order_id` in the receipt matches. This omission allows a user to deposit `target_coin` into an order different from the one that initiated the `limit_order::flash_loan`. Consequently, the original order loses `PayCoin` and fails to receive `TargetCoin`, resulting in a financial loss.

## Proof of Concept
1. An attacker creates an order with the same `PayCoin` and `TargetCoin` as the victim’s order.
2. The attacker flash loans the victim’s order to take the `PayCoin`.
3. When repaying the flash loan, the attacker deposits the amount of `TargetCoin` specified in the receipt into their own order instead of the victim’s order.
4. The victim does not receive the `TargetCoin`, and the attacker claims the `TargetCoin` from their own order.

## Remediation
Ensure that the `order_id` in the receipt matches the ID of the `limit_order`.

```rust
> _order.moved_diff
@@ -677,6 +677,8 @@ module limit_order::limit_order {
target_repay_amount
} = receipt;
+ assert!(order_id == id(limit_order), EMismatchedOrder);
+
// store target coin into order
let target_coin = coin::split(coin, target_repay_amount, ctx);
let target_balance = coin::into_balance(target_coin);
```

## Patch
Fixed in a commit `a1e ba1`.

© 2024 Otter Audits LLC. All Rights Reserved. 6/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cetus |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://www.cetus.zone/
- **GitHub**: https://github.com/CetusProtocol/cetus-limitorder
- **Contest**: https://www.cetus.zone/

### Keywords for Search

`vulnerability`

