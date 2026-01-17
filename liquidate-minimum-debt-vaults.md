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
solodit_id: 48529
audit_firm: OtterSec
contest_link: https://argo.fi/
source_link: https://argo.fi/
github_link: github.com/argodao/argo-move.

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Liquidate Minimum Debt Vaults

### Overview


The bug report discusses an issue with Argo's liquidation process for repaying vaults. The problem is that the system enforces a minimum debt threshold, but also requires that the collateral ratio of the vault is not fully repaid. This means that vaults with low debt cannot be liquidated. The bug has been resolved in a recent patch.

### Original Finding Content

## Argo Minimum Debt Threshold and Collateral Ratio Check

Argo enforces a minimum debt threshold when repaying vaults. Unfortunately, `liquidate_repay` also enforces that the collateral ratio of the vault isn’t repaid fully.

## Code Snippet (RUST)

```rust
let collateral_ratio = collateral_ratio_internal(engine, vault);
assert!(
    collateral_ratio < engine.liquidation_collateral_ratio,
    error::invalid_argument(ELIQUIDATE_TOO_MUCH),
);
```

This means that vaults that are close to the minimum debt threshold cannot be liquidated.

## Remediation

Rework the minimum collateral ratio check.

### Patch

Resolved in commit `2c31c5c`.

## Code Snippet (RUST)

```rust
let collateral_ratio = collateral_ratio(
    coin::value(&vault.collateral),
    max(scaled_debt_internal(engine, vault), engine.minimum_debt),
    safe::price(engine.safe_addr),
    coin::decimals<CoinType>(),
);
assert!(
    collateral_ratio < engine.liquidation_collateral_ratio,
    error::invalid_argument(ELIQUIDATE_TOO_MUCH),
);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

