---
# Core Classification
protocol: Argo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48532
audit_firm: OtterSec
contest_link: https://argo.fi/
source_link: https://argo.fi/
github_link: github.com/argodao/argo-move.

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Unify Health Checks

### Overview

See description below for full details.

### Original Finding Content

## Code Review: Unifying Collateral Ratio Checks in Argo

Argo currently uses a number of disjoint checks for each function that interacts with the collateral ratio.

### Existing Checks

In the `argo_engine/sources/engine_v1.move` file, we have the following checks:

```rust
assert!(
    withdraw_passes_initial_collateral_ratio_internal(engine, vault, amount),
    error::invalid_argument(ECOLLATERAL_RATIO_TOO_LOW),
);
```

```rust
assert!(
    mint_passes_minimum_debt_internal(engine, vault, amount),
    error::invalid_argument(EBELOW_MINIMUM_DEBT),
);
```

It would be cleaner to unify these checks by checking against the collateral ratio after the relevant operations.

### Proposed Patch

This issue has been resolved in commit `2c31c5c`. The new code in `argo_engine/sources/engine_v1.move` file is as follows:

```rust
// Check resulting debt is greater than the minimum debt and resulting
// collateral ratio is above the initial collateral ratio
assert!(
    scaled_debt_internal(engine, vault) >= engine.minimum_debt,
    error::invalid_argument(EBELOW_MINIMUM_DEBT),
);
``` 

This change consolidates the checks, making the codebase cleaner and easier to maintain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Argo |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://argo.fi/
- **GitHub**: github.com/argodao/argo-move.
- **Contest**: https://argo.fi/

### Keywords for Search

`vulnerability`

