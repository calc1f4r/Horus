---
# Core Classification
protocol: Kanpaipandas Lzapponft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45128
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/KanpaiPandas-LzAppONFT-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[H-01] Denial of Service Risk Due to Frozen `token_escrow` in `ONFT::Adapter`

### Overview


This bug report addresses a high-risk issue in the `init_ONft` instruction, where the `token_mint` is set without proper validation. This means that a `token_mint` with a `freeze_authority` can be initialized, which poses a risk to the functioning of the ONFT. If the `token_escrow` is frozen, it will be impossible to transfer the locked token to it, causing a Denial of Service (DoS) and rendering the ONFT unusable. The recommendation is to implement a check during initialization to prevent the use of tokens with freeze authority and display a warning to users. The team has fixed the issue.

### Original Finding Content

## Severity

High Risk

## Description

In the `init_ONft` instruction, the `token_mint` is set without validation, allowing the initialization of a `token_mint` with a `freeze_authority`. SPL tokens with a freeze authority can have their accounts frozen by the token issuer or an authorized entity, posing a risk to the functioning of the ONFT.

```rs
impl InitAdapterONft<'_> {
  pub fn apply(ctx: &mut Context<InitAdapterONft>, params: &InitAdapterONftParams) -> Result<()> {
      ctx.accounts.ONft_config.bump = ctx.bumps.ONft_config;
      ctx.accounts.ONft_config.token_mint = ctx.accounts.token_mint.key();
      ctx.accounts.ONft_config.ext = ONftConfigExt::Adapter(ctx.accounts.token_escrow.key());
      ctx.accounts.ONft_config.token_program = ctx.accounts.token_program.key();

      ctx.accounts.lz_receive_types_accounts.ONft_config = ctx.accounts.ONft_config.key();
      ctx.accounts.lz_receive_types_accounts.token_mint = ctx.accounts.token_mint.key();

      let oapp_signer = ctx.accounts.ONft_config.key();
      ctx.accounts.ONft_config.init(
          params.endpoint_program,
          params.admin,
          params.shared_decimals,
          ctx.accounts.token_mint.decimals,
          ctx.remaining_accounts,
          oapp_signer,
      )
```

## Impact

If the `token_escrow` is frozen, it will be impossible to transfer the locked token to it, causing a Denial of Service (DoS) in the `send` instruction. This will render the ONFT unusable because token transfers to the token_escrow will revert at this point:

```rs
 match &ctx.accounts.ONft_config.ext {
    ONftConfigExt::Adapter(_) => {
        if let Some(escrow_acc) = &mut ctx.accounts.token_escrow {
            // lock
            token_interface::transfer_checked(
                CpiContext::new(
                    ctx.accounts.token_program.to_account_info(),
                    TransferChecked {
                        from: ctx.accounts.token_source.to_account_info(),
                        mint: ctx.accounts.token_mint.to_account_info(),
                        to: escrow_acc.to_account_info(),
                        authority: ctx.accounts.signer.to_account_info(),
                    },
                ),
                amount_sent_ld,
                ctx.accounts.token_mint.decimals,
            )?;
        } else {
            return Err(ONftError::InvalidTokenEscrow.into());
        }
    },
```

## Recommendation

1. During ONFT initialization, check if the `token_mint` has a `freeze_authority` and return an error if detected.
2. If support for such tokens is necessary, display a warning on the UI to inform traders of the associated risks.
3. Keep in mind that major regulated stablecoins, such as USDC, have a `freeze_authority` for security reasons (e.g., preventing money laundering). If the protocol wishes to support USDC or similar tokens, implement an allowlist for trusted tokens while applying strict checks on others.

### Sample Implementation

Add this check in the `init_ONFT` function to the mint account to prevent using tokens with freeze authority:

```rs
if mint_account.freeze_authority.is_some() {
    return Err(Error::MintHasFreezeAuthority);
}
```

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Kanpaipandas Lzapponft |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/KanpaiPandas-LzAppONFT-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

