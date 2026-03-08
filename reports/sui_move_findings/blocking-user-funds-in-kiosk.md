---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48096
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Blocking User Funds In Kiosk

### Overview


The kiosk's extensions rely on the uid_mut function, but the current implementation may prevent its use by disabling extensions. This can cause users' funds to be locked when transferred to the extension. A solution is to create a fallback mechanism to improve the functionality of extensions. This issue has been resolved in a new version of the API.

### Original Finding Content

## Kiosk Extensions and uid_mut Functionality

The concept of the kiosk’s extensions heavily depends on utilizing the `uid_mut` function. However, the current implementation may disallow the use of this function by calling `set_allow_extensions` with `allow_extensions` set to `false`. This may result in the locking of users’ funds that were transferred to the extension.

## Code Snippet

```rust
/// Get the mutable `UID` for dynamic field access and extensions.
/// Aborts if `allow_extensions` set to `false`.
public fun uid_mut(self: &mut Kiosk): &mut UID {
    assert!(self.allow_extensions, EExtensionsDisabled);
    &mut self.id
}
```

## Remediation

Implement a fallback mechanism that enables the termination of the extensions to enhance their functionality.

## Patch

This API is now deprecated, and this issue no longer exists.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

