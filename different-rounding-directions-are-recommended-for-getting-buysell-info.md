---
# Core Classification
protocol: Sudoswap
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18415
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-01-Sudoswap.md
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
  - rounding

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Hans
  - Alex Roan
  - 0kage
  - Giovanni Di Siena
---

## Vulnerability Title

Different rounding directions are recommended for getting buy/sell info

### Overview


This bug report is about the need for more implementation of different rounding directions for buy and sell operations in the AMM pools. In several `ICurve` implementations, the same rounding direction was applied for buy and sell operations, which does not align with the best practices for AMM pools. This may lead to financial loss for pair creators and negatively impact the platform's overall stability, especially for tokens with fewer decimals.

The recommended mitigation for this issue is to ensure that the buy price and protocol/trade fees are rounded up to prevent selling items at a lower price than desired and leaking value from the system. This issue has been fixed in the commit 902eee on the Sudoswap GitHub repository and has been verified by Cyfrin.

### Original Finding Content

**Description:**
This issue pertains to the need for more implementation of different rounding directions for buy and sell operations in the AMM pools.
In several `ICurve` implementations (`XykCurve`, `GDACurve`), the `ICurve::getBuyInfo` and `ICurve::getSellInfo` functions are implemented using the same rounding direction.
This does not align with the best practices for AMM pools, which dictate that different rounding directions should be applied for buy and sell operations to prevent potential issues. The problem becomes more significant for tokens with fewer decimals, resulting in larger pricing discrepancies.

Note that `ExponentialCurve` explicitly uses different rounding directions for buy and sell operations, which aligns with the best practices.

Additionally, across all curves, calculations of the protocol and trade fees currently do not round in favor of the protocol and fee recipients, which means that value may leak from the system in favor of the traders.

**Impact:**
The issue may result in financial loss for pair creators and negatively impact the platform's overall stability, especially for tokens with fewer decimals. We, therefore, rate the severity as MEDIUM.

**Recommended Mitigation:**
Ensure that the buy price and protocol/trade fees are rounded up to prevent selling items at a lower price than desired and leaking value from the system.

**Sudoswap:**
Fixed in [commit 902eee](https://github.com/sudoswap/lssvm2/commit/902eee37890af3953a55472d885bf6265b329434).

**Cyfrin:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Hans, Alex Roan, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-01-Sudoswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Rounding`

