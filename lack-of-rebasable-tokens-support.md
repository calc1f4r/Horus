---
# Core Classification
protocol: XPress
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56843
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/XPress/OnchainCLOB/README.md#4-lack-of-rebasable-tokens-support
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Lack of rebasable tokens support

### Overview


The report describes a problem with the `LOB` contract, which is used for rebasable tokens (tokens that adjust their supply over time). The issue is that during a rebase (a change in supply), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This can lead to situations where users who attempt to withdraw their tokens may not receive their full share because the contract's actual balance is less than the recorded balances. To fix this, the contract should be updated to dynamically adjust internal records based on the current total supply and the contract's actual balance.

### Original Finding Content

##### Description
The issue is identified in the [`LOB`](https://github.com/longgammalabs/hanji-contracts/blob/09b6188e028650b9c1758010846080c5f8c80f8e/src/OnchainLOB.sol) contract.

For rebasable tokens, such as those that adjust their supply over time (e.g., Ampleforth), the LOB contract may keep all rewards in the contract balance. During a rebase (positive or negative), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This discrepancy can lead to scenarios where, after a negative rebase (slashing), the remaining users attempting to withdraw may not be able to receive their full share of assets because the contract’s actual balance is less than the sum of the recorded balances.

##### Recommendation
To handle rebasable tokens properly, the contract should dynamically adjust internal records to reflect rebases. This can be done by recalculating balances based on the current total supply and the contract's actual balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | XPress |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/XPress/OnchainCLOB/README.md#4-lack-of-rebasable-tokens-support
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

