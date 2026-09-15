---
# Core Classification
protocol: Symmetry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48603
audit_firm: OtterSec
contest_link: https://www.symmetry.fi/
source_link: https://www.symmetry.fi/
github_link: https://github.com/symmetry-protocol/funds-program

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
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Unsecure Token Swaps

### Overview


The report discusses a bug in a program that allows for token swaps using Pyth prices. The bug can be exploited by an attacker who can manipulate the order of transactions and profit from the swap. This is done by reordering the transactions to occur after the oracle update, allowing the attacker to swap tokens at a higher price and then swap them back at a profit. To fix this issue, a protocol fee should be implemented to prevent attackers from profiting from small changes in the oracle price feed. A patch has been implemented to use a custom step price curve and reduce the output amount as a fee.

### Original Finding Content

## Token Swap Vulnerability

In the `swap_fund_tokens` instruction, the program uses Pyth prices directly to perform token swaps. No fee is charged if the tokens are not being swapped to/from USDC. This could be exploited with a MEV reordering attack.

An attacker would have the primitive to observe transactions before they are executed and also control the ordering of the transactions. Essentially, the attacker can control when the oracle update takes place and reorder the transactions to profit from the swap. The attacker can execute these swaps repeatedly and drain the protocol funds.

It can be seen in the code snippet below that Pyth prices are used directly for token swaps.

```rust
pub fn swap_fund_tokens(
    ctx: Context<SwapFundTokens>,
    [...]
    let from_token_value = usd_value(
        amount_to_swap,
        token_info.decimals[from_token_id as usize] as u64,
        *Price::load(&pyth_accounts[from_token_index]).unwrap(),
    );
    let mut to_amount = amount_from_usd_value(
        from_token_value,
        token_info.decimals[to_token_id as usize] as u64,
        *Price::load(&pyth_accounts[to_token_index]).unwrap(),
    );
    [...]
    transfer(ctx.accounts.into_transfer_from_fund_to_buyer_context(
        &[&seeds[..]]), to_amount)?;
```

## Proof of Concept

1. The attacker receives the transaction packets before they are processed by the validator.
2. If the Pyth oracle shows that token A appreciated in value relative to token B, the attacker can swap a lot of token B for token A.
3. The attacker reorders the transaction such that the oracle update takes place after the swap transaction.
4. The attacker then swaps token A back for token B at a profit.

## Remediation

Ideally, an additional protocol fee should be levied on the token swaps. This would prevent an attacker from profiting from small changes in the oracle price feed.

## Patch

Implemented a custom step price curve to get an output amount based on the size of the amount and use the reduced amount as a fee.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Symmetry |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.symmetry.fi/
- **GitHub**: https://github.com/symmetry-protocol/funds-program
- **Contest**: https://www.symmetry.fi/

### Keywords for Search

`vulnerability`

