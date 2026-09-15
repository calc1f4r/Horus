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
solodit_id: 28328
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#2-no-variable-check-in-initialize-function
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

No variable check in initialize function

### Overview


This bug report describes an issue with the smart contract for a voting app on the Ethereum blockchain. The issue is that the `token` variable is not checked in the `initialize()` function, meaning that if the address value of `token` is equal to zero when the `initialize()` function is executed, the smart contract will need to be reinstalled. To solve this issue, it is recommended to add a check.

### Original Finding Content

##### Description
There is no check of the variable in the initialize function at the line
- https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L87.
The `token` variable is initialized in only one place.
If the value of the address variable `token` is equal to zero when the `initialize()` function is executed, then this smart contract will have to be reinstalled.

##### Recommendation
It is recommended to add a check.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#2-no-variable-check-in-initialize-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

