---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41247
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#25-unnecessary-inheritance
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
  - MixBytes
---

## Vulnerability Title

Unnecessary Inheritance

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [`CSFeeOracle` contract](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSFeeOracle.sol#L17). `CSFeeOracle` contract inherits both from `AssetRecoverer` contract and `IAssetRecovererLib` interface, but `AssetRecoverer` contract already implements `IAssetRecovererLib` and there is no need for `CSFeeOracle` to follow the same interface.

##### Recommendation
We recommend removing unnecessary inheritance from the `IAssetRecovererLib` interface.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#25-unnecessary-inheritance
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

