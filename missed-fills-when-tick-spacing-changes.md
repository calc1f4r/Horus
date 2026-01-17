---
# Core Classification
protocol: Algebra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57979
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Limit%20Order%20Plugin/README.md#1-missed-fills-when-tick-spacing-changes
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missed Fills When Tick-Spacing Changes

### Overview


The report describes a bug in the LimitOrderManager function, which uses a value called tickLowerLasts to calculate lower and upper boundaries for swaps. However, if the pool's tick-spacing is changed, the stored tickLowerLast value no longer aligns with the new grid and can cause open positions to be skipped. This can result in loss of user funds and trading errors. The recommendation is to reset tickLowerLasts on every tick-spacing change to avoid this issue. The client suggests that dexes using this function should notify users to close their positions when the tick-spacing changes to prevent any potential risks.

### Original Finding Content

##### Description
`LimitOrderManager._getCrossedTicks()` relies on `tickLowerLasts[pool]`, a value recorded under the previous tick-spacing. If governance changes a pool’s tick-spacing (e.g., from 10 to 20), the stored `tickLowerLast` no longer aligns with the new grid. When the next swap occurs, the function calculates `lower` and `upper` from mismatched bases, causing any open positions between the old and new boundaries to be skipped and never filled. 

This directly affects user funds and trading logic, warranting **Medium** severity.
<br/>
##### Recommendation
We recommend resetting `tickLowerLasts[pool]` to `getTickLower(getTick(pool), newTickSpacing)` on every tick-spacing change so the correct boundary is retrieved after an update.

> **Client's Commentary:**
> Commit: https://github.com/cryptoalgebra/plugins-monorepo/commit/b1adba18438bebd5e0267cebcd39039aada125cb. Tickspacing changes are rare (usually before limit order plugin is used) and do not pose a risk to user funds. However, we believe that dexes using this plugin should notify users to close their positions when the tickspacing changes

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Algebra Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Limit%20Order%20Plugin/README.md#1-missed-fills-when-tick-spacing-changes
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

