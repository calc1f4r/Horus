---
# Core Classification
protocol: Navi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48035
audit_firm: OtterSec
contest_link: https://www.naviprotocol.io/
source_link: https://www.naviprotocol.io/
github_link:  github.com/naviprotocol/protocol-core

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
  - Ajay Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Loss Of Funds In Lending

### Overview


This bug report discusses a problem in the lending.move function where the CoinType type tag is not being verified against the coin type set in ReserveData. This can lead to the loss of funds when calling the functions. Specifically, the withdraw function allows an attacker to specify an asset and pool, resulting in the deduction of a large amount of USD from the ReserveData but receiving a much larger amount of Bitcoin due to a lack of validation. The report recommends implementing input validation to ensure the provided asset and pool parameters are valid. This issue has been resolved in the latest patch.

### Original Finding Content

## Vulnerability Assessment of lending.move

In all functions in `lending.move`, the `CoinType` type tag lacks verification against the coin type set in `ReserveData` for the corresponding asset. This absence may lead to the loss of funds when calling the functions.

## Example: Withdraw Function in lending.move

```rust
public entry fun withdraw<CoinType>(
    clock: &Clock,
    oracle: &PriceOracle,
    storage: &mut Storage,
    pool: &mut Pool<CoinType>,
    asset: u8,
    amount: u64, // e.g. 100USDT(1000000) -> 100 * 1e6
    to: address,
    ctx: &mut TxContext
) {
    when_not_paused(storage);
    let sender = tx_context::sender(ctx);
    // e.g. 100000000 -> 100000000000
    let normal_withdraw_amount = pool::normal_amount(pool, amount);
    validation::validate_withdraw(storage, asset, normal_withdraw_amount);
    let actual_amount = logic::execute_withdraw(clock, oracle, storage, asset,
        sender, (normal_withdraw_amount as u256));
    let normal_actual_amount = pool::unnormal_amount(pool, actual_amount);
    pool::withdraw(pool, normal_actual_amount, to, ctx);
    emit(WithdrawEvent {
        reserve: asset,
        sender: tx_context::sender(ctx),
        to: to,
        amount: normal_withdraw_amount
    })
}
```

The function allows an attacker to supply an asset parameter indicating USD and a pool with Bitcoin as `CoinType`. By specifying an amount of `10^8`, the function deducts 100 USD from the USD `ReserveData` in storage. However, due to the attacker specifying a Bitcoin pool, they will receive `10^8` Bitcoin units, equivalent to one Bitcoin when accounting for decimals. The attacker acquires one Bitcoin for only 100 USD.

**Note:** Within the module, similar issues may occur in the other functions as well.

## Remediation

Implement input validation to ensure that the provided asset and pool parameters are valid against the `CoinType` supplied.

## Patch

Resolved in `a7ea49c` by incorporating validation for the `CoinType` against the provided asset.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Navi |
| Report Date | N/A |
| Finders | Ajay Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.naviprotocol.io/
- **GitHub**:  github.com/naviprotocol/protocol-core
- **Contest**: https://www.naviprotocol.io/

### Keywords for Search

`vulnerability`

