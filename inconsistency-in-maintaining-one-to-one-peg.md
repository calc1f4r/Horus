---
# Core Classification
protocol: Thala LSD + Deps
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53239
audit_firm: OtterSec
contest_link: https://www.thala.fi/
source_link: https://www.thala.fi/
github_link: https://github.com/ThalaLabs/thala-modules

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
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Inconsistency in Maintaining One-to-One Peg

### Overview

See description below for full details.

### Original Finding Content

## Risks in Staking with thAPT

In staking, `burn_from_thapt` and `reconcile` introduce risks that may break the intended 1:1 peg between thAPT and staked APT. thAPT is meant to be pegged 1:1 to staked APT, representing a claim on the underlying collateral. However, by burning thAPT, the total supply decreases while the underlying APT remains unchanged.

## Code Snippet

```rust
// Source: thala_lsd/sources/staking.move
public entry fun burn_from_thapt(manager: &signer, account_address: address, amount: u64)
,→ acquires TLSD {
    assert!(manager::is_authorized(manager), ERR_TLSD_UNAUTHORIZED);
    coin::burn_from(account_address, amount,
    ,→ &borrow_global<TLSD>(package::resource_account_address()).thAPT_burn_capability)
}

public entry fun reconcile(manager: &signer, amount: u64) acquires TLSD {
    assert!(manager::is_authorized(manager), ERR_TLSD_UNAUTHORIZED);
    let minted = coin::mint(amount,
    ,→ &borrow_global<TLSD>(package::resource_account_address()).thAPT_mint_capability);
    coin::deposit(signer::address_of(manager), minted)
}
```

While this may be mitigated via `reconcile`, which allows the authorized manager to mint new thAPT tokens, excessive minting may inflate the supply of thAPT, breaking the peg in the opposite direction (more thAPT in circulation than staked APT), giving rise to a similar problem.

## Remediation

Introduce checks to ensure the total thAPT supply always matches the total staked APT.

### Patch

Fixed in `5ba884a`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala LSD + Deps |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://www.thala.fi/
- **GitHub**: https://github.com/ThalaLabs/thala-modules
- **Contest**: https://www.thala.fi/

### Keywords for Search

`vulnerability`

