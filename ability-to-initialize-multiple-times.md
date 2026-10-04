---
# Core Classification
protocol: ComposableFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47366
audit_firm: OtterSec
contest_link: https://www.picasso.network/
source_link: https://www.picasso.network/
github_link: https://github.com/ComposableFi/emulated-light-client

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
finders_count: 2
finders:
  - Ajay Shankar Kunapareddy
  - Akash Gurugunti
---

## Vulnerability Title

Ability To Initialize Multiple Times

### Overview


This bug report discusses an issue with the Initialize instruction in a staking program. Due to the use of init_if_needed, the staking parameters can be altered multiple times by anyone, potentially leading to security vulnerabilities. The report suggests using init instead of init_if_needed to ensure that initialization can only happen once. The issue has been fixed by using init instead of init_if_needed in the code.

### Original Finding Content

## Potential Security Vulnerabilities in Initialize Instruction

In the Initialize instruction, while initializing the staking parameters, due to the use of `init_if_needed`, the staking parameters may be altered with new values multiple times by anyone. The ability to initialize the staking parameters multiple times may result in security vulnerabilities. For example, an attacker may repeatedly call the Initialize instruction with different parameters, altering the staking configuration and affecting the entire protocol.

> _restaking/programs/restaking/src/lib.rs_

## Code Example

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub admin: Signer<'info>,
    #[account(init_if_needed, payer = admin, seeds = [STAKING_PARAMS_SEED, TEST_SEED], bump, space = 1024)]
    pub staking_params: Account<'info, StakingParams>,
    pub rewards_token_mint: Account<'info, Mint>,
    #[account(init_if_needed, payer = admin, seeds = [REWARDS_SEED, TEST_SEED], bump, token::mint = rewards_token_mint, token::authority = staking_params)]
    pub rewards_token_account: Account<'info, TokenAccount>,
    [...]
}
```

## Remediation

Use `init` instead of `init_if_needed` for the Initialize instruction. This ensures that the initialization can only happen once.

## Patch

Fixed by using `init` instead of `init_if_needed` for Initialize in e565006.

© 2024 Otter Audits LLC. All Rights Reserved. 6/20

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | ComposableFi |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Akash Gurugunti |

### Source Links

- **Source**: https://www.picasso.network/
- **GitHub**: https://github.com/ComposableFi/emulated-light-client
- **Contest**: https://www.picasso.network/

### Keywords for Search

`vulnerability`

