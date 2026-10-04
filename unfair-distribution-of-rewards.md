---
# Core Classification
protocol: Retro/Thena Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33074
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/retro-thena-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Unfair Distribution of Rewards

### Overview


The VoterV3 contract has a function called `_notifyRewardAmount` which allows people to contribute to the rewards for the next voting period. However, there is a bug in this function where the rewards are distributed based on the current number of votes, rather than at the end of the voting period. This means that someone could contribute a large amount of rewards and receive all of them back if they are the only voter, even though they did not contribute anything meaningful. To fix this, the function should be changed to distribute rewards at the end of the voting period. This bug has been resolved in a recent update to the contract.

### Original Finding Content

In the `VoterV3` contract, the [`_notifyRewardAmount`](https://github.com/ThenafiBNB/THENA-Contracts/blob/e5458ee4ea811788576585af7a56c02986d16122/contracts/VoterV3.sol#L703) function allows individuals to contribute to the next epoch's total rewards.


Reward distribution is calculated by directly increasing the [`index`](https://github.com/ThenafiBNB/THENA-Contracts/blob/e5458ee4ea811788576585af7a56c02986d16122/contracts/VoterV3.sol#L708-L710) parameter. During an [`_updateFor`](https://github.com/ThenafiBNB/THENA-Contracts/blob/e5458ee4ea811788576585af7a56c02986d16122/contracts/VoterV3.sol#L810) call, which is called every time a vote is cast to a gauge, the rewards are allocated to the gauges when [`claimable`](https://github.com/ThenafiBNB/THENA-Contracts/blob/e5458ee4ea811788576585af7a56c02986d16122/contracts/VoterV3.sol#L823) is updated. Since `_updateFor` calculates the rewards [based off of the current number of votes](https://github.com/ThenafiBNB/THENA-Contracts/blob/e5458ee4ea811788576585af7a56c02986d16122/contracts/VoterV3.sol#L812-L813), the reward will be distributed in proportion to the snapshot of votes in the system when the funds were contributed.


This does not follow the rest of the protocol's calculations, where voters are given rewards at the end of the voting epoch and the votes' distribution is final. Additionally, this could lead to bizarre contributions where a user can contribute a large sum of rewards, but be the only voter in the epoch, resulting in all of the contributed funds being directed to them, signaling a large contribution but really not contributing anything.


In order to match other accounting done in the system and avoid the distribution of rewards based on intermediate voting state, consider changing the `_notifyRewardAmount` to distribute rewards at the end of the epoch rather than during one.


***Update:** Resolved in [pull request #4](https://github.com/ThenafiBNB/THENA-Contracts/pull/4) at commit [8f108fd](https://github.com/ThenafiBNB/THENA-Contracts/pull/4/commits/8f108fdf1fcb141c531c3195d965a1ee17abe1bd). `_notifyRewardAmount` has been completely removed.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Retro/Thena Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/retro-thena-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

