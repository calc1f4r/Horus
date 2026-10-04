---
# Core Classification
protocol: Concur Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1430
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/107

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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - csanuragjain
  - Czar102
  - CertoraInc
  - leastwood
  - hickuphh3
---

## Vulnerability Title

[M-20] `MasterChef.updatePool()` Fails To Update Reward Variables If `block.number >= endBlock`

### Overview


This bug report is about a vulnerability in the `updatePool` function of the MasterChef.sol contract. This function is responsible for calculating the accumulated Concur rewards by tracking the number of blocks passed since the last update to correctly determine how many Concur tokens should be distributed to each share. If a pool has not recently updated itself and has reached the `block.number >= endBlock` statement, then any rewards that it would normally be entitled to prior to reaching `endBlock` will not be attributed to the pool, giving an advantage to more active pools. The vulnerability was identified through manual code review. The recommended mitigation steps include ensuring that once the `block.number >= endBlock` statement has been reached, the `pool.accConcurPerShare` is updated to reflect the number of blocks that have passed up until `endBlock`. This will ensure stale pools are not negatively impacted once `endBlock` has been reached by the contract.

### Original Finding Content

_Submitted by leastwood, also found by CertoraInc, csanuragjain, Czar102, hickuphh3, kirk-baird, and WatchPug_

The `updatePool` function intends to calculate the accumulated Concur rewards by tracking the number of blocks passed since the last update to correctly determine how many Concur tokens to distribute to each share. The reward distribution has a start and end block which dictates the timeframe by which rewards will be distributed to the underlying pool.

If a pool has not recently updated itself and has reached the  `block.number >= endBlock` statement in `updatePool`, then any rewards that it would normally be entitled to prior to reaching `endBlock` will not be attributed to the pool. Therefore, once rewards are no longer being distributed, pools who had not recently called `updatePool` before reaching `endBlock` are at a disadvantage as compared to more active pools.

#### Proof of Concept

[MasterChef.sol#L135-L154](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/MasterChef.sol#L135-L154)

    // Update reward variables of the given pool to be up-to-date.
    function updatePool(uint _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        if (block.number <= pool.lastRewardBlock) {
            return;
        }
        uint lpSupply = pool.depositToken.balanceOf(address(this));
        if (lpSupply == 0 || pool.allocPoint == 0) {
            pool.lastRewardBlock = block.number;
            return;
        }
        if(block.number >= endBlock) {
            pool.lastRewardBlock = block.number;
            return;
        }        

        uint multiplier = getMultiplier(pool.lastRewardBlock, block.number);
        uint concurReward = multiplier.mul(concurPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
        pool.accConcurPerShare = pool.accConcurPerShare.add(concurReward.mul(_concurShareMultiplier).div(lpSupply));
        pool.lastRewardBlock = block.number;
    }

### Recommended Mitigation Steps

Ensure that once the `block.number >= endBlock` statement has been reached, the `pool.accConcurPerShare` is updated to reflect the number of blocks that have passed up until `endBlock`. The number of blocks should be equal to `endBlock - pool.lastRewardBlock`. This will ensure stale pools are not negatively impacted once `endBlock` has been reached by the contract.

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/107)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-concur-findings/issues/107#issuecomment-1103304716):**
 > The warden has identified a way in which the contract will not release rewards that are due for a depositor.
> 
> Because the check doesn't accrue until the last eligible block, the reward loss can be quantified as:<br>
> LastTimeAccrueBeforeEndBlock - endBlock
> 
> The finding is valid, but because it pertains to loss of yield, and because the loss can be quantified and reduced by simply calling at the last available block, I believe Medium Severity to be more appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Concur Finance |
| Report Date | N/A |
| Finders | csanuragjain, Czar102, CertoraInc, leastwood, hickuphh3, WatchPug, kirk-baird |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/107
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`vulnerability`

