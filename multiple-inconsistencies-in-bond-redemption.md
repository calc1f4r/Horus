---
# Core Classification
protocol: Etherfuse Stablebond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46998
audit_firm: OtterSec
contest_link: https://www.etherfuse.com/
source_link: https://www.etherfuse.com/
github_link: https://github.com/etherfuse/stablebond

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

Multiple Inconsistencies In Bond Redemption

### Overview


The bug report states that there is a problem with how the user's bond token accounts are managed and closed in the bond::process_redeem_bond function. The cross-program invocation (CPI) call to NftIssuanceVault::close_user_token_account does not specify which token account should be closed, and the if statement intended to check the balance of the user's token account is actually checking the balance of the payment token account. Additionally, there is no use of the close_nft_token_account function and no verification of the payment_mint_account_info using the PaymentFeed. The suggested solution is to move the bond token account closing to the request_redeem function and ensure all accounts are included in the CPI call and that the payment_mint_account_info is verified using the PaymentFeed. This issue has been resolved in patch #104.

### Original Finding Content

## Logical Flaw in Bond Token Account Management

There is a logical flaw in the way the user’s bond token accounts are managed and closed in `bond::process_redeem_bond`. The cross-program invocation (CPI) call to `NftIssuanceVault::close_user_token_account` utilizes `user_wallet_account_info` and `mint_account_info` but does not provide the specific token account that should be closed. 

Also, `user_token_account` is unpacked from `user_payment_token_account_info`, which implies that the `if user_token_account.amount == 0` condition (intended to check if the user’s token account balance is zero to determine if it should be closed) is checking the balance of the payment token account rather than the bond token account.

> _src/processor/bond.rs rust_
```rust
pub fn process_redeem_bond(_program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    [...]
    // Close user's bond token account if they don't have anymore
    {
        let user_token_account =
            Token2022Account::unpack_from_slice(&user_payment_token_account_info.data.borrow())?;
        msg!("User Token Account Amount: {}", user_token_account.amount);
        if user_token_account.amount == 0 {
            invoke(
                &NftIssuanceVault::close_user_token_account(
                    user_wallet_account_info.key,
                    mint_account_info.key,
                ),
                &[
                    user_wallet_account_info.clone(),
                    token_2022_program_info.clone(),
                ],
            )?;
        }
    }
    [...]
}
```

Furthermore, there is an absence of utilization of the `close_nft_token_account` in the `process_redeem_bond` instruction and a lack of verification of the `payment_mint_account_info` using the `PaymentFeed`. Without verification, there is no guarantee that the `payment_mint_account_info` provided by the user corresponds to the expected token mint.

## Remediation

Move the bond token account closing to the `request_redeem` instruction, as the closing of accounts should typically occur when a user’s position or holding in that asset is fully redeemed or withdrawn, not at the point of processing the redemption. 

Also, ensure the correctness of checks and that all accounts are included within the CPI call, and verify the `payment_mint_account_info` using the `PaymentFeed`.

## Patch

Resolved in #104.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Etherfuse Stablebond |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.etherfuse.com/
- **GitHub**: https://github.com/etherfuse/stablebond
- **Contest**: https://www.etherfuse.com/

### Keywords for Search

`vulnerability`

