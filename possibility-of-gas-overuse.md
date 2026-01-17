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
solodit_id: 28330
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#4-possibility-of-gas-overuse
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

Possibility of gas overuse

### Overview


The bug report describes an issue with the lines of code found at https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L331-L341. The issue is that if a voter previously voted 'yea' and then votes 'yea' again, or previously voted 'nay' and then votes 'nay' again, the vote_.yea variable is calculated twice. This means that the vote is decreased and then increased, which is not the desired behavior. 

The recommendation is to add a check to see if the voter's previous vote is the same as their current vote. This will ensure that the vote is not calculated twice, and that the desired behavior is achieved.

### Original Finding Content

##### Description
At the lines
 https://github.com/lidofinance/aragon-apps/blob/8c46da8704d0011c42ece2896dbf4aeee069b84a/apps/voting/contracts/Voting.sol#L331-L341
if `voter` previosly voted `yea` and now voting `yea` again `vote_.yea` calculates twice: first it decreases and then it increases.
And the same case occurs if `voter` previosly voted `nay` and now voting `nay`.

##### Recommendation
It is recommended to add checking if `voter` previosly vote equals his curent vote.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Aragon%20Voting/README.md#4-possibility-of-gas-overuse
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

