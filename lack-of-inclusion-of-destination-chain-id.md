---
# Core Classification
protocol: Mayan Solana
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53221
audit_firm: OtterSec
contest_link: https://mayan.finance/
source_link: https://mayan.finance/
github_link: https://github.com/mayan-finance/anchor

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Lack of Inclusion of Destination Chain ID

### Overview


The bug report discusses a vulnerability in the SwiftSourceSolanaState account, where the seeds are incorrectly defined in some instructions. This leads to the omission of the destination chain ID, which can cause the instruction execution to fail. To fix this issue, the destination chain ID needs to be included in all instructions that require SwiftSourceSolanaState seeds. This bug has been resolved in the b0729c8 patch. 

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns incorrectly defined seeds in the state account. The seeds of the `SwiftSourceSolanaState` are incorrectly set in some instructions.

## Details

In the **Refund** instruction, the seeds for the state account in the context and `state_seeds` defined in `handle_refund` do not contain the emitter chain ID. As it stands, the seeds only incorporate `SwiftSourceSolanaState::SEED_PREFIX` and the hash of the order, without the destination chain ID.

> **Code Reference:** `programs/swift/src/processor/refund.rs`
> 
> ```rust
> #[derive(Accounts)]
> pub struct Refund<'info> {
>     [...]
>     #[account(
>         mut,
>         seeds = [
>             SwiftSourceSolanaState::SEED_PREFIX,
>             CancelMessage::parse_unchecked(VaaAccount::load_unchecked(&vaa_cancel)
>                 .payload().into()).hash().as_ref(),
>         ],
>         [...]
>     )]
>     pub state: Box<Account<'info, SwiftSourceSolanaState>>,
>     [...]
> }
> ```

Similarly, in the **InitOrder** instruction, the derived signer seeds (stored in `state_signer_seeds`) lack the destination chain ID. Without the destination chain ID, the instruction execution might fail.

## Remediation

Include the destination chain ID in all the instructions that require `SwiftSourceSolanaState` seeds (both in **InitOrder** and **Refund** instructions).

## Patch

Resolved in `b0729c8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mayan Solana |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://mayan.finance/
- **GitHub**: https://github.com/mayan-finance/anchor
- **Contest**: https://mayan.finance/

### Keywords for Search

`vulnerability`

