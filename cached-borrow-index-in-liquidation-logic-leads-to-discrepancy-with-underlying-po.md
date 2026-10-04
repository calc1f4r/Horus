---
# Core Classification
protocol: Evoq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45926
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
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
  - Zokyo
---

## Vulnerability Title

Cached Borrow Index in Liquidation Logic Leads to Discrepancy with Underlying Pool

### Overview


This bug report discusses an issue with the _isLiquidatable function in EvoqUtils, which is used to calculate user debt. The function uses cached borrow indexes that may become outdated over time, causing inconsistencies with the liquidation mechanics of the underlying pool. This can make it difficult for liquidators to execute liquidations and reduces the effectiveness of the process. The recommendation is to update the cached indexes more frequently to align with real-time data. The client also notes that this issue may not affect normal use cases.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged 

**Description**:

The _isLiquidatable function in EvoqUtils uses cached borrow indexes (lastPoolIndexes[_poolToken].lastBorrowPoolIndex) to calculate user debt. These indexes are updated only during interactions with the market but may become outdated over time. As a result:
Users who are liquidatable on the underlying pool may not be flagged as liquidatable in Evoq.
Liquidators must first interact with the market (e.g., supply, borrow, or repay) to update the cached indexes before executing liquidations, adding friction to the process.
This discrepancy introduces inconsistency with the liquidation mechanics of the underlying pool (e.g. Venus) and reduces the efficacy of liquidators.

**Recommendation**:

Ensure that _isLiquidatable explicitly calls _updateP2PIndexes for all user-entered markets to align with real-time data.
implement an off-chain or on-chain mechanism to periodically update lastPoolIndexes for all markets to minimize reliance on liquidator-triggered updates.

**Client comment**: 

Under normal use case, this does not pose any issue. _isLiquidatable function is always called after updateP2PIndexes in the contract logic.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Evoq |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

