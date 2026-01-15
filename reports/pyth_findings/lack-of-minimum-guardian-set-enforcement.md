---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54006
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
github_link: none

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
finders_count: 3
finders:
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Lack of minimum guardian set enforcement 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Summary

## Context
- **File Locations**: 
  - `engine.rs` (Lines 367-369)
  - `users.rs` (Lines 70-74)

## Description
The current implementation of `set_guardian_set` only checks if the guardian set is non-empty. This check is insufficient as it allows for a guardian set with just one guardian.

```rust
pub(crate) fn set_guardian_set(&mut self, gs: pyth::GuardianSet) -> Result<(), Error> {
    ensure!(!gs.addresses.is_empty(), Error::PythGuardianSetInvalid);
    self.guardian_set = Some(gs);
    Ok(())
}
```

## Recommendation
Implement a minimum threshold for the number of guardians in the set.

## LayerN
Fixed in PR 860 and PR 1060.

## Cantina Managed
Fixed. The `set_guardian_set` function now requires a minimum of 3 different guardians.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

