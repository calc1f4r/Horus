---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27187
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Guardian Audits
---

## Vulnerability Title

LIQH-2 | Incorrect Blocks For Liquidation

### Overview


This bug report is about a problem with the `processLiquidation` function in the GMX platform. The `marketDecrease` order that is created for liquidation does not get touched, so the `updatedAtBlock` is always 0. This makes it impossible to execute a liquidation with the correct block number for oracle prices. Furthermore, the `oracleBlockNumber` requirements for a `MarketDecrease` order stipulate that the prices come from the block in which the order was updated at, which is impossible as the block has not yet been confirmed. 

The recommendation was to resolve the contradiction in block numbers for liquidations and `MarketDecrease` orders, and to make sure to call `touch()` on the order when creating it in the `processLiquidation` function. The GMX Team implemented this recommendation, and the bug is now resolved.

### Original Finding Content

**Description**

In `processLiquidation`, the `marketDecrease` order that is created for liquidation does not get touched, therefore the `updatedAtBlock` is always 0.

Therefore it is impossible to execute a liquidation with the correct block number for oracle prices and by extension impossible to liquidate any position.

Furthermore, the `oracleBlockNumber` requirements for a `MarketDecrease` order stipulate that the prices come from the block in which the order was updated at. This would demand that the oracle provide finalized prices for the block in which the liquidation transaction is to be executed, which is impossible as the block has not yet been confirmed.

**Recommendation**

Resolve the contradiction in block numbers for liquidations and `MarketDecrease` orders. Additionally, make sure to call `touch()` on the order when creating it in the `processLiquidation` function.

**Resolution**

GMX Team: The recommendation was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

