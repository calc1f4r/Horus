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
solodit_id: 28111
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#7-confusing-naming-can-lead-to-vulnerabilities-in-the-future-code-edits
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

Confusing naming can lead to vulnerabilities in the future code edits

### Overview

See description below for full details.

### Original Finding Content

##### Description

A voting passes two stages: 
1. Vote is open for yeas and nays
2. Vote is open for nays only

To check for those stages these methods are used:
1. `_isVoteOpen`, `_canVote`, `canVote`
2. `_isVoteOpenForObjection`, `_canObject`, `canObject`

Namings to check that the voting is in the first stage are confusing, because name `_isVoteOpen` doesn't clearly say that it is checking the first stage only and for the second stage of voting it will return `false`. The same thing refers to `canVote()` and `_canVote()`. Their names suggest that they should return `true` for any unfinished voting, while they return `true` only if the voting is in the first stage.

This confusion may lead to bugs in the future if the contract code base becomes larger and it will become harder to keep in mind that the behavior of some methods differs from what their name seems to imply.

There are already cases of the incorrect use of methods in the code:
https://github.com/lidofinance/aragon-apps/blob/7e5cd1961697a1bc514bfebdeab08a296e51d700/apps/voting/contracts/Voting.sol#L384
```solidity
function _vote(uint256 _voteId, bool _supports, address _voter) internal {
  ...
  if (!_isVoteOpen(vote_)) { // objection phase
  ...
  emit CastObjection(_voteId, _voter, voterStake);
}
```
It is obvious that instead of `!_isVoteOpen(vote_)` you should use `_isVoteOpenForObjection(vote_)`. It is not a vulnerability now because in the current context these two lines are interchangeble.

However, if in the future the development team decides to add another voting phase, they will have to find and fix all the lines with the incorrect use of methods and if the code base becomes large and the namings would be still confusing it will be easy to miss some line and create a vulnerability.


##### Recommendation

Change method names to be more clear about what they really do. For example, instead of `_isVoteOpen` you could use `_isVoteOpenFirstStage`. And instead of `_canVote` you could use `_canVoteFirstStage`.

The `canVote` method is a public method so it may be better to keep its name for API compatibility. But perhabs it should be marked as deprecated in the code comments and another,`canVoteFirstStage` method should be added.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Two-Phase%20Voting/README.md#7-confusing-naming-can-lead-to-vulnerabilities-in-the-future-code-edits
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

