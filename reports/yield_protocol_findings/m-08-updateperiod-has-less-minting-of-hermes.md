---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26077
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/737

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
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - chaduke
---

## Vulnerability Title

[M-08] `updatePeriod()` has less minting of `HERMES`

### Overview


A bug report has been filed, which states that if a `weekly` emission has not been taken, it may result in an insufficient minting of `HERMES`. This is due to the current balance of the contract being compared to `_required` without taking into consideration the `weekly` that has not yet been taken. The bug has been assessed as Medium, as rare edge cases are still in-scope for this severity level, and theoretical monetary loss is involved.

The code of the function `updatePeriod()` has been provided, which will first determine if the balance of the current contract is less than `_required`. If it is less, then mint new `HERMES`, so that there will be enough `HERMES` for the distribution.

The recommended mitigation steps are to modify the code, so that the current balance of the contract is compared with `weekly + _growth + share` instead of `_required`. This will ensure that the last `weekly` `HERMES` is taken into consideration, and that enough `HERMES` will be minted for the distribution.

### Original Finding Content


If there is a `weekly` that has not been taken, it may result in an insufficient minting of `HERMES`.

### Proof of Concept

In `updatePeriod()`, mint new `HERMES` every week with a certain percentage of `weeklyEmission`.

The code is as follows:

```solidity
    function updatePeriod() public returns (uint256) {
        uint256 _period = activePeriod;
        // only trigger if new week
        if (block.timestamp >= _period + week && initializer == address(0)) {
            _period = (block.timestamp / week) * week;
            activePeriod = _period;
            uint256 newWeeklyEmission = weeklyEmission();
@>          weekly += newWeeklyEmission;
            uint256 _circulatingSupply = circulatingSupply();

            uint256 _growth = calculateGrowth(newWeeklyEmission);
            uint256 _required = _growth + newWeeklyEmission;
            /// @dev share of newWeeklyEmission emissions sent to DAO.
            uint256 share = (_required * daoShare) / base;
            _required += share;
            uint256 _balanceOf = underlying.balanceOf(address(this));          
@>          if (_balanceOf < _required) {
                HERMES(underlying).mint(address(this), _required - _balanceOf);
            }

            underlying.safeTransfer(address(vault), _growth);

            if (dao != address(0)) underlying.safeTransfer(dao, share);

            emit Mint(msg.sender, newWeeklyEmission, _circulatingSupply, _growth, share);

            /// @dev queue rewards for the cycle, anyone can call if fails
            ///      queueRewardsForCycle will call this function but won't enter
            ///      here because activePeriod was updated
            try flywheelGaugeRewards.queueRewardsForCycle() {} catch {}
        }
        return _period;
    }
```

The above code will first determine if the balance of the current contract is less than `_required`. If it is less, then mint new `HERMES`, so that there will be enough `HERMES` for the distribution.

But there is a problem. The current balance of the contract may contain the last `weekly` `HERMES`, that  `flywheelGaugeRewards` has not yet taken (e.g. last week's allocation of `weeklyEmission`).

Because the `gaugeCycle` of `flywheelGaugeRewards` may be greater than one week, it is possible that the last `weekly` `HERMES` has not yet been taken.

So we can't use the current balance to compare with `_required` directly, we need to consider the `weekly` staying in the contract if it hasn't been taken, to avoid not having enough balance when `flywheelGaugeRewards` comes to take `weekly`.

### Recommended Mitigation Steps

```solidity
    function updatePeriod() public returns (uint256) {
        uint256 _period = activePeriod;
        // only trigger if new week
        if (block.timestamp >= _period + week && initializer == address(0)) {
            _period = (block.timestamp / week) * week;
            activePeriod = _period;
            uint256 newWeeklyEmission = weeklyEmission();
            weekly += newWeeklyEmission;
            uint256 _circulatingSupply = circulatingSupply();

            uint256 _growth = calculateGrowth(newWeeklyEmission);
            uint256 _required = _growth + newWeeklyEmission;
            /// @dev share of newWeeklyEmission emissions sent to DAO.
            uint256 share = (_required * daoShare) / base;
            _required += share;
            uint256 _balanceOf = underlying.balanceOf(address(this));          
-           if (_balanceOf < _required) {
+           if (_balanceOf < weekly + _growth + share ) {
-              HERMES(underlying).mint(address(this), _required - _balanceOf);
+              HERMES(underlying).mint(address(this),weekly + _growth + share - _balanceOf);
            }

            underlying.safeTransfer(address(vault), _growth);

            if (dao != address(0)) underlying.safeTransfer(dao, share);

            emit Mint(msg.sender, newWeeklyEmission, _circulatingSupply, _growth, share);

            /// @dev queue rewards for the cycle, anyone can call if fails
            ///      queueRewardsForCycle will call this function but won't enter
            ///      here because activePeriod was updated
            try flywheelGaugeRewards.queueRewardsForCycle() {} catch {}
        }
        return _period;
    }
```

### Assessed type

Context

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/737#issuecomment-1640123826):**

**[deadrxsezzz (warden) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/737#issuecomment-1652526189):**
 > > Because the `gaugeCycle` of `flywheelGaugeRewards` may be greater than one week.
> 
> The warden describes a possible vulnerability if a `gauge` has a cycle length longer than a week. This is incorrect. `gaugeCycle` refers to the `block.timestamp` of the current cycle. I suppose the warden refers to `gaugeCycleLength`, which is an immutable set to a week.

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/737#issuecomment-1652553968):**
 > It might make sense to be a low/QA, because it does require a rare edge case for this to happen; i.e. no one queuing rewards for any `gauge` during 1 week and have a large amount of gauges. Everyone in the protocol is economically incentivized to queue rewards asap every week: team, LPs, voters, etc.
> 
> But it is a valid issue. If this were to happen and `queueRewardsForCycle` revert, (for example, because the gauge's array is too large), it would mean that `weekly` could be larger than `_required`. So not enough tokens would be minted and `getRewards` would revert because the minter contract wouldn't have enough balance to transfer the desired tokens.

**[Trust (judge) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/737#issuecomment-1653234537):**
 > Will leave as Med, as rare edge cases are still in-scope for this severity level and theoretical monetary loss is involved.

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/737#issuecomment-1708804312):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/104-737).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | bin2chen, chaduke |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/737
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

