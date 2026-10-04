---
# Core Classification
protocol: EulerEarn_2025-07-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62177
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-04] Missing slippage and deadline protection exposes users to pricing risks

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The `EulerEarn` contract does not provide users with slippage protection or deadline enforcement in the `deposit()`, `mint()`, `withdraw()`, and `redeem()` functions. These functions interact with multiple ERC4626-compliant strategy vaults, and users’ assets may be distributed across or pulled from different strategy vaults based on available capacity.

Key concerns:

- **Slippage risk**: During deposits or mints, assets may be split across multiple strategy vaults with varying share prices. During withdrawals or redemptions, the strategy vaults are accessed in a fixed order, and varying liquidity or share price can cause users to receive fewer shares or assets than expected.

- **No deadline enforcement**: If transactions get stuck in the mempool (e.g., during high network congestion), users may be exposed to more significant price movements before execution, further increasing slippage risks.

This lack of user-defined controls exposes depositors and withdrawers to unfavorable outcomes due to timing and price variations in the underlying vaults.

Recommendation:  
Introduce parameters such as `minShares`(`maxShares`) and `minAssets` (`maxAssets`), along with an optional `deadline` field, to allow users to enforce minimum acceptable output and time bounds for their transactions.

### Euler comments

We acknowledge the finding, will keep as is.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | EulerEarn_2025-07-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

