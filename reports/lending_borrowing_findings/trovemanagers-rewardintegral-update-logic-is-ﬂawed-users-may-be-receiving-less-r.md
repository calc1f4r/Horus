---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46266
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - pkqs90
  - 0xBeastBoy
  - santipu
---

## Vulnerability Title

TroveManager's RewardIntegral update logic is ﬂawed, users may be receiving less rewards than expected 

### Overview


The TroveManager contract is designed to reward users with Bima tokens based on the amount of debt they have. However, there is a bug where the global reward rate is calculated using the total debt, which includes interest, but individual user reward rates may not be updated in sync. This results in users receiving less rewards than expected. The likelihood of this happening is high and the impact is medium, so it is recommended to always accrue interest before calculating rewards.

### Original Finding Content

## TroveManager Reward Calculation Issue

## Context
(No context files were provided by the reviewer)

## Description
TroveManager rewards users with the Bima token based on the amount of debt they have. Rewards are updated by the `_updateIntegrals` function. The updating mechanism is similar to Sushiswap Masterchef, maintaining the amount of reward tokens per debt token in `rewardIntegral` (global) and `rewardIntegralFor[account]` (per account). The key difference is that debt is always accruing interest.

The issue is that the global reward rate `rewardIntegral` always uses the total debt as the denominator, which is frequently updated to include the latest interest, but the user's `rewardIntegralFor[account]` may not be updated in sync. This discrepancy leads to the user's amount of debt being less than what the global `rewardIntegral` expects, resulting in a loss of rewards for users.

### Example
1. **Initial Status**: 
   - Global debt = 100, 
   - User debt = 50. 
   - Current `rewardIntegral` = 0, `rewardIntegralFor[user]` = 0.

2. **Accrue Interest**: 
   - Some time passes, 10% debt interest is accrued. 
   - Another user comes in and performs some actions (e.g., claims rewards), triggering `_applyPendingRewards()`, which increases totalActiveDebt to 100 * (1 + 10%) = 110.

3. **Reward Claim**: 
   - Some time passes, and we have 100 pending Bima rewards. 
   - The original user tries to claim rewards. 
   - First, we update the global variable:
     - `rewardIntegral = 100 / 110 = 0.909`
   - Then update for user:
     - `storedPendingReward += 50 * (0.909 - 0) = 45.45`.

The user should have received 50 rewards, but only received 45.45. The bug occurs because in step 2, we already updated `totalActiveDebt` with 10% interest to 110, while the user's debt remains unchanged. Thus, in step 3, we calculate the user's rewards using the before-debt-accrued amount (50), leading to a loss of rewards.

## Code Reference
- **TroveManager.sol#L952-L980**:

```solidity
function _applyPendingRewards(address _borrower) internal returns (uint256 coll, uint256 debt) {
    Trove storage t = Troves[_borrower];
    if (t.status == Status.active) {
        uint256 troveInterestIndex = t.activeInterestIndex;
        uint256 supply = totalActiveDebt; // <<<
        uint256 currentInterestIndex = _accrueActiveInterests();
        debt = t.debt;
        uint256 prevDebt = debt; // <<<

        // @audit-bug: Use previous debt instead of updated one.
        _updateIntegrals(_borrower, prevDebt, supply); // <<<
    }
}
```

```solidity
function _updateIntegrals(address account, uint256 balance, uint256 supply) internal {
    // @audit-note: Global reward update.
    uint256 integral = _updateRewardIntegral(supply);
    // @audit-note: Single user reward update.
    _updateIntegralForAccount(account, balance, integral);
}
```

```solidity
function _updateIntegralForAccount(address account, uint256 balance, uint256 currentIntegral) internal {
    uint256 integralFor = rewardIntegralFor[account];
    if (currentIntegral > integralFor) {
        storedPendingReward[account] += (balance * (currentIntegral - integralFor)) / 1e18;
        rewardIntegralFor[account] = currentIntegral;
    }
}
```

```solidity
function _updateRewardIntegral(uint256 supply) internal returns (uint256 integral) {
    uint256 _periodFinish = periodFinish;
    uint256 updated = _periodFinish;
    if (updated > block.timestamp) updated = block.timestamp;
    uint256 duration = updated - lastUpdate;
    integral = rewardIntegral;
    if (duration > 0) {
        lastUpdate = uint32(updated);
        if (supply > 0) {
            integral += (duration * rewardRate * 1e18) / supply;
            rewardIntegral = integral;
        }
    }
    _fetchRewards(_periodFinish);
}
```

## Impact
Users would receive less rewards than expected. The likelihood of this issue is high (would almost always happen), and the impact is medium (loss of rewards), hence reported as high severity.

## Recommendation
Always accrue interest before calculating rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | pkqs90, 0xBeastBoy, santipu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

