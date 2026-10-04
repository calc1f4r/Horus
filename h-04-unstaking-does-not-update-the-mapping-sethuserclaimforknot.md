---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5891
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/90

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - HE1M
  - 9svR6w
---

## Vulnerability Title

[H-04] Unstaking does not update the mapping sETHUserClaimForKnot

### Overview


A bug has been identified in the code of the 2022-11-stakehouse repository on GitHub. This bug affects users who stake sETH and later decide to unstake some of it. If a user stakes some sETH, and after some time decides to unstake some amount of sETH, they will not be qualified or be less qualified to claim ETH on the remaining staked sETH.

The bug is in the code of the Syndicate.sol file, on line 245. The code does not update the mapping sETHUserClaimForKnot correctly when a user unstakes sETH. This mapping should be updated based on the remaining sETH (which is 2 sETH) but is instead updated based on the time when 5 sETH were staked. As a result, Alice can not claim ETH or she will qualify for less amount.

The recommended mitigation step is to add the following line on line 274 of the Syndicate.sol file:
```
sETHUserClaimForKnot[_blsPubKey][msg.sender] =
                (accumulatedETHPerShare * sETHStakedBalanceForKnot[_blsPubKey][msg.sender]) / PRECISION
```

This bug should be fixed as soon as possible to ensure that users are not disadvantaged when staking and unstaking sETH.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L245


## Vulnerability details

## Impact

If a user stakes some sETH, and after some time decides to unstake some amount of sETH, later s/he will not be qualified or be less qualified to claim ETH on the remaining staked sETH.

## Proof of Concept

Suppose Alice stakes 5 sETH by calling `stake(...)`.
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L203
So, we will have:
 -  `sETHUserClaimForKnot[BLS][Alice] = (5 * 10^18 * accumulatedETHPerFreeFloatingShare) / PRECISION`
 - `sETHStakedBalanceForKnot[BLS][Alice] = 5 * 10^18`
 - `sETHTotalStakeForKnot[BLS] += 5 * 10^18`

Later, Alice decides to unstake 3 sETH by calling `unstake(...)`.
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L245

So, all ETH owed to Alice will be paid:
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L257

Then, we will have:
 -  `sETHUserClaimForKnot[BLS][Alice] = (5 * 10^18 * accumulatedETHPerFreeFloatingShare) / PRECISION`
 - `sETHStakedBalanceForKnot[BLS][Alice] = 2 * 10^18`
 - `sETHTotalStakeForKnot[BLS] -= 3 * 10^18`

It is clear that the mapping `sETHStakedBalanceForKnot` is decreased as expected, but the mapping `sETHUserClaimForKnot` is not changed. In other words, the mapping `sETHUserClaimForKnot` is still holding the claimed amount based on the time 5 sETH were staked.

If, after some time, the ETH is accumulated per free floating share for the BLS public key that Alice was staking for, Alice will be qualified to some more ETH to claim (because she has still 2 sETH staked). 

If Alice unstakes by calling `unstake(...)` or claim ETH by calling `claimAsStaker(...)`, in both calls, the function `calculateUnclaimedFreeFloatingETHShare` will be called to calculate the amount of unclaimed ETH:
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L652

In this function, we will have:
 - `stakedBal = sETHStakedBalanceForKnot[BLS][Alice]` = 2 * 10^18
 - `userShare = (newAccumulatedETHPerShare * stakedBal) / PRECISION`
 
The return value which is unclaimed ETH will be:
```
userShare - sETHUserClaimForKnot[BLS][Alice] = 
(newAccumulatedETHPerShare * 2 * 10^18) / PRECISION - (5 * 10^18 * accumulatedETHPerFreeFloatingShare) / PRECISION
```

This return value is not correct (it is highly possible to be smaller than 0, and as a result Alice can not claim anything), because the claimed ETH is still based on the time when 5 sETH were staked, not on the time when 2 sETH were remaining/staked.

The vulnerability is that during unstaking, the mapping `sETHUserClaimForKnot` is not updated to the correct value. In other words, this mapping is updated in `_claimAsStaker`, but it is updated based on 5 sETH staked, later when 3 sETH are unstaked, this mapping should be again updated based on the remaing sETH (which is 2 sETH).

As a result, Alice can not claim ETH or she will qualify for less amount.

## Tools Used

## Recommended Mitigation Steps
The following line should be added on line 274:
```
sETHUserClaimForKnot[_blsPubKey][msg.sender] =
                (accumulatedETHPerShare * sETHStakedBalanceForKnot[_blsPubKey][msg.sender]) / PRECISION
```

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/syndicate/Syndicate.sol#L274

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | HE1M, 9svR6w |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/90
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Don't update state`

