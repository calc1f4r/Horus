---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34999
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Function `getTotalStake()` fails to account for pending validators, leading to inaccurate accounting

### Overview


The `getTotalStake()` function in the `CasimirManager` contract is used to calculate the total amount of ETH staked in the contract. However, it does not take into account the ETH staked by validators in the pending state. This means that the total stake calculated by the function is less than it should be, leading to incorrect calculations in the `rewardStakeRatioSum` variable. This bug can cause problems if all pending validators are not activated before the finalization of a report. The recommended solution is to add the stake of pending validators to the `getTotalStake()` function. The bug has been fixed in the Casimir contract and verified by Cyfrin.

### Original Finding Content

**Description:** The `getTotalStake()` function is the core accounting function to calculate the total stake of the `CasimirManager`. It's used to compute the change for `rewardStakeRatioSum` within the `finalizeReport()` function.

```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
```

This function aggregates the stakes from various sources, including the `32 ETH` from each "ready validator" (`readyValidatorIds.length * VALIDATOR_CAPACITY`) and the ETH staked in "staked validators" (`latestActiveBalanceAfterFee`).

However, it fails to account for the ETH in pending validators.

A validator must go through three steps to become active/staked:

1. Every time users make a deposit, the contract checks if the unassigned balance has reached `32 ETH`. If it has, the next validator ID is added to `readyValidatorIds`.
2. The reporter calls `depositValidator()` to deposit `32 ETH` from the validator into the beacon deposit contract. In this step, the validator ID moves from `readyValidatorIds` to `pendingValidatorIds`.
3. The reporter calls `activateValidator()`, which moves the validator ID from `pendingValidatorIds` to `stakedValidatorIds` and updates `latestActiveBalanceAfterFee` to reflect the total stake in the beacon chain.

As shown, the `getTotalStake()` function accounts for validators in steps 1 and 3, but ignores the stake of validators in the pending state (step 2). In the current design, there is nothing that stops report finalization if pending validators > 0.

**Impact:** Function getTotalStake() will return the value of total stake less than it should be. The result is rewardStakeRatioSum calculation will be incorrect in a scenario where all pending validators are not activated before report finalization.

```solidity
uint256 totalStake = getTotalStake();

rewardStakeRatioSum += Math.mulDiv(rewardStakeRatioSum, gainAfterFee, totalStake);

rewardStakeRatioSum += Math.mulDiv(rewardStakeRatioSum, gain, totalStake);

rewardStakeRatioSum -= Math.mulDiv(rewardStakeRatioSum, loss, totalStake);
```

**Recommended Mitigation:** Consider adding `pendingValidatorIds.length * VALIDATOR_CAPACITY` to function `getTotalStake()`.

**Casimir:**
Fixed in [10fe228](https://github.com/casimirlabs/casimir-contracts/commit/10fe228406dc3f889db42e8850add94561a7325e)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

