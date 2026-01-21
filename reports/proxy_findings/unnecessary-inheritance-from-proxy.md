---
# Core Classification
protocol: Gearbox Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30793
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.1/README.md#3-unnecessary-inheritance-from-proxy
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

Unnecessary inheritance from `Proxy`

### Overview


The report states that there is a bug in the `yVault` functions that are called from the proxy. This is because the storage is not the same, which is causing the functions to not work properly. The recommendation is to remove the inheritance from the `Proxy` in order to fix the bug.

### Original Finding Content

##### Description
All functions for `yVault` called from proxy wouldn't work because the storage is not the same:
https://github.com/Gearbox-protocol/gearbox-contracts/blob/0ac33ba87212ce056ac6b6357ad74161d417158a/contracts/integrations/yearn/YearnPriceFeed.sol#L17
##### Recommendation
We recommend removing inheritance from `Proxy`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Gearbox Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.1/README.md#3-unnecessary-inheritance-from-proxy
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

