---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40811
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b1baa964-865e-4ae7-9087-72859d9c46ea
source_link: https://cdn.cantina.xyz/reports/cantina_competition_olas_lockbox_jan2024.pdf
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
  - 99Crits
---

## Vulnerability Title

Ineffective slippage control 

### Overview


Summary:

The deposit function in Lockbox V2 is not properly controlling for slippage, allowing attackers to manipulate the deposit process and profit from it. This is caused by the function using the current onchain price to determine the requested liquidity, which can be manipulated by an attacker buying up a lot of token B. To fix this, the deposit instruction should take an additional liquidity_amount parameter to properly account for slippage. This is considered a medium risk issue.

### Original Finding Content

## Lockbox V2 Deposit Instruction Issue

## Context
lib.rs#L192

## Description
The deposit instruction of Lockbox V2 performs insufficient slippage control. This allows an attacker to sandwich the LP deposit for profit and cause the depositor to get much less liquidity than they ought to get. The deposit function takes `token_max_a` and `token_max_b` as input parameters:

```rust
pub fn deposit(ctx: Context<DepositPositionForLiquidity>,
    token_max_a: u64,
    token_max_b: u64,
) -> Result<()> {
```

`token_max_a` is used to calculate the liquidity that will be requested at current prices:

```rust
let sqrt_price_current_x64 = ctx.accounts.whirlpool.sqrt_price;
let sqrt_price_upper_x64 = sqrt_price_from_tick_index(ctx.accounts.position.tick_upper_index);
let liquidity_amount = get_liquidity_from_token_a(token_max_a as u128, sqrt_price_current_x64,
sqrt_price_upper_x64)?;
```

`liquidity_amount` is subsequently used to determine the deltas for token A and B:

```rust
let (delta_a, delta_b) = calculate_liquidity_token_deltas(
    tick_index_current,
    sqrt_price_current_x64,
    &ctx.accounts.position,
    liquidity_amount as i128
)?;
```

Those three values are then used to invoke the `increase_liquidity` instruction of ORCA's whirlpool program:

```rust
whirlpool::cpi::increase_liquidity(cpi_ctx_modify_liquidity, liquidity_amount, delta_a, delta_b)?;
```

The issue is that the liquidity that the user requests is determined based on `token_max_a` at the current on-chain price of the pool. This enables an attacker to sandwich the LP transaction (e.g., using Jito Bundles) by doing the following:

1. Buy up a lot of token B.
2. User transaction executes. They will deposit `token_max_a` and a little amount of token B due to the skewed prices. However, they will also get much less liquidity accounted for than they intended to.

Looking at the calculation in `get_liquidity_from_token_a`:

```rust
fn get_liquidity_from_token_a(amount: u128, sqrt_price_lower_x64: u128, sqrt_price_upper_x64: u128) {
    // liquidity = a * ((sqrt_price_lower * sqrt_price_upper) / (sqrt_price_upper - sqrt_price_lower))
```

`sqrt_price_lower` will be the current price of the pool (see snippet above), and by buying up a lot of token B, it will be lower. A lower `sqrt_price_lower` means the numerator decreases while the denominator increases, resulting in a lower amount of liquidity requested (and received).

3. Sell token B back into the pool and profit due to higher liquidity.

## Recommendation
The deposit instruction should mimic the interface of Orca's `increase_liquidity` instruction and take an additional `liquidity_amount` parameter. From a high-level perspective, this is what should happen to have proper slippage control:

1. User selects the amount they want to deposit and a slippage value in percent, e.g., 100 token A, 200 token B, and 1.5% max slippage.
2. Frontend (or other client) calculates the liquidity amount that the user should get at current non-manipulated prices.
3. Frontend makes the user sign a deposit transaction with the calculated `liquidity_amount` from step 2 and `max_token_a` and `max_token_b` values that account for the maximum acceptable slippage.
4. The lockbox forwards these parameters to the Orca whirlpool program.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Olas |
| Report Date | N/A |
| Finders | 99Crits |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_olas_lockbox_jan2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b1baa964-865e-4ae7-9087-72859d9c46ea

### Keywords for Search

`vulnerability`

