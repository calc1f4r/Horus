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
solodit_id: 28340
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#1-possible-incorrect-initialization
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

Possible incorrect initialization

### Overview


This bug report is about a function in a contract called `_stETH` which allows a zero address to be used. This is not desirable behavior and it is recommended that a check is added to the contract to ensure that a zero address cannot be used. The proposed check is `address(_stETH) != address(0), "wstETH: incorrect address");`. This check should be added to the contract in order to prevent the use of a zero address.

### Original Finding Content

##### Description
In the following function `_stETH` can be zero address:
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L39
##### Recommendation
We recommend to add the following check:
```solidity=
address(_stETH) != address(0), "wstETH: incorrect address");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#1-possible-incorrect-initialization
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

