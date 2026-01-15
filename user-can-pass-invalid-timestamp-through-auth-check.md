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
solodit_id: 54007
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

User can pass invalid timestamp through auth check 

### Overview

See description below for full details.

### Original Finding Content

## Context: auth.rs#L131

## Description
The `i64::abs` function, given `i64::MIN`, will crash or return `i64::MIN` depending on compilation settings. A user can observe the current likely node timestamp through a side channel (observing the Pyth feed) or even get it publicly served from an operator if they expose such facts about the current state of the rollup (which would be sensible) or simply guess at likely current timestamp values and spam insignificant transactions based on them, to obtain a timestamp value which is `i64::MIN + store.timestamp()` at the time of processing.

This will either cause a panic and kill the thread (in dev mode) or result in the transaction passing authorization. In the case of passing authorization, the error will be caught by the engine performing an `abs_diff` check, so it will not go through. However, it may be worth respecting the invariant that only transactions with reasonable timestamps get through the authorization check.

## Recommendation
Use `abs_diff()` to perform difference calculations:
```rust
if decoded_action.timestamp.abs_diff(last_timestamp) > engine::Genesis::ACTION_TIMESTAMP_STALE_THRESHOLD as u64
```

## LayerN
Fixed in PR 925.

## Cantina Managed
Fixed. `abs_diff` is now used as recommended.

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

