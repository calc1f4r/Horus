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
solodit_id: 34996
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

Anyone can submit proofs via  EigenPod `verifyAndProcessWithdrawals` to break the accounting of `withdrawRewards`

### Overview


The bug report discusses an issue with the `CasimirManager::withdrawRewards` operation, which is used to withdraw rewards for partial withdrawals of a validator. The operation is supposed to update the `delayedRewards` based on the last element in the array of `userDelayedWithdrawalByIndex`. However, anyone can submit proofs directly to `EigenPod::verifyAndProcessWithdrawals` instead of going through the proper process, which bypasses the necessary steps for updating the `delayedRewards`. This can result in broken accounting and prevent withdrawals from being processed. The bug has been fixed and verified by the team. To prevent this issue, it is recommended to track the `eigenWithdrawals.delayedWithdrawals` and `eigenWithdrawals.delayedWithdrawalsCompleted` on EigenLayer to calculate delayedRewards.

### Original Finding Content

**Description:** `CasimirManager::withdrawRewards` is an `onlyReporter` operation that performs the key tasks below:

1. Submits proofs related to the partial withdrawal of a validator at a given index.
2. Updates the `delayedRewards` based on the last element in the array of `userDelayedWithdrawalByIndex`.

Note that anyone, not just the pod owner, can submit proofs directly to `EigenPod::verifyAndProcessWithdrawals`. In such a case, the `delayedRewards` will not be updated, and the subsequent accounting during report finalization will be broken.

Any attempt to withdraw rewards by calling `CasimirManager::withdrawRewards` will revert because the withdrawal has already been processed. Consequently, `delayedRewards` will never be updated.

This same issue is applicable when submitting proofs for processing a full withdrawal. Critical accounting parameters that are updated in `CasimirManager::withdrawValidator` are effectively bypassed when proofs are directly submitted to EigenLayer.

**Impact:** If `delayedRewards` is not updated, the `rewardStakeRatioSum` and `latestActiveBalanceAfterFee` accounting will be broken.

**Recommended Mitigation:** EigenLayer does not restrict access to process withdrawals only to the pod owner. To that extent, access control to `CasimirManager::withdrawRewards` can always be bypassed. Assuming that all withdrawals will happen only through a reporter, consider adding logic that directly tracks the `eigenWithdrawals.delayedWithdrawals` and `eigenWithdrawals.delayedWithdrawalsCompleted` on EigenLayer to calculate delayedRewards.

**Casimir:**
Fixed in [eb31b43](https://github.com/casimirlabs/casimir-contracts/commit/eb31b4349e69eb401615e0eca253e9ab8cc0999d)

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

