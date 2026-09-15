---
# Core Classification
protocol: KittenSwap_2025-06-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58211
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-06-12.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Voters' rewards may be manipulated

### Overview


This bug report is about a problem in a voter contract where voters can earn rewards based on their voting weight. The issue is that the voting power of veTokens (tokens used for voting) decreases over time, and malicious users can take advantage of this by using a function called `poke` to update their voting weight near the end of a voting period. This can result in users receiving fewer rewards than expected, especially if their veToken has a longer locking period. The recommendation is to fix the `poke` function to prevent this manipulation.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

In voter contract, voters vote for different gauges. Voters can gain some rewards from the rebaseReward and votingReward contract according to the actual voting weight. If the voting weight is higher, the voter may gain more rewards.

The problem here is that veToken's voting power will decrease over time. When the voter finishes voting at the start of the new voting period. Malicious users can trigger `poke` function when we are near to the end of the voting period to update voting weight. Then users may get fewer rewards than expected.

When one veToken has one long locking period, voting power may not decrease too much in 7 days. However, if one veToken's locking period is expired in one month, malicious users can cause that users may lose 1/3 or 1/2 of rewards in this reward epoch period.

```solidity
    function _vote(
        uint256 _tokenId,
        address[] memory _poolVote,
        uint256[] memory _weights
    ) internal {
        IVotingReward(votingReward[_gauge])._deposit(
            uint256(_poolWeight),
            _tokenId
        );
        rebaseReward._deposit(uint256(_poolWeight), _tokenId);
    }
    function poke(uint256 _tokenId) external {
        address[] memory _poolVote = poolVote[_tokenId];
        uint256 _poolCnt = _poolVote.length;
        uint256[] memory _weights = new uint256[](_poolCnt);

        for (uint256 i = 0; i < _poolCnt; i++) {
            _weights[i] = votes[_tokenId][_poolVote[i]];
        }

        _vote(_tokenId, _poolVote, _weights);
    }
```

## Recommendations

`poke` function aims to help users to update their voting power. The problem here is that if the voter has already voted, malicious users can still poke to manipulate the reward a little bit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | KittenSwap_2025-06-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/KittenSwap-security-review_2025-06-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

