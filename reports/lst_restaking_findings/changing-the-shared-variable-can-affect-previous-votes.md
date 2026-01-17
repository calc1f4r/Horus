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
solodit_id: 28326
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#1-changing-the-shared-variable-can-affect-previous-votes
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

Changing the shared variable can affect previous votes

### Overview


The bug report describes an issue with the `unsafelyChangeVoteTime()` method in the `Voting.sol` file. This method allows for the changing of the `voteTime` variable, which affects the voting results of existing votes. This action is potentially dangerous and may cause unexpected side effects. It is recommended to save the value of the variable `voteTime` in the structure `Vote` in the same way as for the `supportRequiredPct` and `minAcceptQuorumPct` variables. This will help to ensure that the voting results are not affected by unexpected changes to the `voteTime` variable.

### Original Finding Content

##### Description
At the lines 
https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L126-L133 in the `unsafelyChangeVoteTime()` method is a change in the common for all voting variable `voteTime`.
Changing this variable will extend or shorten the voting time on existing voting.
This will affect the voting results, because the process will not go as planned when creating a vote.
So this action is potentially dangerous and may bring the unexpected side effects.

##### Recommendation
It is recommended to save the value of the variable `voteTime` in the structure `Vote`. 
This will be done in the same way as for the `supportRequiredPct` and `minAcceptQuorumPct` variables.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#1-changing-the-shared-variable-can-affect-previous-votes
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

