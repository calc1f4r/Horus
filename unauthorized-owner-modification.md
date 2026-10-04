---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46802
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
finders_count: 2
finders:
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Unauthorized Owner Modification

### Overview


The Adrena protocol allows unauthorized actors to potentially manipulate locked stakes. The "finalize_locked_stake" and "finalize_lock_campaign" instructions are meant to be called only by the authorized Sablier worker program identified by "sablier_sdk::ID". However, the current implementation only checks the caller's owner address to be "sablier_sdk::ID", which can be exploited by an attacker. They can create a new account and change the owner to "sablier_sdk::ID", allowing them to appear as the Sablier worker program and prematurely finalize stakes belonging to other users. This can affect their rewards and potentially lock them out of their stake until manual intervention. To fix this, it is suggested to use a Program Derived Address (PDA) for the authorized Sablier worker account instead of solely relying on the owner address. This issue has been resolved in #124.

### Original Finding Content

## Security Protocol Overview

The protocol allows unauthorized actors to potentially manipulate locked stakes. The `finalize_locked_stake` and `finalize_lock_campaign` instructions are designed to be called only by the authorized Sablier worker program identified by `sablier_sdk::ID`. This ensures proper control and prevents unintended modifications to user stakes. The current implementation relies solely on checking the caller’s owner address to be `sablier_sdk::ID`.

## Code Example

```rust
/// admin/pool/finalize_genesis_lock_campaign.rs
pub fn finalize_genesis_lock_campaign<'info>(
    ctx: Context<'_, '_, '_, 'info, FinalizeGenesisLockCampaign<'info>>,
) -> Result<()> {
    // Sablier worker needs to be the one to call the ix
    require!(
        ctx.accounts.caller.owner.eq(&sablier_sdk::ID),
        AdrenaError::InvalidCaller
    );
    [...]
}
```

## Potential Exploit

An attacker may exploit this by creating a new account (`attacker_account`), and utilizing the `solana_program::system_instruction::assign` instruction to change the owner of `attacker_account` to `sablier_sdk::ID`. This manipulation allows the attacker's account to appear as the Sablier worker program to the Adrena protocol. Consequently, they may finalize stakes belonging to other users prematurely, impacting their rewards and potentially locking them out of their stake until manual intervention. They may also finalize lock campaigns before their intended completion, affecting the overall liquidity and functionality of the Adrena protocol.

## Remediation

Instead of relying solely on the owner address, consider utilizing a Program Derived Address (PDA) for the authorized Sablier worker account.

## Patch

Resolved in #124.

---

© 2024 Otter Audits LLC. All Rights Reserved. 35 / 59

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

