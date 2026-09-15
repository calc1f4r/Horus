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
solodit_id: 28342
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#3-steth-can-be-paused
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

`stETH` can be paused

### Overview


This bug report is about the `stETH` contract, which can be paused and cause all transfers to revert. The report provides two links to the code, which shows that the contract can be paused at lines 57, 73 and 81. The recommendation is to add a check to the interface to ensure that transfers cannot be stopped. This check should require that the `stETH` contract is not stopped before allowing a transfer.

### Original Finding Content

##### Description
`stETH` can be paused, so all transfers would revert:
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L57
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L73
https://github.com/lidofinance/lido-dao/tree/ea6fa222004b88e6a24b566a51e5b56b0079272d/contracts/0.6.12/WstETH.sol#L81
##### Recommendation
We recommend to add the following check (for this check it is necessary to update interface):
```solidity=
require(!stETH.isStopped(), "wstETH: transfer stopped");
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/WstETH/README.md#3-steth-can-be-paused
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

