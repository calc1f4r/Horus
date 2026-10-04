---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45603
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
  - Zokyo
---

## Vulnerability Title

Insufficient Liquidity Removal Protection in reduceLiquidity Function

### Overview


This bug report describes a critical issue in the MMTrade contract that could potentially be exploited by users. The function responsible for reducing liquidity does not properly track individual user contributions, which could allow users to remove more liquidity than they have actually added. This could affect the overall balance of the liquidity pool and lead to unintended behavior. The recommendation is to implement individual user liquidity tracking to prevent this issue and maintain the integrity of the pool.

### Original Finding Content

**Severity** : Critical 

**Status**: Invalid

**Description**

The reduceLiquidity function in the MMTrade contract contains a logic flaw that can lead to potential abuse and unintended behavior. The function checks if the last time liquidity was added by the caller is at least mimTime (4 days) ago. However, this check is based on the lastAdded timestamp which is updated whenever liquidity is added. There is no mechanism to prevent users from removing liquidity that they themselves did not add, leading to possible exploitation.

**Scenario** : 

User A adds a significant amount of liquidity and updates their lastAdded timestamp.
User B, who previously added liquidity but did not wait the required time, waits for the mimTime (4 days) to pass.
After mimTime passes, User B can remove liquidity, potentially more than they contributed, affecting the overall pool balance.

**Recommendation** 

Implement individual user liquidity tracking to ensure that users can only remove the liquidity they have personally contributed, preventing potential exploitation and maintaining the integrity of the liquidity pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

