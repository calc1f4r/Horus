---
# Core Classification
protocol: Stakedotlink Polygon Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58678
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
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
  - 0kage
  - holydevoti0n
---

## Vulnerability Title

Unfair distribution of unbonding due to improper validator withdrawal index advancement

### Overview


The `PolygonStrategy::unbond` function currently has a bug where the `validatorWithdrawalIndex` is advanced based on the loop progression rather than actual unbonding actions. This can lead to uneven distribution of unbonding across validators, causing some to be unfairly shielded from unbonding while others bear a disproportionate share of the burden. A fix has been proposed and implemented in the Stake.link and Cyfrin projects.

### Original Finding Content

**Description:** `PolygonStrategy::unbond` tracks the `validatorWithdrawalIndex` to evenly distribute unbonding requests across vaults. The index is advanced based on the loop progression rather than actual unbonding actions, which can lead to uneven distribution of unbonding across validators.

Currently, when processing vaults during unbonding:

 - The function starts at the validatorWithdrawalIndex and iterates through vaults
- If a vault has sufficient rewards to cover the unbonding amount, only rewards are withdrawn with no actual unbonding of principal
- The validatorWithdrawalIndex is still updated to the next vault in sequence, even if no principal was unbonded
- If the index reaches the end of the vaults array, it wraps around to 0

This logic causes validators with high rewards to effectively "shield" their principal deposits from being unbonded, unfairly pushing the unbonding burden to other validators that might have already unbonded.

Specifically, in the unbond function:

```solidity
while (toUnbondRemaining != 0) {
    // Process vault[i]...
    ++i;
    if (i >= vaults.length) i = 0;
}
validatorWithdrawalIndex = i; // @audit This happens regardless of whether unbonding occurred on the last processed vault or not
```
Even if the rewards were sufficient to honor `unbond` request, `vaultWithdrawalIndex` still advances.


**Impact:** This issue creates a potential fairness problem in the distribution of unbonding actions across validators. Validators that generate more rewards are less likely to have their principal deposits unbonded, while validators with fewer rewards will bear a disproportionate share of the unbonding burden.

Effectively, some vaults get repeatedly unbonded while others skip their turn.


**Proof of Concept:** In the `unbond should work correctly` test, at line 304 in `polygon-strategy.test.ts`, note that the `validatorWithdrawalIndex` resets to 0 even though the there was no unbonding on vault[2]. vault[0] gets unbonded twice while vault[2] skips unbonding altogether in the current round.


**Recommended Mitigation:** Consider modifying the `unbond` function to only advance the `validatorWithdrawalIndex` when actual unbonding of principal deposits occurs, not just when rewards are withdrawn:

```diff solidity
function unbond(uint256 _toUnbond) external onlyFundFlowController {
    if (numVaultsUnbonding != 0) revert UnbondingInProgress();
    if (_toUnbond == 0) revert InvalidAmount();

    uint256 toUnbondRemaining = _toUnbond;
    uint256 i = validatorWithdrawalIndex;
    uint256 skipIndex = validatorRemoval.isActive
        ? validatorRemoval.validatorId
        : type(uint256).max;
    uint256 numVaultsUnbonded;
    uint256 preBalance = token.balanceOf(address(this));
++ uint256 nextIndex = i; // Track the next index separately

    while (toUnbondRemaining != 0) {
        if (i != skipIndex) {
            IPolygonVault vault = vaults[i];
            uint256 deposits = vault.getTotalDeposits();

            if (deposits != 0) {
                uint256 principalDeposits = vault.getPrincipalDeposits();
                uint256 rewards = deposits - principalDeposits;

                if (rewards >= toUnbondRemaining) {
                    vault.withdrawRewards();
                    toUnbondRemaining = 0;
                } else {
                    toUnbondRemaining -= rewards;
                    uint256 vaultToUnbond = principalDeposits >= toUnbondRemaining
                        ? toUnbondRemaining
                        : principalDeposits;

                    vault.unbond(vaultToUnbond);
++               nextIndex = (i + 1) % vaults.length; // Update next index only when unbonding principal
                    toUnbondRemaining -= vaultToUnbond;
                    ++numVaultsUnbonded;
                }
            }
        }

        ++i;
        if (i >= vaults.length) i = 0;
    }
--    validatorWithdrawalIndex = i;
++    // Only update the index if we actually unbonded principal from at least one vault
++    if (numVaultsUnbonded > 0) {
++       validatorWithdrawalIndex = nextIndex;
++   }

    numVaultsUnbonding = numVaultsUnbonded;

    uint256 rewardsClaimed = token.balanceOf(address(this)) - preBalance;
    if (rewardsClaimed != 0) totalQueued += rewardsClaimed;

    emit Unbond(_toUnbond);
}

```

**Stake.link:**
Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/9fd654b46a0b9008a134fe67145d446f7e04d8ce).

**Cyfrin:** Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Stakedotlink Polygon Staking |
| Report Date | N/A |
| Finders | 0kage, holydevoti0n |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

