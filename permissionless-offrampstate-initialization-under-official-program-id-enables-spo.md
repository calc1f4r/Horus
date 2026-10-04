---
# Core Classification
protocol: Securitize Solana Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64312
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
github_link: none

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
finders_count: 4
finders:
  - Alex Roan
  - Naman
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Permissionless OffRampState initialization under official program ID enables spoofed “official” instances

### Overview


This bug report discusses a vulnerability in the `initialize` instruction of the `OffRampState` program. This instruction allows any signer to create a new `OffRampState` and become its `admin`. However, the global `OffRampCounter` is not properly guarded, meaning that anyone can create a new state under the same Program ID and present it as an official Securitize off ramp. This can lead to potential scams and fraudulent activities. To mitigate this issue, the report recommends adding a `GlobalConfig` PDA with an `authorized_initializer` or allowlist, and requiring the `admin` signer to be on that list during initialization. The bug has been fixed by Securitize in their latest commit and verified by Cyfrin.

### Original Finding Content

**Description:** The `initialize` instruction lets any signer create a new `OffRampState` and become its `admin`. The global `OffRampCounter` is `init_if_needed` and unguarded, and the new state PDA is derived from `[OFF_RAMP_STATE_SEED, off_ramp_counter.counter.to_le_bytes()]`. There is no allowlist or registry check tying the initializer to an official Securitize operator.
This means anyone can spin up an OffRamp instance under the same Program ID and emit an `Initialized` event, which can be marketed as if it were an official, Securitize backed off ramp.
```rust
/// Global counter for generating unique off-ramp IDs
#[account(
    init_if_needed,
    payer = admin,
    space = 8 + OffRampCounter::INIT_SPACE,
    seeds = [OFF_RAMP_COUNTER_SEED],
    bump,
)]
pub off_ramp_counter: Box<Account<'info, OffRampCounter>>,

/// Off-ramp state containing configuration and settings
#[account(
    init,
    payer = admin,
    space = 8 + OffRampState::INIT_SPACE,
    seeds = [OFF_RAMP_STATE_SEED, off_ramp_counter.counter.to_le_bytes().as_ref()],
    bump,
)]
pub off_ramp_state: Box<Account<'info, OffRampState>>,
```

**Impact:** A third party can deploy a look alike instance with arbitrary fees, NAV provider, and recipient policy, then present it as “the Securitize off ramp” because it is hosted under the same Program ID.


**Recommended Mitigation:** Add a `GlobalConfig` PDA that stores an `authorized_initializer` or allowlist. In `initialize`, require the `admin` signer to be on that list.

**Securitize:** Fixed in [30362cf](https://github.com/securitize-io/bc-solana-redemption-sc/commit/30362cf3d6b349cad72134f843808464d7477502).

**Cyfrin:** Verified.


\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Solana Redemption |
| Report Date | N/A |
| Finders | Alex Roan, Naman, Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

