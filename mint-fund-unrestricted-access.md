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
solodit_id: 48606
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

Mint Fund Unrestricted Access

### Overview


The report states that there is a bug in the mint_fund instruction that allows anyone to mint a BuyState, which can result in a buyer being forced to pay a high slippage of 3%. This can happen if the BuyState is not rebalanced within 180 seconds or if the cron job fails to run. The attacker can also manipulate the funds and force the buyer to pay the high slippage. The bug has been fixed in the latest patch.

### Original Finding Content

## Vulnerability in mint_fund Instruction

It was found that the `mint_fund` instruction can be invoked by anyone to mint a `BuyState`. This would mean that a buyer can be forced to pay a high slippage of **3%** if someone mints the `BuyState` before it is rebalanced.

In the code snippet below, it can be seen that the program allows the minting of a `BuyState` if its lifetime is greater than **180 seconds** or **90%** of the funds have been used. If a user doesn’t rebalance the `BuyState` or the cron job fails to run within this period, then the `mint_fund` instruction can be invoked and the buyer would be forced to pay the high slippage. The attacker can also rebalance only **90%** of the funds and mint before the **180 second** period to force the user to pay the highest slippage on the remaining funds.

## Code Snippet

```rust
pub const BUY_STATE_LIFETIME: u64 = 3 * 60;
pub const BUY_STATE_REMAINING_AMOUNT_DENOMENATOR: u64 = 10;
// [...]
pub struct MintFund<'info> {
// [...]
    pub token_info: AccountLoader<'info, TokenInfo>,
    #[account(
        mut,
        has_one = buyer_fund_token_account,
        constraint = buy_state.fund == fund_state.key(),
        constraint = buy_state.buyer == buyer.key(),
        constraint = (
            (buy_state.creation_timestamp + BUY_STATE_LIFETIME <
             (Clock::get()?.unix_timestamp) as u64) ||
            (buy_state.usdc_contributed /
            BUY_STATE_REMAINING_AMOUNT_DENOMENATOR >
            buy_state.usdc_left)
        ),
        close = buyer
    )]
    pub buy_state: Box<Account<'info, BuyState>>,
}
```

## Proof of Concept

1. Buyer invokes the `buy_state` instruction to buy a fund.
2. The attacker can use the `buy_state_rebalance` instruction to rebalance the `BuyState` such that only **90%** of the funds are spent.
3. The `mint_fund` instruction can then be invoked and the buyer is forced to pay a high **3%** slippage on the remaining funds.

## Remediation

Access to the `mint_fund` instruction should be limited. Ideally, to the buyer and the backend service.

## Patch

Resolved in commit **6bde2b9**.

© 2022 OtterSec LLC. All Rights Reserved.

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

