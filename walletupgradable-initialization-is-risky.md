---
# Core Classification
protocol: CloudWalk
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27984
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/CloudWalk/README.md#1-walletupgradable-initialization-is-risky
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

`WalletUpgradable` initialization is risky

### Overview


This bug report is about an upgradable wallet that requires multiple steps to initialize. The current process includes having an external admin transfer proxy ownership to the wallet in order to finalize initialization. It is recommended that the same factory-pattern for wallets be applied to guarantee correct finalized initialization. Another solution is to use UUPSUpgradeable with the correct setting _authorizeUpgrade() method via onlySelfCall.

### Original Finding Content

##### Description

The current initialization of an upgradable wallet includes multiple steps, where a wallet proxy is owned by some external admin. The admin has to transfer proxy ownership directly to the wallet to finalize the initialization.

##### Recommendation

We recommend applying the same factory-pattern for wallets as well in order to guarantee correct finalized initialization.

Also one of the solutions is to use `UUPSUpgradeable` with the correct setting `_authorizeUpgrade()` method via `onlySelfCall`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | CloudWalk |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/CloudWalk/README.md#1-walletupgradable-initialization-is-risky
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

