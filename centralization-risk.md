---
# Core Classification
protocol: Solayer Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47342
audit_firm: OtterSec
contest_link: https://solayer.org/
source_link: https://solayer.org/
github_link: https://github.com/solayer-labs/restaking-program

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - Robert Chen
---

## Vulnerability Title

Centralization Risk

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability in Token Initialization

In `initialize`, if the `rst_mint` account provided for initialization already possesses a non-zero supply of tokens, it introduces a potential vulnerability. The admin may mint additional tokens to the `rst_mint` account before transferring authority to control the minting process, artificially increasing the token supply.

```rust
// restaking-program/src/contexts/initialize.rs
pub fn initialize(&mut self, bumps: InitializeBumps) -> Result<()> {
    self.pool.set_inner(RestakingPool {
        lst_mint: self.lst_mint.key(),
        rst_mint: self.rst_mint.key(),
        bump: bumps.pool
    });
    Ok(())
}
```

Consequently, the admin may transfer authority to control the minting process to another account while retaining a significant portion of the tokens. This allows the admin to manipulate the market by selling off the inflated tokens for profit, devaluing other users' assets.

## Remediation

Ensure that the `rst_mint` account provided for initialization has a zero supply of tokens before proceeding with the initializaiton process. This pre-condition helps prevent the risk of token inflation.

## Patch

Fixed in `9401126` by ensuring the supply of `rst_mint` in `initialize`.

© 2024 Otter Audits LLC. All Rights Reserved. 7/9

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solayer Labs |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://solayer.org/
- **GitHub**: https://github.com/solayer-labs/restaking-program
- **Contest**: https://solayer.org/

### Keywords for Search

`vulnerability`

