---
# Core Classification
protocol: Abracadabra Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32063
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-abracadabra-money
source_link: https://code4rena.com/reports/2024-03-abracadabra-money
github_link: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/222

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

protocol_categories:
  - oracle
  - dexes
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - grearlake
  - Trust
  - AgileJune
  - Bigsam
---

## Vulnerability Title

[M-07] Permanent loss of yield for stakers in reward pools due to precision loss.

### Overview


This bug report discusses an issue with the LockingMultiRewards contract, which distributes rewards over a specific period of time. The problem arises from a calculation error where the amount is not properly wrapped before being divided, resulting in a loss of precision. This can lead to a significant loss of yield for stakers in reward pools, particularly for popular tokens like USDC and WBTC. The severity of this issue is considered high and it is recommended to store the reward rate in a different format to mitigate the risk. 

### Original Finding Content


The LockingMultiRewards contract facilitates distribution of rewards across the remaining epoch duration. The calculation for reward rate is provided below:
`reward.rewardRate = amount / _remainingRewardTime;`

The `rate` is later multiplied by the  duration to get the total rewards for elapsed time, demonstrated below:

    function rewardsForDuration(address rewardToken) external view returns (uint256) {
        return _rewardData[rewardToken].rewardRate * rewardsDuration;
    }

An issue occurs because there is no sufficient wrapping of the amount before dividing by `_remainingRewardTime`. The number is divided and later multiplied by elapsed time, causing a loss of precision of the amount modulo remaining time. For the provided period of `1 week` by the sponsor, the maximum amount lost can be calculated:
`7 * 24 * 3600 - 1 = 604799`.
Note that the average case loss is half of the worst case assuming even distribution across time. However since rewards are usually not sent at the low end of remaining time (see the `minRemainingTime` variable, the actual average would be higher).

The effect of this size of loss depends on the decimals and value of the reward token. For USDC, this would be $0.6. For WBTC,  it would be $423 (at time of writing). The loss is shared between all stakers relative to their stake amount. The loss occurs for every notification, so it is clear losses will be severe.

Sponsor remarked in the channel that reward tokens would be real, popular tokens. We believe USDC / WBTC on ARB are extremely popular tokens and therefore remain fully in scope as reward tokens.

### Severity Rationalization

Impact - high
Likelihood - medium
\-> Severity - high

### Impact

Permanent loss of yield for stakers in reward pools due to precision loss.

### Proof of Concept

*   Reward pool offers WBTC rewards
*   Epoch has just started,

### Recommended Mitigation Steps

Store the `rewardRate` scaled by 1e18, so loss of precision will be lower by magnitude of `1e18`.

**[0xCalibur (Abracadabra) disputed and commented via duplicate #166](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/166):**
>No factor.

**[Trust (Warden) commented](https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/222#issuecomment-2041019693):**
 > Hi,
> 
> The duplicate has been closed due to loss of "dust amounts". However I show in my submission that it is far from dust, I believe any submissions that have identified material loss of funds should be awarded appropriately.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Abracadabra Money |
| Report Date | N/A |
| Finders | grearlake, Trust, AgileJune, Bigsam |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-abracadabra-money
- **GitHub**: https://github.com/code-423n4/2024-03-abracadabra-money-findings/issues/222
- **Contest**: https://code4rena.com/reports/2024-03-abracadabra-money

### Keywords for Search

`vulnerability`

