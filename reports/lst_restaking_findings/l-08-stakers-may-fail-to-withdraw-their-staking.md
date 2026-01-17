---
# Core Classification
protocol: Kinetiq_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58630
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-08] Stakers may fail to withdraw their staking

### Overview

See description below for full details.

### Original Finding Content


In StakingManager, stakers can request withdraw their staking HYPE via `queueWithdrawal`.

When we queue withdrawal, we will un-delegate the related amount from the current validator. Based on current implementation, one staking manager can support multiple validators, and the owner can rebalance different validators' delegate amount according to actual conditions to earn the maximum profits.

The problem is that when users want to queue withdraw HYPE, they have to un-delegate from the current validator. It's possible that there is not enough delegated HYPE amount in this current validator.

For example:
1. The owner sets the validatorA as current validator via `setDelegation`.
2. Alice stakes 2000 HYPE and these 2000 HYPE will be delegated to the validator A.
3. The owner sets the validatorB to the current validator via `setDelegation`.
4. Alice wants to queue withdraw, we want to un-delegate 2000 HYPE from validatorB. This request will fail.

```solidity
    function queueWithdrawal(uint256 amount) external nonReentrant whenNotPaused {
        require(amount > 0, "Invalid amount");
        require(kHYPE.balanceOf(msg.sender) >= amount, "Insufficient kHYPE balance");

        uint256 withdrawalId = nextWithdrawalId[msg.sender];

        // Lock kHYPE tokens
        kHYPE.transferFrom(msg.sender, address(this), amount);
        _withdrawalRequests[msg.sender][withdrawalId] = WithdrawalRequest({amount: amount, timestamp: block.timestamp});

        nextWithdrawalId[msg.sender]++;
        totalQueuedWithdrawals += amount;
        address currentDelegation = validatorManager.getDelegation(address(this));
        require(currentDelegation != address(0), "No delegation set");

        _withdrawFromValidator(currentDelegation, amount);

        emit WithdrawalQueued(msg.sender, withdrawalId, amount);
    }

```

Recommendations: Allow uses to assign the validator that he want to queue withdraw.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kinetiq_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kinetiq-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

