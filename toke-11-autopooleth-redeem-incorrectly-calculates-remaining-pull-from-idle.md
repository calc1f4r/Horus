---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53532
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[TOKE-11] AutopoolETH redeem incorrectly calculates remaining pull from idle

### Overview


This bug report discusses a problem in a library function that is responsible for pulling assets back from DestinationVaults. The issue occurs when there are multiple rounds and one round has undervalued shares while the other has overvalued shares. This results in the user receiving only 50% of their assets. The cause of this problem is a miscalculation in the conditional on line 791, which does not take into account the losses from overvaluing shares. The suggested solution is to calculate the remaining amount from assets minus the maximum of each loop iteration. This issue has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** vault/libs/AutopoolDebt.sol:redeem#L791

**Description:**

This library function is responsible for pulling assets back from DestinationVaults to let the user redeem their shares for underlying assets.

The algorithm loops over DestinationVaults in the WithdrawalQueue and uses the cached debt and value to calculate the decrease in debt. After the algorithm, depending on some conditions, the assets may be increased from the assets in `currentIdle`.

In this conditional branch however, the `Math.max(info.assetsPulled, info.debtMinDecrease)` expresses the maximum between the sum of the assets pulled and the sum of the debt-min decrease. This is incorrect because in the algorithm, the running counter in `info.assetsToPull` which determines whether the algorithm should terminate or not is decreased by `Math.max(debtMinDecrease, pulledAssets)`, which is the maximum between the debtMin decrease and pulled assets of each specific round.

This doesn’t work when there are multiple round (i.e. multiple DestinationVaults in the WithdrawalQueue) and one has undervalued shares (`debtMinDecrease < pulledAssets`) and the other one has overvalued shares (`debtMinDecrease > pulledAssets`). In each round, the larger one would be used to decrease the counter and so it could terminate while both of them are at for example 50% of `assets`.

In the case where the destination vaults are empty (and `exhaustedDestinations` is true), the conditional will hold true and the remaining 50% would be taken from `currentIdle`. If there was even a slight amount left in the destination vault, `exhaustedDestinations` would be false and the user would receive only 50% of `assets`.

This is caused by the calculation of the `remaining` amount in the conditional on line 791: it does not take into account whether the user suffered losses from overvaluing shares. This causes strange behaviour where taking a few `wei` less could result in 50% less assets.

```
if (
    info.assetsPulled < assets && info.debtMinDecrease < assets && info.currentIdle > 0 && exhaustedDestinations
) {
    uint256 remaining = assets - Math.max(info.assetsPulled, info.debtMinDecrease); 
    if (remaining < info.currentIdle) {
        info.assetsFromIdle = remaining;
    } else {
        info.assetsFromIdle = info.currentIdle;
    }
}
```

**Remediation:**  The remaining amount here should be calculated from assets minus the sum of the max of each loop iteration.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

