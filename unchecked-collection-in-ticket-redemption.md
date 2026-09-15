---
# Core Classification
protocol: Frakt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48678
audit_firm: OtterSec
contest_link: https://frakt.xyz/
source_link: https://frakt.xyz/
github_link: github.com/frakt-solana/frakt-lending-protocol-

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
  - Harrison Green
  - Ethan Wu
  - OtterSec
  - William Wang
---

## Vulnerability Title

Unchecked collection in ticket redemption

### Overview


The report states that there is a bug in the redeemWinningLotTicket instruction, where the raffle winner can purchase NFT collateral from the protocol and transfer funds to the loan's liquidity pool without proper checks. This can allow an attacker to transfer funds to a different liquidity pool, resulting in the NFT collateral being cheaper than intended. The suggested solution is to verify that the provided liquidity pool and collection_info accounts match what is specified in the loan account. A patch has been provided to fix the bug.

### Original Finding Content

## Redeem Winning Lot Ticket Instruction

In the `redeemWinningLotTicket` instruction, the raffle winner purchases the NFT collateral from the protocol, transferring funds to the loan’s liquidity pool. However, this association between loan and liquidity pool is not checked. This allows an attacker who wins the liquidation raffle to transfer funds to a different liquidity pool. Depending on parameters, this can result in the NFT collateral being cheaper than intended.

## Code Snippet

```rust
instructions/redeem_winning_lot_ticket.rs
loan.reward_amount =
    convert_u128_to_u64(u128::from(liquidity_pool.borrow_cumulative)
        .checked_sub(u128::from(loan.reward_interest_rate.expect("no reward staked"))).unwrap()
        .checked_mul(u128::from(loan.amount_to_get)).unwrap()
        .checked_div(u128::from(PRICE_BASED_TIME_DENOMINATOR)).unwrap()
        .checked_div(u128::from(BASE_POINTS)).unwrap()).unwrap();
```

## Remediation

Verify that the provided `liquidity_pool` and `collection_info` accounts match what is specified in the loan account.

## Patch

```diff
@@ -26,7 +26,9 @@ pub struct RedeemWinningLotTicket<'info> {
 #[account(
 mut,
 constraint = loan.loan_status==LoanStatus::Liquidated @ ErrorCodes::LotIsNotLiquidatedYet,
 - has_one = nft_mint @ ErrorCodes::WrongNftMintOnLoan,
 + has_one = nft_mint @ ErrorCodes::WrongNftMintOnLoan,
 + has_one = liquidity_pool @ ErrorCodes::WrongLiqPoolOnLoan,
 + has_one = collection_info @ ErrorCodes::WrongCollectionInfoOnLoan,
 // constraint=loan.expired_at > now_ts()? || loan.loan_type == LoanType::PriceBased @ ErrorCodes::TimeIsNotExpired
 )]
```

© 2022 OtterSec LLC. All Rights Reserved. 7 / 25

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Frakt |
| Report Date | N/A |
| Finders | Harrison Green, Ethan Wu, OtterSec, William Wang |

### Source Links

- **Source**: https://frakt.xyz/
- **GitHub**: github.com/frakt-solana/frakt-lending-protocol-
- **Contest**: https://frakt.xyz/

### Keywords for Search

`vulnerability`

