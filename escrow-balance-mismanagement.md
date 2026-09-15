---
# Core Classification
protocol: Exponent Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46952
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Escrow Balance Mismanagement

### Overview


The report discusses a bug in the WithdrawLp instruction in exponent_core, which is used to transfer LP tokens from the market's escrow account to the user's destination account. However, the market's total amount of LP tokens held in escrow, called market.lp_escrow_amount, is not being updated (decremented) after the transfer. This can lead to issues with the distribution of emissions from the SY program and farms. The bug has been fixed in PR#710 and users are advised to ensure that market.lp_escrow_amount is properly decremented when withdrawing LP tokens.

### Original Finding Content

## WithdrawLp Instruction in Exponent Core

In the `WithdrawLp` instruction in `exponent_core`, `do_transfer_lp_out` transfers LP tokens from the market’s escrow account to the user’s destination account (`token_lp_dst`). However, the `market.lp_escrow_amount`, which represents the total amount of LP (Liquidity Provider) tokens held in escrow by the market, is not decremented after the withdrawal.

If `market.lp_escrow_amount` is not updated (decremented) after the transfer, the protocol will continue to consider the withdrawn tokens as part of the market’s liquidity pool. This will lead to improper distribution of emissions from the SY program and farms.

> _exponent_core/src/instructions/market_two/withdraw_lp.rs_
>
> ```rust
> /// Transfer LP tokens from escrow to dst
> fn do_transfer_lp_out(&self, amount: u64) -> Result<()> {
> #[allow(deprecated)]
> token_2022::transfer(
> self.transfer_lp_out_context()
> .with_signer(&[&self.market.signer_seeds()]),
> amount,
> )
> }
> ```

## Remediation

Ensure that `market.lp_escrow_amount` is decremented by the amount of LP tokens withdrawn.

## Patch

Fixed in PR#710.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Core |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

