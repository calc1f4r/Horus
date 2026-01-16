---
# Core Classification
protocol: Coinflip_2025-02-19
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55508
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
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

[M-05] User can frontrun `completeGame` to finalize stake or unstake request

### Overview


The report talks about a bug that allows users to cheat the staking system in a game called Flip. This bug is of medium impact and likelihood and can result in unfair gains for the user. The bug allows users to finalize their stake or unstake request before the game is completed, which can help them avoid big losses or participate in big wins. To prevent this, the report suggests implementing the following measures: 
1. Allowing other users to finalize a user's stake or unstake request to prevent unfair gains.
2. Defining a deadline for finalizing the transaction to prevent pending requests from being exploited.
3. Considering the minimum share price at the time of request and finalization to avoid manipulation.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Staking user can frontrun `Flip.completeGame()` and finalize his stake/unstake request (based on game result loss or win):

```solidity
    function finalizeUnstake(address token) external nonReentrant {
        UnstakeRequest memory request = unstakeRequests[token][msg.sender];
        uint256 sharesToRedeem = request.shares;
        require(sharesToRedeem > 0, "No unstake request found");
        require(block.timestamp >= request.requestTime + unstakeDelay, "Unstake delay not passed");
        --snipp--
    }
```

```solidity

    function finalizeStake(address token) external nonReentrant {
        StakeRequest memory request = stakeRequests[token][msg.sender];
        require(request.amount > 0, "No stake request found");
        require(block.timestamp >= request.requestTime + depositDelay, "Stake delay not passed");
        --snipp--
    }
```

As a result, the staking user can scape from big losses in the game or participate in big wins.

## Recommendations

To decrease the probability of this attack happening, consider the following:

1. **Let Others Finalize**: Allow other users to finalize a user’s stake or unstake request as they have incentives to prevent unfair gains by attackers.

2. **Window Time to Finalize**: Define a deadline for finalizing the transaction. After this deadline, any pending stake or unstake request should can be canceled.

3. **Minimum Share**: Consider using the minimum of share price between the time of request and the time of finalization.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-19 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-19.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

