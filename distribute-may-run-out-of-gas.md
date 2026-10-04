---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60917
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

`distribute()` May Run Out of Gas

### Overview


The report is about a bug in the `DepositerRewardDistributor.distribute()` function in the `rewards/DepositerRewardDistributor.sol` file. This function is responsible for distributing rewards to users, but it can fail if the `extraRewards` list is too long. This is because the function performs expensive operations for each element in the list, which can lead to high gas requirements. To prevent this, it is recommended to set an upper limit for the length of the `extraRewards` list. This will ensure that the function runs successfully and rewards are distributed properly.

### Original Finding Content

**Update**
An upper bound of `12` has been introduced for the length of `extraRewards`.

**File(s) affected:**`rewards/DepositerRewardDistributor.sol`

**Description:** The `DepositerRewardDistributor.distribute()` function iterates over every element in `extraRewards`, performing expensive operations, including calling other contracts:

```
for (uint256 i = 0; i < extraRewards.length; i++) {
    uint256 totalSupply = IERC20Upgradeable(stakingToken).totalSupply();
    uint256 balance = IERC20Upgradeable(stakingToken).balanceOf(extraRewards[i]);
    uint256 ratio = balance.mul(PRECISION).div(totalSupply);
    uint256 amounts = _rewards.mul(ratio).div(PRECISION);

    _approve(rewardToken, extraRewards[i], amounts);

    IAbstractReward(extraRewards[i]).distribute(amounts);

    emit Distribute(extraRewards[i], _rewards);
}
```

If `extraRewards` has a very large number of elements, then the function could fail due to high gas requirements. The `DepositerRewardDistributor.distribute()` function forms a critical part of the reward distribution workflow, and no rewards will be distributed if it does not run successfully to completion.

**Recommendation:** Consider enforcing an upper bound on the length of `extraRewards`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

