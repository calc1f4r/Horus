---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28431
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Liquity%20Stability%20Pool/README.md#3-overreportion-of-the-losses
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
  - MixBytes
---

## Vulnerability Title

Overreportion of the losses

### Overview


This bug report describes an issue with the liquidatePosition function in which it may incorrectly report that all requested liquidity is lost even when no losses have actually been suffered. This can occur when the harvest() is called and can lead to major overreporting to the vault and break its accounting.

The recommended solution is to migrate to a "fixing" strategy, which will correct the issue, however the vault accounting will remain invalid until manual interaction of the vault governance and the vault shares will be underpriced. Therefore, it is recommended that the vault governance take steps to manually fix the overreporting issue in order to ensure that the vault shares are properly priced.

### Original Finding Content

##### Description
In some rare conditions the liquidatePosition may report that all requested liquidity is lost even if no losses are actually suffered. Such liquidation may occur during harvest() and do a major overreporting to the vault and break its accounting. As no losses are suffered actually, this state can be fixed by migrating to a "fixing" strategy. However, the vault accounting will be invalid until manual interaction of the vault governance, and the vault shares will be underpriced.

##### Recommendation
To fix overreporting

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Liquity%20Stability%20Pool/README.md#3-overreportion-of-the-losses
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

