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
solodit_id: 28109
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#5-gas-optimization-using-vote_yea
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

Gas optimization using `vote_.yea`

### Overview

See description below for full details.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L433-L440 it is possible to save gas by reading `vote_.yea` into a memory variable.

##### Recommendation
For example:
```solidity
uint256 voteYea = vote_.yea;
uint256 totalVotes = voteYea.add(vote_.nay);
if (!_isValuePct(voteYea, totalVotes, vote_.supportRequiredPct)) {
    return false;
}
// Has min quorum?
if (!_isValuePct(voteYea, vote_.votingPower, vote_.minAcceptQuorumPct)) {
    return false;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#5-gas-optimization-using-vote_yea
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

