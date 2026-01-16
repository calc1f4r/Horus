---
# Core Classification
protocol: Light Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47069
audit_firm: OtterSec
contest_link: https://lightprotocol.com/
source_link: https://lightprotocol.com/
github_link: https://github.com/Lightprotocol

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
  - Tuyết Dương
---

## Vulnerability Title

Utilization of Incorrect Authority for Token Transfers

### Overview


The report discusses a bug in the code for transferring SPL tokens from a specified token account to a token pool account. The function responsible for this transfer, "compress_spl_tokens," uses "cpi_authority_pda" as the authority for the transfer instead of the expected "ctx.accounts.authority." This allows an attacker to set up both the token_pool_pda and the compress_or_decompress_token_account to point to the same token account and effectively steal tokens from the pool. The recommended solution is to ensure that "ctx.accounts.authority" is used as the authority for token transfers. This bug has been resolved in version 043e22a.

### Original Finding Content

## SPL Compression Vulnerability

`compress_spl_tokens` is intended to transfer SPL tokens from a specified token account (`compress_or_decompress_token_account`) to a token pool account (`token_pool_pda`) to compress tokens. In the function, transfer is called with `cpi_authority_pda` as the authority for the token transfer. This implies that `cpi_authority_pda` is utilized to authorize the transfer instead of `ctx.accounts.authority`, which is typically expected to be the signer or authority responsible for the action.

> _compressed-token/src/spl_compression.rs_

```rust
pub fn compress_spl_tokens<'info>(
    inputs: &CompressedTokenInstructionDataTransfer,
    ctx: &Context<'_, '_, '_, 'info, TransferInstruction<'info>>,
) -> Result<()> {
    [...]
    transfer(
        &ctx.accounts
            .compress_or_decompress_token_account
            .as_ref()
            .unwrap()
            .to_account_info(),
        &recipient,
        &ctx.accounts.cpi_authority_pda.to_account_info(),
        [...]
    )
}
```

The attacker may set up both the `token_pool_pda` and the `compress_or_decompress_token_account` to point to the same token account by creating a token account and utilizing it as both the source and destination for the transfer. Since `cpi_authority_pda` is utilized as the authority, the attacker may authorize the transfer even if it is a self-transfer. With tokens effectively self-transferred to a pool account, the attacker may then decompress the tokens. Since the attacker controls both accounts involved in the transfer, they may effectively steal tokens from the pool.

## Remediation

Ensure that `ctx.accounts.authority` is utilized as the authority for token transfers rather than `cpi_authority_pda`. This ensures that only authorized signers may approve transfers.

© 2024 Otter Audits LLC. All Rights Reserved. 11/53  
Light Protocol Audit 04 — Vulnerabilities  
Patch  
Resolved in 043e22a.

© 2024 Otter Audits LLC. All Rights Reserved. 12/53

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Light Protocol |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://lightprotocol.com/
- **GitHub**: https://github.com/Lightprotocol
- **Contest**: https://lightprotocol.com/

### Keywords for Search

`vulnerability`

