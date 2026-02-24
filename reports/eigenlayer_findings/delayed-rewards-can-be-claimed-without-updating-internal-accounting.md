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
solodit_id: 34995
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

Delayed rewards can be claimed without updating internal accounting

### Overview


The `claimRewards()` function in the EigenLayer Delayed Withdrawal Router contract is designed to claim delayed withdrawals and update accounting variables. However, there is a bug that allows the function to be bypassed, resulting in inaccurate accounting. This can be fixed by altering the way rewards are managed and filtering funds from the `eigenWithdrawals` contract. The bug has been fixed in the Casimir contract and verified by Cyfrin.

### Original Finding Content

**Description:** The `claimRewards()` function is designed to claim delayed withdrawals from the EigenLayer Delayed Withdrawal Router and to update accounting variables such as `delayedRewards` and `reservedFeeBalance`.

```solidity
function claimRewards() external {
    onlyReporter();

    uint256 initialWithdrawalsBalance = address(eigenWithdrawals).balance;
    eigenWithdrawals.claimDelayedWithdrawals(
        eigenWithdrawals.getClaimableUserDelayedWithdrawals(address(this)).length
    );
    uint256 claimedAmount = initialWithdrawalsBalance - address(eigenWithdrawals).balance;
    delayedRewards -= claimedAmount;

    uint256 rewardsAfterFee = subtractRewardFee(claimedAmount);
    reservedFeeBalance += claimedAmount - rewardsAfterFee;
    distributeStake(rewardsAfterFee);

    emit RewardsClaimed(rewardsAfterFee);
}
```

However, this function can be bypassed by directly executing the claim on the EigenLayer side via the `DelayedWithdrawalRouter::claimDelayedWithdrawals()` function. This function allows the caller to claim withdrawals for a specified recipient, with the recipient's address provided as an input. If the `CasimirManager` contract address is used as the `recipient`, the claim is made on its behalf.

**Impact:** This process does not update the accounting variables, leading to inaccurate accounting within the contract. Even though the rewards have been claimed, they are still accounted for in the `delayedRewards`, resulting in an incorrect total stake value.

**Proof of Concept:** EigenLayer contract that handles delayed withdrawal claims can be found [here](https://github.com/Layr-Labs/eigenlayer-contracts/blob/0139d6213927c0a7812578899ddd3dda58051928/src/contracts/pods/DelayedWithdrawalRouter.sol#L80)

**Recommended Mitigation:** Consider altering the way the contract manages rewards claims. This could be achieved by moving the accounting for claimed reward amounts to the `receive()` function, and by only filtering funds received from the `eigenWithdrawals` contract.

**Casimir:**
Fixed in [4adef64](https://github.com/casimirlabs/casimir-contracts/commit/4adef6482238c3d0926f72ffdff04e7a49886045)

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

