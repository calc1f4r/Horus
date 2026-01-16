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
solodit_id: 35008
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
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
  - Hans
  - 0kage
---

## Vulnerability Title

Users could avoid loss by frontrunning to request unstake

### Overview


This report describes a bug where a loss can occur when a validator is slashed in the `finalizeReport()` function. This can happen because users can front-run an unstake request, which allows them to avoid the loss by creating and fulfilling the request within the same `reportPeriod`. This is unfair as it allows them to keep their profits while avoiding losses. The recommended mitigation for this bug is to implement a waiting period for unstake requests and to not allow them to be fulfilled in the same `reportPeriod`. Additionally, a small user fee for unstaking could also be considered. The bug has been fixed in the Casimir contract and has been verified by Cyfrin.

### Original Finding Content

**Description:** A loss can occur when a validator is slashed, which is reflected in the `finalizeReport()` function. If the `change` is less than 0, this indicates that a loss has occurred. Consequently, the accounting updates the `rewardStakeRatioSum` to decrease the stake value of all users in the `CasimirManager`.

```solidity
} else if (change < 0) {
    uint256 loss = uint256(-change);
    rewardStakeRatioSum -= Math.mulDiv(rewardStakeRatioSum, loss, totalStake);
    latestActiveBalanceAfterFee -= loss;
}
```

However, users can avoid this loss by front-running an unstake request. This is because they can create and fulfill an unstake request within the same `reportPeriod`. If users anticipate a potential loss in the next report (by watching the mempool), they can avoid it by requesting to unstake. The contract processes all unstake requests in a First-In-First-Out (FIFO) queue, meaning reporters must fulfill earlier requests before later ones.

```solidity
function getNextUnstake() public view returns (Unstake memory unstake, bool fulfillable) {
    // @audit Allow to create and fulfill unstake within the same `reportPeriod`
    if (unstakeQueue.length > 0) {
        unstake = unstakeQueue[0];
        fulfillable = unstake.period <= reportPeriod && unstake.amount <= getWithdrawableBalance();
    }
}
```

**Impact:** This can lead to unfairness. The front-runner can avoid losses while retaining all profits.

**Recommended Mitigation:** Consider implementing a waiting or delay period for unstake requests before they can be fulfilled. Do not allow the unstake request to be fulfilled in the same `reportPeriod` in which it was created. Additionally, considering adding a small user fee for unstaking.

**Casimir:**
Fixed in [28baa81](https://github.com/casimirlabs/casimir-contracts/commit/28baa8191a1b5a27d3ee495dee0d993177bf7e5f)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

