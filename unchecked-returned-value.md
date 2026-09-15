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
solodit_id: 28343
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#4-unchecked-returned-value
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

Unchecked returned value

### Overview


This bug report is about the Lido DAO contract, specifically the WstETH.sol file. The issue is that the returned value for `transfer` and `transferFrom` functions is not being checked. This means that if either of these functions fail, there is no indication of this to the user. To fix this, it is recommended to add a check to the code that will provide an error message if either of the functions fail.

### Original Finding Content

##### Description
Returned value for `transfer`, `transferFrom` not checked:
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L57
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L73
##### Recommendation
We recommend to add a check like this:
```solidity=
require(stETH.transferFrom(msg.sender, address(this), _stETHAmount), "wstETH: transfer fails");
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#4-unchecked-returned-value
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

