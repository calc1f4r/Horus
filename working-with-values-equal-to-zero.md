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
solodit_id: 28341
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#2-working-with-values-equal-to-zero
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

Working with values equal to zero

### Overview


This bug report is about the potential for `wstETHAmount` or `stETHAmount` to be zero. This bug was found in the code for the Lido-Dao project, which is hosted on GitHub. It is recommended that a check be added to the code, requiring that `wstETHAmount` be greater than zero, with an error message of "wstETH: stETH return 0 shares" if this requirement is not met. This check should help to prevent the issue of `wstETHAmount` or `stETHAmount` being zero.

### Original Finding Content

##### Description
`wstETHAmount` or `stETHAmount` potentially can be zero:
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L56
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L73
##### Recommendation
We recommend to add the following check:
```solidity=
require(wstETHAmount > 0, "wstETH: stETH return 0 shares");
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#2-working-with-values-equal-to-zero
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

