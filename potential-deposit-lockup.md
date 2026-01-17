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
solodit_id: 47307
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: https://github.com/aries-markets/aries-markets

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

Potential Deposit Lockup

### Overview


The report highlights a potential vulnerability in the logic of the deposit_coin_to_reserve function. This function prioritizes repaying existing loans with the repay_coin before using it for minting liquidity provider tokens. However, the function then utilizes the minted liquidity provider tokens for collateral through reserve::add_collateral<Coin0>(lp_coin), which may not be allowed for some coins within the Aries Markets protocol. This can result in the function failing and potentially leaving the user with outstanding debt and liquidation penalties. The recommended solution is to modify the function to check if the deposit_coin is an acceptable collateral type before using it as collateral. The issue has been fixed in version 06f2587.

### Original Finding Content

## Potential Vulnerability in `deposit_coin_to_reserve` Logic

There is a potential vulnerability in the logic of `deposit_coin_to_reserve`. It prioritizes repaying existing loans with the `repay_coin` before utilizing it for minting liquidity provider tokens. However, the function then utilizes the minted liquidity provider tokens (representing the remaining `deposit_coin`) for collateral through `reserve::add_collateral<Coin0>(lp_coin)`.

> _controller.moverust_
```rust
fun deposit_coin_to_reserve<Coin0>(
    repay_coin: Coin<Coin0>,
    deposit_coin: Coin<Coin0>,
) {
    let repay_remaining_coin = reserve::repay<Coin0>(repay_coin);
    coin::destroy_zero<Coin0>(repay_remaining_coin);
    let lp_coin = reserve::mint<Coin0>(deposit_coin);
    reserve::add_collateral<Coin0>(lp_coin);
}
```

The issue arises because some coins may not be allowed as collateral within the Aries Markets protocol. If the `repay_coin` is one such coin, it gets utilized for repayment first. But since the minted liquidity provider tokens represent the remaining `deposit_coin` (of the same type as `repay_coin`), adding them as collateral fails. Thus, even if the `repay_coin` amount is enough to cover the entire loan, the call will fail, because it may not be utilized as collateral, rendering the user with outstanding debt and potential liquidation penalties.

## Remediation

Modify the function to check if `deposit_coin` is an acceptable collateral type before utilizing it as collateral.

## Patch

Fixed in `06f2587`.

© 2024 Otter Audits LLC. All Rights Reserved. 11/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: https://github.com/aries-markets/aries-markets
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`

