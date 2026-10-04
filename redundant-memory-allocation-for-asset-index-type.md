---
# Core Classification
protocol: Pickle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28758
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Pickle%20Finance/Strategy-Curve-scrv-v4_1/README.md#1-redundant-memory-allocation-for-asset-index-type
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

Redundant memory allocation for asset index type

### Overview

See description below for full details.

### Original Finding Content

`getMostPremium()` function (in here: [strategy-curve-scrv-v4_1.sol#L81](https://github.com/pickle-finance/protocol/blob/master/src/strategies/curve/strategy-curve-scrv-v4_1.sol#L81)
returns tuple `(address, uint256)`, which
contains unnecessarily huge asset index type `uint256`. Since the function 
structure would require to update the contract anyway in case new stablecoins
would be added, there is no need in reserving index type sized for enormously 
huge amount of assets. 

Storing asset index in a type like `uint8` would be more appropriate for now.

*This issue was resolved with the following PR: https://github.com/pickle-finance/protocol/pull/6.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Pickle Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Pickle%20Finance/Strategy-Curve-scrv-v4_1/README.md#1-redundant-memory-allocation-for-asset-index-type
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

