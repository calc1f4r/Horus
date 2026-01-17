---
# Core Classification
protocol: Morpheus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62536
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-morpheus
source_link: https://code4rena.com/reports/2025-08-morpheus
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.40
financial_impact: low

# Scoring
quality_score: 2
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] If a deposit pool has more than 1 public pools connected to it, issues will occur for some users after migration

### Overview

See description below for full details.

### Original Finding Content


Deposit pools can have more than 1 reward pools attached to it. In the case whereby we have 2 reward `rewardPoolIndex_` for Deposit pool A, and there is some staked tokens in each of these reward pool indexes, after migration, some users will be locked out of withdrawing.

<https://github.com/code-423n4/2025-08-morpheus/blob/main/contracts/capital-protocol/DepositPool.sol# L137-L160>
```

function migrate(uint256 rewardPoolIndex_) external onlyOwner {
        require(!isMigrationOver, "DS: the migration is over");
        if (totalDepositedInPublicPools == 0) {
            isMigrationOver = true;
            emit Migrated(rewardPoolIndex_);

            return;
        }

        IRewardPool rewardPool_ = IRewardPool(IDistributor(distributor).rewardPool());
        rewardPool_.onlyExistedRewardPool(rewardPoolIndex_);
        rewardPool_.onlyPublicRewardPool(rewardPoolIndex_);

        // Transfer yield to prevent the reward loss
        uint256 remainder_ = IERC20(depositToken).balanceOf(address(this)) - totalDepositedInPublicPools;
        require(remainder_ > 0, "DS: yield for token is zero");

        IERC20(depositToken).transfer(distributor, remainder_);

        IDistributor(distributor).supply(rewardPoolIndex_, totalDepositedInPublicPools);

        isMigrationOver = true;

        emit Migrated(rewardPoolIndex_);
    }
```

Suppose there are 2 public reward pool indexes of 0 & 1. And we have DepositPool A where users have staked stETH.

1. stETH staked on reward pool index 0 is 500
2. stETH staked on reward pool index 1 is also 500. The `totalDepositedInPublicPools` in this case would be 1000 stETH
3. When we call the `migrate()` function, it would send 1000 stETH to the Distributor contract on behalf of whatever `rewardPoolIndex_` we call the `migrate()` function with. That is to say, if we call the function with `rewardPoolIndex_` args of 0, then it will deposit all 1k stETH for users of `rewardPoolIndex_` 0. But the total staked by those users is 500 stETH where the users of `rewardPoolIndex_` 1 contributed the rest 500 stETH.
4. In this case, 500 stETH will be lost by users of `rewardPoolIndex_` 1 as these cannot be withdrawn since we supplied all 1k stETH on `rewardPoolIndex_` 0 in the Distributor contract.

It is better to migrate the amount deposited by users of `rewardPoolIndex_` x when the `migrate` function is called. This way, the migrations of 0 & 1 will accurately supply 500 stETH each in the Distributor contract for users.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 2/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Morpheus |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-morpheus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-08-morpheus

### Keywords for Search

`vulnerability`

