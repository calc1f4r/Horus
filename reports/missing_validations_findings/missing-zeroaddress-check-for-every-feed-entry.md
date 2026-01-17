---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62683
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#13-missing-zeroaddress-check-for-every-feed-entry
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

Missing Zero‑Address Check for Every Feed Entry

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the constructor of the `ChainlinkCompositeOracleProvider` contract. 

Only the first feed is validated:
```solidity
if (i == 0 && address(_configs[i].feed) == address(0)) revert InvalidFeed();
```
Subsequent feeds can be the zero address, causing `latestRoundData()` to revert at runtime.
##### Recommendation
We recommend validating every feed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#13-missing-zeroaddress-check-for-every-feed-entry
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

