---
# Core Classification
protocol: Nft Loots
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20618
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Two people might win the same prize

### Overview


This bug report is about an issue with the `NFTLootbox` game. The current way to decide if a player wins and what they win is the `getPrizeIndex` method, which has a flaw in that multiple people might draw a small `randomNumber` and get the same `prizeIndex` returned, resulting in them being able to claim the same reward. This is amplified by the fact that the `probabilities` array is not enforced to be sorted. This means there is a race condition for the first person to get an NFT's `prizeIndex`, as front-running can be used to get the ERC721 token from another winner even if you played later than him. Additionally, if it is a USD based prize, then it is possible that multiple people win it but it is not enforced that the contract has this balance, meaning some people lose their expected rewards. The impact of this bug is high, as people might not get their prizes, but the likelihood is low.

As a solution, it is recommended to enforce only 1 winner per `prizeIndex` and also to enforce the `probabilities` array to be sorted. This will ensure that only one person can win the same prize and that the probability of winning is properly distributed.

### Original Finding Content

**Impact:**
High, as people might not get their prizes

**Likelihood:**
Low, as it requires same `prizeIndex` wins

**Description**

The current way in `NFTLootbox` to decide if a player wins and what it wins is the `getPrizeIndex` method, which has the following implementation:

```solidity
uint256[] storage _probabilities = lootboxes[_lootboxId].probabilities;
uint256 sum;

// Calculate the cumulative sum of probabilities and find the winning prize
for (uint256 i; i < _probabilities.length; ++i) {
    sum += _probabilities[i];
    if (_randomNumber <= sum) {
        return i;
    }
}

// If no prize is won, return a missing prize index (100001)
return MAX_PROBABILITY + 1;
```

This shows that the smaller `randomNumber` you get, the bigger chance you have of winning. The flaw is that multiple people might draw a small `randomNumber` and get the same `prizeIndex` returned, resulting in them being able to claim the same reward. This is also amplified by the fact that the `probabilities` array is not enforced to be sorted - if the first values in the `probabilities` array are big then it is more possible that winners will get the same `prizeIndex` and prize.

While the game currently looks like it handles this, as multiple users can claim the same prize with the same `prizeIndex`, this shouldn't be the case, as it means there is a race condition for the first person to get an NFT's `prizeIndex`, because front-running can be used to get the ERC721 token from another winner even if you played later than him (given that you got the same `prizeIndex` win). Also, if it is a USD based prize, then it is possible that multiple people win it but it is not enforced that the contract has this balance. This can mean some people lose their expected rewards.

**Recommendations**

Enforce only 1 winner per `prizeIndex` and also enforce the `probabilities` array to be sorted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nft Loots |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

