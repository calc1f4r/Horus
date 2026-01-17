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
solodit_id: 27736
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Plugins/README.md#2-missing-flags-validation-in-new-pluginconfig
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

Missing flags validation in new `pluginConfig`

### Overview


A bug has been identified in the new `pluginConfig` set with `AlgebraPool.setPluginConfig()` which has no validation of flags. This can lead to the invocation of hooks that will constantly revert, such as `BEFORE_FLASH_FLAG`, `AFTER_FLASH_FLAG`, and `AFTER_SWAP_FLAG` (without currently connected incentive). This bug has a medium severity, as it can partially or fully stop the pool until the `pluginConfig` is corrected. It is recommended that all interaction with `pluginConfig` is moved to the plugin contract, and that any modification of `pluginConfig` should consider the current version and state of the plugin.

### Original Finding Content

##### Description
There is no validation of flags in new `pluginConfig` set with `AlgebraPool.setPluginConfig()`. This can lead to the invocation of hooks that will constantly revert. E.g. `BEFORE_FLASH_FLAG`, `AFTER_FLASH_FLAG`,  `AFTER_SWAP_FLAG` (without currently connected incentive) can be switched on.
This issue has a MEDIUM severity since it can partially or fully stop the pool until `pluginConfig` is corrected.

##### Recommendation
We recommend moving all interaction with `pluginConfig` to the plugin contract. Any modification of `pluginConfig` should consider the current version and state of the plugin.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Algebra Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Plugins/README.md#2-missing-flags-validation-in-new-pluginconfig
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

