---
# Core Classification
protocol: Ajna Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20083
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-ajna
source_link: https://code4rena.com/reports/2023-05-ajna
github_link: https://github.com/code-423n4/2023-05-ajna-findings/issues/373

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
finders_count: 3
finders:
  - patitonar
  - troublor
  - bytes032
---

## Vulnerability Title

[M-04] Potential unfair distribution of Rewards due to MEV in `updateBucketExchangeRatesAndClaim`

### Overview


This bug report is about a vulnerability in the reward system of a protocol that allows malicious actors to exploit the system by frontrunning transactions and unfairly claiming rewards, thereby disincentivizing honest users from updating the bucket exchange rates and contributing to the system. 

The `updateBucketExchangeRatesAndClaim` function is publicly callable and serves two main purposes: updating the exchange rate of a list of buckets and, if eligible, the caller can claim 5% of the rewards accumulated to each bucket since the last burn event. This function is vulnerable to MEV (Miner Extractable Value) exploitation, meaning that malicious actors can use bots to frontrun any transactions submitted by honest users, preventing them from claiming the rewards.

Two potential solutions have been suggested to mitigate this vulnerability. The first one is to introduce a randomized reward mechanism, such as a lottery system or a probabilistic reward distribution for people who contribute to updating buckets, to reduce the predictability of rewards and hence the potential for MEV exploitation. The second solution is to limit the reward claim process to users who have staked in the rewards manager, and couple it with a rate-limitting mechanism by implementing a maximum claim per address per time period. 

The bug report has been acknowledged, and the team is currently looking into the possible solutions.

### Original Finding Content


This vulnerability allows malicious actors to exploit the reward system by frontrunning transactions and unfairly claiming rewards, thereby disincentivizing honest users from updating the bucket exchange rates and contributing to the system.

### Proof of Concept

The `updateBucketExchangeRatesAndClaim` function is publicly callable and serves two main purposes:

1.  Updates the exchange rate of a list of buckets.
2.  If eligible, the caller can claim `5%` of the rewards accumulated to each bucket since the last burn event, if it hasn't already been updated.

<https://github.com/code-423n4/2023-05-ajna/blob/fc70fb9d05b13aee2b44be2cb652478535a90edd/ajna-core/src/RewardsManager.sol#L310-L318>

```solidity
function updateBucketExchangeRatesAndClaim(
        address pool_,
        uint256[] calldata indexes_
    ) external override returns (uint256 updateReward) {
        updateReward = _updateBucketExchangeRates(pool_, indexes_);

        // transfer rewards to sender
        _transferAjnaRewards(updateReward);
    }

```

So, to summarize it's primary purpose is to incentivize people who keep the state updated. However, given the nature of the function (first come, first serve) it becomes very prone to MEV.

Consider the following scenario:

1.  Alice is hard-working, non-technical and constantly keeps track of when to update the buckets so she can claim a small reward. Unfortunately, she becomes notorious for getting most of the rewards from updating the bucket exchange rate.
2.  A malicious actor spots Alice's recent gains and creates a bot to front run **any** transactions to RewardsManager's `_updateBucketExchangeRateAndCalculateRewards`submitted by Alice.
3.  The day after that, Alice again see's theres a small reward to claim, attempts to claim it, but she gets front runned by whoever set the bot.
4.  Since Alice is non-technical, she cannot ever beat the bot so she is left with a broken heart and no longer able to claim rewards.

I believe the system should be made fair to everybody that wants to contribute, hence this is a vulnerability that should be taken care of to ensure the fair distribution of awards to people who care about the protocol instead of .

### Recommended Mitigation Steps

I see potentially two solutions here:

1.  Introduce a randomized reward mechanism, such as a lottery system or a probabilistic reward distribution for people who contribute to updating buckets. This could reduce the predictability of rewards and hence the potential for MEV exploitation.
2.  Consider limiting the reward claim process to users who have staked in the rewards manager because they are the individuals that are directly affected if the bucket is not updated, because if its not updated for 14 days they won't be getting rewards. Additionally, you can couple it with a rate-limitting mechanism by implementing a maximum claim per address per time period

**[MikeHathaway (Ajna) acknowledged](https://github.com/code-423n4/2023-05-ajna-findings/issues/373#issuecomment-1571025508)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ajna Protocol |
| Report Date | N/A |
| Finders | patitonar, troublor, bytes032 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-ajna
- **GitHub**: https://github.com/code-423n4/2023-05-ajna-findings/issues/373
- **Contest**: https://code4rena.com/reports/2023-05-ajna

### Keywords for Search

`vulnerability`

