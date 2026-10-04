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
solodit_id: 28107
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#3-double-check-of-the-_supports-variable
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

Double check of the `_supports` variable

### Overview

See description below for full details.

### Original Finding Content

##### Description
At line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L374-L380 there is a double check of variable `_supports`.

The assignment at line https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L380 can be moved inside the if-else statement to save gas. Additionally, the if-else statement is more readable than a ternary operator.

##### Recommendation
It is recommended to change to:
```solidity
if (_supports) {
    vote_.yea = vote_.yea.add(voterStake);
    vote_.voters[_voter] = VoterState.Yea;
} else {
    vote_.nay = vote_.nay.add(voterStake);
    vote_.voters[_voter] = VoterState.Nay;
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#3-double-check-of-the-_supports-variable
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

