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
solodit_id: 28329
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#3-function-parameter-not-used
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

Function parameter not used

### Overview


The bug report states that in the Voting contract, the canForward() function has two parameters, but the second parameter has no name and is not used anywhere. The second parameter is called `evmCallScript` in the IForwarder interface and should be delegated to the `_sender` address to execute the script. However, the function in the Voting contract does not modify any data, but only outputs a boolean value with the result of checking the rights to create new votes for the address. Therefore, it is recommended to remove the second variable for the canForward() function.

### Original Finding Content

##### Description
At the line 
https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L211, the `canForward()` function has 2 parameters. But the second parameter has no name and is not used anywhere.
In the `IForwarder` interface, the second parameter is called `evmCallScript`.
Thus, in a function from the interface, control must be delegated to the `_sender` address to execute the script.
But in fact, in the `Voting` contract, this function does not modify the data, but only outputs a boolean value with the result of checking the rights to create new votes for the address.
The second variable is not needed in the `Voting` contract.

##### Recommendation
It is recommended to remove the second variable for the `canForward()` function.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#3-function-parameter-not-used
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

