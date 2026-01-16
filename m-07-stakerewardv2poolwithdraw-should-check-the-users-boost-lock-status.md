---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21152
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/773

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
  - validation

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - Co0nan
  - ke1caM
  - KupiaSec
  - DedOhWale
  - 0xkazim
---

## Vulnerability Title

[M-07] `stakerewardV2pool.withdraw()` should check the user's boost lock status.

### Overview


This bug report details an issue in the LybraFinance protocol which allows users to withdraw their staking token immediately after charging more rewards using boost, without locking their funds. This is due to a lack of logic in the `withdraw()` function which should prevent withdrawals during the boost lock. To demonstrate this, the report provides steps and code snippets to show how users can charge more rewards without locking their funds. The recommended mitigation step is to add a check to the `withdraw()` function which checks the boost lock duration before allowing withdrawals. LybraFinance acknowledged the issue and the judge decreased the severity to medium.

### Original Finding Content


Users can withdraw their staking token immediately after charging more rewards using boost.

### Proof of Concept

`withdraw()` should prevent withdrawals during the boost lock, but there is no such logic.

The below steps show how users can charge more rewards without locking their funds.

1.  Alice stakes their funds using [stake()](https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/miner/stakerewardV2pool.sol#L83).
2.  They set the longest lock duration to get the highest boost using [setLockStatus()](https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/miner/esLBRBoost.sol#L38).
3.  After that, when they want to withdraw their staking funds, they call [withdraw()](https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/miner/stakerewardV2pool.sol#L93).

```solidity
    function withdraw(uint256 _amount) external updateReward(msg.sender) {
        require(_amount > 0, "amount = 0");
        balanceOf[msg.sender] -= _amount;
        totalSupply -= _amount;
        stakingToken.transfer(msg.sender, _amount);
        emit WithdrawToken(msg.sender, _amount, block.timestamp);
    }
```

4.  Then, the highest boost factor will be applied to their rewards in [earned()](https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/miner/stakerewardV2pool.sol#L106) and they can withdraw all of their staking funds and rewards immediately without checking any lock duration.

```solidity
    // Calculates and returns the earned rewards for a user
    function earned(address _account) public view returns (uint256) {
        return ((balanceOf[_account] * getBoost(_account) * (rewardPerToken() - userRewardPerTokenPaid[_account])) / 1e38) + rewards[_account];
    }
```

### Tools Used

Manual Review

### Recommended Mitigation Steps

`withdraw()` should check the boost lock like this:

```solidity
    function withdraw(uint256 _amount) external updateReward(msg.sender) {
        require(block.timestamp >= esLBRBoost.getUnlockTime(msg.sender), "Your lock-in period has not ended.");

        require(_amount > 0, "amount = 0");
        balanceOf[msg.sender] -= _amount;
        totalSupply -= _amount;
        stakingToken.transfer(msg.sender, _amount);
        emit WithdrawToken(msg.sender, _amount, block.timestamp);
    }
```

### Assessed type

Invalid Validation

**[LybraFinance acknowledged](https://github.com/code-423n4/2023-06-lybra-findings/issues/773#issuecomment-1635523068)**

**[0xean (judge) decreased severity to Medium](https://github.com/code-423n4/2023-06-lybra-findings/issues/773#issuecomment-1655658314)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | Co0nan, ke1caM, KupiaSec, DedOhWale, 0xkazim, yudan, 0xRobocop, LaScaloneta, Toshii, Hama, Kenshin, Inspecktor |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/773
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`Validation`

