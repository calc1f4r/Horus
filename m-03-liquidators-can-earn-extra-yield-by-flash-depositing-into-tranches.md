---
# Core Classification
protocol: Arcadia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31495
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Liquidators can earn extra yield by flash depositing into tranches

### Overview


**Severity**: Medium

**Impact**: Liquidity providers may not receive liquidation yields

**Likelihood**: Medium, only applicable in certain situations

**Description**: The liquidation penalty, which is meant to reward liquidity providers, can be taken by liquidators without any additional cost. This is because the liquidation penalty is given at a specific moment, allowing users to deposit a large amount into a tranche pool, collect the yield, and then withdraw the funds to pay off a flash loan. Liquidators can also take advantage of this by depositing and withdrawing in the same transaction, making it a profitable attack for them. This issue affects all unlocked tranches, and can be carried out on any chain without the need for frontrunning.

**Recommendations**: To prevent this issue, deposits and withdrawals in the same transaction or block should be forbidden.

### Original Finding Content

**Severity**

**Impact**: Medium, Liquidation yields can be denied to liquidity providers

**Likelihood**: Medium, Not applicable in current deployment configuration, but valid in general

**Description**

The `liquidationPenalty` part of the liquidation incentives is dealt out to the tranches as extra yield according to their weights via the `_syncLiquidationFeeToLiquidityProviders` function. This increases the amount corresponding to each tranch share. The issue is that liquidators can snipe this extra yield at no extra cost via flash deposits.

During liquidations, only the juinor-most tranche is locked, while other tranches are open and can be deposited into. The `liquidationPenalty` is given at an instant of time, thus users can theoretically deposit a very large amount to these tranche pools, collect the yield, and then withdraw it all out and pay off the flash loan.

However, the liquidators themselves can do this at no cost. So when a liquidator sees a profitable liquidation position, they can flash deposit into the tranches in the very same transaction, carry out the liquidation, and collect the termination fee, a large part of the liquidation penalty, and any discounts on the collateral price. This is a very profitable attack, and can be carried out by any liquidator.

This affects all the unlocked tranches, i.e. all except the junior-most tranche. This attack requires no frontrunning, so can be executed on all chains, irrespective of the visibility of transactions. Yield from liquidations can be denied to liquidity providers at no extra cost for the attacker.

**Recommendations**

Forbid deposits and withdrawals to a tranche in the same transaction / block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Arcadia |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

