---
# Core Classification
protocol: Paladin Valkyrie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61569
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
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
finders_count: 2
finders:
  - Draiakoo
  - Giovanni Di Siena
---

## Vulnerability Title

Deposited rewards get stuck in incentive logic contracts when there is no pool liquidity

### Overview


This bug report describes a scenario where there is no money available in a pool, but rewards are still being given out. This can result in a loss of funds. The recommended solution is to assign the corresponding rewards to the owner. The bug has been fixed by the developers and verified by a third party.

### Original Finding Content

**Description:** For an interval of time during which there is zero liquidity in the pool and a reward has been actively distributed, the proportional amount of rewards that correspond to this interval when the liquidity has been zero will not be withdrawable by anyone.

**Impact:** While it is highly improbable for this scenario to occur, it would result in a loss of funds.

**Recommended Mitigation:** Assign the corresponding reward amount to the owner by accumulating it in the `accumulatedFees` storage variable:

```diff
    function _updateRewardState(IncentivizedPoolId id, address token, address account) internal virtual {
        // Sync pool total liquidity if not already done
        if(!poolSynced[id]) {
            _syncPoolLiquidity(id);
            poolSynced[id] = true;
        }

        RewardData storage _state = poolRewardData[id][token];
        uint96 newRewardPerToken = _newRewardPerToken(id, token).toUint96();
        _state.rewardPerTokenStored = newRewardPerToken;

++      uint256 lastUpdateTimeApplicable = block.timestamp < _state.endTimestamp ? block.timestamp : _state.endTimestamp;
++      if (poolStates[id].totalLiquidity == 0) {
++          accumulatedFees[token] += (lastUpdateTimeApplicable - _state.lastUpdateTime) * _state.ratePerSec;
++      }
++      _state.lastUpdateTime = uint32(lastUpdateTimeApplicable);

--      uint32 endTimestampCache = _state.endTimestamp;
--      _state.lastUpdateTime = block.timestamp < endTimestampCache ? block.timestamp.toUint32() : endTimestampCache;

        // Update user state if an account is provided
        if (account != address(0)) {
            if(!userLiquiditySynced[id][account]) {
                _syncUserLiquidity(id, account);
                userLiquiditySynced[id][account] = true;
            }

            UserRewardData storage _userState = userRewardStates[id][account][token];
            _userState.accrued = _earned(id, token, account).toUint160();
            _userState.lastRewardPerToken = newRewardPerToken;
        }
    }
```

**Paladin:** Fixed by commit [`653ca73`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/653ca73877737196c7728db8c01d2a803959d72d).

**Cyfrin:** Verified. All `_updateRewardState()` implementations have been updated to accumulate rewards distributed to zero liquidity as fees. However, in all instances, the last update time is erroneously cast to `uint32` instead of `uint48`:
```solidity
_state.lastUpdateTime = uint32(lastUpdateTimeApplicable);
```

**Paladin:** Fixed by commit [`f3e5251`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/f3e52516ef4c9c99795772227b25f1cd3878bab3).

**Cyfrin:** Verified. The unnecessary downcasts have been removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Paladin Valkyrie |
| Report Date | N/A |
| Finders | Draiakoo, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

